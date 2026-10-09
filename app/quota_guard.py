"""Small, local circuit breaker for explicit Gemini API quota failures.

Does not query Google for remaining quota, nor bypass provider limits. An observed
429 with a provider retry delay prevents *new* live calls until that deadline.
This is deliberately project-wide: a free-tier project can exhaust more than
one model, and blindly cascading into a second model can compound the issue.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import time
from typing import Any

from app.config import ROOT

DEFAULT_STATE_PATH = ROOT / ".runtime" / "gemini_quota.json"


class QuotaCooldown(RuntimeError):
    """User-visible message when live Gemini requests have been paused."""


def _retry_delay_seconds(message: str) -> int | None:
    # SDK exceptions may display JSON, Python dicts, or plain text.
    match = re.search(r"['\"]?retryDelay['\"]?\s*[:=]\s*['\"]?(\d+(?:\.\d+)?)s", message)
    if match:
        return max(1, int(float(match.group(1)) + .999))
    match = re.search(r"Please retry in\s+(?:(\d+)h)?(?:(\d+)m)?(?:(\d+(?:\.\d+)?)s)?", message, re.I)
    if match and any(group is not None for group in match.groups()):
        h, m, s = match.groups()
        return max(1, int((int(h or 0) * 3600 + int(m or 0) * 60 + float(s or 0)) + .999))
    return None


def classify_quota_error(error: object) -> dict[str, Any] | None:
    """Only act on genuine-looking provider 429 errors, not ordinary prose."""
    message = str(error)
    if "RESOURCE_EXHAUSTED" not in message and not re.search(r"\b429\b", message):
        return None
    if not any(term in message for term in (
        "Quota exceeded", "quotaMetric", "free_tier_requests", "rate limit",
        "RESOURCE_EXHAUSTED", "current quota",
    )):
        return None
    kind = "daily" if "PerDay" in message else "per-minute" if "PerMinute" in message else "unspecified"
    seconds = _retry_delay_seconds(message)
    # Without a provider delay, use a short, conservative cooldown, not a
    # fabricated calendar reset time. It is just a local anti-retry safeguard.
    seconds = seconds or (3600 if kind == "daily" else 60)
    match = re.search(r"\bmodel:\s*(gemini-[\w.-]+)", message, re.I)
    return {"kind": kind, "delay_seconds": seconds, "model": match.group(1) if match else None}


def _read_state(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(value, dict) and isinstance(value.get("blocked_until"), (float, int)):
            return value
    except (FileNotFoundError, ValueError, OSError):
        pass
    return None


def quota_status(*, path: Path = DEFAULT_STATE_PATH, now: float | None = None) -> dict[str, Any] | None:
    current = time.time() if now is None else now
    status = _read_state(path)
    if status is None or status["blocked_until"] <= current:
        return None
    return {**status, "remaining_seconds": max(1, int(status["blocked_until"] - current + 0.999))}


def cooldown_message(status: dict[str, Any]) -> str:
    seconds = status["remaining_seconds"]
    minutes = (seconds + 59) // 60
    return (
        f"Live Gemini requests are paused locally after an API quota error "
        f"({status.get('kind', 'unknown')} limit; roughly {minutes} minute(s) remaining). "
        "This is based on a prior provider error, not a live quota check. "
        "Continue with Location Explorer, Unit Economics, and Evidence without an API call. "
        "Check https://ai.dev/rate-limit before trying again."
    )


def ensure_api_allowed(*, path: Path = DEFAULT_STATE_PATH, now: float | None = None) -> None:
    status = quota_status(path=path, now=now)
    if status:
        raise QuotaCooldown(cooldown_message(status))


def record_quota_failure(error: object, *, path: Path = DEFAULT_STATE_PATH, now: float | None = None) -> dict[str, Any] | None:
    issue = classify_quota_error(error)
    if issue is None:
        return None
    current = time.time() if now is None else now
    until = current + issue["delay_seconds"]
    previous = _read_state(path)
    if previous is not None:
        until = max(until, float(previous["blocked_until"]))
    state = {"blocked_until": until, "kind": issue["kind"], "model": issue["model"]}
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    try:
        temp.write_text(json.dumps(state, indent=2), encoding="utf-8")
        os.replace(temp, path)
    finally:
        try:
            temp.unlink(missing_ok=True)
        except OSError:
            pass
    return quota_status(path=path, now=current)


def clear_cooldown(*, path: Path = DEFAULT_STATE_PATH) -> None:
    """Manually clear local gate after verifying quota; does not reset Google quota."""
    path.unlink(missing_ok=True)


def pause_api_calls(minutes: int, *, path: Path = DEFAULT_STATE_PATH, now: float | None = None) -> dict[str, Any]:
    """Manually pause calls if Agno swallows a provider 429 and succeeds via fallback."""
    if not 1 <= minutes <= 1440:
        raise ValueError("minutes must be between 1 and 1440")
    current = time.time() if now is None else now
    until = current + minutes * 60
    previous = _read_state(path)
    if previous:
        until = max(until, previous["blocked_until"])
    state = {"blocked_until": until, "kind": "manual", "model": None}
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    try:
        temp.write_text(json.dumps(state, indent=2), encoding="utf-8")
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)
    return quota_status(path=path, now=current)


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Inspect local Gemini quota cooldown (no API requests).")
    parser.add_argument("command", choices=["status", "clear", "pause"], nargs="?", default="status")
    parser.add_argument("minutes", nargs="?", type=int, help="Minutes to pause if command is 'pause'")
    args = parser.parse_args()
    if args.command == "pause":
        if args.minutes is None:
            parser.error("pause requires the number of minutes")
        print(cooldown_message(pause_api_calls(args.minutes)))
        return
    if args.command == "clear":
        clear_cooldown()
        print("Local cooldown cleared. This does NOT reset Gemini API quota.")
        return
    status = quota_status()
    print(cooldown_message(status) if status else "No locally recorded active Gemini quota cooldown. This does NOT prove API quota is available.")


if __name__ == "__main__":
    main()
