# System Architecture and Design Decisions

## Purpose

The **Intelligent Market Expansion Advisor — UAE** is decision-support software for a Jordanian restaurant whose core offerings are meaty pizza and kebab sandwiches. It explores a **single initial branch** in Dubai or Abu Dhabi. It is not an automated investment, property, tax or regulatory approval tool.

## Implementation overview

```text
                         Executive user
                              |
                     Streamlit UI / CLI
                              |
               app.advisory_service.run_advice
                              |
                   Input and quota checks
                              |
             +----------------+----------------+
             |                                 |
   Complete standalone                 Business advisory
   financial scenario                       question
             |                                 |
   Python financial guard         Prepared snapshot + reviewed
   (no Gemini call)               official source notes (offline)
             |                                 |
             |                       Focused Agent (default)
             |                                 or
             |                        Agno Team coordinator
             |                                 |
             |           +----------+----------+---------+----------+
             |           |          |          |         |          |
             |        Location   Competitor  Menu     Growth   Operations
             |         Agent      Agent      Agent    Agent       Agent
             |           |          |          |         |          |
             |           +----------+----------+---------+----------+
             |                     Local Python tools
             |                                 |
             +----------------+----------------+
                              |
                   Answer + evidence disclosure
                              |
                       Executive dashboard
```

Five Agno specialists are always configured, and a **sixth optional live-research agent** is configured only when `ENABLE_LIVE_RESEARCH=true`. The tested normal configuration is `false`. The team coordinator decides which specialists to call; this is **not** a guarantee it invokes all five on every question.

## Modules and responsibilities

| Module | Responsibility |
| --- | --- |
| `app/ui.py` | Streamlit chat, location explorer, financial scenarios, evidence catalog and local quota status |
| `app/cli.py` | Terminal-based advisor through the same guarded service |
| `app/advisory_service.py` | Question routing, prompt evidence assembly, Agno invocation, source appendix, financial-projection safeguards |
| `app/agents.py` | Agno coordinator and five domain specialists; optional live research specialist |
| `app/tools/decision_tools.py` | Deterministic **qualitative** location-screening scores and ties |
| `app/tools/market_tools.py` | Scenario data lookups and illustrative unit-economics arithmetic |
| `app/finance_guard.py` | Standalone complete-input financial question parser and Python results |
| `app/evidence_registry.py` | Source-note selection and attributed offline reference appendix |
| `app/quota_guard.py` | Locally persistent cooldown after detected Gemini `429` errors |
| `data/market_snapshot.json` | Dated, unverified area and pricing **planning** assumptions |
| `data/source_registry.json` | Reviewed official-page notes, URLs, narrow supported claims, and limitations |

## Design choices

**Two interaction modes.** The default Focused Agent uses fewer model requests. The Full Agno Team delegates specialist subtasks and synthesizes them. A previously recorded real run returned two member responses, from Location and Menu/Pricing, and corresponding Python tool calls; see `evals/MULTI_AGENT_VALIDATION.md`.

**Python-owned arithmetic.** Fully specified standalone financial inputs are computed deterministically with zero AI API calls. The dashboard's Unit Economics tab is also offline. It models combined labor/rent/other as percentages rather than site-specific fixed costs, so it is neither net profit nor a break-even calculation.

**Bounded evidence.** A reviewed reference note supports only the narrow claim in its registry record; an official neighborhood guide does **not** verify demand, rents, footfall, occupancy, or ROI. The separately appended references are not an automatic fact-check of model-generated text. Live research is disabled in the tested configuration.

**Cost controls.** Gemini has a configurable primary/fallback model, model-level retries set to zero, and a persistent local cooldown following detectable provider `429` errors. Agno can still internally attempt fallback within the original request; the guard cannot prevent that first cascade or query remaining provider quota.

## Validation boundaries

- **Confirmed on Windows (2026-10-10):** 72 offline tests pass; Streamlit starts on port 8501; local quota status command works.
- **Confirmed from an earlier live team run (2026-10-09):** five configured agents, two delegated responses, two Python tools called, final synthesized response; intermittent `429` provider errors occurred.
- **Not established:** all five specialists executing in one run; production uptime; current official approval details; independent proof of commercial profitability; current competitor menu prices; correctness of every LLM statement; successful on-demand live web research.

See `evals/FINAL_EVALUATION_REPORT.md` and `docs/COST_AND_LIMITATIONS.md` for verification evidence and caveats.
