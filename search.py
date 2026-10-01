"""Retrieval layer for Sakhi AI.

Two providers:
  * Tavily  -> https://api.tavily.com/search   (preferred, set TAVILY_API_KEY)
  * Gemini Google Search grounding tool        (used when Tavily is not configured)

Both paths return the same shape: a list of
``{"title", "url", "content", "official", "score"}`` dicts, with official
government domains ranked first.
"""

import os
import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import httpx

from query import official_url_score

logger = logging.getLogger("sakhi.search")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY") or os.getenv("TAVILY_KEY")
TAVILY_URL = "https://api.tavily.com/search"
TAVILY_MODEL_KEY = "tavily"
GEMINI_MODEL_KEY = "google_search_grounding"

MAX_RESULTS = int(os.getenv("SAKILY_MAX_RESULTS", "6"))
TIMEOUT = float(os.getenv("TAKILY_TIMEOUT", "25"))


def _normalise(title: Any, url: Any, content: Any, score: Any) -> Dict[str, Any]:
    url = str(url or "")
    return {
        "title": str(title or "Government source").strip()[:140],
        "url": url,
        "content": " ".join(str(content or "").split())[:1200],
        "official": official_url_score(url) == 1,
        "score": float(score or 0),
    }


def rank_sources(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Official .gov.in evidence first, then by relevance score. Duplicates removed."""
    seen = set()
    unique: List[Dict[str, Any]] = []
    for item in results:
        url = item.get("url", "")
        if not url or url in seen:
            continue
        seen.add(url)
        unique.append(item)
    unique.sort(key=lambda r: (not r["official"], -r["score"]))
    return unique


def search_tavily(query: str, max_results: int = MAX_RESULTS) -> List[Dict[str, Any]]:
    """Live web search restricted to Indian government portals."""
    if not TAVILY_API_KEY:
        raise RuntimeError("TAVILY_API_KEY is not set")

    enhanced = (
        f"{query} site:myscheme.gov.in OR site:pib.gov.in "
        "OR site:nsp.edu.in OR site:nhm.gov.in OR site:*.gov.in"
    )
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": enhanced,
        "search_depth": "advanced",
        "max_results": max_results,
        "include_answer": False,
        "include_raw_content": False,
    }
    with httpx.Client(timeout=TIMEOUT) as client:
        response = client.post(TAVILY_URL, json=payload)
        response.raise_for_status()
        data = response.json()

    results = [
        _normalise(r.get("title"), r.get("url"), r.get("content"), r.get("score"))
        for r in data.get("results", [])
    ]
    logger.info("tavily_results=%d official=%d", len(results), sum(r["official"] for r in results))
    return rank_sources(results)


def build_context(results: List[Dict[str, Any]], limit: int = 5) -> str:
    """Render sources into a compact, citable context block for the LLM."""
    if not results:
        return ""
    blocks: List[str] = []
    for i, r in enumerate(results[:limit], start=1):
        blocks.append(
            f"[SOURCE {i}] {r['title']}\nURL: {r['url']}\nOFFICIAL: {'yes' if r['official'] else 'no'}\n"
            f"EXCERPT: {r['content'] or '(no text returned)'}"
        )
    return "\n\n".join(blocks)


def retrieval_status() -> Dict[str, Any]:
    return {
        "provider": TAVILY_MODEL_KEY if TAVILY_API_KEY else GEMINI_MODEL_KEY,
        "tavily_configured": bool(TAVILY_API_KEY),
        "max_results": MAX_RESULTS,
    }
