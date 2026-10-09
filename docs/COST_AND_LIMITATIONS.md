# API Cost Control, Reliability, and Limitations

## Observed provider constraint

In the user-supplied October 2026 terminal logs, Google's Gemini API responded with `429 RESOURCE_EXHAUSTED`. One logged message specified an observed free-tier **20 requests/day/project/model** allowance for `gemini-3.6-flash`. This is an observation for that Google project, not a universal or permanent Google pricing promise. A multi-agent question can require multiple requests and exhaust allowance faster than a single focused question.

## What the implementation does

- **Default Focused Advisor:** normally fewer LLM calls than full Team mode.
- **Optional Full Team:** team coordinator plus specialist calls; should only be used when relevant and quota permits.
- **Fallback Gemini model:** configured for availability but **not** guaranteed to have a separate, unexhausted quota.
- **No model-level retry loop:** configured with `retries=0`; the current Agno run may still attempt fallback internally.
- **Persistent cooldown:** after an explicit detected 429, `app/quota_guard.py` stores a local cooldown in ignored `.runtime/gemini_quota.json` and blocks *new* live requests until it expires.
- **No-API features:** Location Explorer, Unit Economics, Evidence & Methodology, and complete-input standalone financial chat calculations.
- **No live-research cost by default:** `ENABLE_LIVE_RESEARCH=false`.

### Safe commands

```powershell
.\.venv\Scripts\python.exe -m app.quota_guard status
.\.venv\Scripts\python.exe -m app.quota_guard pause 60
.\.venv\Scripts\python.exe -m app.quota_guard clear
```

`clear` removes only the **local** cooldown. It does not reset the provider allowance. Check the actual quota at https://ai.dev/rate-limit before spending requests. If the service returns a 429, avoid repeated manual retries.

## What the project does not promise

1. **Financials:** percentages of monthly revenue approximate labor/rent/other rather than modelling fixed operating expenses; VAT treatment, capex, financing and working capital are outside the simple illustration. No investment-grade cash-flow or break-even assertion.
2. **Locations:** snapshot scenario scores are subjective heuristics, not measured footfall, real estate pricing, verified delivery demand, or cross-city profitability measures.
3. **Competitors:** benchmark categories are not a live location-specific audit or verified current menu-price database.
4. **Licensing/tax:** official notes provide narrow, previously reviewed information; changing rules and site-specific approvals must be checked with relevant authorities and qualified advisers.
5. **AI output:** prompt restrictions and output checks lower known risks but are not a general hallucination detector. Member delegation varies by question.
6. **Live source freshness:** the standard source registry is offline and dated, with no automatic current-web validation for each answer.
7. **API availability:** provider throttling and internal Agno fallback may still prevent a live response even when all offline tests pass.

## Production improvements

Before operational or commercial deployment, add site-specific fixed-cost inputs, source-refresh checks, deterministic policy and evidence validation, on-disk response caching, maximum-request budgets, targeted live integration tests, and human approval for investments.
