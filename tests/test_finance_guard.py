"""Regression tests for the critical incorrect-LLM-arithmetic case."""
import pytest

from app.finance_guard import deterministic_financial_answer, extract_financial_inputs
from app.advisory_service import run_advice

FINANCIAL_QUESTION = """Evaluate financial feasibility using these illustrative assumptions:
Daily orders: 100
Average order value: AED 49
Trading days per month: 30
Food cost: 20% of sales
Combined labour, rent, and other operating costs: 37% of sales
Delivery share: 30% of orders and sales
Delivery commission: 25% of delivery sales
Calculate monthly revenue, contribution and contribution margin.
Compare scenarios with 70, 100, and 130 daily orders, holding other assumptions constant.
"""

def test_parses_only_explicit_input_values():
    parsed = extract_financial_inputs(FINANCIAL_QUESTION)
    assert parsed is not None
    assert parsed.scenarios == (70, 100, 130)
    assert parsed.ticket == 49
    assert parsed.other == .37
    assert parsed.days == 30

def test_exact_test7_financial_regression():
    answer = deterministic_financial_answer(FINANCIAL_QUESTION)
    assert answer is not None
    for expected in ("36,529.50", "52,185.00", "67,840.50", "35.50"):
        assert expected in answer
    assert "64,680" not in answer
    assert "net-profit estimate" in answer

@pytest.mark.parametrize("mode", ["focused", "team"])
def test_full_numeric_question_bypasses_agnos_external_api(mode, monkeypatch):
    # Fail immediately if any attempt to prepare prompt evidence / import Agno
    # occurred during deterministic finance routing.
    import app.advisory_service as module
    monkeypatch.setattr(module, "build_evidence", lambda *a, **k: (_ for _ in ()).throw(AssertionError("API branch entered")))
    answer = run_advice(FINANCIAL_QUESTION, mode=mode)
    assert "52,185.00" in answer

def test_missing_financial_inputs_are_not_silently_filled():
    assert extract_financial_inputs("Calculate monthly profit for 100 orders with 30% food cost") is None

def test_reject_invalid_specified_financial_data():
    bad = FINANCIAL_QUESTION.replace("Trading days per month: 30", "Trading days per month: 32")
    with pytest.raises(ValueError, match="trading days"):
        extract_financial_inputs(bad)
