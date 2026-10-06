"""
Streamlit Page 3: Issue Categorization & Top Issue Deep-Dive.
"""
import streamlit as st
import plotly.express as px
from analysis.insights_aggregator import InsightsAggregator
from database.database import SessionLocal
from database.models import AnalysisResult, ScrapedItem
from app.components.styles import apply_custom_theme, render_hero
from app.components.nudges import render_insight_cue, render_next_step_nudge, render_sidebar_journey_flow

st.set_page_config(page_title="Issue Analysis — Google Photos", page_icon="🔍", layout="wide")
apply_custom_theme()

render_hero(
    title="🔍 Issue Classification & Root-Cause Discovery",
    subtitle="Survey-calibrated taxonomy ranking user pain points across Play Store, Reddit, and Primary User Surveys.",
    badge_text="Root-Cause Analysis"
)

render_sidebar_journey_flow(3)

render_insight_cue(
    "Missing Results (21.0%) and Wrong/Irrelevant Photos (19.4%) dominate search complaints. "
    "Over 55% of all identified breakdowns concentrate in the initial retrieval and ranking stage."
)

agg = InsightsAggregator()

st.markdown("""
<style>
div.row-widget.stRadio > div { flex-direction: row; justify-content: center; gap: 10px; }
div.row-widget.stRadio > div > label { background-color: #202124; padding: 0.5rem 1rem; border-radius: 20px; border: 1px solid #3C4043; cursor: pointer; transition: 0.2s; }
div.row-widget.stRadio > div > label:hover { background-color: #2D2F31; border-color: #8AB4F8; }
div.row-widget.stRadio > div > label[data-checked="true"] { background-color: rgba(66,133,244,0.15); border-color: #4285F4; }
div.row-widget.stRadio > div > label > div:first-child { display: none; }
</style>
""", unsafe_allow_html=True)

# Shared Multi-Channel Interactive Data Filter
source_filter = st.radio(
    "Select Data Channel:",
    ["All Sources", "play_store", "app_store", "reddit", "stack_exchange", "open_web", "survey"],
    format_func=lambda x: {"All Sources": "🌐 All Sources", "play_store": "📱 Play Store", "app_store": "🍎 App Store", "reddit": "🔥 Reddit", "stack_exchange": "💻 StackExchange", "open_web": "🕸️ Web Forums", "survey": "📋 Survey"}.get(x, x),
    horizontal=True,
    label_visibility="collapsed"
)

summary = agg.get_full_summary(source_filter)
issues = summary["issues"]
top_issue = summary["top_issue"]
top_name = top_issue.get("issue", "missing_results").replace("_", " ").title()

# High-Impact Executive Top Issue Card
st.markdown(f"""
<div class="gp-highlight-box" style="border-left: 6px solid #fb7185;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
        <span class="gp-badge gp-badge-red">⭐ #1 Highest-Frequency Search Issue</span>
        <span style="font-weight: 700; color: #fb7185; font-size: 0.9rem;">Validated by Primary Research</span>
    </div>
    <div style="font-size: 1.85rem; font-weight: 800; color: #fda4af; margin-bottom: 0.5rem;">
        {top_name}
    </div>
    <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.6; margin-bottom: 1rem;">
        Users search for known photos that exist in their library, but Google Photos displays <em>"No photos found"</em> or completely irrelevant random photos. 
        This is corroborated by our survey where <strong>~40% of users</strong> reported random wrong photos and <strong>~35%</strong> reported missing results.
    </p>
    <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
        <div class="gp-stat-chip">
            <span style="color: #94a3b8; font-size: 0.8rem; font-weight: 600;">COMPLAINT VOLUME</span><br>
            <strong style="color: #fb7185; font-size: 1.25rem;">{top_issue.get('count')} mentions ({top_issue.get('percentage')}%)</strong>
        </div>
        <div class="gp-stat-chip">
            <span style="color: #94a3b8; font-size: 0.8rem; font-weight: 600;">FAILURE STAGE</span><br>
            <strong style="color: #f8fafc; font-size: 1.25rem;">Retrieval & Ranking</strong>
        </div>
        <div class="gp-stat-chip">
            <span style="color: #94a3b8; font-size: 0.8rem; font-weight: 600;">USER REACTION</span><br>
            <strong style="color: #fbbf24; font-size: 1.25rem;">Manual Timeline Scrolling</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Issue Frequency Ranking")
    if issues:
        fig_bar = px.bar(
            x=[i["count"] for i in issues],
            y=[i["issue"].replace("_", " ").title() for i in issues],
            orientation="h",
            labels={"x": "Total Mentions", "y": "Issue Category"},
            color=[i["count"] for i in issues],
            color_continuous_scale=["#F28B82", "#EA4335", "#C5221F"],
            text=[f"{i['count']} ({i['percentage']}%)" for i in issues]
        )
        fig_bar.update_traces(textposition='inside', textfont=dict(color='white'))
        fig_bar.update_layout(
            yaxis=dict(autorange="reversed"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_family="Google Sans, Roboto, sans-serif",
            coloraxis_showscale=False,
            height=420,
            margin=dict(t=10, b=10, l=10, r=10),
            xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
            yaxis_gridcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("⚠️ Journey Failure Point Funnel")
    fail_points = summary["failure_points"]
    if fail_points:
        fig_funnel = px.bar(
            x=list(fail_points.keys()),
            y=list(fail_points.values()),
            labels={"x": "Journey Stage", "y": "Breakdowns"},
            color=list(fail_points.keys()),
            color_discrete_sequence=["#EA4335", "#FBBC05", "#4285F4", "#34A853", "#8AB4F8"],
            text=list(fail_points.values())
        )
        fig_funnel.update_traces(textposition='outside')
        fig_funnel.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_family="Google Sans, Roboto, sans-serif",
            showlegend=False,
            height=420,
            margin=dict(t=10, b=10, l=10, r=10),
            xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        )
        st.plotly_chart(fig_funnel, use_container_width=True)

st.divider()

# User Quotes Cards
st.subheader("💬 Authentic User Feedback Excerpts")
db = SessionLocal()
q_samples = db.query(ScrapedItem.source, ScrapedItem.text, AnalysisResult.primary_issue)\
    .join(AnalysisResult).filter(ScrapedItem.is_relevant == True)
if source_filter and source_filter != "All Sources":
    q_samples = q_samples.filter(ScrapedItem.source == source_filter)
sample_items = q_samples.limit(4).all()
db.close()

qc1, qc2 = st.columns(2)
for idx, (src, txt, issue_name) in enumerate(sample_items):
    col = qc1 if idx % 2 == 0 else qc2
    with col:
        st.markdown(f"""
        <div class="gp-quote-card">
            "{txt[:220]}..."
            <div class="gp-quote-author">📌 [{src.upper()}] — <strong>{issue_name.replace('_', ' ').title()}</strong></div>
        </div>
        """, unsafe_allow_html=True)

render_next_step_nudge(
    headline="Synthesize Behavioral Patterns: Stories vs. Keywords",
    description="Connect specific complaints to the deeper mental model gap: how users remember events in sensory narratives versus keyword retrieval.",
    target_page="pages/4_Themes.py",
    button_label="Next Step: 4. Strategic Themes",
    icon="🧩"
)
