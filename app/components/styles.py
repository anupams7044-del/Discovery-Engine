"""
Theme and custom styling utility for Google Photos AI Discovery Engine.
Injects cohesive Google Material 3 styling and component builders across all pages.
"""
import streamlit as st
from pathlib import Path

def get_google_photos_icon_svg(size: int = 36) -> str:
    """Return inline SVG of official Google Photos pinwheel logo with mandated clear space."""
    return f'''<span style="display: inline-flex; align-items: center; justify-content: center; padding: 4px; margin-right: 2px;">
        <svg width="{size}" height="{size}" viewBox="0 0 59 59" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <path d="M14.75 13.41c8.146 0 14.75 6.603 14.75 14.75v1.34H1.34C.6 29.5 0 28.9 0 28.16c0-8.147 6.604-14.75 14.75-14.75z" fill="#FBBC05"/>
            <path d="M45.59 14.75c0 8.146-6.603 14.75-14.75 14.75H29.5V1.34C29.5.6 30.1 0 30.84 0c8.147 0 14.75 6.604 14.75 14.75z" fill="#EA4335"/>
            <path d="M44.25 45.59c-8.146 0-14.75-6.603-14.75-14.75V29.5h28.16c.74 0 1.34.6 1.34 1.34 0 8.147-6.604 14.75-14.75 14.75z" fill="#4285F4"/>
            <path d="M13.41 44.25c0-8.146 6.603-14.75 14.75-14.75h1.34v28.16c0 .74-.6 1.34-1.34 1.34-8.147 0-14.75-6.604-14.75-14.75z" fill="#34A853"/>
        </svg>
    </span>'''

def apply_custom_theme():
    """Inject global CSS into the Streamlit application and configure dark theme and Google Photos logo."""
    try:
        import plotly.io as pio
        google_dark = pio.templates["plotly_dark"]
        google_dark.layout.colorway = ["#4285F4", "#EA4335", "#FBBC05", "#34A853", "#8AB4F8", "#F28B82"]
        google_dark.layout.font.family = "Google Sans, Product Sans, Roboto, sans-serif"
        google_dark.layout.paper_bgcolor = "rgba(0,0,0,0)"
        google_dark.layout.plot_bgcolor = "rgba(0,0,0,0)"
        pio.templates.default = "plotly_dark"
    except Exception:
        pass

    # Global Google Photos Logo in sidebar & header
    logo_path = Path("app/static/google_photos_logo_dark.svg")
    icon_path = Path("app/static/google_photos_icon.svg")
    if logo_path.exists():
        try:
            st.logo(str(logo_path), icon_image=str(icon_path) if icon_path.exists() else None, size="large")
        except Exception:
            pass

    css_path = Path("app/static/styles.css")
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_accent_bar():
    """Render the Google Photos 4-color gradient bar."""
    st.markdown('<div class="gp-accent-bar"></div>', unsafe_allow_html=True)

def render_hero(title: str, subtitle: str, badge_text: str = "NextLeap Fellowship"):
    """Render an executive dark hero section with Google Photos logo."""
    render_accent_bar()
    icon_svg = get_google_photos_icon_svg(36)
    st.markdown(f"""
    <div class="gp-hero-card">
        <div style="display: flex; align-items: center; gap: 0.65rem; margin-bottom: 0.85rem;">
            {icon_svg}
            <span class="gp-badge gp-badge-blue">{badge_text}</span>
        </div>
        <div class="gp-hero-title">{title}</div>
        <div class="gp-hero-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(label: str, value: str, sub: str = "", badge: str = "Live"):
    """Render a styled metric card."""
    sub_html = f'<div class="gp-metric-sub">{sub}</div>' if sub else ""
    return f"""
    <div class="gp-metric-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div class="gp-metric-label">{label}</div>
            <span class="gp-badge gp-badge-blue">{badge}</span>
        </div>
        <div class="gp-metric-value">{value}</div>
        {sub_html}
    </div>
    """

def render_quote(text: str, source: str, author: str = ""):
    """Render a stylized quote callout card."""
    author_txt = f" — {author}" if author else ""
    st.markdown(f"""
    <div class="gp-quote-card">
        "{text}"
        <div class="gp-quote-author">📌 [{source.upper()}]{author_txt}</div>
    </div>
    """, unsafe_allow_html=True)
