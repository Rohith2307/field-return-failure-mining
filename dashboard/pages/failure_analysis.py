"""
Failure Analysis Page
"""

import streamlit as st
import plotly.express as px
import pandas as pd


def render_failure_analysis():

    st.title("📊 Failure Analysis")

    if "dataset" not in st.session_state:

        st.warning("Please upload a dataset first.")

        return

    df = st.session_state["dataset"]

    st.sidebar.markdown("## Filters")

    if "Severity" in df.columns:

        severity = st.sidebar.multiselect(
            "Severity",
            sorted(df["Severity"].dropna().unique()),
            default=sorted(df["Severity"].dropna().unique()),
        )

        df = df[df["Severity"].isin(severity)]

    col1, col2 = st.columns(2)

    with col1:

        if "Issue" in df.columns:

            issue_df = (
                df["Issue"]
                .value_counts()
                .reset_index()
            )

            issue_df.columns = ["Issue", "Count"]

            fig = px.bar(
                issue_df,
                x="Issue",
                y="Count",
                title="Top Failure Modes",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

    with col2:

        if "Severity" in df.columns:

            fig = px.pie(
                df,
                names="Severity",
                title="Severity Distribution",
                hole=0.55,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

    st.divider()

    if "Model" in df.columns:

        model_df = (
            df["Model"]
            .value_counts()
            .reset_index()
        )

        model_df.columns = [
            "Model",
            "Count",
        ]

        fig = px.bar(
            model_df,
            x="Model",
            y="Count",
            title="Product-wise Failures",
            color="Count",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        st.divider()

        st.subheader("📈 Pareto Analysis (80/20 Rule)")

        pareto_df = (
            df.groupby("Failure")
            .size()
            .reset_index(name="Count")
            .sort_values("Count", ascending=False)
        )

        pareto_df["Cumulative"] = (
            pareto_df["Count"].cumsum()
            / pareto_df["Count"].sum()
            * 100
        )

        fig = px.bar(
            pareto_df,
            x="Failure",
            y="Count",
            color="Count",
        )

        fig.add_scatter(
            x=pareto_df["Failure"],
            y=pareto_df["Cumulative"],
            mode="lines+markers",
            name="Cumulative %",
            yaxis="y2",
        )

        fig.update_layout(
            yaxis2=dict(
                title="Cumulative %",
                overlaying="y",
                side="right",
                range=[0, 100],
            ),
            legend=dict(
                orientation="h",
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )