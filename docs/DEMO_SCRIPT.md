# 1–3 Minute Demonstration Script (Quota-Safe)

**Target runtime:** about **2 minutes 20 seconds**.  
**Goal:** Show genuine useful behavior without relying on Gemini being available during filming. Record the user's actual Phase 6 desktop; do not imply recorded tests are happening live.

## Before recording

- Start Streamlit: `.\.venv\Scripts\python.exe -m streamlit run app/ui.py`.
- Open `http://localhost:8501`; use a maximized browser and hide API keys/terminal secrets.
- Set sidebar mode to **Focused Advisor** and `ENABLE_LIVE_RESEARCH=false` (usual configuration).
- Prepare a suitable Dubai location view and one Unit Economics example. Do **not** click a live AI example if the provider quota is unavailable.
- Have `evals/MULTI_AGENT_VALIDATION.md` ready to show the recorded team output if needed.

## Narration and screen sequence

**0:00–0:17 — Introduction (AI Advisor tab)**

> "This is the Intelligent Market Expansion Advisor, a Python and Agno application for a Jordanian meaty-pizza and kebab-sandwich brand considering one first branch in Dubai or Abu Dhabi. It combines AI business reasoning with deterministic tools and traceable evidence notes."

**0:17–0:45 — Location Explorer (no API calls)**

> "Here, managers compare UAE neighborhoods across scenarios. The weighted screening is transparent, and equal scores remain tied. These rankings are planning hypotheses—not measured rent, footfall, or profitability."

Show Dubai/JLT and Deira under **Balanced**. Switch to Abu Dhabi briefly to show Al Zahiyah. Avoid presenting a cross-city numerical score comparison as investment proof.

**0:45–1:17 — Unit Economics (no API calls)**

> "This calculator takes explicitly supplied order volume, ticket size, costs, and delivery commissions. Python computes revenue and an illustrative contribution sensitivity. It does not claim to calculate audited profit, tax, or break-even."

Show the visible scenario sensitivity table and adjust daily orders once. Keep existing numbers if quicker; do not narrate numbers you have not checked on screen.

**1:17–1:44 — Evidence & Methodology (no API calls)**

> "Our reviewed source registry stores official-page links, narrowly supported claims, dates, and limitations. Tourist descriptions don't prove restaurant demand, so the system separates source notes from assumptions and field-validation tasks."

Expand a JLT or Federal Tax Authority reference to show its supported claim and limitation.

**1:44–2:07 — Agno multi-agent proof (recorded result, not a new live request)**

> "The application also contains a five-specialist Agno team. In our recorded live diagnostic, the coordinator delegated to the Location and Menu/Pricing agents, and both ran Python tools. The test completed, although Gemini quota errors were also observed."

Show `evals/MULTI_AGENT_VALIDATION.md` and the sanitized excerpt. **Do not** describe all five specialists as executed in that run.

**2:07–2:20 — Close**

> "The project includes 72 passing offline tests, ten manually reviewed business scenarios, an API cooldown guard, and documented limitations. The next commercial step would be independent validation of actual sites, customers, contracts and approvals."

## Optional live AI segment

Only if quota is confirmed available, replace the recorded-run portion with **one short Focused Advisor question** asking for a conditional UAE first-location recommendation using the internal snapshot. A fresh live response is not essential to this video because real multi-agent delegation has already been documented.

## Final checks

- Runtime between 1 and 3 minutes.
- Screen shows actual project behavior, not fabricated output.
- No `.env`, API tokens, email, confidential data, or fake GitHub links on screen.
- Narration accurately distinguishes offline tests, captured live team execution, and unverified commercial assumptions.
