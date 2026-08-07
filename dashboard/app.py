"""
Dashboard Application
"""

import streamlit as st

from dashboard.styles.css import load_css
from dashboard.components.header import render_header
from dashboard.components.sidebar import render_sidebar
from dashboard.pages.dashboard_page import render_dashboard
from dashboard.pages.upload_page import render_upload_page
from dashboard.pages.failure_analysis import render_failure_analysis
from dashboard.pages.trends_page import render_trends_page
from dashboard.pages.ai_page import render_ai_page


def run() -> None:
    """
    Launch the dashboard.
    """

    st.set_page_config(
        page_title="InsightForge AI",
        page_icon="🛠️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        load_css(),
        unsafe_allow_html=True,
    )

    page = render_sidebar()

    render_header()

    if page == "Dashboard":
        render_dashboard()

    elif page == "Upload Dataset":
        render_upload_page()

    elif page == "Failure Analysis":
        render_failure_analysis()

    elif page == "Trend Analytics":
        render_trends_page()

    elif page == "AI Insights":
        render_ai_page()

    else:
        st.info(f"{page} page is under development.")