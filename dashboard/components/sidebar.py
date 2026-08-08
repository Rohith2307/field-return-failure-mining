"""
Premium Sidebar Navigation
"""

import streamlit as st


def render_sidebar():

    # --------------------------------------------------
    # Sidebar Branding
    # --------------------------------------------------

    st.sidebar.markdown(
        """
        <div class="if-sidebar-brand">
            <div class="if-brand-title">InsightForge AI</div>
            <div class="if-brand-subtitle">
                Failure Intelligence Platform
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        '<div class="if-sidebar-divider"></div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------
    # Navigation State
    # --------------------------------------------------

    pages = [
        ("⌂", "Dashboard"),
        ("↑", "Upload Dataset"),
        ("⚠", "Failure Analysis"),
        ("↗", "Trend Analytics"),
        ("✦", "AI Insights"),
        ("▣", "Engineering Report"),
    ]

    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "Dashboard"

    # --------------------------------------------------
    # Navigation Buttons
    # --------------------------------------------------

    for icon, page_name in pages:

        active = (
            st.session_state["active_page"]
            == page_name
        )

        button_label = f"{icon}   {page_name}   ›"

        if st.sidebar.button(
            button_label,
            key=f"nav_{page_name}",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            st.session_state["active_page"] = page_name
            st.rerun()

    # --------------------------------------------------
    # Return Current Page
    # --------------------------------------------------

    return st.session_state["active_page"]