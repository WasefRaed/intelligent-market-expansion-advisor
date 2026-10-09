# Intelligent Market Expansion Advisor — UAE

Agentic AI advisory system for a Jordanian restaurant specializing in **meaty pizza and kebab sandwiches** and evaluating expansion into **Dubai and Abu Dhabi**.

## Submission snapshot (2026-10-10)

**Latest Windows verification:** `72 passed in 0.43s`; the local quota-status command ran and Streamlit started at `http://localhost:8501`. The 2026-10-09 live Agno diagnostic recorded **two delegated specialists** (Location and Menu/Pricing) from five configured agents, plus Gemini 429 errors. These are engineering observations, **not** independent verification of UAE market claims or flawless API availability.

**Start here for assessment:**

- [Architecture and design choices](docs/ARCHITECTURE.md)
- [Final evaluation report and ten manually reviewed scenarios](evals/FINAL_EVALUATION_REPORT.md)
- [Recorded multi-agent delegation](evals/MULTI_AGENT_VALIDATION.md)
- [Official sources and provenance](docs/SOURCES.md)
- [Cost, quota reliability and limitations](docs/COST_AND_LIMITATIONS.md)
- [AI tool usage disclosure](docs/AI_TOOL_DISCLOSURE.md)
- [1–3-minute demonstration script](docs/DEMO_SCRIPT.md)
- [GitHub publishing walkthrough](docs/GITHUB_PUBLISHING.md)
- [Final submission checklist](docs/SUBMISSION_CHECKLIST.md)

> **Caution:** This project is a decision-support prototype. All location scores and menu price bands are unverified planning estimates. Reviewed official source notes support only narrow claims, not sales or investment results. `ENABLE_LIVE_RESEARCH=false` in the tested configuration.

## What it does

The advisor is a **Streamlit dashboard and CLI chatbot** built with **Python + Agno + Google Gemini**. Focused mode uses one Agno agent to conserve API calls; Full Team mode delegates to five domain specialists, plus an optional live-research specialist.

### Advisory coverage

1. Branch location strategy
2. Competitor intelligence and positioning
3. UAE menu localization
4. AED pricing architecture
5. Launch and growth marketing
6. Operations and staffing
7. Delivery-platform strategy
8. Licensing / food-safety / tax validation checklist
9. Supplier and quality strategy
10. Ramadan, summer and Eid seasonality
11. Illustrative unit economics

## Architecture

```text
Executive
   |
   v
Streamlit UI / CLI
   |
   +--> Focused Agno Agent (quota-aware)
   |
   v
Agno Coordinator Team
   |-------------------------------|
   |        |         |       |    |
v Location v Comp.  v Menu  v Growth v Ops/Risk
   |        |         |       |      |
   +--------+---------+-------+------+
                    |
                    v
             Executive Synthesis
                    |
                    v
          Structured recommendation
```

Five domain agents use small deterministic Python tools backed by `data/market_snapshot.json`. A sixth, optional agent provides live Google Search grounding. The snapshot provides a controlled reference, but **does not guarantee** that model answers are factual. The model is responsible for reasoning, prioritization and synthesis; Python owns the research snapshot and calculations.

Agno's Team abstraction is the main agentic framework. Agno supports agents, teams and workflows for orchestrating model-driven work. See the official docs in the references below.

## Why this design

- **Agent specialization:** location, competition, menu/pricing, growth and operations require different reasoning lenses.
- **Evidence grounding:** recommendations are generated from a versioned research snapshot rather than unrestricted model memory.
- **Cost control:** no unnecessary live web-search tool is invoked on every message; a small local evidence set is reused.
- **Auditability:** research snapshot sources and hypotheses are documented; live factual claims must have traceable evidence and still require verification.
- **Executive UX:** answers are intentionally structured around recommendation, evidence, tradeoffs, actions and metrics.
- **Extensibility:** the research tools can later be replaced by live APIs, vector retrieval, Google Maps data, delivery menus, or a property-data provider.

## Quick start — Windows PowerShell

### 1. Create a virtual environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Configure the API key

```powershell
Copy-Item .env.example .env
notepad .env
```

Set:

```text
GOOGLE_API_KEY=your_gemini_key_here
GEMINI_MODEL=gemini-3.6-flash
GEMINI_FALLBACK_MODEL=gemini-3.5-flash-lite
ENABLE_LIVE_RESEARCH=false
```

Use a model available to your Google AI Studio project. Keep `ENABLE_LIVE_RESEARCH=false` for lower API use while validating basic operation; switch it to `true` when you need current web research and have quota. Restart the CLI after editing `.env`. Never commit the `.env` file.

### 3. Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

### 4. Launch the executive dashboard

```powershell
.\.venv\Scripts\python.exe -m streamlit run app/ui.py
```

Open http://localhost:8501. Location Explorer and Unit Economics are offline; Focused and Full Team modes use Gemini.

### 5. Optional CLI

```powershell
.\.venv\Scripts\python.exe -m app.cli
```

## Demo flow

The prepared **quota-safe 1–3 minute walkthrough** demonstrates the offline Location Explorer, Unit Economics sensitivity, Evidence & Methodology catalog, and the **recorded** two-specialist Agno delegation test. It does not require live Gemini traffic while filming; optional AI chat may be shown if quota is available. See [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md).

## Research and data policy

`data/market_snapshot.json` is a dated research snapshot, **not a continuously verified database**. It is designed to distinguish:

- **Previously source-backed descriptions:** official tourism context, company pages, and tax guidance as documented when compiled. All may require rechecking; presence and prices can change.
- **Strategic estimates:** proposed price bands, ranking weights and launch tactics.

The project must not be used to sign a lease or make a final investment decision without fresh validation. A source URL attached to an LLM claim must be opened and checked before marking the claim verified.

## Cost / API usage control

1. One coordinator team instead of multiple independent end-to-end calls.
2. Reusable local research snapshot; on-demand live Google Search through a separate research agent.
3. Short specialist instructions and executive-focused output.
4. No embeddings/vector database required for the initial evidence set; use cautious local qualitative site screening.
5. Primary and fallback Gemini models configurable through `.env`. Optional search is disabled by default because it can consume limited API quota.
6. **Phase 3 guard:** fully specified *financial-only* questions (explicit order volume, ticket, food/operating costs and delivery assumptions) bypass Agno and are answered by tested Python arithmetic. Use the Unit Economics tab for controlled scenarios.
7. **Phase 4 provenance:** Mixed executive questions with complete financial inputs preserve the executive conversation and attach deterministic Python results to the Agno prompt. The Focused Agent no longer has a callable finance tool that could be invoked with invented assumptions. When input assumptions are missing, an offline output guard suppresses unrequested calculated monthly-financial-statement sections. This is a narrow safety net, **not a claim that all AI statements are verified**.

For production, add request budgets, token logging, caching, rate limits and a smaller model for simple questions.

## Scenario screening (offline, no API needed)

A new deterministic location-screening tool uses explicit planning weights, qualitative area-fit proxies and occupancy-pressure labels already in the snapshot. It produces **heuristic scores only**; these are **not measured demand, actual rent, investment returns, or statistically calibrated confidence scores**.

```powershell
.\.venv\Scripts\python.exe -c "from app.tools.decision_tools import get_area_screening; print(get_area_screening('Dubai', 'balanced'))"
```

Valid scenarios are `balanced`, `cost_control`, and `demand_first` for `Dubai` or `Abu Dhabi`. Compare the scenarios and explain the assumptions rather than asserting a universal location winner.

## Evaluation

See [`evals/EVALUATION.md`](evals/EVALUATION.md) for baseline executive questions and [`evals/USER_TEST_RESULTS.md`](evals/USER_TEST_RESULTS.md) for the ten manually reviewed real-world scenarios and the critical arithmetic finding. Offline tests: `python -m pytest -q`. **A passing offline suite does not prove live Agno routing, search grounding, or answer accuracy.**

## Limitations

- Location rankings use qualitative proxies, not proprietary footfall/rent datasets.
- Pricing is a planning band, not a live competitive price scrape.
- Competitor analysis is category-level and does not estimate market share.
- Licensing guidance is a checklist, not legal advice.
- The research snapshot can become stale; refresh it before investment decisions.
- Live delivery commissions, lease terms, labor costs and supplier quotes must be inserted before financial modeling.

## Production roadmap

1. Add live web/property/delivery research connectors with source timestamps.
2. Add a structured property scoring model using actual rent, frontage, parking, delivery radius and footfall data.
3. Add competitor menu scraping with terms-of-service compliant sources.
4. Add a financial model with capex, rent, labor, food cost, commissions, VAT and tax.
5. Continue to polish and validate the existing Streamlit dashboard, with chat, assumptions, source review, area screening and offline financial scenarios.
6. Add approval gates so high-impact claims require human review.
7. Add evaluation datasets and LLM-as-judge plus deterministic checks.

## AI Tool Usage Disclosure

AI assistance was used to accelerate development and review of this submission.

- **ChatGPT / OpenAI:** architecture brainstorming, code drafting/review, documentation structure and evaluation design.
- **Gemini:** intended inference provider; live results must be independently reviewed.
- **Web research:** current Agno documentation and public UAE tourism, restaurant and government sources were consulted for the research snapshot.

The implementation that should be understood by the submitter is the Python project structure, Agno agent/team orchestration, evidence-tool layer, deterministic unit-economics calculator, CLI, tests, evaluation methodology and documentation. Before submission, the developer should run the project, inspect every file, and be able to explain the delegation flow and all assumptions.

## Key sources

- Agno workflows and orchestration: https://docs.agno.com/workflows/overview
- Agno teams: https://docs.agno.com/teams/running-teams
- Dubai Municipality food establishments: https://www.dm.gov.ae/municipality-business/food-traders-establishments/
- UAE VAT: https://u.ae/en/information-and-services/finance-and-investment/taxation/vat/valueaddedtaxvat
- UAE Corporate Tax: https://u.ae/en/information-and-services/finance-and-investment/taxation/corporate-tax
- Visit Dubai neighbourhoods: https://www.visitdubai.com/en/explore-dubai/dubai-neighbourhoods
- Experience Abu Dhabi: https://visitabudhabi.ae/
- PizzaExpress UAE: https://www.pizzaexpress.ae/
- Zaatar w Zeit UAE: https://zaatarwzeit.com/UAE/home
- Zaroob: https://www.zaroob.com/
- Laffah: https://www.laffahrestaurants.com/

## Revision notes

See [`docs/UPDATE_NOTES.md`](docs/UPDATE_NOTES.md) for the exact changes made after inspection of the user's October 8 ZIP, and the remaining work required before submission.

## License

MIT for the project code. Research data remains subject to the terms of its original sources.

## Phase 2 — Executive dashboard (recommended for demonstrations)

Start the Streamlit UI:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app/ui.py
```

The **AI Advisor** offers a default **Focused** mode that prepares deterministic market evidence for a single Agno Agent; this usually needs fewer provider calls than the optional coordinating **Full multi-agent team** mode. The latter remains the project's core multi-agent architecture and may use multiple requests per question. Both modes can be affected by quota errors.

Other pages work entirely without an API key: a **Location Explorer** with transparent scenario scores for Dubai / Abu Dhabi, **Unit Economics** with editable assumptions, and **Evidence & Methodology** with research leads and caveats. Read [`docs/PHASE2_UI.md`](docs/PHASE2_UI.md) for details.

**Note:** If you are using a free-tier Google project limited to 5 requests/minute for `gemini-3.6-flash`, favor Focused mode and keep `ENABLE_LIVE_RESEARCH=false` until you can validate usage and cost. The interface does not manufacture live answers when Gemini is unavailable.


## Phase 3 integrity improvements

- Financial chat prompts with **all explicitly labelled assumptions** use a deterministic Python calculation pathway (zero API calls); this prevents the Test 7 arithmetic error. Other financial language still requires review. It is not a universal natural-language parser.
- Scenario screening ranks give equal ranks to equal scores (e.g. #1, #1, #3); initial snapshot order is not a tie-break justification.
- Unit Economics accepts 1–31 trading days, shows a deterministic low/base/high order-volume comparison, and retains its limitation disclosure.
- Location charts are horizontal to improve area-label readability.
- Agno focused/team prompts strengthen single-branch scope, menu boundaries, evidence labeling, supply safety, tax verification, and privacy/contract safeguards. Prompt controls are not equivalent to independent fact checking.

**Historical note (Phase 3):** at the time of that phase, only offline tests were complete. Subsequent Windows checks confirmed Streamlit startup and a separate actual two-member Agno delegation run, documented in the final evaluation report. Live Google Search grounding and broad commercial accuracy remain unverified.


## Phase 4 quality gates — integrated brief regression

The manual integrated test (2026-10-09) covered the single-branch constraint, markets, menu, pricing, operations and 90-day roadmap. Remaining risks: Al Zahiyah's 4.25 proxy score should **not** be interpreted as commercial superiority over JLT's 4.0; no live external claims were verified; the model generated a financial example (AED 135,000 sales / AED 24,300 residual) without management supplying its operating assumptions. Those example arithmetic values are internally consistent but are not justified as a forecast or as evidence of a confirmed calculator call.

Phase 4 adds a focused-agent no-invented-tool policy, suppresses projected finance sections without explicit inputs, keeps mixed question coverage, and includes regression checks against the exact supplied 146-line model answer. It does **not** establish live research truth, production legal compliance, guaranteed tool invocation in Full Team mode or validated UAE business economics.

## Phase 5 — Official reference notes (offline, low quota)

Phase 5 adds an auditable source registry, `data/source_registry.json`, reviewed **2026-10-09**, and selection helpers in `app/evidence_registry.py`. The **Evidence & Methodology** tab now separates:

1. **Reviewed official-page notes** — exact narrow statements that an authority or official destination guide supports, with URLs, limitations and review date.
2. **Unreviewed snapshot research leads** — links and heuristic planning inputs that **are not** verified claims.

A relevant advisor response appends source notes independently of the model. That appendix does **not** fact-check the rest of the AI-generated response. With `ENABLE_LIVE_RESEARCH=false`, there is no Google Search request. Government and tourism sources **do not validate site rents, footfall, market shares, local customer demand, or the final location ranking**.

Key implementation details and maintenance policy: `docs/PHASE5_RESEARCH_EVIDENCE.md` and `docs/SOURCES.md`.

**API usage:** Your observed free-tier Gemini 3.6 Flash usage cap was 20 requests/day on this project; quotas differ by account and model. On a 429 daily-exhausted error, do not repeatedly send AI prompts; use the offline Location, Unit Economics and Evidence tabs and wait for the reset shown in Google AI Studio. The previously reported Streamlit `use_container_width` warning was also addressed (now `width="stretch"`).

This phase preserves all prior safeguards (including Python-owned financial calculation and the 53 earlier tests) and adds new offline provenance regression tests. Live Streamlit and Agno behavior must be confirmed in your Windows environment.

## Phase 6 — API quota reliability (local circuit breaker)

A provider `429 RESOURCE_EXHAUSTED` with a retry delay now sets a local cooldown saved in `.runtime/gemini_quota.json` (ignored by Git). New **Focused** and **Full Team** requests are stopped during that cooldown rather than blindly repeated. This is a conservative local safeguard, **not** a live check of remaining Gemini quota. Offline Location Explorer, Unit Economics and Evidence continue working. Agno's internal fallback may still attempt calls in the original request before the failure reaches the guard.

Check the cooldown without using the API:

```powershell
.\.venv\Scripts\python.exe -m app.quota_guard status
```

If a team run was successful through fallback but logs contain a `429` that Agno handled internally, manually pause subsequent AI requests: `python -m app.quota_guard pause 60` (using your venv Python). After confirming the reset on Google AI Studio, `python -m app.quota_guard clear` only clears the local pause; it cannot reset provider quotas.

The **documented actual specialist delegation** from the user's Phase 5 run is preserved in `evals/MULTI_AGENT_VALIDATION.md`. Read `docs/PHASE6_RELIABILITY.md` for limits and test commands. The live validation script (`verify_team.py`) is optional and is not run by offline tests.
