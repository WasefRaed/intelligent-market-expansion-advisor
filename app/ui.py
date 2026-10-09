"""Executive Streamlit interface; run: python -m streamlit run app/ui.py"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# `streamlit run app/ui.py` may put the app/ directory ahead of the repo root.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

from app.advisory_service import run_advice
from app.config import MODEL_ID, FALLBACK_MODEL_ID, ENABLE_LIVE_RESEARCH
from app.runtime import friendly_provider_error
from app.quota_guard import quota_status, cooldown_message
from app.tools.decision_tools import WEIGHTS, area_screening
from app.tools.market_tools import calculate_unit_economics, load_market_data
from app.evidence_registry import source_registry

st.set_page_config(
    page_title="UAE Expansion Advisor | Executive Intelligence",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root { --navy:#15243b; --mint:#068f7d; }
.block-container { padding-top:1.7rem; padding-bottom:3rem; max-width:1330px; }
[data-testid="stSidebar"] { background: #10243a; }
[data-testid="stSidebar"] * { color: #f0f5f7; }
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] * { color:#14253b; }
[data-testid="stSidebar"] .stRadio [role="radiogroup"] { gap: 0.8rem; }
.hero-wrap { background:linear-gradient(115deg,#10263d 0%,#163e54 64%,#0d706c 100%);
 border-radius:19px; padding:25px 32px; margin-bottom:1.15rem; color:white; }
.hero-eyebrow {color:#b3e8db;letter-spacing:.13em;font-weight:700;font-size:.77rem;}
.hero-wrap h1 {font-size:2rem;line-height:1.15;font-weight:770;margin:10px 0 9px;color:white;}
.hero-wrap p {color:#d8e7ea; margin:0;font-size:1rem;}
.small-note {font-size:.86rem;color:#667689;line-height:1.5;}
.metric-label {font-weight:700;color:#244257;}
[data-testid="stMetric"] { border:1px solid #e4e9ef; border-radius:13px; padding:11px 16px; }
[data-testid="stMetricLabel"] {font-size:.84rem;}
[data-testid="stChatMessage"] {border-radius:14px;}
</style>
""", unsafe_allow_html=True)

snapshot = load_market_data()

with st.sidebar:
    st.markdown("## ◈ UAE Advisor")
    st.caption("MARKET INTELLIGENCE • JORDAN → UAE")
    st.divider()
    st.markdown("**Analysis mode**")
    mode_label = st.radio(
        "Analysis mode", ["Focused advisor", "Full multi-agent team"],
        index=0, label_visibility="collapsed",
        help="Focused mode makes a single Agno Agent request, with a fallback if needed. Full team delegates and can use many API requests.",
    )
    if mode_label == "Full multi-agent team":
        st.warning("Higher API usage. Your free-tier rate limit may be reached by one team question.")
    st.markdown("**Business priority**")
    scenario = st.selectbox(
        "Business priority", ["balanced", "cost_control", "demand_first"],
        format_func=lambda s: {"balanced":"Balanced entry", "cost_control":"Cost control", "demand_first":"Demand first"}[s],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("MODEL SETTINGS")
    st.markdown(f"Primary: `{MODEL_ID}`")
    st.markdown(f"Fallback: `{FALLBACK_MODEL_ID}`")
    st.markdown("Live web research: **" + ("ON" if ENABLE_LIVE_RESEARCH else "OFF") + "**")
    st.caption("Snapshot: " + str(snapshot["metadata"].get("snapshot_date", "undated")))
    st.caption("No API calls are used in location, finance, or the reviewed-source catalog.")
    local_cooldown = quota_status()
    if local_cooldown:
        st.warning(cooldown_message(local_cooldown))
    else:
        st.caption("Quota not checked live. A 429 daily limit will not be fixed by repeated retries.")
    st.divider()
    st.caption("**Important:** Snapshot scores are subjective scenarios, not measured demand, rent, or guaranteed returns.")

st.markdown("""
<div class="hero-wrap">
  <div class="hero-eyebrow">STRATEGY STUDIO / UAE EXPANSION</div>
  <h1>Intelligent Market Expansion Advisor</h1>
  <p>Executive decision support for Jordanian meaty pizza & kebab sandwiches · Dubai + Abu Dhabi</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Markets covered", "2", "Dubai · Abu Dhabi", delta_color="off")
with c2:
    st.metric("Planning locations", "10", "5 per city", delta_color="off")
with c3:
    st.metric("Advisory specialties", "5", "Agno specialist agents", delta_color="off")

chat_tab, location_tab, economics_tab, evidence_tab = st.tabs([
    "✦ AI Advisor", "◎ Location Explorer", "◫ Unit Economics", "▤ Evidence & Methodology"
])

with chat_tab:
    st.subheader("Ask the executive advisor")
    st.caption("Choose Focused for fewer Gemini requests. Full team is optional and consumes more API quota.")
    prompts = [
        "Which Dubai location best fits our meaty-pizza and kebab-sandwich concept?",
        "Compare JLT in Dubai with Al Reem Island in Abu Dhabi.",
        "Design a realistic UAE menu and pricing architecture.",
        "Build a 90-day launch plan with measurable KPIs.",
    ]
    quick_cols = st.columns(2)
    for idx, prompt in enumerate(prompts):
        with quick_cols[idx % 2]:
            if st.button(prompt, key=f"suggest-{idx}", width="stretch"):
                st.session_state["pending_question"] = prompt

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if st.button("Clear conversation", icon="🗑️", help="Clear messages from the dashboard only"):
        st.session_state["chat_history"] = []

    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    typed = st.chat_input("Ask about UAE expansion, competition, pricing, risks, or launch plans…")
    question = st.session_state.pop("pending_question", None) or typed
    if question:
        st.session_state["chat_history"].append({"role":"user", "content":question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Preparing evidence-based advice…"):
                try:
                    answer = run_advice(
                        question,
                        "team" if mode_label == "Full multi-agent team" else "focused",
                        scenario,
                    )
                except Exception as exc:
                    friendly = friendly_provider_error(str(exc))
                    answer = (
                        "**The live AI response is unavailable.** "
                        + (friendly or "The request could not be completed. Check your API quota and connection.")
                        + "\n\nYou can still explore both cities and calculate scenarios in the "
                        "**Location Explorer** and **Unit Economics** tabs without the API."
                    )
                st.markdown(answer)
                st.caption("Business advice is hypothetical until validated. Reviewed official-source notes are separate from the model's unsourced strategic claims.")
        st.session_state["chat_history"].append({"role":"assistant", "content":answer})

with location_tab:
    st.subheader("Location opportunity screening")
    st.caption("Transparent scenario scoring from the dated internal market snapshot. Rankings are exploratory, not site investment forecasts.")
    city = st.segmented_control("City", ["Dubai", "Abu Dhabi"], default="Dubai", key="location_city")
    city = city or "Dubai"
    result = area_screening(city, scenario)
    rankings = result["ranking"]
    w = result["weights"]
    st.markdown(
        "**Scenario weights:** " + " · ".join(
            f"{k.replace('_',' ').title()}: {v:.0%}" for k, v in w.items()
        )
    )
    shortlist = rankings[:3]
    cols = st.columns(3)
    for col, item in zip(cols, shortlist):
        with col:
            st.metric(f"#{item['rank']}{' (tied)' if item['tied'] else ''} · {item['name']}", f"{item['screening_score_out_of_5']:.2f}/5")
            st.caption(item["why"])
    df = pd.DataFrame({
        "Area": [r["name"] for r in rankings],
        "Scenario score": [r["screening_score_out_of_5"] for r in rankings],
    }).set_index("Area")
    st.bar_chart(df, horizontal=True, x_label="Heuristic score (0–5)", y_label="Area")
    st.caption("Equal scores are tied. Ordering among tied locations is for display only, not an economic preference.")
    details = pd.DataFrame([
        {
            "Rank": f"{r['rank']} (tie)" if r["tied"] else str(r["rank"]), "Location": r["name"],
            "Screening (0–5)": r["screening_score_out_of_5"],
            "Concept fit": r["source_signals"]["fit"],
            "Traffic proxy": r["source_signals"]["traffic_qualitative_proxy"],
            "Rent pressure": r["source_signals"]["rent_pressure_qualitative_proxy"],
        }
        for r in rankings
    ])
    st.dataframe(details, hide_index=True, width="stretch")
    with st.expander("Why these locations? What needs validation?"):
        for r in rankings:
            st.markdown(f"**{r['name']}** — {r['why']} **Tradeoff:** {r['tradeoff']}")
        st.info(result["interpretation"])

with economics_tab:
    st.subheader("Illustrative store economics")
    st.caption("Change assumptions and instantly see contribution estimates. These are NOT profit forecasts or investment-grade financial statements.")
    left, right = st.columns([1, 1.15], gap="large")
    with left:
        orders = st.number_input("Orders per day", min_value=1, max_value=10000, value=100, step=10)
        ticket = st.number_input("Average order value (AED)", min_value=1.0, max_value=5000.0, value=49.0, step=1.0)
        food = st.slider("Food cost (% of sales)", 0, 100, 30) / 100
        other = st.slider("Labour, rent and other (% of sales)", 0, 100, 45) / 100
        delivery = st.slider("Delivery order share (%)", 0, 100, 35) / 100
        commission = st.slider("Delivery platform commission (%)", 0, 100, 25) / 100
        trading_days = st.number_input("Trading days per month", min_value=1, max_value=31, value=30, step=1)
    result = json.loads(calculate_unit_economics(
        int(orders), ticket, food, other, delivery, commission,
        trading_days_per_month=int(trading_days),
    ))
    with right:
        a, b = st.columns(2)
        a.metric("Monthly gross sales", f"AED {result['monthly_sales_aed']:,.0f}")
        b.metric("Contribution (illustrative)", f"AED {result['illustrative_contribution_before_tax_and_capex_aed']:,.0f}")
        st.metric("Illustrative contribution margin", f"{result['contribution_margin_pct']:.1f}%")
        costs = pd.DataFrame({
            "Category": ["Food", "Labour/rent/other", "Delivery fees", "Residual contribution"],
            f"AED / {int(trading_days)} days": [result["food_cost_aed"], result["labor_rent_other_aed"],
                             result["delivery_commission_aed"], result["illustrative_contribution_before_tax_and_capex_aed"]],
        }).set_index("Category")
        st.bar_chart(costs, horizontal=True)
    st.warning(result["warning"])
    st.markdown("**Scenario sensitivity (same assumptions):**")
    from app.finance_guard import format_financial_scenarios, FinancialInputs
    volumes = (max(1, int(orders * 0.7)), int(orders), max(1, int(orders * 1.3)))
    st.markdown(format_financial_scenarios(FinancialInputs(
        int(orders), ticket, int(trading_days), food, other, delivery, commission, volumes
    )))
    st.download_button(
        "Download scenario JSON", json.dumps(result, indent=2),
        file_name="uae_economics_scenario.json", mime="application/json",
    )

with evidence_tab:
    st.subheader("Evidence, assumptions, and model limitations")
    st.info("The market snapshot is a planning baseline dated " + str(snapshot["metadata"]["snapshot_date"]) + ". It is **not** a live, independently verified market database.")
    st.markdown("**What is deterministic?** Location scenario scores and the illustrative unit-economics calculator. Neither requires Gemini API access.")
    st.markdown("**What uses AI?** Focused mode uses one Agno Agent and can attempt a fallback model. Full mode uses the coordinating Agno Team and specialist agents, potentially making multiple model requests.")
    st.markdown("**What has not been verified?** Real unit rents, actual customer footfall, present-day restaurant inventory, current competitor prices, aggregator contract rates, available licenses for a specific property.")
    registry = source_registry()
    st.markdown("### Reviewed official source notes")
    st.caption(
        f"Reviewed: {registry['reviewed_on']} · Frozen offline references. "
        "This is not a live regulatory feed and does not validate any recommended branch or financial forecast."
    )
    for source in registry["sources"]:
        with st.expander(f"[{source['id']}] {source['title']} · {source['publisher']}"):
            st.markdown(f"**Narrow claim supported:** {source['supported_claim']}")
            st.warning("**Limitations:** " + source["limitations"])
            st.markdown(f"[Open official reference]({source['url']})")
    st.markdown("### Unreviewed snapshot research leads")
    st.caption("Links below came from the original market snapshot; their presence does not verify individual claims.")
    urls = snapshot.get("regulatory", {}).get("sources", []) + snapshot.get("price_bands", {}).get("source_urls", [])
    urls.extend(c["source"] for c in snapshot["competitors"] if c.get("source"))
    seen = set()
    for url in urls:
        if url not in seen:
            seen.add(url)
            st.markdown(f"- {url}")
    st.caption("Listed URLs are research leads; opening a URL does not automatically verify every market claim in the snapshot.")
    st.download_button("Download the dated snapshot", json.dumps(snapshot, ensure_ascii=False, indent=2),
                       file_name="uae_market_snapshot.json", mime="application/json")
