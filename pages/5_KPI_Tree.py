"""
Streamlit Page 5: KPI Tree & Search Performance Decomposition.
"""
import streamlit as st
import plotly.graph_objects as go
from analysis.insights_aggregator import InsightsAggregator
from app.components.styles import apply_custom_theme, render_hero
from app.components.nudges import render_insight_cue, render_next_step_nudge, render_sidebar_journey_flow

st.set_page_config(page_title="KPI Tree — Google Photos", page_icon="📈", layout="wide")
apply_custom_theme()

render_hero(
    title="📈 Business Metrics & KPI Tree Decomposition",
    subtitle="Mapping user retrieval pain points to North Star metrics, friction indicators, and guardrail safeguards.",
    badge_text="Executive Metric Framework"
)

render_sidebar_journey_flow(5)

render_insight_cue(
    "40.3% of complaints directly depress the Search Success Rate. Avg Queries/Session is artificially inflated "
    "by users trapped in repetitive query reformulation loops."
)

agg = InsightsAggregator()
kpi_data = agg.get_kpi_tree_impact()

# North Star Formula Card
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3a8a 0%, #1e293b 100%); border-radius: 14px; padding: 1.5rem 2rem; color: white; margin-bottom: 2rem;">
    <div style="font-size: 0.85rem; font-weight: 700; color: #93c5fd; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">
        Top-Level Business Metric Formula
    </div>
    <div style="font-size: 1.5rem; font-weight: 800; font-family: monospace;">
        Total Successful Searches = Total Search Queries × Search Success Rate (%)
    </div>
    <p style="color: #cbd5e1; font-size: 0.95rem; margin-top: 0.5rem; margin-bottom: 0;">
        Where Search Success Rate is defined as searches culminating in an active target engagement (View / Share / Edit / Save) without abandoned back-navigations.
    </p>
</div>
""", unsafe_allow_html=True)

st.subheader("🌳 Interactive Metric Hierarchy (Treemap)")

st.markdown("""
<div style="display: flex; gap: 1.5rem; justify-content: flex-start; align-items: center; margin: 0.4rem 0 1.2rem 0; flex-wrap: wrap;">
    <span style="display: inline-flex; align-items: center; gap: 0.45rem; font-size: 0.88rem; font-weight: 700; color: #4ade80;">
        <span style="width: 12px; height: 12px; background: #22c55e; border-radius: 3px; display: inline-block;"></span>
        🟢 Metrics to Increase
    </span>
    <span style="display: inline-flex; align-items: center; gap: 0.45rem; font-size: 0.88rem; font-weight: 700; color: #facc15;">
        <span style="width: 12px; height: 12px; background: #d97706; border-radius: 3px; display: inline-block;"></span>
        🟡 Intermediate / Balancing
    </span>
    <span style="display: inline-flex; align-items: center; gap: 0.45rem; font-size: 0.88rem; font-weight: 700; color: #f87171;">
        <span style="width: 12px; height: 12px; background: #dc2626; border-radius: 3px; display: inline-block;"></span>
        🔴 Metrics to Decrease (Minimize Friction)
    </span>
</div>
""", unsafe_allow_html=True)

ids = [
    "total_successful",
    "total_queries",
    "success_rate",
    "search_users",
    "searches_per_user",
    "active_users",
    "search_sessions",
    "queries_per_session",
    "target_action_rate",
]

parents = [
    "",
    "total_successful",
    "total_successful",
    "total_queries",
    "total_queries",
    "search_users",
    "searches_per_user",
    "searches_per_user",
    "success_rate",
]

labels = [
    "Total Successful Searches (North Star Target)",
    "Total Search Queries (Balancing Metric)",
    "Search Success Rate (%) (Core Conversion Driver)",
    "Total Search Users (Adoption)",
    "Avg Searches / User (⬇ MINIMIZE)",
    "Active Users × % Who Search<br><b>(Adoption Driver)</b>",
    "Avg Search Sessions<br><b>(Balancing Metric)</b>",
    "Avg Queries / Session<br><b>(⬇ FRICTION - MINIMIZE)</b>",
    "Target Action Rate<br><b>(View / Share / Edit)</b>",
]

# Strategic proportional sizing with branchvalues="total":
# active_users (28) -> search_users (28)
# search_sessions (22) + queries_per_session (24) -> searches_per_user (46)
# search_users (28) + searches_per_user (46) -> total_queries (74)
# target_action_rate (32) -> success_rate (32)
# total_queries (74) + success_rate (32) -> total_successful (106)
values = [106, 74, 32, 28, 46, 28, 22, 24, 32]

# Strategic color assignments:
# GREEN: Metrics to Increase (Google Green #34A853)
# RED: Metrics to Decrease / Friction (Google Red #EA4335)
# YELLOW / AMBER: Intermediate / Balancing metrics (Google Yellow #FBBC05)
metric_colors = [
    "#34A853",  # total_successful -> Google Green (Maximize)
    "#FBBC05",  # total_queries -> Google Yellow (Balancing)
    "#34A853",  # success_rate -> Google Green (Maximize)
    "#2D9247",  # search_users -> Google Green (Maximize)
    "#EA4335",  # searches_per_user -> Google Red (Minimize)
    "#34A853",  # active_users -> Google Green (Maximize)
    "#E5AB04",  # search_sessions -> Google Yellow (Intermediate)
    "#EA4335",  # queries_per_session -> Google Red (Minimize)
    "#2D9247",  # target_action_rate -> Google Green (Maximize)
]

fig_tree = go.Figure(go.Treemap(
    ids=ids,
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",
    textinfo="label",
    insidetextfont=dict(color="#ffffff", size=15, family="Google Sans, Roboto, sans-serif"),
    outsidetextfont=dict(color="#ffffff", size=15, family="Google Sans, Roboto, sans-serif"),
    marker=dict(colors=metric_colors),
    tiling=dict(pad=18),
))
fig_tree.update_layout(
    font_family="Google Sans, Roboto, sans-serif",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=580,
    margin=dict(t=8, l=8, r=8, b=8),
    uniformtext=dict(minsize=12)
)
st.plotly_chart(fig_tree, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("⚡ Friction vs. Success Impact")
    st.markdown(f"""
    <div class="gp-metric-card">
        <div class="gp-metric-label">Search Success Rate Impact</div>
        <div class="gp-metric-value" style="color: #f87171;">{kpi_data['search_success_rate_impact']}%</div>
        <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.5; margin-top: 0.5rem;">
            Of all analyzed complaints directly depress the Search Success Rate due to inaccurate results or missing photos.
        </p>
        <hr style="border: 0; border-top: 1px solid rgba(255, 255, 255, 0.08); margin: 1rem 0;">
        <div class="gp-metric-label">Friction Metric Warning</div>
        <div style="font-weight: 700; color: #fbbf24; font-size: 1.05rem;">
            Avg Queries per Session is artificially inflated
        </div>
        <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.5; margin-top: 0.25rem;">
            Users enter 3 to 5 repetitive variations (e.g., "mom goa", "mom beach 2021", "goa 2021") in a frantic retry loop.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("🛡️ Guardrail Metrics Status")
    guardrails = [
        ("Search Result Relevance", "🔴 High Risk", "Over 40% of feedback reports random wrong results or missing known photos.", "rgba(244, 63, 94, 0.12)", "#fb7185"),
        ("Zero-Result Query Rate", "🔴 High Risk", "Users frequently report 'No photos found' for photos verified to exist.", "rgba(244, 63, 94, 0.12)", "#fb7185"),
        ("Demographic Parity Gap", "🟡 Monitored", "Multi-person face similarity errors occur across diverse skin tones and ages.", "rgba(251, 191, 36, 0.12)", "#fbbf24"),
        ("Search Latency", "🟢 Healthy", "Query execution latency is rarely a complaint in user feedback (<500ms).", "rgba(52, 211, 153, 0.12)", "#34d399"),
        ("Crash Rate", "🟢 Healthy", "App crashes during search operations are negligible (<0.01%).", "rgba(52, 211, 153, 0.12)", "#34d399"),
    ]

    for metric, status, detail, bg, fg in guardrails:
        st.markdown(f"""
        <div style="background: {bg}; border-radius: 10px; padding: 0.75rem 1rem; margin-bottom: 0.6rem; border-left: 4px solid {fg}; border-top: 1px solid rgba(255,255,255,0.05); border-right: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: {fg}; font-size: 0.95rem;">{metric}</strong>
                <span style="font-weight: 700; font-size: 0.8rem; color: {fg};">{status}</span>
            </div>
            <div style="color: #cbd5e1; font-size: 0.85rem; margin-top: 0.25rem;">{detail}</div>
        </div>
        """, unsafe_allow_html=True)

render_next_step_nudge(
    headline="Validate with Primary Field Research",
    description="Examine authentic responses and verbatim quotes from 70+ Google Photos users confirming these exact behavioral patterns.",
    target_page="pages/6_Survey.py",
    button_label="Next Step: 6. Survey Deep-Dive",
    icon="📋",
    secondary_page="pages/7_Chatbot.py",
    secondary_label="Or Ask AI Chatbot",
    secondary_icon="🤖"
)
