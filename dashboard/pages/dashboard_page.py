import streamlit as st
import pandas as pd
import plotly.express as px

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

    st.subheader("📊 Engineering Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if "dataset" in st.session_state:
            health_score = "Calculating..."
        else:
            health_score = "N/A"

        metric_card(
            "Health Score",
            f"{calculate_health_score()}%",
            "Live",
        )

    with col2:
        metric_card(
            "Repair Logs",
            str(len(repair_logs())),
            "+0%"
        )

    with col3:
        metric_card(
            "Failure Modes",
            str(distribution_data()["Failure"].nunique()),
            "+0"
        )

    with col4:
        metric_card(
            "Products",
            str(repair_logs()["Model"].nunique()),
            "+0"
        )

    st.divider()

    left, right = st.columns([2, 1])

    with left:

        fig = px.line(
            trend_data(),
            x="Month",
            y="Failures",
            markers=True,
            title=""
        )

        fig.update_layout(
            template="plotly",
            height=350,
            margin=dict(l=10, r=10, t=20, b=10),
        )

        render_chart(fig, "Monthly Failure Trend")

    with right:

        pie = px.pie(
            distribution_data(),
            names="Failure",
            values="Count",
            hole=0.65,
        )

        pie.update_layout(
            template="plotly",
            height=350,
            margin=dict(l=10, r=10, t=20, b=10),
        )

        render_chart(
            pie,
            "Failure Distribution",
        )

    st.divider()

    render_summary()

    st.divider()

    logs = repair_logs()

    st.subheader("🔍 Search & Filters")

    col1, col2 = st.columns([3, 1])

    with col1:
        search = st.text_input(
            "Search Issue / Model",
            placeholder="Search...",
        )

    with col2:
        severity = st.selectbox(
            "Severity",
            ["All", "High", "Medium", "Low"],
        )

    if search:
        logs = logs[
            logs["Model"].str.contains(search, case=False)
            | logs["Issue"].str.contains(search, case=False)
        ]

    if severity != "All":
        logs = logs[
            logs["Severity"] == severity
        ]

    render_table(logs)