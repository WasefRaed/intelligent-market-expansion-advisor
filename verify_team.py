"""Run once when quota is available to verify actual Agno delegation.

Important: one team question can generate many requests. This script does NOT
assert that every specialist is needed for a narrow prompt.
"""
from app.advisory_service import build_evidence
from app.quota_guard import ensure_api_allowed, record_quota_failure, QuotaCooldown

QUESTION = (
    "We are opening ONE Jordanian meaty-pizza and kebab-sandwich restaurant. "
    "Please have the Location Strategy Agent compare JLT and Deira/Bur Dubai "
    "and the Menu and Pricing Agent suggest indicative menu architecture. "
    "Use only dated internal planning assumptions. Explain ties and don't "
    "invent quantitative sales, rents or competition data. Keep the answer short."
)


def main():
    try:
        ensure_api_allowed()
    except QuotaCooldown as exc:
        print(exc)
        return 2

    # Load Agno *after* the local guard so blocked calls stay offline.
    from app.agents import advisor

    advisor.store_member_responses = True
    evidence = build_evidence(QUESTION, "balanced")
    print("Agno team:", advisor.name)
    print("Configured member agents:", [a.name for a in advisor.members])
    print("Starting ONE diagnostic request. Do not repeatedly rerun on 429.")
    try:
        response = advisor.run("Executive question:\n" + QUESTION + "\nInternal evidence:\n" + evidence)
    except Exception as exc:
        record_quota_failure(exc)
        print("Execution failed:", type(exc).__name__, str(exc)[:800])
        return 1

    print("\n========== DELEGATION REPORT ==========")
    members = getattr(response, "member_responses", None) or []
    print("Recorded delegated runs:", len(members))
    for index, member in enumerate(members, start=1):
        name = (getattr(member, "agent_name", None) or
                getattr(member, "team_name", None) or
                getattr(member, "agent_id", "Unknown"))
        print(f"{index}. Agent: {name}")
        for tool in getattr(member, "tools", None) or []:
            print("   Tool:", getattr(tool, "tool_name", None) or getattr(tool, "name", "Unknown"))
    print("\n========== FINAL RESPONSE ==========")
    print(str(getattr(response, "content", response))[:7500])
    print("\n========== END ==========")
    return 0 if members else 3


if __name__ == "__main__":
    raise SystemExit(main())
