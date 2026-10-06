"""
Streamlit Page 6: Primary User Research — Google Form Survey Analysis.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from app.components.styles import apply_custom_theme, render_hero
from app.components.nudges import render_insight_cue, render_next_step_nudge, render_sidebar_journey_flow

st.set_page_config(page_title="Survey Insights — Google Photos", page_icon="📋", layout="wide")
apply_custom_theme()

render_hero(
    title="📋 Primary Research: 70+ User Survey Deep-Dive",
    subtitle="Direct findings from authentic Google Form survey responses regarding photo library sizes, memory cues, and search abandonment.",
    badge_text="Primary Field Research"
)

render_sidebar_journey_flow(6)

render_insight_cue(
    "Primary survey of 70+ users validates high-friction search reality: 45% abandon search for manual scrolling, "
    "and 75% have never attempted video search due to zero discoverability."
)

survey_path = Path("data/survey_responses.tsv")
if not survey_path.exists():
    survey_path = Path("data/survey_responses.csv")

if survey_path.exists():
    sep = "\t" if str(survey_path).endswith(".tsv") else ","
    df = pd.read_csv(survey_path, sep=sep, on_bad_lines="skip")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="gp-metric-card">
            <div class="gp-metric-label">Survey Sample Size</div>
            <div class="gp-metric-value">{len(df)}</div>
            <div class="gp-metric-sub">👥 Verified Photo Users</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="gp-metric-card">
            <div class="gp-metric-label">Dominant Library Size</div>
            <div class="gp-metric-value" style="font-size: 1.5rem;">1K to 10K</div>
            <div class="gp-metric-sub">📁 High-Volume Archives</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="gp-metric-card">
            <div class="gp-metric-label">Search Abandonment</div>
            <div class="gp-metric-value" style="color: #dc2626;">45%</div>
            <div class="gp-metric-sub" style="color: #dc2626;">⚠️ Fall Back to Timeline Scroll</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 Photo Library Size")
        if df.shape[1] > 2:
            size_counts = df.iloc[:, 2].value_counts()
            fig_size = px.pie(
                names=size_counts.index,
                values=size_counts.values,
                hole=0.45,
                color_discrete_sequence=["#4285F4", "#34A853", "#FBBC05", "#EA4335"]
            )
            fig_size.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#202124', width=2)))
            fig_size.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_family="Google Sans, Roboto, sans-serif",
                height=340,
                margin=dict(t=10, b=10, l=10, r=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_size, use_container_width=True)

    with col2:
        st.subheader("⏱️ Usage Frequency")
        if df.shape[1] > 1:
            freq_counts = df.iloc[:, 1].value_counts()
            fig_freq = px.bar(
                x=freq_counts.index,
                y=freq_counts.values,
                labels={"x": "Frequency", "y": "Respondents"},
                color=freq_counts.index,
                color_discrete_sequence=["#4285F4", "#34A853", "#FBBC05", "#9AA0A6"],
                text=freq_counts.values
            )
            fig_freq.update_traces(textposition='outside')
            fig_freq.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_family="Google Sans, Roboto, sans-serif",
                showlegend=False,
                height=340,
                margin=dict(t=10, b=10, l=10, r=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
            )
            st.plotly_chart(fig_freq, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🧠 Memory Cues: What Comes to Mind First?")
        if df.shape[1] > 4:
            cues = df.iloc[:, 4].dropna().str.split(",").explode().str.strip().value_counts()
            fig_cues = px.bar(
                x=cues.values,
                y=cues.index,
                orientation="h",
                labels={"x": "Mentions", "y": "Memory Cue"},
                color=cues.values,
                color_continuous_scale=["#8AB4F8", "#4285F4", "#1A73E8"],
                text=cues.values
            )
            fig_cues.update_traces(textposition='inside', textfont=dict(color='white'))
            fig_cues.update_layout(
                yaxis=dict(autorange="reversed"),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_family="Google Sans, Roboto, sans-serif",
                coloraxis_showscale=False,
                height=360,
                margin=dict(t=10, b=10, l=10, r=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
                yaxis_gridcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_cues, use_container_width=True)

    with col4:
        st.subheader("🔍 Reported Struggles (Question 6)")
        if df.shape[1] > 6:
            struggles = df.iloc[:, 6].dropna().str.split(",").explode().str.strip().value_counts()
            fig_strug = px.bar(
                x=struggles.values,
                y=struggles.index,
                orientation="h",
                labels={"x": "Mentions", "y": "Search Problem"},
                color=struggles.values,
                color_continuous_scale=["#F28B82", "#EA4335", "#C5221F"],
                text=struggles.values
            )
            fig_strug.update_traces(textposition='inside', textfont=dict(color='white'))
            fig_strug.update_layout(
                yaxis=dict(autorange="reversed"),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_family="Google Sans, Roboto, sans-serif",
                coloraxis_showscale=False,
                height=360,
                margin=dict(t=10, b=10, l=10, r=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
                yaxis_gridcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_strug, use_container_width=True)

    st.divider()

    st.subheader("💬 User Anecdotes: \"Last Time I Couldn't Find a Photo\"")
    if df.shape[1] > 14:
        anecdotes = df.iloc[:, 14].dropna()
        q_cols = st.columns(2)
        valid_count = 0
        for story in anecdotes:
            story_str = str(story).strip()
            if len(story_str) > 20 and story_str not in ("NA", "N/A", "None", "No"):
                col = q_cols[valid_count % 2]
                with col:
                    st.markdown(f"""
                    <div class="gp-quote-card">
                        "{story_str}"
                        <div class="gp-quote-author">📌 Survey Respondent #{valid_count + 1}</div>
                    </div>
                    """, unsafe_allow_html=True)
                valid_count += 1
                if valid_count >= 6:
                    break

    render_next_step_nudge(
        headline="Interrogate Feedback Directly with the AI Chatbot",
        description="Ask complex strategic questions, test hypotheses, and verify citations grounded in 1,246 real user reviews and survey data.",
        target_page="pages/7_Chatbot.py",
        button_label="Final Step: 7. Interactive Discovery Chatbot",
        icon="🤖"
    )
else:
    st.warning("Survey responses file not found in data/ directory.")
