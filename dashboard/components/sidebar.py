"""
Sidebar Component
"""

import streamlit as st


def render_sidebar() -> str:
    """
    Render sidebar.

    Returns
    -------
    str
        Selected page.
    """

    with st.sidebar:

        st.title("InsightForge AI")

        st.caption(
            "Failure Intelligence Platform"
        )

        st.divider()

        page = st.radio(

            "Navigation",

            [

                "Dashboard",

                "Upload Dataset",

                "Failure Analysis",

                "Trend Analytics",

                "AI Insights",

                "Engineering Report",

            ],

        )

        return page