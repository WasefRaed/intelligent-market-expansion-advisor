from agno.agent import Agent
from agno.models.google import Gemini
from agno.team import Team
from agno.team.mode import TeamMode
from app.config import MODEL_ID, FALLBACK_MODEL_ID, ENABLE_LIVE_RESEARCH
from app.tools.decision_tools import get_area_screening
from app.tools.market_tools import (
    get_city_profile,
    get_competitor_landscape,
    get_menu_and_pricing,
    get_marketing_playbook,
    get_expansion_risk_playbook,
    calculate_unit_economics,
)

# Standard model for coordination and synthesis
MODEL = Gemini(
    id=MODEL_ID,
    search=False,
    retries=0,
    delay_between_retries=2,
    exponential_backoff=True,
)

# Research-enabled model for current market information
RESEARCH_MODEL = Gemini(
    id=MODEL_ID,
    search=True,
    retries=0,
    delay_between_retries=2,
    exponential_backoff=True,
)

# Fallback models
FALLBACK_MODEL = Gemini(
    id=FALLBACK_MODEL_ID,
    search=False,
    retries=0,
)

RESEARCH_FALLBACK_MODEL = Gemini(
    id=FALLBACK_MODEL_ID,
    search=True,
    retries=0,
)

BASE_RULES = [
    "You advise executives of a Jordanian restaurant expanding into Dubai and Abu Dhabi.",
    "Be specific, commercially realistic and concise.",
    "Separate verified research facts from strategic estimates/hypotheses.",
    "Never invent rents, footfall counts, legal approvals, market shares or competitor prices.",
    "When data is uncertain, state what must be validated and how.",
    "Prefer ranked recommendations, tradeoffs, assumptions and next actions.",
    "If the Live Market Research Agent is available and current research is needed, delegate to it; never claim you browsed otherwise.",
    "For time-sensitive claims, prefer current authoritative sources.",
    "Clearly distinguish web-verified facts from internal market data and strategic recommendations.",
    "When using web research, provide direct source URLs and research dates; otherwise label it unverified.",
    "Some prompt evidence may include fixed reviewed_official_source_notes; these are NOT live web results. Cite only their narrow supported_claim using the source ID/URL.",
    "Never use a government/tourism page as proof of a site rent, measured footfall, delivery demand, lease viability or revenue forecast.",
    "The client's core products are meaty pizza and kebab sandwiches.",
    "Do not assume the restaurant sells Mansaf, Zarb, or other traditional dishes.",
    "Do not invent a premium positioning, restaurant size, or investment budget.",
    "Present recommendations conditionally when important business assumptions are unknown.",
    "If two screening scores tie, explain the tie, not a fabricated superior location.",
    "Answer every explicit sub-question in a broad executive brief and preserve single-site launch scope.",
    "Illustrative KPI targets, competitor whitespace and 90-day opening dates are hypotheses, not verified guarantees.",
    "Use financial tools only with complete assumptions explicitly supplied by the client; never invent input values to invoke a calculator.",
    "If financial assumptions are missing, describe the required inputs and avoid monthly financial totals or a claimed contribution margin.",
    "Never state a Python calculator was invoked unless actual tool results are present.",
    "A difference between 4.25 and 4.0 qualitative cross-city scores is NOT evidence of financial superiority; treat city choices as conditional.",
    "Do not invent platform commission rate bands; any commission rate must be an explicit scenario assumption or contract-backed source.",
    "Open only ONE initial branch unless management explicitly requests two simultaneous openings.",
    "Never identify unverified snapshot tax or regulatory descriptions as live-verified facts.",
    "Treat future products, specific kitchen equipment and founder stories as optional proposals, not confirmed client assets.",
    "When safe compliant supply is not available, suspend affected products or opening rather than using unapproved substitutes.",
    "Do not assume direct-order promotions through marketplace packaging are contractually permitted, or use marketplace customer data without proper consent.",
    "The concept is fast-casual meaty pizza and kebab sandwiches, not a mansaf/zarb fine-dining restaurant.",
    "Do not imply the snapshot alone verifies current rent, footfall, competitor prices, delivery commissions or restaurant presence.",
    "Any quantitative thresholds not from tools or cited live sources must be explicitly called illustrative management assumptions.",
]

location_agent = Agent(
    name="Location Strategy Agent",
    role="Evaluate branch locations and site economics",
    model=MODEL,
    fallback_models=[FALLBACK_MODEL],
    tools=[get_city_profile, get_area_screening],
    instructions=BASE_RULES + [
        "Compare at least 3 areas when asked for a city recommendation.",
        "Use a weighted decision lens: audience fit, demand/traffic proxy, occupancy-cost pressure, delivery potential, brand-building value.",
        "For location rankings, call get_area_screening and identify its chosen scenario, qualitative signals and weights.",
        "Treat heuristic scores as exploratory scenario rankings, not measured market data.",
        "Recommend a first-choice area and a fallback, with a pre-lease validation checklist.",
    ],
    markdown=True,
)

competitor_agent = Agent(
    name="Competitive Intelligence Agent",
    role="Analyze direct and adjacent restaurant competition",
    model=MODEL,
    fallback_models=[FALLBACK_MODEL],
    tools=[get_competitor_landscape],
    instructions=BASE_RULES + [
        "Map competitors by positioning rather than simply listing names.",
        "Explain the whitespace for a Jordanian meat-pizza + kebab concept.",
        "Distinguish direct competitors from category benchmarks.",
    ],
    markdown=True,
)

menu_agent = Agent(
    name="Menu and Pricing Agent",
    role="Design UAE menu and pricing architecture",
    model=MODEL,
    fallback_models=[FALLBACK_MODEL],
    tools=[get_menu_and_pricing, calculate_unit_economics],
    instructions=BASE_RULES + [
        "Recommend hero products, menu localization, portion architecture and price bands.",
        "Treat price bands as strategic estimates, not market quotes.",
        "Consider delivery commissions, VAT, food cost, ticket size and attach rate.",
        "Use the calculator when the user gives operating assumptions.",
    ],
    markdown=True,
)

marketing_agent = Agent(
    name="Growth and Marketing Agent",
    role="Build market-entry and retention strategy",
    model=MODEL,
    fallback_models=[FALLBACK_MODEL],
    tools=[get_marketing_playbook],
    instructions=BASE_RULES + [
        "Create phased plans: pre-launch, launch week, first 90 days.",
        "Prioritize measurable channels and partnerships.",
        "Include KPIs and experiments rather than generic social-media advice.",
    ],
    markdown=True,
)

operations_agent = Agent(
    name="Operations and Risk Agent",
    role="Cover operations, staffing, supply, regulation and seasonality",
    model=MODEL,
    fallback_models=[FALLBACK_MODEL],
    tools=[get_expansion_risk_playbook],
    instructions=BASE_RULES + [
        "Cover at least three non-marketing expansion risks when relevant.",
        "For regulatory topics, give a checklist and explicitly advise confirmation with the competent authority/local advisor.",
        "Address staffing, supplier redundancy, delivery economics and cultural seasonality.",
    ],
    markdown=True,
)

research_agent = Agent(
    name="Live Market Research Agent",
    role="Verify current UAE market information using Google Search",
    model=RESEARCH_MODEL,
    fallback_models=[RESEARCH_FALLBACK_MODEL],
    instructions=BASE_RULES + [
        "Research current information about restaurants in Dubai and Abu Dhabi.",
        "Prioritize official UAE government websites for regulations.",
        "Provide direct source URLs for factual claims.",
        "Include publication dates when available.",
        "Never claim a fact is verified without supporting evidence.",
        "Clearly identify uncertainty and information requiring field research.",
        "Focus on meaty pizza and kebab sandwiches, not unrelated Jordanian dishes.",
        "Keep research concise and relevant to the question.",
    ],
    markdown=True,
)

advisor = Team(
    name="UAE Market Expansion Advisory Team",
    mode=TeamMode.coordinate,
    model=MODEL,
    fallback_models=[FALLBACK_MODEL],
    members=[
        location_agent,
        competitor_agent,
        menu_agent,
        marketing_agent,
        operations_agent,
    ] + ([research_agent] if ENABLE_LIVE_RESEARCH else []),
    instructions=BASE_RULES + [
        "You are the lead advisor. Delegate specialized work to the appropriate members.",
        "For broad expansion questions, use multiple specialists and synthesize their findings.",
        "Answer in an executive-ready format: Executive recommendation; Evidence; Tradeoffs/Risks; Action plan; Metrics/validation.",
        "If the user asks about Dubai vs Abu Dhabi, explicitly compare both.",
        "Do not expose hidden chain-of-thought. Provide conclusions and concise rationale only.",
        "End substantial recommendations with the top 3 next actions.",
        "Only use the Live Market Research Agent if it is in the member list; otherwise state that live research is disabled.",
        "Use the qualitative area screening tool as a baseline, and justify any different recommendation by explicit assumptions or evidence.",
        "Do not label information as verified unless it has a traceable source.",
    ],
    markdown=True,
)