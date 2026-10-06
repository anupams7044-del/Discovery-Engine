"""
Streamlit Page 7: Conversational RAG Chatbot with Clickable Questions Library & Citations.
"""
import streamlit as st
from chatbot.rag_pipeline import ChatbotRAG
from app.components.styles import apply_custom_theme, render_hero
from app.components.nudges import render_insight_cue, render_sidebar_journey_flow

st.set_page_config(page_title="AI Chatbot — Google Photos", page_icon="🤖", layout="wide")
apply_custom_theme()

render_hero(
    title="🤖 Conversational Discovery Assistant",
    subtitle="Semantic Q&A engine powered by ChromaDB vector search and multi-channel feedback intelligence.",
    badge_text="RAG Intelligence Assistant"
)

render_sidebar_journey_flow(7)

render_insight_cue(
    "Grounding Engine Active: Directly query 1,246 real user feedback entries and survey findings. "
    "Use the 4 category tabs below for quick analysis or ask custom strategic questions in the chat box."
)

# Initialize RAG chatbot
if "rag_bot" not in st.session_state:
    st.session_state.rag_bot = ChatbotRAG()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Hello!** I am your **Google Photos Search Discovery Assistant**.\n\n"
                "I have direct semantic access to **1,246 real user feedback entries** across Play Store, Reddit, and Primary User Surveys.\n\n"
                "Click any question below or type your own in the chat input to generate an evidence-grounded answer!"
            ),
            "sources": []
        }
    ]

def ask_question(q_text: str):
    """Submit a question and generate response with citations."""
    st.session_state.messages.append({"role": "user", "content": q_text, "sources": []})
    with st.spinner("Analyzing question & retrieving evidence..."):
        res = st.session_state.rag_bot.answer(q_text, st.session_state.messages[:-1])
    st.session_state.messages.append({
        "role": "assistant",
        "content": res["answer"],
        "sources": res.get("sources", []),
    })
    st.session_state["scroll_to_answer"] = True
    st.rerun()

# Clickable Questions Library Section
st.markdown("### 💬 Clickable Questions Library")
st.caption("Click any question below to immediately generate an analytical, data-grounded answer:")

tab_metrics, tab_issues, tab_behavior, tab_solutions = st.tabs([
    "📊 Discovery Metrics",
    "🔍 Search Failures",
    "🧠 User Behavior & Survey",
    "💡 Solutions & Roadmap"
])

with tab_metrics:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 How many reviews were analyzed in total?", key="btn_m1", use_container_width=True):
            ask_question("How many reviews were analyzed in total?")
        if st.button("🎭 What's the overall sentiment towards search?", key="btn_m2", use_container_width=True):
            ask_question("What's the overall sentiment towards search?")
        if st.button("⭐ What is the most common search complaint?", key="btn_m3", use_container_width=True):
            ask_question("What is the most common search complaint?")
    with col2:
        if st.button("📉 What percentage of complaints impact Search Success Rate?", key="btn_m4", use_container_width=True):
            ask_question("What percentage of complaints impact the Search Success Rate?")
        if st.button("🏷️ What are the top 3 discovered issues across the dataset?", key="btn_m5", use_container_width=True):
            ask_question("What are the top 3 discovered issues across the dataset?")

with tab_issues:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Why do search results miss known photos in the library?", key="btn_i1", use_container_width=True):
            ask_question("Why do search results miss known photos that exist in the library?")
        if st.button("🎯 Why do users get random wrong photos when searching?", key="btn_i2", use_container_width=True):
            ask_question("Why do users get random wrong photos when searching?")
        if st.button("👥 What do users say about face recognition search?", key="btn_i3", use_container_width=True):
            ask_question("What do users say about face recognition search?")
        if st.button("📅 Why does searching by date or year fail?", key="btn_i4", use_container_width=True):
            ask_question("Why does searching by date or year fail?")
    with col2:
        if st.button("📍 What problems occur with location and place search?", key="btn_i5", use_container_width=True):
            ask_question("What problems occur with location and place search?")
        if st.button("🏷️ What are the limitations of search filters and sorting?", key="btn_i6", use_container_width=True):
            ask_question("What are the limitations of search filters and sorting?")
        if st.button("🎬 Why has almost nobody used video search in Google Photos?", key="btn_i7", use_container_width=True):
            ask_question("Why has almost nobody used video search in Google Photos?")

with tab_behavior:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚶 Why do users give up and scroll manually?", key="btn_b1", use_container_width=True):
            ask_question("Why do users give up and scroll manually?")
        if st.button("🧠 What is the 'Stories vs Keywords' mental model paradox?", key="btn_b2", use_container_width=True):
            ask_question("What is the 'Stories vs Keywords' mental model paradox?")
        if st.button("📋 What did the primary survey find about user search habits?", key="btn_b3", use_container_width=True):
            ask_question("What did the primary survey find about user search habits?")
    with col2:
        if st.button("💭 What are the top memory cues users remember first?", key="btn_b4", use_container_width=True):
            ask_question("What are the top memory cues users remember first?")
        if st.button("🌳 How does search friction impact the KPI Tree?", key="btn_b5", use_container_width=True):
            ask_question("How does search friction impact the KPI Tree?")

with tab_solutions:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💡 What are the recommended product solutions to fix search?", key="btn_s1", use_container_width=True):
            ask_question("What are the recommended product solutions to fix search?")
        if st.button("🤖 How would Conversational Disambiguation help Google Photos?", key="btn_s2", use_container_width=True):
            ask_question("How would Conversational Disambiguation help Google Photos search?")
    with col2:
        if st.button("💊 How would Dynamic Filter Pills improve multi-entity search?", key="btn_s3", use_container_width=True):
            ask_question("How would Dynamic Filter Pills improve multi-entity search?")
        if st.button("🏷️ How would Match Transparency Notes rebuild user trust?", key="btn_s4", use_container_width=True):
            ask_question("How would Match Transparency Notes rebuild user trust?")

st.markdown("---")

# Sidebar with quick prompts and reset
with st.sidebar:
    st.markdown("### 💡 Quick Click Prompts")
    quick_prompts = [
        "What is the most common search complaint?",
        "Why do search results miss known photos?",
        "Why do users give up and scroll manually?",
        "What do users say about face recognition search?",
        "How many reviews were analyzed in total?",
        "What are the recommended product solutions?",
    ]
    for q in quick_prompts:
        if st.button(q, key=f"side_{hash(q)}", use_container_width=True):
            ask_question(q)

    st.markdown("---")
    if st.button("🗑️ Reset Chat History", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "👋 **Hello!** I am your **Google Photos Search Discovery Assistant**.\n\n"
                    "I have direct semantic access to **1,246 real user feedback entries** across Play Store, Reddit, and Primary User Surveys.\n\n"
                    "Click any question above or type your own in the chat input to generate an evidence-grounded answer!"
                ),
                "sources": []
            }
        ]
        st.rerun()

# Direct "Sample Query" Sandbox
st.markdown("### 🧪 Direct 'Sample Query' Sandbox")
st.caption("Select a real-world failed user query to instantly simulate its root cause, KPI impact, and proposed AI fix.")

def trigger_sandbox_query():
    sq = st.session_state.sandbox_dropdown
    if sq == "Select an authentic failed query to analyze...":
        return
    
    # Map query to structured analysis
    cards = {
        '"Yellow dress in Goa"': (
            "**🔍 Failure Reason:** The Multi-Entity Wall. The engine correctly identified 'Goa' (location) but failed to intersect it with 'yellow dress' (color/object), returning a massive dump of all Goa photos.\n\n"
            "**📉 KPI Impacted:** *Search Friction (Retry Loops).* The user abandons search and manually scrolls through hundreds of vacation photos.\n\n"
            "**💡 Recommended AI Fix:** *Conversational Disambiguation.* Prompt: 'Did you mean your 2021 or 2023 Goa trip?' combined with *Dynamic Filter Pills* to isolate [Yellow] + [Dress]."
        ),
        '"Car insurance document"': (
            "**🔍 Failure Reason:** Semantic OCR Mismatch. The system searches for visual cars instead of recognizing a photographed piece of paper as a 'document' containing the word 'insurance'.\n\n"
            "**📉 KPI Impacted:** *Search Success Rate (Task Abandonment).* Users urgently need a document and lose trust when a smart gallery cannot retrieve it.\n\n"
            "**💡 Recommended AI Fix:** *Match Transparency Notes.* Label the result with 'Matched text: Car Insurance' to reassure the user why a seemingly random document was surfaced."
        ),
        '"Dog playing in snow"': (
            "**🔍 Failure Reason:** Action/Context Failure. The engine finds 'dog' and 'snow' independently but fails to understand the action ('playing'). It returns static photos of dogs and separate photos of snowy landscapes.\n\n"
            "**📉 KPI Impacted:** *Search Accuracy (Irrelevant Wrong Photos).* Precision degrades drastically on multi-modal action queries.\n\n"
            "**💡 Recommended AI Fix:** *The 2x2 Visual Choice Grid.* Project the query into 4 distinct centroids: [Dog in snow], [Dog inside], [Snowy mountains], [Skiing]. One tap resolves the visual ambiguity instantly."
        )
    }
    
    if sq in cards:
        st.session_state.messages.append({"role": "user", "content": f"Simulate Failed Query: {sq}", "sources": []})
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"### 🧪 Sandbox Simulation\n\n{cards[sq]}",
            "sources": []
        })
        st.session_state["scroll_to_answer"] = True
    
    # Reset dropdown
    st.session_state.sandbox_dropdown = "Select an authentic failed query to analyze..."

# Setup selectbox with callback
sandbox_options = [
    "Select an authentic failed query to analyze...",
    '"Yellow dress in Goa"',
    '"Car insurance document"',
    '"Dog playing in snow"'
]

if "sandbox_dropdown" not in st.session_state:
    st.session_state.sandbox_dropdown = sandbox_options[0]

st.selectbox(
    "Simulate Failed User Query:",
    sandbox_options,
    key="sandbox_dropdown",
    on_change=trigger_sandbox_query,
    label_visibility="collapsed"
)

st.markdown("---")

# Display chat message history
st.markdown("### 🗨️ Conversation Stream")

total_msgs = len(st.session_state.messages)
for idx, msg in enumerate(st.session_state.messages):
    # Anchor immediately above the latest assistant answer
    if idx == total_msgs - 1 and msg["role"] == "assistant" and total_msgs > 1:
        st.markdown('<div id="latest-answer" style="scroll-margin-top: 100px; height: 1px;"></div>', unsafe_allow_html=True)
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander(f"📚 Retrieved Evidence & Citations ({len(msg['sources'])} sources)"):
                for s in msg["sources"]:
                    st.markdown(f"""
                    <div class="gp-citation-box">
                        <strong>📌 {s.get('platform', 'Database')}</strong>: <em>"{s.get('snippet', '')}"</em>
                    </div>
                    """, unsafe_allow_html=True)

# Auto-scroll execution when triggered
if st.session_state.get("scroll_to_answer", False):
    import streamlit.components.v1 as components
    components.html(
        """
        <script>
        function doScroll() {
            try {
                var doc = window.parent.document;
                var target = doc.getElementById('latest-answer');
                if (!target) {
                    var msgs = doc.querySelectorAll('[data-testid="stChatMessage"]');
                    if (msgs.length > 0) {
                        target = msgs[msgs.length - 1];
                    }
                }
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            } catch (err) {
                console.log("Auto-scroll error:", err);
            }
        }
        setTimeout(doScroll, 80);
        setTimeout(doScroll, 250);
        setTimeout(doScroll, 500);
        </script>
        """,
        height=0,
        width=0
    )
    st.session_state["scroll_to_answer"] = False

# Chat input for custom questions
if user_input := st.chat_input("Ask any custom question about Google Photos search feedback..."):
    ask_question(user_input)
