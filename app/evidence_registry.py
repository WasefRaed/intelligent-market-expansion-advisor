"""Auditable, offline public-source reference layer.

References have been human-reviewed once, not fetched on every user request.
Do not use them as proof of a whole LLM answer or site-level market statistics.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

_REGISTRY_PATH = Path(__file__).resolve().parents[1] / "data" / "source_registry.json"


@lru_cache(maxsize=1)
def source_registry() -> dict:
    data = json.loads(_REGISTRY_PATH.read_text(encoding="utf-8"))
    assert data["reviewed_on"]
    ids = set()
    for item in data["sources"]:
        assert item["id"] not in ids
        ids.add(item["id"])
        assert urlparse(item["url"]).scheme == "https"
        assert urlparse(item["url"]).hostname
        assert item["supported_claim"] and item["limitations"]
    return data


def selected_references(question: str, max_sources: int = 6) -> list[dict]:
    """Select only relevant narrow source notes, no inference or live search."""
    q = question.casefold()
    tax = any(t in q for t in ("vat", "tax", "financial", "finance", "regulat", "compliance", "corporate", "investment"))
    safety = any(t in q for t in ("license", "licens", "permit", "approval", "safety", "kitchen", "operation", "supplier", "regulat", "compliance"))
    dubai = any(t in q for t in ("dubai", "jlt", "jumeirah lakes", "deira", "business bay"))
    abu = any(t in q for t in ("abu dhabi", "zahiyah", "reem island", "tourist club"))
    location = any(t in q for t in ("where", "location", "branch", "expansion", "expand", "market-entry", "enter", "site", "jlt", "zahiyah"))
    selected = set()
    if tax:
        selected |= {"FTA-VAT-REG", "FTA-CT-RATES", "FTA-CT-REG"}
    if safety:
        if dubai or not abu:
            selected.add("DM-FOOD")
        if abu or not dubai:
            selected.add("UAE-FOOD-AUTH")
    if location and dubai:
        selected.add("DXB-JLT-GUIDE")
    if location and abu:
        selected.add("AUH-ZAHIYAH-GUIDE")
    return [s for s in source_registry()["sources"] if s["id"] in selected][:max_sources]


def reference_context(question: str) -> dict:
    """Compact scope-limited citation information for the model."""
    sources = selected_references(question)
    return {
        "reference_review_date": source_registry()["reviewed_on"],
        "source_mode": "offline_previously_reviewed_official_pages; NOT live research",
        "scope_warning": "Citing a URL supports only its supported_claim, not other claims in your answer.",
        "claim_references": [
            {"id": s["id"], "claim": s["supported_claim"], "url": s["url"], "limits": s["limitations"]}
            for s in sources
        ],
    }


def format_reference_notes(question: str) -> str:
    """Append facts independently of the model; never imply its claims were checked."""
    sources = selected_references(question)
    if not sources:
        return ""
    lines = [
        "### Reviewed source notes (not live research)",
        "The following official-page notes were reviewed on **" + source_registry()["reviewed_on"] + "**. "
        "They support ONLY the specific statements below; **they do not verify the AI recommendation, local demand, rents, competitor prices or profitability.**",
        "",
    ]
    for s in sources:
        lines.append(f"- **[{s['id']}] {s['publisher']}** — {s['supported_claim']} [Official page]({s['url']}). *Limit:* {s['limitations']}")
    return "\n".join(lines)
