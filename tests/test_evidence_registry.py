"""Source-provenance policy regression tests: zero API calls."""
import json
from types import SimpleNamespace

from app.advisory_service import build_evidence, run_advice
from app.evidence_registry import source_registry, selected_references, reference_context, format_reference_notes


def test_source_registry_unique_https_and_review_date():
    data = source_registry()
    assert data["reviewed_on"] == "2026-10-09"
    assert len(data["sources"]) >= 6
    assert len({s["id"] for s in data["sources"]}) == len(data["sources"])
    for source in data["sources"]:
        assert source["url"].startswith("https://")
        assert source["supported_claim"] and source["limitations"]


def test_jlt_location_gets_official_description_not_tax_and_not_rent():
    refs = selected_references("Is JLT in Dubai a suitable first branch location?")
    assert [s["id"] for s in refs] == ["DXB-JLT-GUIDE"]
    assert "rent" in refs[0]["limitations"].lower() or "rental" in refs[0]["limitations"].lower()


def test_abu_dhabi_zahiyah_gets_no_dubai_reference():
    refs = selected_references("Compare Al Zahiyah in Abu Dhabi for branch location")
    ids = {s["id"] for s in refs}
    assert "AUH-ZAHIYAH-GUIDE" in ids
    assert "DXB-JLT-GUIDE" not in ids


def test_tax_claims_are_narrow_and_correct():
    refs = selected_references("Check VAT and Corporate Tax registration for the restaurant")
    ids = {s["id"] for s in refs}
    assert {"FTA-VAT-REG", "FTA-CT-RATES", "FTA-CT-REG"} <= ids
    ct = next(s for s in refs if s["id"] == "FTA-CT-RATES")
    assert "taxable income" in ct["supported_claim"].lower()
    assert "not turnover" in ct["limitations"].lower()


def test_non_regulatory_menu_without_place_does_not_pretend_to_browse():
    assert selected_references("Propose three new sauces for the kebab sandwich") == []
    assert format_reference_notes("Propose three new sauces for the kebab sandwich") == ""


def test_model_evidence_includes_review_date_and_bounded_urls():
    evidence = json.loads(build_evidence("Compare JLT Dubai vs Al Zahiyah Abu Dhabi"))
    notes = evidence["reviewed_official_source_notes"]
    assert notes["source_mode"] == "offline_previously_reviewed_official_pages; NOT live research"
    assert {item["id"] for item in notes["claim_references"]} == {"DXB-JLT-GUIDE", "AUH-ZAHIYAH-GUIDE"}
    assert all("https://" in item["url"] for item in notes["claim_references"])
    assert "internal_planning_only" == evidence["evidence_policy"]["origin"]


def test_reference_section_not_falsely_applied_to_all_ai_claims(monkeypatch):
    class FakeAgent:
        def run(self, _question):
            return SimpleNamespace(content="### Recommendation\nConditionally compare one Dubai site and one Abu Dhabi site.")

    monkeypatch.setattr("app.advisory_service._focused_agent", lambda: FakeAgent())
    answer = run_advice("Compare JLT Dubai vs Al Zahiyah Abu Dhabi")
    assert "Conditionally compare" in answer
    assert "Reviewed source notes (not live research)" in answer
    assert "do not verify the AI recommendation" in answer
    assert "visitdubai.com" in answer and "visitabudhabi.ae" in answer


def test_safe_reference_context_has_no_claim_of_new_web_research():
    ctx = reference_context("What is Dubai food licensing and tax registration?")
    assert "NOT live research" in ctx["source_mode"]
    assert "NOT live research" not in ctx["scope_warning"]  # scope warning is distinct
    assert all("supported_claim" not in rec for rec in ctx["claim_references"])
