# Phase 4 — Quality Gates (2026-10-09)

## Input: Integrated executive recommendation test

- Correctly constrained launch to **one** initial branch and preserved meaty pizza + kebab sandwich identity.
- Included Abu Dhabi, Dubai, menu price bands, competitor positioning, marketing, delivery, supply, financial context, conditional 90-day milestones and pre-investment actions.
- Presented **Al Zahiyah as baseline** largely from a 4.25 qualitative score versus JLT at 4.0; these are *not calibrated cross-market ROI forecasts*.
- Labeled the market snapshot as dated, but no claims were verified using live sources in the test.
- Produced a mathematically consistent but **unrequested illustrative** financial scenario with assumed 100 orders/day, AED 45 AOV, etc., and claimed Python tool provenance not demonstrated in the response trace.

## Corrective changes

1. Focused Agno Agent does not receive a callable financial tool. Explicit full-input arithmetic is performed locally, before inference.
2. Complete multi-topic requests receive a deterministic financial scenario as context rather than being converted to an isolated finance table.
3. Generated monthly-financial-statement sections are suppressed when the question does not supply all inputs. Other parts of the executive response are preserved when possible.
4. All Focused / no-live-research responses append source-status disclosure.
5. Team-agent instructions prohibit selecting operating input figures without management supplying them and warn against treating 4.25 vs 4.0 as verified return superiority.
6. Extra offline regression tests prove this routing and section filtering without any model-key requirement.

## Constraints and known limitations

- Section filtering is narrow; it cannot eliminate every incorrect quantitative claim. Human review and authoritative independent sources are still essential.
- Full multi-agent runs can use more quota and may still perform independent tool calls; these must be verified by live run traces.
- Source URLs in the snapshot are verification **leads**, not citations validating live claims.
- Live Gemini behavior, Google grounding support, extraction accuracy, Streamlit visual layouts and integration were not verified in this sandbox.

## Suggested verification on Windows

1. Run `python -m pytest -q` and confirm all tests pass.
2. Launch Streamlit; ask the original integrated question. Confirm the answer does not include a fabricated monthly revenue/contribution scenario when no financial inputs are supplied.
3. Ask the explicit Test 7 full-input question; confirm the Python result and no API call.
4. For full-team demonstrations, monitor Agno tool invocation and Google API quota. Keep research off unless actual grounded source links are needed and available.
