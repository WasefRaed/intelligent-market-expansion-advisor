"""Offline regression tests; no Google API key or external network required."""
import json
import math
import pytest

from app.tools.market_tools import (
    get_city_profile, get_competitor_landscape, get_menu_and_pricing,
    get_marketing_playbook, get_expansion_risk_playbook,
    calculate_unit_economics, load_market_data,
)
from app.tools.decision_tools import area_screening, get_area_screening, WEIGHTS


def test_city_profiles():
    assert "Jumeirah Lakes Towers (JLT)" in get_city_profile("Dubai")
    assert "Al Reem Island" in get_city_profile("Abu Dhabi")
    assert "Jumeirah Lakes Towers (JLT)" in get_city_profile("  dubai  ")
    assert "Unsupported city" in get_city_profile("Paris")


def test_competitor_filter():
    all_rows = json.loads(get_competitor_landscape())
    assert any(row["name"] == "Zaatar w Zeit" for row in all_rows)
    dubai_rows = json.loads(get_competitor_landscape("Dubai"))
    assert all("Dubai" in row["cities"] for row in dubai_rows)
    assert len(dubai_rows) <= len(all_rows)


def test_menu_pricing():
    result = json.loads(get_menu_and_pricing())
    assert any("kebab" in x["item"].lower() for x in result["pricing"]["bands_aed"])
    assert any("pizza" in x["item"].lower() for x in result["pricing"]["bands_aed"])
    assert any("Meat Pizza" in x for x in result["menu"]["hero_items"])


def test_marketing_ops():
    assert "prelaunch" in get_marketing_playbook()
    assert "delivery" in get_expansion_risk_playbook()


def test_unit_economics_expected_values():
    result = json.loads(calculate_unit_economics(100, 45))
    assert result["monthly_sales_aed"] == 135000
    assert result["food_cost_aed"] == 40500
    assert result["delivery_commission_aed"] == 11812.5
    assert result["illustrative_contribution_before_tax_and_capex_aed"] == 21937.5
    assert "not a real P&L" in result["warning"]


@pytest.mark.parametrize("orders", [-1, 0, 1.5, True, "5", None])
def test_reject_bad_order_counts(orders):
    with pytest.raises(ValueError, match="orders_per_day"):
        calculate_unit_economics(orders, 45)


@pytest.mark.parametrize("ticket", [-5, 0, float("inf"), float("nan"), True, None])
def test_reject_bad_tickets(ticket):
    with pytest.raises(ValueError, match="average_ticket_aed"):
        calculate_unit_economics(20, ticket)


@pytest.mark.parametrize("kw", [
    {"food_cost_pct": -0.1}, {"food_cost_pct": 1.1},
    {"labor_rent_other_pct": float("nan")},
    {"delivery_share": -0.1}, {"delivery_share": 1.1},
    {"delivery_commission_pct": float("inf")},
])
def test_reject_bad_rates(kw):
    with pytest.raises(ValueError):
        calculate_unit_economics(100, 45, **kw)


def test_screening_contains_all_areas_without_fake_data():
    d = load_market_data()
    for city in ("Dubai", "Abu Dhabi"):
        result = area_screening(city)
        assert len(result["ranking"]) == len(d["cities"][city]["areas"])
        ranks = [x["rank"] for x in result["ranking"]]
        assert ranks == sorted(ranks)
        assert ranks[0] == 1
        assert all(1 <= rank <= len(ranks) for rank in ranks)
        assert all(
            a["rank"] == b["rank"]
            for a in result["ranking"] for b in result["ranking"]
            if a["screening_score_out_of_5"] == b["screening_score_out_of_5"]
        )
        assert all(1 <= x["screening_score_out_of_5"] <= 5 for x in result["ranking"])
        assert "NOT" in result["interpretation"]


def test_screening_deterministic_and_transparent():
    a = area_screening("Dubai", "balanced")
    b = area_screening("Dubai", "balanced")
    assert a == b
    assert math.isclose(sum(a["weights"].values()), 1)
    assert isinstance(json.loads(get_area_screening("Dubai")), dict)
    for weights in WEIGHTS.values():
        assert math.isclose(sum(weights.values()), 1.0)


def test_screening_priorities_not_hidden():
    cost = area_screening("Dubai", "cost_control")
    demand = area_screening("Dubai", "demand_first")
    assert cost["weights"] != demand["weights"]


@pytest.mark.parametrize("city,scenario", [("Paris", "balanced"), ("Dubai", "magic")])
def test_screening_rejects_unsupported_inputs(city, scenario):
    with pytest.raises(ValueError):
        area_screening(city, scenario)


def test_snapshot_has_date_currency_and_concept():
    data = load_market_data()
    assert data["metadata"]["currency"] == "AED"
    assert data["metadata"]["snapshot_date"]
    assert any("Meat Pizza" in x for x in data["menu_strategy"]["hero_items"])
    assert all(r["source"].startswith("https://") for r in data["competitors"])


def test_explicit_ties_do_not_claim_priority():
    ranked = area_screening("Dubai", "balanced")["ranking"]
    jlt = next(r for r in ranked if "JLT" in r["name"])
    deira = next(r for r in ranked if "Deira" in r["name"])
    assert jlt["screening_score_out_of_5"] == deira["screening_score_out_of_5"]
    assert jlt["rank"] == deira["rank"]
    assert jlt["tied"] and deira["tied"]

def test_variable_trading_days_and_invalid_day_count():
    data = json.loads(calculate_unit_economics(100, 49, .2, .37, .3, .25, trading_days_per_month=25))
    assert data["monthly_sales_aed"] == 122500
    assert data["monthly_orders"] == 2500
    for days in (0, 32, True, 30.2):
        with pytest.raises(ValueError, match="trading_days_per_month"):
            calculate_unit_economics(100, 49, trading_days_per_month=days)
