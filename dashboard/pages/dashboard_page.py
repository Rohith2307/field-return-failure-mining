import streamlit as st
import pandas as pd
import plotly.express as px
from textwrap import dedent

from dashboard.components.metric_card import metric_card
from dashboard.components.chart_container import render_chart
from dashboard.components.summary_card import render_summary
from dashboard.components.data_table import render_table

from src.core.demo_data import (
    trend_data,
    distribution_data,
    repair_logs,
    calculate_health_score,
)


def render_dashboard():

    # ==================================================
    # HERO SECTION
    # ==================================================

    st.markdown(
        dedent("""
        <div class="hero-section">
            <div class="hero-badge">● LIVE RELIABILITY MONITORING</div>
            <h1>Field Return Intelligence</h1>
            <p>
                Monitor product reliability, identify failure patterns,
                and turn field-return data into actionable engineering insights.
            </p>
        </div>
        """),
        unsafe_allow_html=True,
    )

    # ==================================================
    # DATA
    # ==================================================

    logs = repair_logs()
    distribution = distribution_data()
    trend = trend_data()

    health_score = calculate_health_score()

    # ==================================================
    # KPI CARDS
    # ==================================================

    st.markdown(
        '<div class="section-label">ENGINEERING HEALTH</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            "Health Score",
            f"{health_score}%",
            "Live",
        )

    with col2:
        metric_card(
            "Repair Logs",
            f"{len(logs):,}",
            "Tracked",
        )

    with col3:
        metric_card(
            "Failure Modes",
            str(distribution["Failure"].nunique()),
            "Detected",
        )

    with col4:
        metric_card(
            "Products",
            str(logs["Model"].nunique()),
            "Affected",
        )

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    # ==================================================
    # HEALTH STATUS
    # ==================================================

    if health_score >= 80:
        status = "Healthy"
        status_icon = "✓"
        status_class = "health-good"
    elif health_score >= 60:
        status = "Needs Attention"
        status_icon = "!"
        status_class = "health-warning"
    else:
        status = "Critical"
        status_icon = "!"
        status_class = "health-critical"

    st.markdown(
        f'<div class="health-banner {status_class}">'
        f'<div class="health-icon">{status_icon}</div>'
        f'<div>'
        f'<div class="health-title">System Health: {status}</div>'
        f'<div class="health-description">'
        f'Current reliability score is <strong>{health_score}%</strong>. '
        f'Continue monitoring failure concentration and severity trends.'
        f'</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    # ==================================================
    # FAILURE INTELLIGENCE
    # ==================================================

    st.markdown(
        '<div class="section-label">FAILURE INTELLIGENCE</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([2, 1])

    with left:

        trend = trend.copy()

        month_order = [
            "Jan", "Feb", "Mar", "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec",
        ]

        if "Month" in trend.columns:

            trend["Month"] = pd.Categorical(
                trend["Month"],
                categories=month_order,
                ordered=True,
            )

            trend = trend.sort_values("Month")

        fig = px.area(
            trend,
            x="Month",
            y="Failures",
        )

        fig.update_layout(
            height=380,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10,
            ),
            xaxis_title=None,
            yaxis_title="Failures",
            hovermode="x unified",
            showlegend=False,
        )

        fig.update_traces(
            line=dict(width=3),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Failures: %{y}"
                "<extra></extra>"
            ),
        )

        render_chart(
            fig,
            "Monthly Failure Trend",
        )

    with right:

        pie = px.pie(
            distribution,
            names="Failure",
            values="Count",
            hole=0.68,
        )

        pie.update_layout(
            height=380,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10,
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.18,
                xanchor="center",
                x=0.5,
            ),
        )

        pie.update_traces(
            textposition="inside",
            textinfo="percent",
        )

        render_chart(
            pie,
            "Failure Distribution",
        )

    # ==================================================
    # ENGINEERING SUMMARY
    # ==================================================

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-label">ENGINEERING SUMMARY</div>',
        unsafe_allow_html=True,
    )

    render_summary()

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    # ==================================================
    # REPAIR LOGS
    # ==================================================

    st.markdown(
        '<div class="section-label">FIELD RETURN RECORDS</div>',
        unsafe_allow_html=True,
    )

    st.subheader("🔍 Recent Repair Logs")

    col1, col2 = st.columns([3, 1])

    with col1:

        search = st.text_input(
            "Search",
            placeholder="Search issue or product model...",
            label_visibility="collapsed",
        )

    with col2:

        severity = st.selectbox(
            "Severity",
            [
                "All",
                "High",
                "Medium",
                "Low",
            ],
            label_visibility="collapsed",
        )

    if search:

        search = search.strip()

        if search:

            logs = logs[
                logs["Model"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False,
                )
                |
                logs["Issue"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False,
                )
            ]

    if severity != "All":

        logs = logs[
            logs["Severity"] == severity
        ]

    render_table(logs)

    # ==================================================
    # FOOTER
    # ==================================================

    st.markdown(
        """
        <div class="dashboard-footer">
            <div>INSIGHTFORGE AI</div>
            <span>Field Return Failure Intelligence Platform</span>
        </div>
        """,
        unsafe_allow_html=True,
    )