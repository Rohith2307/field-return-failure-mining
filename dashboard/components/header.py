"""
Header Component
"""

import streamlit as st


def render_header() -> None:
    """
    Render application header.
    """

    st.title("InsightForge AI")

    st.caption(
        "AI-powered Field Return Intelligence Platform"
    )

    st.divider()