"""Sakhi AI - grounded FastAPI gateway.

Flow: spoken/text query -> query transformer -> live web search (Tavily, or Gemini
Search grounding as fallback) -> official-source filter -> LLM -> strict JSON answer
with citations.
"""

import logging
import os
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import llm
import search
from query import build_search_query, detect_language, official_url_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sakhi")

app = FastAPI(title="Sakhi AI Grounded Engine", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_INSTRUCTION = """
You are 'Sakhi' (सखी / சகி), a caring, elder-sisterly counselor helping Indian rural women
with zero digital experience access verified government welfare benefits.

Grounding & Behavior Rules:
1. Answer ONLY from the OFFICIAL SOURCE EXCERPTS provided in the user's message. Those excerpts
   come from a live web search of myscheme.gov.in, pib.gov.in and state portals.
2. Copy scheme names, benefit amounts, eligibility rules, document lists and office names exactly
   as the sources state them. Never invent, round up, or guess a rupee amount.
3. If the excerpts do not clearly contain the answer, set confidence to "low", say plainly in
   benefit_summary that the information could not be confirmed today, and suggest which office to
   ask in person. A wrong amount is worse than an honest gap.
4. Reject commercial loan advertisements, private insurance products, chit funds and blog
   aggregators even if they appear in the sources. Trust only .gov.in, .nic.in and RBI sources.
5. Avoid bureaucratic jargon. Say "card with your photo", "ration card", "the anganwadi sister".
6. Address the woman as a sister. Never call her 'bhaiya', 'bhai' or 'sir'. In Tamil, Hindi and
   other Indian languages use the respectful 'Akka' or 'Didi' and short, warm, everyday sentences
   free of Sanskritised legal vocabulary. If the language is English, use plain simple English at a
   6th-grade reading level.
"""

RESPONSE_SCHEMA: Dict[str, Any] = {
    "type": "OBJECT",
    "properties": {
        "scheme_name": {"type": "STRING"},
        "benefit_summary": {
            "type": "STRING",
            "description": "Plain one-line benefit, e.g. 'Rs 5,000 in your bank account'.",
        },
        "eligibility": {"type": "ARRAY", "items": {"type": "STRING"}},
        "documents_needed": {"type": "ARRAY", "items": {"type": "STRING"}},
        "where_to_go": {
            "type": "STRING",
            "description": "Physical local office, e.g. Anganwadi, Gram Panchayat, Block office, CSC.",
        },
        "spoken_script": {
            "type": "STRING",
            "description": "Warm 3-sentence encouragement in the user's language, for text-to-speech.",
        },
        "confidence": {
            "type": "STRING",
            "description": "high | medium | low - how strongly the official sources back this answer.",
        },
    },
    "required": [
        "scheme_name",
        "benefit_summary",
        "eligibility",
        "documents_needed",
        "where_to_go",
        "spoken_script",
    ],
}


class UserQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    language: str = "auto"


def _build_prompt(raw_query: str, language: str, search_query: str, context: str) -> str:
    return f"""
User language of interaction: {language}
User's spoken words (colloquial, dialectal, possibly ungrammatical): "{raw_query}"
Search query used: "{search_query}"

OFFICIAL SOURCE EXCERPTS FROM LIVE WEB SEARCH:
{context or '(no sources returned)'}

Task:
1. Identify the single most relevant government welfare scheme in the excerpts for this woman's
   situation.
2. Extract the official scheme name, the cash or in-kind benefit and amount, who qualifies, which
   physical documents she must carry, and the physical office where she applies locally.
3. Write spoken_script: exactly three warm, encouraging sentences in {language}, addressed to her as
   a sister, naming the benefit, the documents to carry, and the office to visit. It will be read
   aloud, so keep it speakable and free of URLs, abbreviations and English words.
4. Set confidence: "high" if an official excerpt states the amount and eligibility, "medium" if
   only part is confirmed, "low" if the answer is inferred or unconfirmed.
"""

ALIASES = {
    "scheme_name": ("scheme_name", "official_scheme_name", "scheme", "name", "title"),
    "benefit_summary": ("benefit_summary", "cash_or_in_kind_benefit", "benefit", "benefits", "summary"),
    "eligibility": ("eligibility", "who_qualifies", "who_can_apply", "eligibility_criteria"),
    "documents_needed": ("documents_needed", "documents_to_carry", "documents", "required_documents"),
    "where_to_go": ("where_to_go", "physical_office_to_apply", "where_to_apply", "office", "place"),
    "spoken_script": ("spoken_script", "spoken", "audio_script", "speech", "tts_script"),
    "confidence": ("confidence", "certainty"),
}


def _pick(data: Dict[str, Any], field: str) -> Any:
    for key in ALIASES[field]:
        if key in data and data[key] not in (None, "", [], {}):
            return data[key]
    return None


def _flatten(value: Any) -> str:
    """Local models sometimes nest an object inside a string field; keep it readable."""
    if isinstance(value, dict):
        parts = [f"{k}: {v}" for k, v in value.items() if v not in (None, "", [], {})]
        return " | ".join(parts)
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def _normalise_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """Guarantee the response contract the UI depends on, whatever the model returned."""

    def as_list(value: Any) -> List[str]:
        if isinstance(value, list):
            return [_flatten(v).strip() for v in value if str(v).strip()]
        if isinstance(value, dict):
            return [f"{k}: {v}" for k, v in value.items()]
        if isinstance(value, str) and value.strip():
            return [
                p.strip("-•* ").strip()
                for p in value.replace(";", "\n").split("\n")
                if p.strip("-•* ")
            ]
        return []

    def as_text(value: Any) -> str:
        return _flatten(value).strip() if value else ""

    confidence = str(_pick(data, "confidence") or "medium").strip().lower()
    if confidence not in ("high", "medium", "low"):
        confidence = "medium"

    return {
        "scheme_name": as_text(_pick(data, "scheme_name")) or "Government scheme",
        "benefit_summary": as_text(_pick(data, "benefit_summary")),
        "eligibility": as_list(_pick(data, "eligibility")),
        "documents_needed": as_list(_pick(data, "documents_needed")),
        "where_to_go": as_text(_pick(data, "where_to_go")),
        "spoken_script": as_text(_pick(data, "spoken_script")),
        "confidence": confidence,
    }


def _sources_payload(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "title": r["title"],
            "url": r["url"],
            "official": r["official"],
            "excerpt": r.get("content", "")[:280],
        }
        for r in results
    ]


def _retrieve(search_query: str) -> tuple[List[Dict[str, Any]], str]:
    """Live search. Tavily when configured, else Gemini Search grounding tool."""
    if search.TAVILY_API_KEY:
        try:
            return search.search_tavily(search_query), search.TAVILY_MODEL_KEY
        except Exception as exc:  # noqa: BLE001 - fall back to Gemini search
            logger.warning("tavily failed (%s), falling back to Gemini grounding", exc)

    results, provider_name = _gemini_grounding_search(search_query)
    return results, provider_name


def _gemini_grounding_search(search_query: str) -> tuple[List[Dict[str, Any]], str]:
    if not llm.GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="no_search_backend: set TAVILY_API_KEY (recommended) or GEMINI_API_KEY",
        )
    from google import genai
    from google.genai import types

    prompt = (
        "Search the web for current official Indian government welfare schemes matching this "
        f"request: {search_query}. Prefer myscheme.gov.in, pib.gov.in and state .gov.in portals. "
        "List each scheme with its official name, benefit amount, eligibility, required documents "
        "and the office where a woman applies."
    )
    try:
        client = genai.Client(api_key=llm.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=llm.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            ),
        )
    except Exception as exc:  # noqa: BLE001
        status = getattr(exc, "code", None) or getattr(exc, "status_code", None)
        if status == 429 or "RESOURCE_EXHAUSTED" in str(exc):
            raise HTTPException(status_code=429, detail="quota_exceeded") from exc
        if status in (401, 403):
            raise HTTPException(status_code=502, detail="invalid_api_key") from exc
        raise HTTPException(status_code=502, detail=f"search_failed: {exc}") from exc

    results: List[Dict[str, Any]] = []
    try:
        chunks = response.candidates[0].grounding_metadata.grounding_chunks or []
    except (AttributeError, IndexError, TypeError):
        chunks = []
    for chunk in chunks:
        web = getattr(chunk, "web", None)
        url = getattr(web, "uri", None) if web else None
        if not url:
            continue
        results.append(
            {
                "title": (getattr(web, "title", None) or "Government official portal")[:140],
                "url": url,
                "content": " ".join((response.text or "").split())[:1200],
                "official": official_url_score(url) == 1,
                "score": 1.0,
            }
        )
    if not results:
        results = [
            {
                "title": "Gemini search grounding",
                "url": "https://www.google.com/search?q=" + search_query.replace(" ", "+"),
                "content": " ".join((response.text or "").split())[:1200],
                "official": False,
                "score": 1.0,
            }
        ]
    return search.rank_sources(results), search.GEMINI_MODEL_KEY


@app.post("/api/query")
async def process_user_query(req: UserQuery):
    language = req.language if req.language and req.language != "auto" else detect_language(req.query)
    search_query = build_search_query(req.query, language)

    results, retrieval = _retrieve(search_query)
    context = search.build_context(results)
    prompt = _build_prompt(req.query, language, search_query, context)

    try:
        raw, model = llm.generate(prompt, SYSTEM_INSTRUCTION, RESPONSE_SCHEMA)
    except llm.LLMError as exc:
        status = exc.status or 500
        if status >= 500 and str(exc).startswith("No LLM key"):
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        raise HTTPException(status_code=status, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("llm failure")
        raise HTTPException(status_code=500, detail=f"answer_failed: {exc}") from exc

    data = _normalise_payload(raw)
    data["sources"] = _sources_payload(results)
    data["language"] = language
    data["search_query"] = search_query
    data["retrieval"] = retrieval
    data["model"] = model
    data["verified"] = any(s["official"] for s in data["sources"])
    data["sources_consulted"] = len(data["sources"])
    return data


@app.get("/health")
def health():
    payload = {
        "status": "ok",
        "retrieval": search.retrieval_status(),
        "llm": llm.status(),
    }
    payload["ready"] = bool(
        (search.TAVILY_API_KEY or llm.GEMINI_API_KEY)
        and llm.provider() != "none"
    )
    return payload


@app.get("/api/schemes")
def popular_schemes():
    return {
        "schemes": [
            {"name": "PMMVY (Maternity Benefit)", "language": "Tamil"},
            {"name": "Lakhpati Didi (SHG Loan)", "language": "Hindi"},
            {"name": "PM Ujjwala Yojana (LPG)", "language": "Hindi"},
            {"name": "National Scholarship Portal", "language": "Tamil"},
        ]
    }
