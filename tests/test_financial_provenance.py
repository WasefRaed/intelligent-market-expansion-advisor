"""Offline tests for auditable financial claims and mixed-domain routing."""
from types import SimpleNamespace

from app.advisory_service import (
    is_standalone_financial_question,
    run_advice,
    suppress_unverified_financial_projections,
)
from tests.test_finance_guard import FINANCIAL_QUESTION


def test_pure_financial_scenario_still_uses_deterministic_route():
    assert is_standalone_financial_question(FINANCIAL_QUESTION)
    answer = run_advice(FINANCIAL_QUESTION)
    assert "52,185.00" in answer
    assert "calculated in Python" in answer


def test_integrated_question_with_finance_data_not_reduced_to_table(monkeypatch):
    prompt = (FINANCIAL_QUESTION + "\nBuild a 90-day launch plan and compare Dubai vs Abu Dhabi "
              "for our branch location and executive recommendation.")
    seen = []

    class FakeAgent:
        def run(self, question):
            seen.append(question)
            return SimpleNamespace(content="### Recommendation\nOpen one initial branch conditionally.\n")

    monkeypatch.setattr("app.advisory_service._focused_agent", lambda: FakeAgent())
    answer = run_advice(prompt)
    assert "Open one initial branch" in answer
    assert len(seen) == 1
    assert "PYTHON-CALCULATED FINANCIAL SCENARIO" in seen[0]
    assert "52,185.00" in seen[0]


def test_removes_unrequested_financial_statement_keeps_recommendations():
    generated = (
        "### Recommendation\nStart in JLT conditionally.\n\n"
        "### Illustrative Unit Economics (Planning Model Output)\n"
        "Monthly Gross Revenue: AED 135,000.00\n"
        "Monthly contribution: AED 24,300.00\n"
        "Contribution margin: 18%\n\n"
        "### Evidence Limits\nThe site data is an unverified heuristic.\n"
    )
    out = suppress_unverified_financial_projections("Where should we open first?", generated)
    assert "Start in JLT" in out
    assert "Evidence Limits" in out
    assert "135,000" not in out
    assert "24,300" not in out
    assert "Financial projections — awaiting validated inputs" in out


def test_unheaded_monthly_revenue_claim_is_withheld():
    generated = "Projected monthly revenue will be AED 135,000 and monthly contribution AED 24,300."
    out = suppress_unverified_financial_projections("Advise our expansion", generated)
    assert "answer withheld" in out
    assert "135,000" not in out


def test_menu_price_ranges_are_not_suppressed():
    generated = (
        "### Menu and Pricing\n"
        "Kebab sandwiches: AED 24–34; individual meat pizzas: AED 38–52.\n"
        "These are unverified planning ranges."
    )
    out = suppress_unverified_financial_projections("Suggest menu pricing", generated)
    assert out == generated


def test_generated_claims_removed_from_actual_model_response(monkeypatch):
    class FakeAgent:
        def run(self, question):
            return SimpleNamespace(content=(
                "### Recommendation\nChoose one site only.\n"
                "### Illustrative Unit Economics\n"
                "Monthly revenue: AED 135,000; monthly contribution: AED 24,300.\n"
                "### Five Actions\nValidate rent quotes.\n"
            ))

    monkeypatch.setattr("app.advisory_service._focused_agent", lambda: FakeAgent())
    out = run_advice("Prepare an executive recommendation for Dubai and Abu Dhabi")
    assert "Choose one site" in out
    assert "Validate rent quotes" in out
    assert "135,000" not in out
    assert "Financial projections — awaiting validated inputs" in out
