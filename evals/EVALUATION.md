# Evaluation / Testing

> **Historical design-time question plan (October 8).** This file lists the original ten candidate questions and quality criteria. It is **not** the record of ten executed runs. For actual user-run scenarios, outcomes, and Phase 6 status see [`FINAL_EVALUATION_REPORT.md`](FINAL_EVALUATION_REPORT.md) and [`USER_TEST_RESULTS.md`](USER_TEST_RESULTS.md).


## Evaluation method

The advisor was designed against 10 executive questions covering all required advisory domains plus extra expansion topics. A successful answer should: (1) identify the correct city/decision, (2) use the evidence tools, (3) separate facts from estimates, (4) state tradeoffs, and (5) end with actionable next steps or validation metrics.

## Test questions

| # | Executive question | Expected behavior |
|---|---|---|
| 1 | Which Dubai area should we target first? | Rank areas and explain audience/rent/traffic tradeoffs. |
| 2 | Compare JLT vs Al Reem Island. | Cross-city comparison with a clear recommendation. |
| 3 | Who are our competitors? | Segment direct/adjacent competitors and identify whitespace. |
| 4 | How should we adapt the menu? | Give hero products, portions, localization and simplification. |
| 5 | What should we charge? | Give AED bands, positioning logic and delivery-margin caveat. |
| 6 | Build a launch plan. | Pre-launch, launch week and 90-day retention with KPIs. |
| 7 | How should delivery work? | Explain acquisition vs contribution-margin tradeoff and first-party retention. |
| 8 | What staffing/supply model is needed? | Cover store manager, SOPs, cross-training and supplier redundancy. |
| 9 | What legal/tax items matter? | Provide a validation checklist; avoid pretending to give legal advice. |
| 10 | How should Ramadan/summer/Eid change the plan? | Explain hours, bundles, delivery and seasonal marketing adaptations. |

## What should work well

- Questions about areas should return JLT and Al Reem as strong initial candidates, while explicitly noting that rent and footfall must be validated at site level.
- Competitive questions should identify Zaatar w Zeit, Zaroob, Laffah, Operation: Falafel and PizzaExpress as useful benchmarks, but should not claim market share.
- Menu/pricing questions should produce the strategic AED bands in the research snapshot and label them as estimates.
- Operations questions should go beyond marketing and cover staffing, supply, delivery economics and quality controls.
- Regulatory questions should distinguish official tax facts from the need to confirm local approvals.

## Known uncertainty / failure modes

1. **Rent and footfall:** qualitative area scores cannot replace live property data.
2. **Delivery commissions:** contracts vary by platform, account and promotion; the calculator requires explicit assumptions.
3. **Competitor prices:** menus and promotions change frequently.
4. **Licensing:** activity, premises and approvals are case-specific.
5. **LLM routing:** a coordinator can occasionally under-delegate a broad question; production should add routing tests and tool-call telemetry.
6. **Model variance:** two runs can produce different recommendations even with the same evidence.

## Quality improvements

- Add a property-data connector and require actual rent/area/parking/frontage inputs before final location scoring.
- Add live menu snapshots with source dates and automated price-drift checks.
- Add a structured scoring schema with deterministic weights before LLM synthesis.
- Add factuality checks for numbers, URLs and regulatory statements.
- Add human approval for legal, lease and investment decisions.
- Add a golden evaluation set with expected key facts and regression testing in CI.

## Cost improvements

- Cache static research.
- Use a smaller model for classification/routing and a stronger model only for final synthesis.
- Limit specialist delegation to the domains relevant to the question.
- Enforce maximum tool calls and token budgets.
- Persist only useful conversation state.

## October 8 review: observed actual behavior vs intended behavior

Observed from submitted CLI logs:
- Tests passed 5/5 before this revision. Those tests were narrow keyword checks.
- Gemini 3.8 repeatedly returned 503, then another run hit 429 `RESOURCE_EXHAUSTED`.
- Agno correctly tried the configured fallback; a response eventually appeared.
- One reported location recommendation differed from an earlier run and discussed Mansaf/Zarb not in the client's defined menu.
- The response included highly specific unsourced numerical claims. Treat these as unverified, not reliable market research.

**Do not call the ten questions 'passed' yet.** Run and grade each one against a live version, recording:

| Criterion | Evidence required |
|---|---|
| Concept fidelity | Meaty pizza and kebab sandwiches, no invented flagship concept |
| Location reasoning | City, weights/assumptions, competing scenarios, site-level validation |
| Citation quality | Source URLs that actually substantiate every significant time-sensitive claim |
| Numerical integrity | Labeled assumptions, correct computation, no invented rent, footfall or margins |
| Actionability | Tradeoffs, practical next steps, measurable validation plan |
| Reliability | Graceful 429/503 handling; accurate mention of what search/tools were used |

In this revision, offline unit tests have expanded; they are **not** a substitute for the live 10-question evaluation.
