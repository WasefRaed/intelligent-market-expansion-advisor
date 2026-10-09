"""Present model/provider failures without exposing verbose raw API errors."""
import json


def friendly_provider_error(result: object) -> str | None:
    """Return a user-oriented message if result looks like a Gemini API failure."""
    content = str(result)
    try:
        payload = json.loads(content)
    except (ValueError, TypeError):
        payload = None
    if isinstance(payload, dict) and isinstance(payload.get("error"), dict):
        code = str(payload["error"].get("code", ""))
        status = str(payload["error"].get("status", ""))
    else:
        # Avoid parsing arbitrary marketing text as an error just because it says "503".
        code = ""
        status = content if "Error from Gemini API" in content or "RESOURCE_EXHAUSTED" in content else ""
        if "503 UNAVAILABLE" in content:
            code = "503"
        elif "429 RESOURCE_EXHAUSTED" in content:
            code = "429"
    if code == "429" or "RESOURCE_EXHAUSTED" in status:
        return ("Gemini quota/rate limit (429). Check https://ai.dev/rate-limit ; "
                "reduce request volume or wait for the applicable reset. "
                "Fallback models using the same project may also be limited.")
    if code == "503" or "UNAVAILABLE" in status and status:
        return ("Gemini temporarily overloaded (503). Retry after capacity recovers. "
                "Configured fallbacks cannot guarantee availability.")
    return None
