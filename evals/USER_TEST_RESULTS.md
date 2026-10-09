# User-run evaluation: ten real business scenarios (2026-10-08–09)

These are **manual functional evaluations of answers the user shared**, not independent field audits or source-verified truth assessments. No live search was enabled for these tests.

| # | Focus | Observed outcome | Main issue | Phase 3 response |
|---|---|---|---|---|
| 1 | Dubai location + tied score | Correctly considered JLT and Deira/Bur Dubai | Equal 4.0 scores received distinct ranks | Equal ranks in location screener; conditional-location instructions |
| 2 | Menu and pricing | Proposed products, prices, bundles, packaging | Unvalidated weights/prices, optional items described as confirmed | Optional-menu distinction reinforced; prices remain illustrative |
| 3 | Competitor positioning | Relevant adjacent competitor categories | Claimed unverified competitive whitespace, not systematic by city | Whitespace hypothesis rule; field audit still needed |
| 4 | 90-day marketing launch | Phases/channels/budget percentages/KPIs | KPI goals and openings too certain; contracts/consent | Conditional milestones, KPI caveat and consent guards |
| 5 | Operational licensing and risk | Covered staffing, halal supply, kitchens and seasonality | Confusion between VAT and corporate-tax thresholds; missing KPI thresholds | Treat snapshot regulations as unverified; official checking remains required |
| 6 | JLT Dubai vs Al Reem Abu Dhabi | Detailed cross-city comparison and five validations | Equal scores, unproven commercial preference | Cross-city scores labeled planning only; conditional choice |
| 7 | Financial sensitivity (70/100/130) | Gross revenue and costs largely correct; **contribution and margin wrong** | Reported AED 64,680 and 44% at 100/day, rather than AED 52,185 and 35.5% | Fully specified scenarios bypass LLM: deterministic Python only, regression tests added |
| 8 | Delivery channels | Hybrid aggregator/direct/pickup recommendation | Assumed simultaneous branches, redirecting app customers, unsupported KPI goals | One-branch, contracts and data consent guardrails |
| 9 | Supply disruption | Supplier backup/staff training/risk matrix | Rejected closure even if no safe compliant supplier | Food-safety-first suspension rule |
| 10 | Integrated executive plan | Combined locations, concept, 90-day plan and risks | Omitted price architecture and detailed delivery strategy; unproven success thresholds | Answer-all-subtopics instruction; KPI assumptions. Must re-test. |

## Critical deterministic regression: Question 7

Inputs: 30 trading days/month, AED 49 average order, food cost 20%, labour/rent/other 37%, delivery share 30%, commission 25%.

| Daily orders | Monthly sales AED | Contribution AED | Margin |
|---:|---:|---:|---:|
| 70 | 102,900 | 36,529.50 | 35.5% |
| 100 | 147,000 | 52,185.00 | 35.5% |
| 130 | 191,100 | 67,840.50 | 35.5% |

The new `finance_guard.py` routes **explicitly labelled, complete** financial scenarios to the tested calculator. If data is missing, it does not invent values and lets advisory dialogue/interactive calculators handle the issue instead. This is an important improvement, **not** proof that any arbitrary generated financial report is now guaranteed correct.

## Historical next steps documented at Phase 3 (2026-10-08)

These were recorded before later Phase 4–6 retests and documentation updates. For the latest verified outcomes, see [`FINAL_EVALUATION_REPORT.md`](FINAL_EVALUATION_REPORT.md).

1. Re-run selected user tests on Phase 3, particularly #7 (financial) and #10 (integrated brief).
2. Verify Agno tool invocation, output coverage and any web-grounding citations in the live app.
3. Check regulator statements against current government sites; don't convert snapshot URLs into "verified" assertions.
4. Validate premises, customer demand, competitor menus, supplier quotes, and aggregator agreements with real-world evidence.
5. Film a 1–3 minute demonstration and finalize README, AI-tool disclosure, Github repository and evaluation evidence.


## Phase 3 integrated retest / Phase 4 improvements

A user-provided integrated executive response (2026-10-09) covered one branch, market selection, concept, menu/pricing, competition, channels, operational risks and conditional 90-day milestones. It provisionally favored Al Zahiyah by higher internal screening score. It also supplied a 100-orders/day, AED 45 AOV scenario with AED 135,000 monthly revenue and AED 24,300 illustrative residual from **model-chosen inputs**. Although arithmetic is internally consistent, source and tool execution were not proven. Phase 4 prevents this example from appearing as an unchecked projection in Focused mode and documents the need for independently validated location choices.
