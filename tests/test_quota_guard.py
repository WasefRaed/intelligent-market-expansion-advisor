import json

import pytest

from app.quota_guard import (
    QuotaCooldown, classify_quota_error, clear_cooldown, cooldown_message,
    ensure_api_allowed, pause_api_calls, quota_status, record_quota_failure,
)


DAILY = """429 RESOURCE_EXHAUSTED Quota exceeded for metric:
limit: 20, model: gemini-3.6-flash
quotaId: GenerateRequestsPerDayPerProjectPerModel-FreeTier
retryDelay: '1281s'"""

PER_MINUTE = """429 RESOURCE_EXHAUSTED Quota exceeded for metric:
quotaId: GenerateRequestsPerMinutePerProjectPerModel-FreeTier
Please retry in 55.4s."""


def test_daily_provider_retry_info_persists_and_expires(tmp_path):
    path = tmp_path / "state.json"
    state = record_quota_failure(DAILY, path=path, now=1000)
    assert state["kind"] == "daily"
    assert state["model"] == "gemini-3.6-flash"
    assert state["remaining_seconds"] == 1281
    assert json.loads(path.read_text())["blocked_until"] == 2281
    with pytest.raises(QuotaCooldown):
        ensure_api_allowed(path=path, now=1050)
    ensure_api_allowed(path=path, now=2282)
    assert quota_status(path=path, now=2282) is None


def test_per_minute_retry_delay(tmp_path):
    path = tmp_path / "state.json"
    state = record_quota_failure(PER_MINUTE, path=path, now=100)
    assert state["kind"] == "per-minute"
    assert state["remaining_seconds"] == 56


def test_retry_delay_hours_minutes_and_seconds():
    issue = classify_quota_error("429 RESOURCE_EXHAUSTED current quota Please retry in 1h7m7.365s.")
    assert issue["delay_seconds"] == 4028


def test_business_prose_does_not_trigger_false_positives(tmp_path):
    path = tmp_path / "state.json"
    assert classify_quota_error("429 new customers ordered pizza last weekend") is None
    assert classify_quota_error("503 UNAVAILABLE") is None
    assert record_quota_failure("429 new customers", path=path, now=10) is None
    assert not path.exists()


def test_repeated_failure_does_not_shorten_existing_cooldown(tmp_path):
    path = tmp_path / "state.json"
    record_quota_failure(DAILY, path=path, now=500)
    state = record_quota_failure(PER_MINUTE, path=path, now=501)
    assert state["blocked_until"] == 1781


def test_manual_pause_and_clear(tmp_path):
    path = tmp_path / "state.json"
    status = pause_api_calls(40, path=path, now=100)
    assert status["kind"] == "manual"
    assert status["remaining_seconds"] == 2400
    assert "not a live quota check" in cooldown_message(status)
    clear_cooldown(path=path)
    assert quota_status(path=path, now=150) is None
    with pytest.raises(ValueError):
        pause_api_calls(0, path=path, now=150)


def test_corrupt_state_is_not_a_permanent_lockout(tmp_path):
    path = tmp_path / "state.json"
    path.write_text("corrupt json")
    assert quota_status(path=path) is None
    ensure_api_allowed(path=path)


def test_offline_financial_scenario_bypasses_gate(monkeypatch):
    from app import advisory_service
    monkeypatch.setattr(advisory_service, "ensure_api_allowed", lambda: (_ for _ in ()).throw(QuotaCooldown("blocked")))
    question = ("Calculate financial scenarios:\nDaily orders: 100\n"
                "Average order value: AED 49\nTrading days per month: 30\n"
                "Food cost: 20%\nOperating costs: 37%\nDelivery share: 30%\n"
                "Delivery commission: 25%\nCompare scenarios with 70, 100, and 130 daily orders.")
    result = advisory_service.run_advice(question)
    assert "52,185" in result


def test_nonfinancial_ai_request_is_blocked_before_model(monkeypatch):
    from app import advisory_service
    monkeypatch.setattr(advisory_service, "ensure_api_allowed", lambda: (_ for _ in ()).throw(QuotaCooldown("blocked")))
    with pytest.raises(QuotaCooldown, match="blocked"):
        advisory_service.run_advice("Which Dubai neighborhood is best for meaty pizza?")


def test_recorded_429_prevents_second_model_call(monkeypatch, tmp_path):
    from app import advisory_service
    from app import quota_guard
    path = tmp_path / "state.json"
    calls = []

    class FakeAgent:
        def run(self, question):
            calls.append(question)
            raise RuntimeError(DAILY)

    monkeypatch.setattr(advisory_service, "_focused_agent", lambda: FakeAgent())
    monkeypatch.setattr(advisory_service, "ensure_api_allowed", lambda: quota_guard.ensure_api_allowed(path=path, now=1000))
    monkeypatch.setattr(advisory_service, "record_quota_failure", lambda exc: quota_guard.record_quota_failure(exc, path=path, now=1000))
    with pytest.raises(RuntimeError, match="429"):
        advisory_service.run_advice("Which Dubai location should we select?")
    with pytest.raises(QuotaCooldown):
        advisory_service.run_advice("Which Dubai location should we select?")
    assert len(calls) == 1


def test_successful_answer_does_not_create_cooldown(monkeypatch, tmp_path):
    from app import advisory_service
    from app import quota_guard
    from types import SimpleNamespace
    path = tmp_path / "state.json"

    class FakeAgent:
        def run(self, question):
            return SimpleNamespace(content="### Recommendation\nConduct a conditional location audit.")

    monkeypatch.setattr(advisory_service, "_focused_agent", lambda: FakeAgent())
    monkeypatch.setattr(advisory_service, "ensure_api_allowed", lambda: quota_guard.ensure_api_allowed(path=path, now=1000))
    monkeypatch.setattr(advisory_service, "record_quota_failure", lambda exc: quota_guard.record_quota_failure(exc, path=path, now=1000))
    answer = advisory_service.run_advice("Which Dubai location should we select?")
    assert "conditional location audit" in answer
    assert not path.exists()
