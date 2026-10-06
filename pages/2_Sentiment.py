"""
Streamlit Page 2: Sentiment Analysis & Emotion Breakdown.
"""
import streamlit as st
import plotly.express as px
from analysis.insights_aggregator import InsightsAggregator
from database.database import SessionLocal
from database.models import AnalysisResult
from sqlalchemy import func
from app.components.styles import apply_custom_theme, render_hero
from app.components.nudges import render_insight_cue, render_next_step_nudge, render_sidebar_journey_flow

st.set_page_config(page_title="Sentiment Analysis — Google Photos", page_icon="💬", layout="wide")
apply_custom_theme()

render_hero(
    title="💬 Sentiment & Emotional Friction Analysis",
    subtitle="Evaluating user sentiment polarity, emotional frustration, and psychological friction when searching for photos.",
    badge_text="NLP Intelligence Layer"
)

render_sidebar_journey_flow(2)

render_insight_cue(
    "Over 65% of search feedback is negatively polarized. Users express acute frustration and helplessness "
    "when searching for photos they know are backed up in their library."
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

sentiment_dist = agg.get_sentiment_distribution(source_filter)

total_sent = sum(sentiment_dist.values()) or 1
neg_count = sentiment_dist.get("negative", 0)
pos_count = sentiment_dist.get("positive", 0)
neu_count = sentiment_dist.get("neutral", 0)
mix_count = sentiment_dist.get("mixed", 0)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="gp-metric-card" style="border-top: 4px solid #EA4335;">
        <div class="gp-metric-label">Negative Sentiment</div>
        <div class="gp-metric-value" style="color: #F28B82;">{round(neg_count / total_sent * 100, 1)}%</div>
        <div class="gp-metric-sub" style="color: #F28B82;">🔴 {neg_count} Dissatisfied Users</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="gp-metric-card" style="border-top: 4px solid #34A853;">
        <div class="gp-metric-label">Positive Sentiment</div>
        <div class="gp-metric-value" style="color: #81C995;">{round(pos_count / total_sent * 100, 1)}%</div>
        <div class="gp-metric-sub" style="color: #81C995;">🟢 {pos_count} Satisfied Mentions</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="gp-metric-card" style="border-top: 4px solid #9AA0A6;">
        <div class="gp-metric-label">Neutral / Informational</div>
        <div class="gp-metric-value" style="color: #9AA0A6;">{round(neu_count / total_sent * 100, 1)}%</div>
        <div class="gp-metric-sub" style="color: #9AA0A6;">⚪ {neu_count} Neutral Inquiries</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="gp-metric-card" style="border-top: 4px solid #FBBC05;">
        <div class="gp-metric-label">Mixed Sentiment</div>
        <div class="gp-metric-value" style="color: #FDD663;">{round(mix_count / total_sent * 100, 1)}%</div>
        <div class="gp-metric-sub" style="color: #FDD663;">🟡 {mix_count} Mixed Feedback</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🥧 Sentiment Proportions")
    if sentiment_dist:
        color_map = {
            "negative": "#EA4335",
            "neutral": "#9AA0A6",
            "positive": "#34A853",
            "mixed": "#FBBC05"
        }
        fig_pie = px.pie(
            names=list(sentiment_dist.keys()),
            values=list(sentiment_dist.values()),
            color=list(sentiment_dist.keys()),
            color_discrete_map=color_map,
            hole=0.45,
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#202124', width=2)))
        fig_pie.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_family="Google Sans, Roboto, sans-serif",
            height=380,
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("😡 Emotional States Detected")
    from database.models import ScrapedItem
    db = SessionLocal()
    q_emo = db.query(AnalysisResult.emotion, func.count(AnalysisResult.id)).join(ScrapedItem, AnalysisResult.item_id == ScrapedItem.id).group_by(AnalysisResult.emotion)
    if source_filter and source_filter != "All Sources":
        q_emo = q_emo.filter(ScrapedItem.source == source_filter)
    emotions = dict(q_emo.all())
    db.close()
    if emotions:
        fig_emo = px.bar(
            x=list(emotions.keys()),
            y=list(emotions.values()),
            labels={"x": "Expressed Emotion", "y": "Count"},
            color=list(emotions.keys()),
            color_discrete_sequence=["#EA4335", "#FBBC05", "#34A853", "#9AA0A6", "#8AB4F8"],
            text=list(emotions.values())
        )
        fig_emo.update_traces(textposition='outside')
        fig_emo.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_family="Google Sans, Roboto, sans-serif",
            showlegend=False,
            height=380,
            margin=dict(t=10, b=10, l=10, r=10),
            xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        )
        st.plotly_chart(fig_emo, use_container_width=True)

# Strategic Takeaway Callout Box
st.markdown(f"""
<div class="gp-highlight-box">
    <div class="gp-highlight-title">📌 Strategic Presentation Takeaway (Slide 5 Hook)</div>
    <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.6; margin: 0;">
        <strong>Over {round(neg_count / total_sent * 100, 0):.0f}% of all search-related feedback exhibits frustration or confusion.</strong>
        The dominant emotion is <em>helplessness</em> when an exact photo known to exist cannot be retrieved, triggering immediate task abandonment.
    </p>
</div>
""", unsafe_allow_html=True)

render_next_step_nudge(
    headline="Diagnose Root Causes Behind the Frustration",
    description="Explore the survey-calibrated taxonomy ranking user pain points to see why 'Missing Results' and 'Random Wrong Photos' lead all complaints.",
    target_page="pages/3_Issues.py",
    button_label="Next Step: 3. Issue Classification",
    icon="🔍"
)
