"""
Intelligent UX Nudge and Guided Walkthrough Components.
Guides users through insights, takeaways, and cross-page narrative progression.
"""
import streamlit as st

def render_insight_cue(cue_text: str, badge: str = "KEY TAKEAWAY", show_toast: bool = True):
    """Render a prominent, pulsating insight cue banner below the page hero with pop-up notification."""
    # Trigger pop-up toast notification on initial page view
    if show_toast:
        toast_key = f"toast_seen_{abs(hash(cue_text))}"
        if toast_key not in st.session_state:
            st.session_state[toast_key] = True
            try:
                st.toast(f"💡 {cue_text}", icon="✨")
            except Exception:
                pass

    st.markdown(f"""
    <div class="gp-insight-cue">
        <div style="display: flex; align-items: center; gap: 0.85rem; flex-wrap: wrap;">
            <span class="gp-badge gp-badge-blue" style="font-size: 0.76rem; font-weight: 800; letter-spacing: 0.06em; padding: 0.35rem 0.8rem; text-transform: uppercase; display: inline-flex; align-items: center;">
                <span class="gp-blinking-dot"></span> 💡 {badge}
            </span>
            <span style="color: #f1f5f9; font-size: 1.02rem; line-height: 1.55; font-weight: 500;">
                {cue_text}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_next_step_nudge(
    headline: str,
    description: str,
    target_page: str,
    button_label: str,
    icon: str = "➡️",
    secondary_page: str = None,
    secondary_label: str = None,
    secondary_icon: str = "💬"
):
    """Render an actionable, pulsating next-best-step card at the bottom of the page to guide user flow."""
    st.markdown("<br><hr style='border: 0; border-top: 1px solid rgba(255, 255, 255, 0.1); margin: 2rem 0 1.5rem 0;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="gp-nudge-card">
        <span class="gp-badge gp-badge-green" style="font-weight: 800; font-size: 0.78rem; letter-spacing: 0.05em; padding: 0.3rem 0.75rem; display: inline-flex; align-items: center;">
            <span class="gp-blinking-dot-green"></span> 🧭 RECOMMENDED NEXT STEP IN DISCOVERY ARC
        </span>
        <div style="font-size: 1.28rem; font-weight: 800; color: #ffffff; margin-top: 0.65rem; margin-bottom: 0.45rem;">
            {headline}
        </div>
        <div style="color: #cbd5e1; font-size: 0.98rem; line-height: 1.6; margin-bottom: 1rem;">
            {description}
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1] if secondary_page else [1, 2])
    with c1:
        st.page_link(target_page, label=button_label, icon=icon, width="stretch")
    if secondary_page and secondary_label:
        with c2:
            st.page_link(secondary_page, label=secondary_label, icon=secondary_icon, width="stretch")

TOUR_PAGES = [
    {
        "index": 0,
        "name": "Main Portal",
        "path": "Main.py",
        "icon": "🏠",
        "title": "Executive Discovery Portal",
        "brief": "Executive briefing synthesizing 1,246 verified user feedback records, research taxonomy, and system telemetry."
    },
    {
        "index": 1,
        "name": "Overview",
        "path": "pages/1_Overview.py",
        "icon": "📊",
        "title": "Data Ingestion & Telemetry",
        "brief": "Multi-channel ingestion monitoring volume & platform splits across Play Store, Reddit, and Primary User Surveys."
    },
    {
        "index": 2,
        "name": "Sentiment",
        "path": "pages/2_Sentiment.py",
        "icon": "🎭",
        "title": "Emotional Friction & Frustration",
        "brief": "NLP emotional intensity analysis showing >65% frustration and psychological helplessness when known photos cannot be found."
    },
    {
        "index": 3,
        "name": "Issues",
        "path": "pages/3_Issues.py",
        "icon": "🏷️",
        "title": "Issue Classification & Funnel",
        "brief": "Survey-calibrated ranking of top search breakdowns: 'Missing Results' (21%) and 'Random Wrong Photos' (19.4%)."
    },
    {
        "index": 4,
        "name": "Themes",
        "path": "pages/4_Themes.py",
        "icon": "🧩",
        "title": "Mental Models: Stories vs. Keywords",
        "brief": "Deconstructs the core mental model gap: sensory narratives vs keyword retrieval, and the 45% manual scroll tax."
    },
    {
        "index": 5,
        "name": "KPI Tree",
        "path": "pages/5_KPI_Tree.py",
        "icon": "🌳",
        "title": "Business Metrics & Guardrails",
        "brief": "Interactive metric hierarchy mapping user search failure directly to Total Successful Searches, retry loops, and Search Success Rate."
    },
    {
        "index": 6,
        "name": "Survey",
        "path": "pages/6_Survey.py",
        "icon": "📋",
        "title": "70+ User Primary Research",
        "brief": "Primary Google Form survey validation confirming library sizes (1K-10K photos), dominant memory cues, and search abandonment."
    },
    {
        "index": 7,
        "name": "Chatbot",
        "path": "pages/7_Chatbot.py",
        "icon": "🤖",
        "title": "Conversational RAG Assistant",
        "brief": "Semantic RAG assistant grounded in ChromaDB vector citations with 4 clickable analytical libraries and custom Q&A."
    },
]

def render_sidebar_journey_flow(active_step: int = 0):
    """Render an interactive guided walkthrough tour pop-up speech bubble anchored right beside the active sidebar menu item."""
    cur_info = TOUR_PAGES[active_step if 0 <= active_step < len(TOUR_PAGES) else 0]
    total_steps = len(TOUR_PAGES)
    current_human_step = cur_info["index"] + 1

    if "show_guided_tour" not in st.session_state:
        st.session_state["show_guided_tour"] = True

    # Calculate exact vertical positioning for the pop-up speech bubble
    # Sidebar header logo + margin ~ 88px
    # Each sidebar nav item is ~43px high
    base_top = 88
    step_height = 43
    bubble_top = base_top + (cur_info["index"] * step_height)

    # Inject dynamic CSS positioning and speech-bubble arrow pointer
    st.markdown(f"""
    <style>
    div[class*="st-key-gp_tour_popup"] {{
        position: fixed !important;
        left: 345px !important;
        top: {bubble_top}px !important;
        width: 325px !important;
        background: #202124 !important;
        border: 1.5px solid #4285F4 !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.75), 0 0 24px rgba(66, 133, 244, 0.45) !important;
        z-index: 999999 !important;
        padding: 0.95rem 1.05rem !important;
        animation: gp-pop-in 0.35s cubic-bezier(0.16, 1, 0.3, 1), gp-pulse-blue-glow 3.5s infinite ease-in-out !important;
    }}

    /* Left-pointing speech bubble arrow directed at the active sidebar menu item */
    div[class*="st-key-gp_tour_popup"]::before {{
        content: "";
        position: absolute;
        left: -11px;
        top: 20px;
        width: 0;
        height: 0;
        border-top: 9px solid transparent;
        border-bottom: 9px solid transparent;
        border-right: 11px solid #4285F4;
    }}

    div[class*="st-key-gp_tour_popup"]::after {{
        content: "";
        position: absolute;
        left: -9px;
        top: 21px;
        width: 0;
        height: 0;
        border-top: 8px solid transparent;
        border-bottom: 8px solid transparent;
        border-right: 10px solid #202124;
    }}

    /* Highlight the currently active sidebar navigation item */
    [data-testid="stSidebarNav"] li:has([aria-current="page"]),
    [data-testid="stSidebarNav"] a[aria-current="page"] {{
        background: linear-gradient(90deg, rgba(66, 133, 244, 0.22) 0%, rgba(66, 133, 244, 0.08) 100%) !important;
        border-left: 4px solid #4285F4 !important;
        border-radius: 0 8px 8px 0 !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
    @media (max-width: 900px) {{
        div[class*="st-key-gp_tour_popup"] {{
            left: 16px !important;
            top: auto !important;
            bottom: 20px !important;
            width: calc(100vw - 32px) !important;
            max-width: 380px !important;
        }}
        div[class*="st-key-gp_tour_popup"]::before,
        div[class*="st-key-gp_tour_popup"]::after {{
            display: none !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

    # Bulletproof JS observer to hide the popup when Streamlit's sidebar collapses
    import streamlit.components.v1 as components
    components.html("""
    <script>
    function updatePopupVisibility() {
        try {
            var doc = window.parent.document;
            var sidebar = doc.querySelector('[data-testid="stSidebar"]');
            var popups = doc.querySelectorAll('div[class*="st-key-gp_tour_popup"]');
            
            if (sidebar && popups.length > 0) {
                // Streamlit sets aria-expanded="false" or changes width/transform when collapsed
                var isCollapsed = sidebar.getAttribute('aria-expanded') === 'false';
                var sidebarRect = sidebar.getBoundingClientRect();
                if (sidebarRect.width < 50 || sidebarRect.x < 0) {
                    isCollapsed = true;
                }
                
                popups.forEach(function(p) {
                    p.style.visibility = isCollapsed ? 'hidden' : 'visible';
                    p.style.opacity = isCollapsed ? '0' : '1';
                    p.style.pointerEvents = isCollapsed ? 'none' : 'auto';
                });
            }
        } catch (e) {}
    }
    
    // Run immediately and then observe DOM changes
    updatePopupVisibility();
    var observer = new MutationObserver(updatePopupVisibility);
    observer.observe(window.parent.document.body, {
        attributes: true, 
        subtree: true,
        attributeFilter: ['aria-expanded', 'style', 'class']
    });
    </script>
    """, height=0, width=0)

    # In the sidebar, provide a clean, unobtrusive toggle so users can re-open or dismiss
    with st.sidebar:
        # Render Floating Pop-up Bubble natively inside the sidebar DOM
        # This guarantees it disappears perfectly when the sidebar collapses because of CSS transforms
        if st.session_state.get("show_guided_tour", True):
            with st.container(key=f"gp_tour_popup_{active_step}"):
                col_b, col_x = st.columns([5, 1])
                with col_b:
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.2rem;">
                        <span class="gp-blinking-dot"></span>
                        <span style="font-size: 0.72rem; font-weight: 800; color: #8AB4F8; text-transform: uppercase; letter-spacing: 0.08em;">
                            🧭 Guided Tour • Step {current_human_step} of {total_steps}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                with col_x:
                    if st.button("✕", key=f"tour_close_btn_{active_step}", help="Dismiss guided tour popup"):
                        st.session_state["show_guided_tour"] = False
                        st.rerun()

                st.markdown(f"""
                <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.2rem; font-family: 'Google Sans', 'Product Sans', sans-serif;">
                    {cur_info['icon']} {cur_info['name']}
                </div>
                <div style="font-size: 0.78rem; font-weight: 600; color: #93C5FD; margin-bottom: 0.35rem;">
                    📌 {cur_info['title']}
                </div>
                <div style="font-size: 0.82rem; color: #E8EAED; line-height: 1.5; margin-bottom: 0.75rem;">
                    {cur_info['brief']}
                </div>
                """, unsafe_allow_html=True)

                prev_idx = cur_info["index"] - 1
                next_idx = cur_info["index"] + 1

                c_prev, c_next = st.columns([1, 1.4])
                with c_prev:
                    if prev_idx >= 0:
                        if st.button("◀ Back", key=f"tour_prev_{active_step}", width="stretch"):
                            st.switch_page(TOUR_PAGES[prev_idx]["path"])
                    else:
                        st.button("◀ Back", key=f"tour_prev_{active_step}", disabled=True, width="stretch")

                with c_next:
                    if next_idx < len(TOUR_PAGES):
                        next_target = TOUR_PAGES[next_idx]
                        if st.button(f"Next: {next_target['name']} ▶", key=f"tour_next_{active_step}", width="stretch", type="primary"):
                            st.switch_page(next_target["path"])
                    else:
                        if st.button("🔄 Restart Tour", key=f"tour_restart_{active_step}", width="stretch", type="primary"):
                            st.switch_page("Main.py")

        st.markdown("---")
        if st.session_state.get("show_guided_tour", True):
            c_sb1, c_sb2 = st.columns([3, 1.2])
            with c_sb1:
                st.markdown(f"""
                <div style="font-size: 0.76rem; color: #8AB4F8; font-weight: 700; display: flex; align-items: center; padding-top: 0.4rem;">
                    <span class="gp-blinking-dot"></span> Tour Active ({current_human_step}/{total_steps})
                </div>
                """, unsafe_allow_html=True)
            with c_sb2:
                if st.button("Hide", key=f"tour_hide_{active_step}", help="Hide guided tour popup"):
                    st.session_state["show_guided_tour"] = False
                    st.rerun()
        else:
            if st.button("🧭 Start Platform Tour", key=f"tour_resume_{active_step}", width="stretch", icon="✨"):
                st.session_state["show_guided_tour"] = True
                st.rerun()
