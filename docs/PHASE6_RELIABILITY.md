# Phase 6: Quota resilience and submission hardening

## Changes

- `app/quota_guard.py` is a local, persistent circuit breaker. It records an explicit Gemini 429, including the provider-supplied `retryDelay` when present, and stops the **next** live inference call until the cooldown expires. It does not reset quotas, estimate remaining allowance, or prevent every internal Agno retry within the initial failed team run.
- Model-level `retries=0` avoids extra retry requests after a failed model call. Agno's primary-to-fallback transition remains configured; a fallback may be subject to project-wide quotas and is **not guaranteed to work**.
- The Streamlit sidebar indicates active local cooldown. Offline Location Explorer, Unit Economics and Evidence remain usable.
- `verify_team.py` reproduces a targeted real delegation test, but runs only after the cooldown check. `evals/MULTI_AGENT_VALIDATION.md` documents the earlier observed two-member delegation.

## Commands (offline; from project root)

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m app.quota_guard status
```

When a full-team run **succeeds but its internal logs still contain 429 errors**, Agno may have swallowed that exception during fallback. In that case, the local guard may not have recorded it. You can **manually pause** all new AI requests, for example for 60 minutes:

```powershell
.\.venv\Scripts\python.exe -m app.quota_guard pause 60
```

After confirming through Google AI Studio that the quota has actually reset, you may remove the local cooldown:

```powershell
.\.venv\Scripts\python.exe -m app.quota_guard clear
```

**Clearing does not increase Google quota.** The persisted data contains only a cooldown deadline, reason and model ID, not API secrets or prompts. It is excluded from Git.

## Limits

- A circuit breaker only operates at the application entry point. If a model makes repeated internal calls during the **first** failing team request, some may still fail before a guard records a problem.
- The guard records explicit 429s that propagate as exceptions or provider-error output. It does not parse arbitrary console logs automatically.
- This layer is intentionally conservative: an observed project-level limit pauses both models locally even if a different model might have some separate remaining quota.
- Never treat offline CI as evidence that live Gemini calls, all specialists, or web grounding succeed.

## Final submission prep

1. Run `pytest` and capture output.
2. Capture screenshots of chat, location, financial scenarios, official-source registry.
3. Use the already-observed multi-agent delegation transcript as evidence, not repeated paid calls.
4. Review the user-facing content for unsupported numeric claims and evaluate on a site/contract-by-contract basis.
5. Update GitHub repository and demo with an explicit statement that the current location scores are qualitative, not market forecasts.
