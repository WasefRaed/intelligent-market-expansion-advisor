import json
from app.runtime import friendly_provider_error


def test_detects_quota_in_json_result():
    body = json.dumps({"error": {"code": 429, "status": "RESOURCE_EXHAUSTED"}})
    assert "quota" in friendly_provider_error(body)


def test_detects_unavailable_in_json_result():
    body = json.dumps({"error": {"code": 503, "status": "UNAVAILABLE"}})
    assert "overloaded" in friendly_provider_error(body)


def test_does_not_reject_business_mentions_of_numbers():
    assert friendly_provider_error("503 people walked by; assume nothing without measurement") is None
    assert friendly_provider_error("Successful executive answer") is None
