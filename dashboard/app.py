"""
Dashboard Application
"""

import streamlit as st

from dashboard.styles.css import load_css
from dashboard.components.sidebar import render_sidebar
from dashboard.pages.dashboard_page import render_dashboard
from dashboard.pages.upload_page import render_upload_page
from dashboard.pages.failure_analysis import render_failure_analysis
from dashboard.pages.trends_page import render_trends_page
from dashboard.pages.blast_radius_page import render_blast_radius_page
from dashboard.pages.ai_page import render_ai_page
from dashboard.pages.report_page import render_report_page


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

    if page == "Dashboard":
        render_dashboard()

    elif page == "Upload Dataset":
        render_upload_page()

    elif page == "Failure Analysis":
        render_failure_analysis()

    elif page == "Trend Analytics":
        render_trends_page()

    elif page == "Blast Radius":
        render_blast_radius_page()

    elif page == "AI Insights":
        render_ai_page()

    elif page == "Engineering Report":
        render_report_page()

    else:
        st.info(f"{page} page is under development.")