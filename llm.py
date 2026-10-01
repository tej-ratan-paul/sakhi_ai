"""LLM layer for Sakhi AI.

Provider is chosen automatically:
  1. ``gemini``    - GEMINI_API_KEY / GOOGLE_API_KEY  (google-genai SDK)
  2. ``openrouter`` - OPENROUTER_API_KEY               (any model they credit)
  3. ``none``      - no key, the API returns a clear 503 instead of pretending

Both providers return the same thing: a dict parsed from the model's JSON plus the
model id that produced it.
"""

import json
import os
import re
import time
from typing import Any, Dict, Optional, Tuple

import httpx

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("SAKHI_OLLAMA_MODEL", "llama3.1")
GEMINI_MODEL = os.getenv("SAKHI_MODEL", "gemini-3.8-flash")
GEMINI_FALLBACKS = tuple(
    m for m in os.getenv("SAKHI_MODEL_FALLBACKS", "gemini-flash-latest").split(",") if m
)
OPENROUTER_MODEL = os.getenv("SAKHI_OPENROUTER_MODEL", "google/gemini-2.5-flash")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
TIMEOUT = float(os.getenv("SAKHI_LLM_TIMEOUT", "90"))


class LLMError(RuntimeError):
    def __init__(self, message: str, status: Optional[int] = None):
        super().__init__(message)
        self.status = status


def ollama_available() -> bool:
    try:
        httpx.get(f"{OLLAMA_HOST}/api/tags", timeout=2)
        return True
    except Exception:  # noqa: BLE001
        return False


def _configured_providers() -> list:
    forced = os.getenv("SAKHI_LLM_PROVIDER", "auto").strip().lower()
    available = []
    if GEMINI_API_KEY:
        available.append("gemini")
    if OPENROUTER_API_KEY:
        available.append("openrouter")
    if ollama_available():
        available.append("ollama")
    if forced != "auto":
        available = [p for p in available if p == forced] or [forced]
    return available


def provider() -> str:
    providers = _configured_providers()
    return providers[0] if providers else "none"


def _strip_fence(text: str) -> str:
    fence = re.search(r"```(?:json)?\s*(.+?)```", text, re.S)
    return (fence.group(1) if fence else text).strip()


def _parse(text: str) -> Dict[str, Any]:
    cleaned = _strip_fence(text or "")
    if not cleaned:
        raise LLMError("empty model response")
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end > start:
            return json.loads(cleaned[start : end + 1])
        raise LLMError(f"invalid JSON from model: {exc}") from exc


def _call_gemini(prompt: str, system: str, schema: Optional[Dict[str, Any]]) -> Tuple[Dict[str, Any], str]:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=GEMINI_API_KEY)
    models = (GEMINI_MODEL,) + GEMINI_FALLBACKS
    last_error: Optional[Exception] = None
    busy: Optional[Exception] = None

    for model in models:
        for attempt in range(1, 3):
            try:
                config = types.GenerateContentConfig(
                    system_instruction=system,
                    temperature=0.2,
                    response_mime_type="application/json",
                    response_schema=schema,
                )
                response = client.models.generate_content(
                    model=model, contents=prompt, config=config
                )
                return _parse(response.text), model
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                message = str(exc)
                status = getattr(exc, "code", None) or getattr(exc, "status_code", None)

                if status in (401, 403):
                    raise LLMError("invalid_api_key", 502) from exc
                if status == 429 or "RESOURCE_EXHAUSTED" in message:
                    raise LLMError("quota_exceeded", 429) from exc
                if status == 404 or "NOT_FOUND" in message:
                    print(f"gemini model {model} unavailable, trying next")
                    break
                if status == 503 or "UNAVAILABLE" in message or "overloaded" in message.lower():
                    busy = exc
                    time.sleep(1.5 * attempt)
                    continue
                raise LLMError(str(exc)) from exc

    if busy is not None:
        raise LLMError("model_busy", 503) from busy
    raise LLMError(str(last_error))


def _schema_hint(schema: Optional[Dict[str, Any]]) -> str:
    """Providers without native schema support (Ollama, OpenRouter json mode) need it in text."""
    if not schema:
        return ""
    props = schema.get("properties", {})
    required = schema.get("required", list(props))
    lines = [f"- {key} ({spec.get('type', 'STRING').lower()})" for key, spec in props.items()]
    return (
        "\n\nReturn ONLY a JSON object with exactly these keys:\n"
        + "\n".join(lines)
        + "\nAll of these keys are required: "
        + ", ".join(required)
        + "\nconfidence must be one of: high, medium, low."
    )


def _call_openrouter(prompt: str, system: str, schema: Optional[Dict[str, Any]]) -> Tuple[Dict[str, Any], str]:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    body: Dict[str, Any] = {
        "model": OPENROUTER_MODEL,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt + _schema_hint(schema)},
        ],
        "response_format": {"type": "json_object"},
    }
    with httpx.Client(timeout=TIMEOUT) as client:
        response = client.post(OPENROUTER_URL, headers=headers, json=body)
        if response.status_code in (401, 403):
            raise LLMError("invalid_api_key", 502)
        if response.status_code == 429:
            raise LLMError("quota_exceeded", 429)
        response.raise_for_status()
        data = response.json()
    text = data["choices"][0]["message"]["content"]
    return _parse(text), OPENROUTER_MODEL


def _call_ollama(prompt: str, system: str, schema: Optional[Dict[str, Any]]) -> Tuple[Dict[str, Any], str]:
    """Local LLM via Ollama - no API key, no quota, works offline."""
    body = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.2},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt + _schema_hint(schema)},
        ],
    }
    with httpx.Client(timeout=300) as client:
        response = client.post(f"{OLLAMA_HOST}/api/chat", json=body)
        response.raise_for_status()
        data = response.json()
    return _parse(data["message"]["content"]), f"ollama/{OLLAMA_MODEL}"


PROVIDER_CALLS = {
    "gemini": _call_gemini,
    "openrouter": _call_openrouter,
    "ollama": _call_ollama,
}


def generate(prompt: str, system: str, schema: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], str]:
    """Try each configured provider in order. Raises LLMError with a usable status code."""
    providers = _configured_providers()
    if not providers:
        raise LLMError(
            "No LLM configured. Set GEMINI_API_KEY, OPENROUTER_API_KEY, or run Ollama locally.",
            503,
        )

    hard_error: Optional[LLMError] = None
    for name in providers:
        try:
            return PROVIDER_CALLS[name](prompt, system, schema)
        except LLMError as exc:
            if exc.status in (401, 403):
                raise
            hard_error = hard_error or exc
            print(f"llm provider {name} failed: {exc}")
        except Exception as exc:  # noqa: BLE001
            hard_error = hard_error or LLMError(str(exc))
            print(f"llm provider {name} failed: {exc}")

    if hard_error and hard_error.status in (429, 502):
        raise hard_error
    if hard_error and hard_error.status == 503:
        raise hard_error
    raise LLMError(str(hard_error) if hard_error else "all providers failed", 502)


def status() -> Dict[str, Any]:
    providers = _configured_providers()
    return {
        "llm_provider": providers[0] if providers else "none",
        "providers_available": providers,
        "gemini_configured": bool(GEMINI_API_KEY),
        "openrouter_configured": bool(OPENROUTER_API_KEY),
        "ollama_available": ollama_available(),
        "ollama_model": OLLAMA_MODEL,
        "models": (
            [GEMINI_MODEL, *GEMINI_FALLBACKS]
            if "gemini" in providers
            else [OPENROUTER_MODEL] if "openrouter" in providers
            else [f"ollama/{OLLAMA_MODEL}"]
        ),
    }
