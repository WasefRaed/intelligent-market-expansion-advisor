import json
import pytest
from app.advisory_service import selected_cities, build_evidence, run_advice


def test_selects_cities_from_location_terms():
    assert selected_cities("Which Dubai area is best near JLT?") == ["Dubai"]
    assert selected_cities("Compare Al Reem with Khalidiya") == ["Abu Dhabi"]
    assert selected_cities("Compare JLT vs Al Reem") == ["Dubai", "Abu Dhabi"]


def test_evidence_contains_concept_and_rankings():
    d = json.loads(build_evidence("Which Dubai area fits our restaurant?"))
    assert set(d["cities"]) == {"Dubai"}
    assert d["scenario_rankings"]["Dubai"]["scenario"] == "balanced"
    assert "MEATY PIZZA" in d["business_concept"]
    assert "Not fresh web research" in d["verification_level"]


def test_snapshot_evidence_selectively_includes_price_anchors():
    d = json.loads(build_evidence("What menu and pizza prices in Abu Dhabi?"))
    assert "illustrative_price_bands" in d
    assert "menu_strategy" in d
    assert "Dubai" not in d["cities"]


def test_deterministic_scenario_switch():
    a = json.loads(build_evidence("Dubai locations", "balanced"))
    b = json.loads(build_evidence("Dubai locations", "cost_control"))
    assert a["scenario_rankings"]["Dubai"]["weights"] != b["scenario_rankings"]["Dubai"]["weights"]


def test_invalid_empty_question_and_mode_fail_before_api():
    with pytest.raises(ValueError):
        build_evidence(" ")
    with pytest.raises(ValueError):
        run_advice("Where should we open?", mode="invalid")
