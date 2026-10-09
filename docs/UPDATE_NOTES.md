# Phase 1 Audit and Improvement Notes (2026-10-08)

> **Historical Phase 1 change notes.** This document describes an early version and its former gaps. For the current Phase 6 submission candidate, use [`ARCHITECTURE.md`](ARCHITECTURE.md), [`COST_AND_LIMITATIONS.md`](COST_AND_LIMITATIONS.md), and [`../evals/FINAL_EVALUATION_REPORT.md`](../evals/FINAL_EVALUATION_REPORT.md).


## Starting point reviewed

User's October 8 ZIP: 6 Agno agents including a live market research agent, Gemini 3.8 primary/3.7 fallback, CLI, JSON market snapshot, documentation, and 5 original tests. We examined the exact ZIP and did not assume the original packaged files matched the user's live environment configuration.

## Verified improvements in this package

1. Requirements use Agno 2.9.0 and Google Gemini (`google-genai`), not the superseded OpenAI setup.
2. `.env.example` documents `GOOGLE_API_KEY`, model IDs and the live-research switch. `.env` is excluded from the archive and ignored by git.
3. Research agent is optional (`ENABLE_LIVE_RESEARCH`), to avoid adding quota-consuming calls by default. Enabling it requires setting the switch to true and restarting CLI.
4. Added deterministic exploratory screening scenarios for Dubai and Abu Dhabi. Scores reflect explicit mappings of subjective qualitative data, **not** measured demand, rents or sales. Check `app/tools/decision_tools.py`.
5. Core location agent is instructed to use the screening tool rather than invent rankings without a stated reasoning baseline.
6. The restaurant concept is consistently identified as *meaty pizza and kebab sandwiches*; unrelated Mansaf/Zarb assumptions are explicitly prohibited in agent instructions.
7. Calculator rejects invalid numeric inputs, documents its simplifications and discloses that it is **not** a real P&L or break-even forecast.
8. CLI recognizes quota and availability API failures and gives helpful diagnostic guidance.
9. Expanded offline regression tests cover financial validation, snapshot assumptions, deterministic area-screening and error handling.
10. Documentation distinguishes observed logs from live validation. The package has **not** been tested with the user's Gemini API key.

## Still necessary for high-quality submission

- **Live runtime validation:** Test Agno 2.9.0 Team, selected model availability, and search grounding on the user's machine.
- **Grounding evaluation:** Check whether actual source URLs returned by research are traceable and support each claim. An LLM-generated URL is not proof of verification.
- **Business model:** Collect measured rents and quotes; build explicit fixed/variable cost treatment and break-even sensitivity. Current unit economics are illustrative only.
- **Evaluation:** Run all 10 questions against the live system, capture successes/failures, and add manual evidence-grounding rubric and per-question results.
- **Professional Streamlit UI:** Add only once this corrected core runs reliably on the user's machine. Target interactive chat, source review, scenario screening, unit economics and an offline demo view.
- **Submission:** Record 1–3 minute demo and include actual evaluation results, the GitHub link, and honest AI tool disclosure.

## Known caveat

Agno native Gemini Google Search (`search=True`) may displace external Python tools in the user's installed integration. Therefore this design isolates search in a research-only Agent. Default switch is off due to previously observed 429 quotas. A fallback model in the same Google project does not guarantee independent quota.
