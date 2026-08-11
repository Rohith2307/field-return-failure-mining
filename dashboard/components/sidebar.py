"""
InsightForge AI — Sidebar Navigation
"""
import streamlit as st
def render_sidebar() -> str:
    """Render the InsightForge AI sidebar and return the active page."""
    # --------------------------------------------------
    # Sidebar Branding
    # --------------------------------------------------
    st.sidebar.markdown(
        '<div class="if-sidebar-brand">'
        '<div class="if-brand-mark">◆</div>'
        '<div class="if-brand-content">'
        '<div class="if-brand-title">Insight<span>Forge</span><sup>AI</sup></div>'
        '<div class="if-brand-subtitle">Failure Intelligence Platform</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    # --------------------------------------------------
    # Navigation
    # --------------------------------------------------
    pages = [
        ("⌂", "Dashboard"),
        ("↑", "Upload Dataset"),
        ("⚠", "Failure Analysis"),
        ("↗", "Trend Analytics"),
        ("💥", "Blast Radius"),
        ("✦", "AI Insights"),
        ("▣", "Engineering Report"),
    ]
    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "Dashboard"
    for icon, page_name in pages:
        active = st.session_state["active_page"] == page_name
        button_label = f"{icon}    {page_name}    ›"
        if st.sidebar.button(
            button_label,
            key=f"nav_{page_name}",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            st.session_state["active_page"] = page_name
            st.rerun()
    # --------------------------------------------------
    # Sidebar Bottom Controls
    # --------------------------------------------------
    st.sidebar.markdown(
        '<div class="if-sidebar-spacer"></div>',
        unsafe_allow_html=True,
    )

    if "cost_per_unit" not in st.session_state:
        st.session_state["cost_per_unit"] = 2500

    cost_per_unit = st.sidebar.number_input(
        "Avg. Cost per Failure (₹)",
        min_value=0,
        value=st.session_state["cost_per_unit"],
        step=100,
    )

    st.session_state["cost_per_unit"] = cost_per_unit

    if "light_mode" not in st.session_state:
        st.session_state["light_mode"] = False
    light_mode = st.sidebar.toggle(
        "Light Mode",
        value=st.session_state["light_mode"],
        key="light_mode_toggle",
    )
    if light_mode != st.session_state["light_mode"]:
        st.session_state["light_mode"] = light_mode
        st.rerun()
    # --------------------------------------------------
    # Footer
    # --------------------------------------------------
    st.sidebar.markdown(
        """
<div class="if-sidebar-footer">
    <div>InsightForge AI © 2026</div>
    <div>All rights reserved.</div>
</div>
        """,
        unsafe_allow_html=True,
    )
    return st.session_state["active_page"]