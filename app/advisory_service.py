"""Quota-aware advisor entry point and reproducible internal evidence assembly.

Focused mode uses one Agno Agent with prepared context rather than a Team of
specialists. Full Team mode remains available for advanced evaluations.
"""
from __future__ import annotations

import json
from functools import lru_cache
import re
from typing import Literal

from app.config import MODEL_ID, FALLBACK_MODEL_ID, ENABLE_LIVE_RESEARCH
from app.runtime import friendly_provider_error
from app.quota_guard import ensure_api_allowed, record_quota_failure
from app.tools.decision_tools import area_screening
from app.tools.market_tools import load_market_data
from app.finance_guard import deterministic_financial_answer
from app.evidence_registry import reference_context, format_reference_notes

AnalysisMode = Literal["focused", "team"]


def selected_cities(question: str) -> list[str]:
    q = question.casefold()
    dubai = any(word in q for word in ("dubai", "jlt", "jumeirah", "business bay", "deira", "jbr", "marina", "jvc"))
    abu = any(word in q for word in ("abu dhabi", "al reem", "khalidiya", "yas island", "al zahiyah", "mussafah"))
    if dubai and not abu:
        return ["Dubai"]
    if abu and not dubai:
        return ["Abu Dhabi"]
    return ["Dubai", "Abu Dhabi"]


def build_evidence(question: str, priority: str = "balanced") -> str:
    """Context is entirely from the dated snapshot and deterministic tools.

    Never present this as live search results, verified footfall or current rent.
    """
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Please enter an executive question")
    data = load_market_data()
    q = question.casefold()
    cities = selected_cities(q)
    market = {city: data["cities"][city] for city in cities}
    screenings = {city: area_screening(city, priority) for city in cities}
    evidence: dict = {
        "business_concept": "Jordanian fast-casual MEATY PIZZA and KEBAB SANDWICHES; other dishes are not assumed.",
        "snapshot_date": data["metadata"].get("snapshot_date"),
        "evidence_policy": {
            "origin": "internal_planning_only",
            "source_urls_are": "research leads only; not proof claims have been checked",
            "verified_external_claims": "none supplied by this snapshot",
            "scoring_basis": "subjective qualitative proxy weights; ties represent no preference",
        },
        "verification_level": (
            "Internal qualitative planning snapshot and assumption-driven screening. "
            "Not fresh web research, validated lease offers, measured footfall or verified prices."
        ),
        "screening_priority": priority,
        "reviewed_official_source_notes": reference_context(question),
        "cities": market,
        "scenario_rankings": screenings,
    }
    pricing_terms = ("price", "pricing", "menu", "pizza", "kebab", "product", "combo", "portion", "margin")
    comp_terms = ("compet", "position", "market", "rival", "differen")
    marketing_terms = ("market", "launch", "customer", "campaign", "brand", "advertis", "90-day")
    ops_terms = ("operation", "risk", "licens", "regulat", "supplier", "staff", "delivery", "tax", "compliance", "season")
    if any(term in q for term in pricing_terms):
        evidence["menu_strategy"] = data["menu_strategy"]
        evidence["illustrative_price_bands"] = data["price_bands"]["bands_aed"]
    if any(term in q for term in comp_terms):
        evidence["competitor_benchmarks"] = [c for c in data["competitors"] if any(city in c["cities"] for city in cities)]
    if any(term in q for term in marketing_terms):
        evidence["marketing_playbook"] = data["marketing"]
    if any(term in q for term in ops_terms):
        evidence["operations"] = data["operations"]
        evidence["regulatory_overview"] = data["regulatory"]
        evidence["seasonality"] = data["seasonality"]
    # Compact serialization to lower tokens and protect free-tier request budgets.
    return json.dumps(evidence, ensure_ascii=False, separators=(",", ":"))


@lru_cache(maxsize=1)
def _focused_agent():
    # Import lazily so source/data tools and unit tests work without API packages.
    from agno.agent import Agent
    from agno.models.google import Gemini

    return Agent(
        name="Focused UAE Expansion Advisor",
        role="Produce grounded, cautious executive advice using supplied UAE restaurant planning data",
        model=Gemini(id=MODEL_ID, search=False, retries=0),
        fallback_models=[Gemini(id=FALLBACK_MODEL_ID, search=False, retries=0)],
        # Numerical answers with complete explicit assumptions are calculated in
        # Python before this agent is invoked. Do not let an LLM call the
        # calculator with invented operating assumptions.
        tools=[],
        instructions=[
            "You advise a Jordanian fast-casual brand selling MEATY PIZZA and KEBAB SANDWICHES.",
            "The supplied planning evidence is a dated internal snapshot, NOT live web research.",
            "Never fabricate sources, site rents, actual footfall, current competitor pricing, permits or quantitative statistics.",
            "Never claim a factual assertion is verified unless the input includes an explicit, checkable source.",
            "Some evidence includes reviewed_official_source_notes. Cite the ID and provided URL only for its EXACT supported_claim; never use one citation to validate an unrelated claim.",
            "The reviewed official pages were checked on the noted date, not fetched for this request, and do not establish rental prices, footfall, local demand, competitor market share or investment ROI.",
            "Do not assume the restaurant offers mansaf, zarb or a premium dine-in format.",
            "Do not invent business budgets, restaurant dimensions, menu prices or delivery commission contracts.",
            "Never generate projected monthly revenue, contribution, profit, tax or ROI figures from assumptions you choose yourself.",
            "When all financial assumptions are supplied the application provides a Python-calculated scenario; quote it exactly.",
            "If no computed scenario is provided, offer the Unit Economics tab and discuss inputs instead of producing financial totals.",
            "Never claim to have invoked a Python tool unless a computed result is explicitly present in the request context.",
            "If numerical assumptions are missing or unclear, request them or refer to Unit Economics rather than guessing.",
            "Treat snapshot tax/regulatory descriptions as UNVERIFIED research leads; do not call them verified without current checked sources.",
            "Recommend only one initial branch unless the client explicitly requests simultaneous openings.",
            "Optional menu extensions, open-fire cooking, founder narratives and equipment specifications are PROPOSALS, not established client facts.",
            "Do not recommend diverting marketplace customers in violation of platform contract terms or using personal data without appropriate consent.",
            "In an unsafe food-supply disruption, pause affected menu items or opening rather than using unapproved suppliers.",
            "Use the provided scenario screening as a baseline and explain any deviation.",
            "Never rank a neighborhood absent from the supplied snapshot as if it had been screened; mark such places as unscreened candidates requiring fresh evidence.",
            "If facts are unavailable, state needed validation, assumptions and next actions.",
            "Label all heuristic scores and internal snapshot observations as unverified planning inputs.",
            "Respond with: Recommendation; Why; Alternatives/tradeoffs; Evidence limits; 3 next actions.",
            "Keep answers concise and specific, suitable for an executive decision memo.",
            "Answer every explicitly requested heading/topic, especially in integrated executive questions.",
            "Where heuristic scores tie, provide a conditional recommendation; never imply snapshot order is commercial evidence.",
            "Cross-city screening scores compare planning assumptions only, not proven sales, site profitability or ROI.",
            "Potential competitive whitespace is a hypothesis, never an established market gap without an actual competitor audit.",
            "Never promise licensing completion or opening by Day 90; use gates and conditional timelines.",
            "Any KPI threshold without provenance is an illustrative management target, not a verified benchmark.",
        ],
        markdown=True,
    )



def is_standalone_financial_question(question: str) -> bool:
    """Do not drop an integrated executive brief just because it includes numbers.

    Routing is intentionally conservative: mixed-domain prompts go to Agno
    with the deterministic calculation attached as evidence.
    """
    mixed_topics = (
        "market entry", "market-entry", "expand into", "which city",
        "which location", "branch location", "site selection", "jlt", "al reem",
        "al zahiyah", "compare dubai", "competitor", "marketing strategy",
        "launch plan", "90-day", "roadmap", "supplier strategy",
        "licensing plan", "risk matrix", "executive recommendation",
    )
    lowered = question.casefold()
    return not any(topic in lowered for topic in mixed_topics)


def suppress_unverified_financial_projections(question: str, answer: str) -> str:
    """Withhold unsupported model-generated unit-economics sections.

    A fully specified scenario is routed through Python. Any other precise
    numeric financial table would have unknown assumptions and no audit trail.
    This guard is intentionally a narrow backstop, not general fact-checking.
    """
    if deterministic_financial_answer(question) is not None:
        return answer
    sections = re.split(r"(?=^#{2,6}\s+)", answer, flags=re.MULTILINE)
    result = []
    blocked = 0
    for section in sections:
        heading = section.split("\n", 1)[0].casefold()
        is_finance = any(term in heading for term in (
            "unit economics", "financial scenario", "financial model",
            "financial projection", "financial feasibility", "profitability model",
            "financial analysis", "financial metrics", "sales forecast", "profit forecast",
        ))
        has_money = bool(re.search(r"\bAED\s*[\d,]+", section, flags=re.IGNORECASE))
        has_computed_metrics = bool(re.search(
            r"\b(?:monthly (?:gross )?(?:revenue|sales|profit|contribution)|contribution margin)\b",
            section, flags=re.IGNORECASE,
        ))
        if is_finance and has_money and has_computed_metrics:
            result.append(
                "### Financial projections — awaiting validated inputs\n\n"
                "Unrequested projected monetary totals were withheld because no "
                "complete operating assumptions were supplied. Use **Unit Economics** "
                "or provide orders/day, average ticket, trading days, food and "
                "operating costs, delivery share, and commission for a Python calculation.\n\n"
            )
            blocked += 1
        else:
            result.append(section)
    guarded = "".join(result)
    # For paragraphs without headings, fail closed rather than show an
    # unauditable projected financial statement as executive advice.
    if not blocked and len(sections) == 1:
        has_monthly_claim = bool(re.search(
            r"\bmonthly (?:gross )?(?:revenue|sales|profit|contribution)\b.{0,140}?\bAED\s*[\d,]+",
            answer, flags=re.IGNORECASE | re.DOTALL,
        ))
        if has_monthly_claim:
            return (
                "**Financial answer withheld:** the generated draft contained precise "
                "monthly financial projections without sufficient validated inputs. "
                "Please specify operating assumptions or use the Unit Economics tab."
            )
    return guarded


def run_advice(question: str, mode: AnalysisMode = "focused", priority: str = "balanced") -> str:
    """Focused uses a single inference entrypoint; team can require many calls."""
    if mode not in ("focused", "team"):
        raise ValueError("mode must be focused or team")
    # Fully specified numeric scenarios bypass generative arithmetic entirely.
    # Works even without a Gemini key or network connection.
    safe_calculation = deterministic_financial_answer(question)
    if safe_calculation is not None and is_standalone_financial_question(question):
        return safe_calculation
    # A previous provider 429 with an explicit retry delay must not trigger
    # another cascade of model calls just because Streamlit was restarted.
    ensure_api_allowed()
    evidence = build_evidence(question, priority)
    if safe_calculation is not None:
        evidence += (
            "\n\nPYTHON-CALCULATED FINANCIAL SCENARIO (audited arithmetic; "
            "do not change the figures):\n" + safe_calculation
        )
    try:
        if mode == "team":
            from app.agents import advisor
            result = advisor.run(
                "Client's executive question: " + question + "\n\n" +
                "Internal planning evidence (not current verified market data):\n" + evidence +
                "\nUse this baseline for the comparison. Only declare claims web-verified when URLs are traceable."
            )
        else:
            result = _focused_agent().run(
                "QUESTION:\n" + question + "\n\nINTERNAL PLANNING EVIDENCE:\n" + evidence
            )
    except Exception as exc:
        # Record the original API error *before* turning it into a friendly
        # message, so RetryInfo and daily/per-minute quota details survive.
        record_quota_failure(exc)
        raise
    answer = str(getattr(result, "content", result))
    provider_error = friendly_provider_error(answer)
    if provider_error:
        record_quota_failure(answer)
        raise RuntimeError(provider_error)
    if not answer.strip():
        raise RuntimeError("The AI returned an empty answer. No market recommendation was generated.")
    safe_answer = suppress_unverified_financial_projections(question, answer)
    if not ENABLE_LIVE_RESEARCH:
        safe_answer += (
            "\n\n---\n**Evidence status:** This response draws on the dated "
            "internal planning snapshot (2026-10-07), not live-verified external "
            "research. Any market, pricing, legal or tax claims require independent "
            "source confirmation before investment."
        )
    reference_notes = format_reference_notes(question)
    if reference_notes:
        safe_answer += "\n\n---\n" + reference_notes
    return safe_answer
