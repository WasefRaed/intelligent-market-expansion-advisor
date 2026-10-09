# Intelligent Market Expansion Advisor — UAE

Agentic AI advisory system for a Jordanian restaurant specializing in **meaty pizza and kebab sandwiches** and evaluating expansion into **Dubai and Abu Dhabi**.

## Verification snapshot (2026-10-10)

**Latest Windows verification:** `72 passed in 0.43s`; the local quota-status command ran and Streamlit started at `http://localhost:8501`. The 2026-10-09 live Agno diagnostic recorded **two delegated specialists** (Location and Menu/Pricing) from five configured agents, plus Gemini 429 errors. These are engineering observations, **not** independent verification of UAE market claims or flawless API availability.

**Technical documentation:**

- [Architecture and design choices](docs/ARCHITECTURE.md)
- [Final evaluation report and ten manually reviewed scenarios](evals/FINAL_EVALUATION_REPORT.md)
- [Recorded multi-agent delegation](evals/MULTI_AGENT_VALIDATION.md)
- [Official sources and provenance](docs/SOURCES.md)
- [Cost, quota reliability and limitations](docs/COST_AND_LIMITATIONS.md)
- [AI tool usage disclosure](docs/AI_TOOL_DISCLOSURE.md)

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
6. **Financial arithmetic guard:** fully specified *financial-only* questions (explicit order volume, ticket, food/operating costs and delivery assumptions) bypass Agno and are answered by tested Python arithmetic. Use the Unit Economics tab for controlled scenarios.
7. **Financial provenance:** Mixed executive questions with complete financial inputs preserve the executive conversation and attach deterministic Python results to the Agno prompt. The Focused Agent no longer has a callable finance tool that could be invoked with invented assumptions. When input assumptions are missing, an offline output guard suppresses unrequested calculated monthly-financial-statement sections. This is a narrow safety net, **not a claim that all AI statements are verified**.

For production, add request budgets, token logging, caching, rate limits and a smaller model for simple questions.

## Scenario screening (offline, no API needed)

A new deterministic location-screening tool uses explicit planning weights, qualitative area-fit proxies and occupancy-pressure labels already in the snapshot. It produces **heuristic scores only**; these are **not measured demand, actual rent, investment returns, or statistically calibrated confidence scores**.

```powershell
.\.venv\Scripts\python.exe -c "from app.tools.decision_tools import get_area_screening; print(get_area_screening('Dubai', 'balanced'))"
```

Valid scenarios are `balanced`, `cost_control`, and `demand_first` for `Dubai` or `Abu Dhabi`. Compare the scenarios and explain the assumptions rather than asserting a universal location winner.

## Evaluation

See the [final evaluation report](evals/FINAL_EVALUATION_REPORT.md), [ten manually reviewed scenarios](evals/USER_TEST_RESULTS.md), and [recorded specialist delegation](evals/MULTI_AGENT_VALIDATION.md). The observed Windows regression suite passed **72 offline tests**. These tests do not establish market accuracy or guarantee Gemini service availability.

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
- **Gemini:** runtime language model for live advisor and specialist synthesis; its answers require independent review.
- **Web research:** current Agno documentation and public UAE tourism, restaurant and government sources were consulted for the research snapshot.

See [AI Tool Usage Disclosure](docs/AI_TOOL_DISCLOSURE.md) for the development roles of the assistant and runtime components, along with human verification responsibilities.

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

## API reliability

Gemini has model- and project-specific API quotas. The project uses configurable primary/fallback models, disables optional live research by default, and records a local cooldown after certain detected 429 quota errors. The guard reduces repeated requests but does not eliminate internal Agno attempts within a failed team run. Offline location scoring, finance, and source browsing remain usable without Gemini.

Check the local status using:

```powershell
.\.venv\Scripts\python.exe -m app.quota_guard status
```

See [Costs and limitations](docs/COST_AND_LIMITATIONS.md) for details.

## License

MIT for project code. Third-party references and data remain subject to their respective owners' terms. See [LICENSE](LICENSE).
