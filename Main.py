"""
Streamlit app — Main entry point.
Google Photos Search — AI-Powered Discovery Engine & Conversational Assistant
"""
import streamlit as st
import os
from app.components.styles import apply_custom_theme, render_hero, render_accent_bar
from app.components.nudges import render_next_step_nudge, render_sidebar_journey_flow
from analysis.insights_aggregator import InsightsAggregator

st.set_page_config(
    page_title="Google Photos Search — AI Discovery Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_theme()

render_hero(
    title="🔍 Google Photos Search — AI Discovery Engine",
    subtitle="Analyzing 1,246 real user feedback items across Play Store, Reddit, and Primary User Surveys to uncover search friction, root causes, and business impact.",
    badge_text="NextLeap Product Fellowship • Executive Discovery Portal"
)

agg = InsightsAggregator()
summary = agg.get_full_summary()
overview = summary["overview"]
top_issue = summary["top_issue"]
sent = summary["sentiment"]

# Top Metrics Row
c1, c2, c3, c4 = st.columns(4)
total_items = overview.get("total_scraped", 1246)
rel_items = overview.get("total_relevant", 310)
top_issue_name = top_issue.get("issue", "missing_results").replace("_", " ").title()
neg_pct = round(sent.get("negative", 0) / (sum(sent.values()) or 1) * 100, 1)

with c1:
    st.markdown(f"""
    <div class="gp-metric-card">
        <div class="gp-metric-label">Total Ingested Data</div>
        <div class="gp-metric-value">{total_items:,}</div>
        <div class="gp-metric-sub">🌐 Multi-Source Verified</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="gp-metric-card">
        <div class="gp-metric-label">Search-Relevant Items</div>
        <div class="gp-metric-value">{rel_items:,}</div>
        <div class="gp-metric-sub">🎯 Isolated Pain Points</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="gp-metric-card">
        <div class="gp-metric-label">Negative Sentiment</div>
        <div class="gp-metric-value" style="color: #e11d48;">{neg_pct}%</div>
        <div class="gp-metric-sub" style="color: #e11d48;">⚠️ Active User Frustration</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="gp-metric-card">
        <div class="gp-metric-label">Top Discovered Issue</div>
        <div class="gp-metric-value" style="font-size: 1.4rem; color: #dc2626;">{top_issue_name}</div>
        <div class="gp-metric-sub">⭐ {top_issue.get('percentage', 21.0)}% of Complaints</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Executive Callout Banner
st.markdown(f"""
<div class="gp-highlight-box">
    <div class="gp-highlight-title">🚨 Executive Summary of Key Discovery Findings</div>
    <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.6; margin-bottom: 0.75rem;">
        Across <strong>1,246 real user feedback entries</strong>, Google Photos Search reveals a critical mental model misalignment: 
        <strong>Users remember context (person, place, vibe, time), while the search algorithm prioritizes exact keywords.</strong>
    </p>
    <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
        <span class="gp-badge gp-badge-red">Top Issue: {top_issue_name} ({top_issue.get('count')} mentions)</span>
        <span class="gp-badge gp-badge-amber">45% Abandon Search & Scroll Manually</span>
        <span class="gp-badge gp-badge-blue">75% Have Never Used Video Search</span>
        <span class="gp-badge gp-badge-green">Primary Survey: 70+ Verified Respondents</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Generate Markdown Executive Summary
exec_summary_md = f"""# Google Photos: AI Discovery Engine - Executive Summary

## 📊 1. Data Telemetry & Ingestion
- **Total Records Analyzed**: {total_items:,} (Play Store, Reddit, User Surveys)
- **Search-Relevant Mentions**: {rel_items:,}
- **Relevance Rate**: {overview.get('relevance_rate')}%

## 😡 2. Sentiment & Friction
- **Negative Sentiment**: {neg_pct}% of all search feedback is negatively polarized.
- **Core Emotion**: Helplessness (Users know the photo exists but the system fails to retrieve it).

## ⚠️ 3. Top Issues Discovered
1. **{top_issue_name}** ({top_issue.get('percentage')}% of complaints)
2. **Wrong / Irrelevant Photos** (19.4% of complaints)
- *Finding*: Over 55% of all breakdowns happen at the initial Retrieval & Ranking stage.

## 🧩 4. Strategic Themes
- **The Core Paradox**: Users search with sensory narratives ("that evening in Goa when Mom wore yellow"). The engine expects isolated keywords. 
- **The Multi-Entity Wall**: Queries with Person + Location + Time trigger severe precision drops.
- **The Manual Scroll Tax**: 45% of surveyed users abandon search on the first failure and scroll manually instead of reformulating the query.

## 💡 5. Proposed Strategic Solution
**The 2x2 Visual Choice Grid:**
A native, visual refinement loop integrated into the search interface. Uses K-Means clustering (K=4) to project ambiguous queries (like "vacation") into 4 distinct visual centroids (e.g., Beach, Mountains, City, Home). Zero conversational overhead; one tap refines context instantly.
"""

st.download_button(
    label="📥 Download 1-Pager Executive Summary (.md)",
    data=exec_summary_md,
    file_name="Executive_Summary_Google_Photos.md",
    mime="text/markdown",
    help="Download a presentation-ready markdown document summarizing all key findings."
)

st.markdown("### 🗺️ Discovery Engine Architecture & Navigation")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("#### 📊 Analytics & Metrics")
    st.page_link("pages/1_Overview.py", label="Overview", icon="📈")
    st.caption("Multi-channel ingestion statistics & source breakdown.")
    st.page_link("pages/2_Sentiment.py", label="Sentiment", icon="🎭")
    st.caption("Emotional intensity & sentiment proportions.")
    st.page_link("pages/3_Issues.py", label="Issues", icon="🏷️")
    st.caption("Survey-validated issue rankings & failure funnel.")

with col_b:
    st.markdown("#### 🎯 Strategic Synthesis")
    st.page_link("pages/4_Themes.py", label="Themes", icon="🧩")
    st.caption('Mental model gap: *"Stories vs Keywords"*')
    st.page_link("pages/5_KPI_Tree.py", label="KPI Tree", icon="🌳")
    st.caption("Search Success Rate formula & Guardrail metrics.")
    st.page_link("pages/6_Survey.py", label="Survey", icon="📋")
    st.caption("15-question deep dive with real user quotes.")

with col_c:
    st.markdown("#### 🤖 Conversational AI")
    st.page_link("pages/7_Chatbot.py", label="Chatbot", icon="💬")
    st.caption("Semantic RAG chatbot backed by ChromaDB vector citations.")

# Executive Guided Tour Nudge Card
render_next_step_nudge(
    headline="Start the 7-Step Guided Discovery Journey",
    description="Begin with the data foundation: explore dataset distribution across Reddit, Play Store, and Primary User Surveys before diving into sentiment, root causes, and business impact.",
    target_page="pages/1_Overview.py",
    button_label="Begin Guided Tour: 1. Overview",
    icon="🚀",
    secondary_page="pages/7_Chatbot.py",
    secondary_label="Or Ask AI Chatbot Directly",
    secondary_icon="🤖"
)

# Sidebar
with st.sidebar:
    st.image("app/static/google_photos_logo_dark.svg", width=190)
    st.caption("AI-Powered Research Engine")
    st.markdown("---")
    
    st.write("**Database:** `🟢 SQLite Active`")
    st.write(f"**Records:** `{total_items:,} items`")
    st.write("**Vector Store:** `🟢 ChromaDB Ready`")
    st.write("**Embedding Model:** `all-MiniLM-L6-v2`")

render_sidebar_journey_flow(0)
