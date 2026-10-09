# Phase 3 — Financial integrity and evidence safeguards

## Changes

- `app/finance_guard.py`: recognizes clearly labelled complete scenario inputs and builds a deterministic Markdown comparison through `calculate_unit_economics`. This direct path **does not call Gemini**.
- `app/advisory_service.py`: uses financial deterministic path for focused/team text requests if complete; provides Python calculator as an Agno tool for focused-mode advisory questions that need it; strengthens evidence, business scope and KPI rules.
- `app/tools/market_tools.py`: supports user-chosen trading days (1–31), reports monthly orders, retains limitations.
- `app/tools/decision_tools.py`: equal screening scores now receive the same rank; original snapshot ordering is only presentation.
- `app/ui.py`: horizontal location/cost charts, tied-ranking labels, trading-days input and automated low/base/high financial scenarios.
- `evals/USER_TEST_RESULTS.md`: manual findings from 10 project questions, clear pass limitations and regression requirements.
- `tests/test_finance_guard.py`: regression test on the previously incorrect AED 64,680 vs correct AED 52,185 calculation, verifies no Agno call for complete scenarios.

## Local run (PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run app/ui.py
```

Set `.env` from previous project (never commit it). The local scenario finance tab works without `.env` or internet.

## Demonstration of the critical fix

Send this to AI Advisor in either mode; it should be computed locally and return immediately even without Gemini:

> Evaluate financial feasibility using these illustrative assumptions: Daily orders: 100; Average order value: AED 49; Trading days per month: 30; Food cost: 20%; Combined labour, rent, and other operating costs: 37%; Delivery share: 30%; Delivery commission: 25%. Compare scenarios with 70, 100, and 130 daily orders.

Expected contributions: **AED 36,529.50**, **AED 52,185.00**, **AED 67,840.50** (all 35.5%).

## Not yet verified

Live Agno tool routing, Gemini generation, Streamlit screenshots/UI behavior, web search evidence grounding, official regulation sources, business site validation and investment projections are not verified by offline tests. Do not imply otherwise.
