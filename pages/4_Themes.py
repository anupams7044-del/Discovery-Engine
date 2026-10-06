"""
Streamlit Page 4: Recurring Themes & Pattern Analysis.
"""
import streamlit as st
import plotly.express as px
from app.components.styles import apply_custom_theme, render_hero
from app.components.nudges import render_insight_cue, render_next_step_nudge, render_sidebar_journey_flow

st.set_page_config(page_title="Themes & Patterns — Google Photos", page_icon="🎯", layout="wide")
apply_custom_theme()

render_hero(
    title="🎯 Strategic Themes: Mental Model Conflicts",
    subtitle="Deconstructing the core behavioral misalignment between user memory cues and keyword-based retrieval.",
    badge_text="Strategic Synthesis"
)

render_sidebar_journey_flow(4)

render_insight_cue(
    "The Multi-Entity Wall: Combining Person + Location + Year triggers sharp precision drop-offs, "
    "forcing 45% of users to abandon search and endure the 'Manual Scroll Tax'."
)

st.markdown("""
<div class="gp-note-box">
    <h3 style="margin-top: 0; color: #60a5fa; font-weight: 800;">🧠 The Core Paradox: Stories vs. Keywords</h3>
    <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.6; margin-bottom: 0;">
        Users remember their lives in <strong>sensory narratives</strong>: <em>"That evening in Goa when Mom wore a yellow saree."</em>
        In contrast, search algorithms expect exact isolated terms. When users combine person + place + time into a single query, 
        the retrieval engine frequently returns empty results or hundreds of unrelated photos.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="gp-metric-card" style="border-top: 4px solid #ea4335;">
        <div class="gp-metric-label">Pattern #1</div>
        <div style="font-size: 1.2rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.5rem;">The Multi-Entity Wall</div>
        <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.5;">
            Searching for single entities (e.g. <em>"dog"</em> or <em>"beach"</em>) works well, but multi-entity queries 
            (<em>"Mom and Dad at the beach"</em>) cause severe precision degradation.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="gp-metric-card" style="border-top: 4px solid #fbbc04;">
        <div class="gp-metric-label">Pattern #2</div>
        <div style="font-size: 1.2rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.5rem;">The Manual Scroll Tax</div>
        <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.5;">
            <strong>45% of surveyed users</strong> immediately abandon search upon encountering a failure and scroll manually, 
            turning a 10-second lookup into a tedious multi-minute browsing session.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="gp-metric-card" style="border-top: 4px solid #34a853;">
        <div class="gp-metric-label">Pattern #3</div>
        <div style="font-size: 1.2rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.5rem;">Underutilized Modalities</div>
        <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.5;">
            Over <strong>75% of users have never tried video search</strong>. Video retrieval has zero discoverability, 
            and users assume spoken lines or moments cannot be found.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🔍 Breakdown of Search Failure Modes")

stages_data = {
    "Retrieval / Missing Known Photos": 65,
    "Ranking / Irrelevant Wrong Photos": 60,
    "Refinement / No Easy Way to Narrow Down": 60,
    "Understanding / Multi-Entity Failure": 61,
    "Query Formulation / Vague Expressions": 64,
}

fig_stages = px.bar(
    x=list(stages_data.values()),
    y=list(stages_data.keys()),
    orientation="h",
    labels={"x": "Incidents Analyzed", "y": "Failure Mode"},
    color=list(stages_data.keys()),
    color_discrete_sequence=["#EA4335", "#FBBC05", "#4285F4", "#34A853", "#8AB4F8"],
    text=list(stages_data.values())
)
fig_stages.update_traces(textposition='inside', textfont=dict(color='white'))
fig_stages.update_layout(
    yaxis=dict(autorange="reversed"),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_family="Google Sans, Roboto, sans-serif",
    showlegend=False,
    height=320,
    margin=dict(t=10, b=10, l=10, r=10),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
    yaxis_gridcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_stages, use_container_width=True)

st.divider()

st.subheader("💡 Proposed Solution: The 2x2 Visual Choice Grid")
st.markdown("""
<div style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.6; margin-bottom: 1.5rem;">
    <strong>The Problem:</strong> When users enter ambiguous queries (like <em>"vacation"</em>), standard algorithms return a flat, homogeneous list. 
    If the top results latch onto the wrong event, the search stalls. Users are forced to either scroll endlessly or struggle to rephrase their query, 
    leading to search abandonment. <br><br>
    <strong>The Solution:</strong> Replace linear scrolling with an active, visual refinement loop natively integrated into the search interface. 
    Using on-the-fly vector clustering ($K=4$), the engine extracts the four most mathematically distinct visual themes from the candidate pool and presents them in a rapid, tap-friendly 2x2 matrix.
</div>
""", unsafe_allow_html=True)

# Interactive Before vs After Solution Playground
tab_before, tab_after = st.tabs(["❌ Current Google Photos (Before)", "✅ Proposed 2x2 Visual Grid (After)"])

with tab_before:
    st.markdown("""
<div style="background-color: #17181A; border: 1px solid #3C4043; border-radius: 12px; padding: 2rem; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 300px;">
    <div style="background-color: #202124; padding: 0.8rem 1.5rem; border-radius: 24px; color: #E8EAED; font-size: 1.1rem; width: 60%; max-width: 400px; display: flex; align-items: center; gap: 10px; margin-bottom: 2rem; border: 1px solid #3C4043;">
        🔍 vacation
    </div>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; width: 60%; max-width: 400px; opacity: 0.7;">
        <div style="background-color: #2D2F31; aspect-ratio: 1; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; color: #9AA0A6;">Beach 1</div>
        <div style="background-color: #2D2F31; aspect-ratio: 1; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; color: #9AA0A6;">Beach 2</div>
        <div style="background-color: #2D2F31; aspect-ratio: 1; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; color: #9AA0A6;">Beach 3</div>
        <div style="background-color: #2D2F31; aspect-ratio: 1; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; color: #9AA0A6;">Beach 4</div>
        <div style="background-color: #2D2F31; aspect-ratio: 1; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; color: #9AA0A6;">Beach 5</div>
        <div style="background-color: #2D2F31; aspect-ratio: 1; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; color: #9AA0A6;">Beach 6</div>
    </div>
    <div style="margin-top: 2rem; text-align: center; color: #F28B82; font-size: 0.95rem;">
        ⚠️ <strong>Failure Mode:</strong> The algorithm incorrectly assumed "vacation" meant the beach trip. The user actually wanted their mountain trip. They are now trapped in a homogeneous feed and forced to manually scroll past 400 beach photos.
    </div>
</div>
""", unsafe_allow_html=True)

with tab_after:
    st.markdown("""
<div style="background-color: #17181A; border: 1px solid #4285F4; border-radius: 12px; padding: 2rem; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 300px; position: relative;">
<div style="background-color: #202124; padding: 0.8rem 1.5rem; border-radius: 24px; color: #E8EAED; font-size: 1.1rem; width: 60%; max-width: 400px; display: flex; align-items: center; gap: 10px; margin-bottom: 1rem; border: 1px solid #4285F4; box-shadow: 0 0 10px rgba(66, 133, 244, 0.2);">
🔍 vacation
</div>
<div style="color: #8AB4F8; font-weight: 600; margin-bottom: 1rem; font-size: 0.95rem;">
✨ Which fits your memory?
</div>
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; width: 60%; max-width: 350px; margin-bottom: 1rem;">
<button style="background: linear-gradient(135deg, rgba(66,133,244,0.1), rgba(66,133,244,0.05)); border: 1.5px solid #4285F4; border-radius: 12px; aspect-ratio: 4/3; color: #E8EAED; font-weight: 600; cursor: pointer; display:flex; flex-direction:column; align-items:center; justify-content:center; gap: 5px; transition: all 0.2s;">
<span style="font-size: 1.5rem;">🏖️</span> Beach
</button>
<button style="background: linear-gradient(135deg, rgba(52,168,83,0.1), rgba(52,168,83,0.05)); border: 1.5px solid #34A853; border-radius: 12px; aspect-ratio: 4/3; color: #E8EAED; font-weight: 600; cursor: pointer; display:flex; flex-direction:column; align-items:center; justify-content:center; gap: 5px; transition: all 0.2s;">
<span style="font-size: 1.5rem;">🏔️</span> Mountains
</button>
<button style="background: linear-gradient(135deg, rgba(251,188,5,0.1), rgba(251,188,5,0.05)); border: 1.5px solid #FBBC05; border-radius: 12px; aspect-ratio: 4/3; color: #E8EAED; font-weight: 600; cursor: pointer; display:flex; flex-direction:column; align-items:center; justify-content:center; gap: 5px; transition: all 0.2s;">
<span style="font-size: 1.5rem;">🌆</span> City Walk
</button>
<button style="background: linear-gradient(135deg, rgba(234,67,53,0.1), rgba(234,67,53,0.05)); border: 1.5px solid #EA4335; border-radius: 12px; aspect-ratio: 4/3; color: #E8EAED; font-weight: 600; cursor: pointer; display:flex; flex-direction:column; align-items:center; justify-content:center; gap: 5px; transition: all 0.2s;">
<span style="font-size: 1.5rem;">🍽️</span> Home Meal
</button>
</div>
<button style="background-color: #2D2F31; border: 1px solid #3C4043; border-radius: 20px; padding: 0.5rem 1rem; color: #9AA0A6; font-size: 0.85rem; cursor: pointer; transition: all 0.2s;">
🔄 None of these (Show others)
</button>
<div style="margin-top: 1.5rem; text-align: center; color: #81C995; font-size: 0.95rem;">
✅ <strong>Zero Conversational Overhead:</strong> Users process these 4 contrasting visual centroids in under 100 milliseconds. One tap refines the context seamlessly, eliminating doom-scrolling entirely.
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

with st.expander("🛠️ Core Mechanics & Technical Architecture", expanded=False):
    st.markdown("""
    - **Candidate Pool Retrieval:** A vague text query ("vacation") is mapped into a multimodal vector space, instantly pulling top 60-100 embeddings.
    - **On-the-Fly Vector Clustering ($K=4$):** Instead of showing the 4 nearest sequential neighbors (which often look identical), a fast K-Means algorithm isolates four statistically distinct visual/contextual themes.
    - **Centroid Representative Selection:** The engine displays the mathematical center of each cluster, ensuring maximum visual contrast across the 2x2 grid.
    - **The "Hot or Cold" Dynamic Pivot:** Clicking "None of these" applies a negative vector weight to the rejected centroids. The backend recalculates the remaining pool and surfaces four completely fresh visual directions—turning a search failure into an intuitive process of elimination.
    """)

render_next_step_nudge(
    headline="Deconstruct Business Impact with the KPI Tree",
    description="Translate user abandonment and retry loops into top-level business formulas, friction indicators, and guardrail metrics.",
    target_page="pages/5_KPI_Tree.py",
    button_label="Next Step: 5. KPI Tree Decomposition",
    icon="🌳"
)
