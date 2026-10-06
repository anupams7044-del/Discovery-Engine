"""
Streamlit Page 1: Overview & Ingestion Metrics.
"""
import streamlit as st
import plotly.express as px
from analysis.insights_aggregator import InsightsAggregator
from app.components.styles import apply_custom_theme, render_hero
from app.components.nudges import render_insight_cue, render_next_step_nudge, render_sidebar_journey_flow

st.set_page_config(page_title="Overview — AI Discovery Engine", page_icon="📊", layout="wide")
apply_custom_theme()

render_hero(
    title="📊 Data Ingestion & System Telemetry",
    subtitle="Live monitoring of data volume across Google Play Store reviews, Reddit communities, and Primary User Surveys.",
    badge_text="Discovery Pipeline • Phase 2 & 3 Verified"
)

render_sidebar_journey_flow(1)

render_insight_cue(
    "Google Photos search feedback across 1,246 data points exhibits a 24.9% search-relevance complaint rate. "
    "Primary survey findings closely corroborate organic Reddit and Play Store frustration patterns."
)

agg = InsightsAggregator()

st.markdown("""
<style>
div.row-widget.stRadio > div { flex-direction: row; justify-content: center; gap: 10px; }
div.row-widget.stRadio > div > label { background-color: #202124; padding: 0.5rem 1rem; border-radius: 20px; border: 1px solid #3C4043; cursor: pointer; transition: 0.2s; }
div.row-widget.stRadio > div > label:hover { background-color: #2D2F31; border-color: #8AB4F8; }
div.row-widget.stRadio > div > label[data-checked="true"] { background-color: rgba(66,133,244,0.15); border-color: #4285F4; }
div.row-widget.stRadio > div > label > div:first-child { display: none; } /* hide standard radio circle */
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

overview = agg.get_overview(source_filter)

# Metric summary cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="gp-metric-card">
        <div class="gp-metric-label">Total Data Ingested</div>
        <div class="gp-metric-value">{overview['total_scraped']:,}</div>
        <div class="gp-metric-sub">🌐 Multi-Source Harvest</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="gp-metric-card">
        <div class="gp-metric-label">Search-Relevant Items</div>
        <div class="gp-metric-value">{overview['total_relevant']:,}</div>
        <div class="gp-metric-sub">🎯 {overview['relevance_rate']}% Relevance Pass Rate</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="gp-metric-card">
        <div class="gp-metric-label">AI-Analyzed Records</div>
        <div class="gp-metric-value">{overview['total_analyzed']:,}</div>
        <div class="gp-metric-sub">🧠 NLP & Vector Embedded</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    subtext_map = {
        "All Sources": "🌐 Multiple data sources",
        "survey": "📋 Google Form survey responses",
        "play_store": "📱 Play Store reviews",
        "app_store": "🍎 App Store reviews",
        "reddit": "🔥 Reddit community threads",
        "stack_exchange": "💻 StackExchange Q&A",
        "open_web": "🕸️ Open Web forums"
    }
    channel_subtext = subtext_map.get(source_filter, "📊 Selected data channel")
    
    st.markdown(f"""
    <div class="gp-metric-card">
        <div class="gp-metric-label">Active Data Channels</div>
        <div class="gp-metric-value">{len(overview['by_source'])}</div>
        <div class="gp-metric-sub">{channel_subtext}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🌐 Ingestion Volume by Channel")
    sources = overview["by_source"]
    if sources:
        fig_src = px.bar(
            x=list(sources.keys()),
            y=list(sources.values()),
            labels={"x": "Data Source", "y": "Items Ingested"},
            color=list(sources.keys()),
            color_discrete_sequence=["#4285F4", "#EA4335", "#FBBC05", "#34A853"],
            text=list(sources.values())
        )
        fig_src.update_traces(textposition='outside', marker_line_width=1.5, opacity=0.9)
        fig_src.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_family="Google Sans, Roboto, sans-serif",
            showlegend=False,
            height=380,
            margin=dict(t=20, b=20, l=10, r=10),
            xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        )
        st.plotly_chart(fig_src, use_container_width=True)

with col_right:
    st.subheader("📱 Platform Distribution")
    platforms = overview["by_platform"]
    if platforms:
        fig_plat = px.pie(
            names=list(platforms.keys()),
            values=list(platforms.values()),
            hole=0.45,
            color_discrete_sequence=["#4285F4", "#EA4335", "#FBBC05", "#34A853"]
        )
        fig_plat.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#202124', width=2)))
        fig_plat.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_family="Google Sans, Roboto, sans-serif",
            height=380,
            margin=dict(t=20, b=20, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_plat, use_container_width=True)

st.markdown("""
<div class="gp-note-box">
    <strong>💡 Methodological Note:</strong> To ensure high statistical rigor without inflating costs or burning tokens unnecessarily, 
    the system targeted a 1,000–1,500 record baseline (per NextLeap mentor guidelines) across public reviews, organic forum questions, and primary survey validation.
</div>
""", unsafe_allow_html=True)

render_next_step_nudge(
    headline="Explore Emotional Friction & Dissatisfaction",
    description="Now that you've seen data volumes and source distributions, uncover the psychological frustration and sentiment breakdown in user feedback.",
    target_page="pages/2_Sentiment.py",
    button_label="Next Step: 2. Sentiment Analysis",
    icon="🎭"
)
