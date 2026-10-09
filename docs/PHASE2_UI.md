# Phase 2 — Quota-aware executive dashboard

## What changed

- `app/ui.py` provides a professional Streamlit interface with an Agno chat advisor, scenario-driven location screening, deterministic unit economics, and evidence/research disclaimers.
- `app/advisory_service.py` provides an evidence-prepared **Focused** mode. It uses one Agno Agent without external tool calls; one model request is typical, although a fallback may add a second. It retains the original coordinating multi-agent Team as an explicitly selected **Full team** mode.
- `.env.example` now defaults to the two models confirmed accessible by the user: `gemini-3.6-flash` (primary) and `gemini-3.5-flash-lite` (fallback). These models may still return 503 or 429 for larger requests.
- Tests verify location selection, evidence packaging, validation, and scenario isolation. They do not verify the live API.

## Windows PowerShell setup

From the extracted project directory, with your `.env` copied from your previous version:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run app/ui.py
```

If this is a freshly extracted directory without a virtual environment, create one with `py -3.12 -m venv .venv` first.

Open the local address printed in the terminal (normally http://localhost:8501).

## Model-call budget

The user's logs show a `GenerateRequestsPerMinutePerProjectPerModel-FreeTier` quota of **5 requests/minute for gemini-3.6-flash**. The full coordinating team may exceed this budget even for one query. Prefer Focused mode for interactive demos and leave live research OFF unless the account's search billing/quota is confirmed. Do not repeatedly retry immediately when the provider specifies a longer `retryDelay`.

## Honest demonstration guidance

- Show the Location and Unit Economics tabs first. Both are genuinely interactive and work offline without fabricated model outputs.
- Then run one Focused Agent request if quota is available.
- Optionally demonstrate a pre-recorded full-team answer as an **explicitly labeled recording**, not as a live interaction.
- Show source limitations. Do not label a number verified just because the model writes “verified.”

## Cautions

- The screenshot-worthy interface does not replace a reproducible 10-question LLM evaluation.
- Focused mode is lower quota, not equivalent to multi-agent coordination. **The project still contains Agno Team coordination** in Full team mode and CLI; show its architecture and a recorded example in the demo.
- There is no claim of live web grounding when the research agent is disabled.
- Scenario rankings are subjective and depend on the snapshot; they are NOT measured sales, rents, or customer demand.
