"""
Failure Analysis Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px


def render_failure_analysis():

    st.title("📊 Failure Analysis")

    st.caption(
        "Identify dominant failure modes, severity patterns, "
        "and products requiring engineering attention."
    )

    if "dataset" not in st.session_state:
        st.warning("Please upload a dataset first.")
        return

    df = st.session_state["dataset"].copy()

    # ==================================================
    # FILTERS
    # ==================================================

    st.sidebar.markdown("## Analysis Filters")

    if "Severity" in df.columns:

        severity_options = [
            "All",
            "High",
            "Medium",
            "Low",
        ]

        selected_severity = st.sidebar.selectbox(
            "Severity",
            severity_options,
        )

        if selected_severity != "All":
            df = df[
                df["Severity"] == selected_severity
            ]

    if df.empty:
        st.warning("No records match the selected filters.")
        return

    # ==================================================
    # KPI CARDS
    # ==================================================

    total_failures = len(df)

    high_failures = 0

    if "Severity" in df.columns:
        high_failures = int(
            (df["Severity"] == "High").sum()
        )

    failure_modes = (
        df["Issue"].nunique()
        if "Issue" in df.columns
        else 0
    )

    affected_products = (
        df["Model"].nunique()
        if "Model" in df.columns
        else 0
    )

    st.markdown(
        '<div class="section-label">FAILURE OVERVIEW</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Total Failures",
            f"{total_failures:,}",
        )

    with c2:
        st.metric(
            "High Severity",
            f"{high_failures:,}",
        )

    with c3:
        st.metric(
            "Failure Modes",
            failure_modes,
        )

    with c4:
        st.metric(
            "Affected Products",
            affected_products,
        )

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    # ==================================================
    # FAILURE MODE + SEVERITY
    # ==================================================

    st.markdown(
        '<div class="section-label">FAILURE PATTERNS</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        if "Issue" in df.columns:

            issue_df = (
                df["Issue"]
                .value_counts()
                .head(10)
                .reset_index()
            )

            issue_df.columns = [
                "Issue",
                "Count",
            ]

            fig = px.bar(
                issue_df,
                x="Count",
                y="Issue",
                orientation="h",
            )

            fig.update_layout(
                height=400,
                margin=dict(
                    l=10,
                    r=20,
                    t=20,
                    b=10,
                ),
                xaxis_title=None,
                yaxis_title=None,
                yaxis=dict(
                    categoryorder="total ascending"
                ),
            )

            fig.update_traces(
                texttemplate="%{x}",
                textposition="outside",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Failures: %{x}"
                    "<extra></extra>"
                ),
            )

            st.markdown(
                "#### Top Failure Modes"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

    with col2:

        if "Severity" in df.columns:

            severity_df = (
                df["Severity"]
                .value_counts()
                .reset_index()
            )

            severity_df.columns = [
                "Severity",
                "Count",
            ]

            st.markdown(
                "#### Severity Distribution"
            )

            fig = px.pie(
                severity_df,
                names="Severity",
                values="Count",
                hole=0.62,
            )

            fig.update_layout(
                height=400,
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10,
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.12,
                    xanchor="center",
                    x=0.5,
                ),
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Failures: %{value}<br>"
                    "Share: %{percent}"
                    "<extra></extra>"
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    # ==================================================
    # PRODUCT ANALYSIS
    # ==================================================

    if "Model" in df.columns:

        st.markdown(
            '<div class="section-label">PRODUCT RELIABILITY</div>',
            unsafe_allow_html=True,
        )

        model_df = (
            df["Model"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        model_df.columns = [
            "Model",
            "Failures",
        ]

        fig = px.bar(
            model_df,
            x="Model",
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
        )

        fig.update_traces(
            texttemplate="%{y}",
            textposition="outside",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # ==================================================
    # ENGINEERING PRIORITY
    # ==================================================

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-label">ENGINEERING PRIORITY</div>',
        unsafe_allow_html=True,
    )

    st.subheader("🎯 Failure Modes Requiring Attention")

    if "Issue" in df.columns:

        priority_df = (
            df.groupby("Issue")
            .size()
            .reset_index(name="Failures")
            .sort_values(
                "Failures",
                ascending=False,
            )
        )

        if not priority_df.empty:

            top_count = priority_df.iloc[0]["Failures"]

            priority_df["Priority"] = "Monitor"

            priority_df.loc[
                priority_df["Failures"] >= top_count * 0.7,
                "Priority"
            ] = "High"

            priority_df.loc[
                (
                    priority_df["Failures"] < top_count * 0.7
                )
                &
                (
                    priority_df["Failures"] >= top_count * 0.4
                ),
                "Priority"
            ] = "Medium"

        st.dataframe(
            priority_df.head(10),
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "Priority is based on relative failure concentration "
            "and helps engineering teams focus investigation effort."
        )