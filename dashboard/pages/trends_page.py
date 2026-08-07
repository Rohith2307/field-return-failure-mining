"""
Trend Analytics Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px


def render_trends_page():

    st.title("📈 Trend Analytics")

    if "dataset" not in st.session_state:
        st.warning("Please upload a dataset first.")
        return

    df = st.session_state["dataset"].copy()

    # -----------------------------
    # Monthly Failure Trend
    # -----------------------------

    st.subheader("Monthly Failure Trend")

    month_order = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    trend = (
        df.groupby("Month", as_index=False)["Failures"]
        .sum()
    )

    trend["Month"] = pd.Categorical(
        trend["Month"],
        categories=month_order,
        ordered=True,
    )

    trend = trend.sort_values("Month")

    fig = px.line(
        trend,
        x="Month",
        y="Failures",
        markers=True,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.divider()

    # -----------------------------
    # Severity Trend
    # -----------------------------

    st.subheader("Severity Trend")

    severity = (
        df.groupby(["Month", "Severity"])
        .size()
        .reset_index(name="Count")
    )

    severity["Month"] = pd.Categorical(
        severity["Month"],
        categories=month_order,
        ordered=True,
    )

    severity = severity.sort_values("Month")

    fig = px.bar(
        severity,
        x="Month",
        y="Count",
        color="Severity",
        barmode="group",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.divider()

    # -----------------------------
    # Top Products
    # -----------------------------

    st.subheader("Top 5 Products")

    top_products = (
        df.groupby("Model")["Failures"]
        .sum()
        .reset_index()
        .sort_values("Failures", ascending=False)
        .head(5)
    )

    fig = px.bar(
        top_products,
        x="Model",
        y="Failures",
        color="Failures",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.divider()

    # -----------------------------
    # Monthly Summary
    # -----------------------------

    st.subheader("Monthly Summary")

    st.dataframe(
        trend,
        use_container_width=True,
        hide_index=True,
    )