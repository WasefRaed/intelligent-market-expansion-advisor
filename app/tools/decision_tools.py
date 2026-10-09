"""Deterministic *screening* of UAE areas using qualitative planning signals.

These ranks are a transparent demonstration of assumptions, NOT a site-level
investment score, rent estimate, measured footfall count or market forecast.
"""

import json
from typing import Literal

from app.tools.market_tools import load_market_data

ScorePriority = Literal["balanced", "cost_control", "demand_first"]

# These are subjective planning weights, not researched measures.
WEIGHTS = {
    "balanced": {"concept_fit": 0.50, "demand_proxy": 0.25, "cost_headroom": 0.25},
    "cost_control": {"concept_fit": 0.35, "demand_proxy": 0.15, "cost_headroom": 0.50},
    "demand_first": {"concept_fit": 0.40, "demand_proxy": 0.45, "cost_headroom": 0.15},
}

QUALITATIVE_SCALE = {
    "low": 1.0,
    "low-medium": 2.0,
    "medium": 3.0,
    "medium-high": 4.0,
    "high": 4.0,
    "very high": 5.0,
    "high on peaks": 3.5,  # High only on select days/dayparts
    "high local": 4.0,      # Geographic concentration not citywide
}


def _signal(label: str) -> float:
    try:
        return QUALITATIVE_SCALE[label.strip().lower()]
    except (KeyError, AttributeError) as exc:
        raise ValueError(f"Unknown qualitative signal: {label!r}") from exc


def area_screening(city: str, priority: ScorePriority = "balanced") -> dict:
    """Return scenario-dependent heuristic rankings and original input signals."""
    if priority not in WEIGHTS:
        raise ValueError(f"priority must be one of: {', '.join(WEIGHTS)}")
    data = load_market_data()
    match = next((name for name in data["cities"] if name.lower() == city.strip().lower()), None)
    if match is None:
        raise ValueError("city must be Dubai or Abu Dhabi")

    weights = WEIGHTS[priority]
    results = []
    for area in data["cities"][match]["areas"]:
        concept_fit = _signal(area["fit"])
        demand_proxy = _signal(area["traffic"])
        cost_headroom = 6.0 - _signal(area["rent_pressure"])
        raw_score = (
            weights["concept_fit"] * concept_fit
            + weights["demand_proxy"] * demand_proxy
            + weights["cost_headroom"] * cost_headroom
        )
        results.append({
            "name": area["name"],
            "screening_score_out_of_5": round(raw_score, 2),
            "source_signals": {
                "fit": area["fit"],
                "traffic_qualitative_proxy": area["traffic"],
                "rent_pressure_qualitative_proxy": area["rent_pressure"],
            },
            "audience": area["audience"],
            "why": area["why"],
            "tradeoff": area["tradeoff"],
        })

    # Equal scores share a rank; the original snapshot order remains only
    # a display ordering, not a claim of superior commercial performance.
    results.sort(key=lambda r: r["screening_score_out_of_5"], reverse=True)
    last_score = None
    last_rank = None
    for i, row in enumerate(results, start=1):
        score = row["screening_score_out_of_5"]
        if score != last_score:
            last_rank = i
        row["rank"] = last_rank
        row["tied"] = sum(other["screening_score_out_of_5"] == score for other in results) > 1
        last_score = score
    return {
        "city": match,
        "scenario": priority,
        "weights": weights,
        "ranking": results,
        "interpretation": (
            "Exploratory heuristic only, built from qualitative snapshot labels; NOT "
            "measured footfall, property rent, expected sales or statistical confidence. "
            "Scores are relative screening aids, not investment recommendations. "
            "Verify site rent, parking, frontage, customer interviews, delivery-radius "
            "performance, restaurant competition and kitchen licensing before signing a lease."
        ),
    }


def get_area_screening(city: str, priority: ScorePriority = "balanced") -> str:
    """Screen Dubai or Abu Dhabi areas with transparent scenario weights and qualitative signals; no fabricated site data."""
    return json.dumps(area_screening(city, priority), ensure_ascii=False, indent=2)
