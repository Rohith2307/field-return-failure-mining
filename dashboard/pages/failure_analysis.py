"""
Failure Analysis Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.core.schema import get_cost_impact


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

    failure_column = (
        "Failure" if "Failure" in df.columns
        else "Issue" if "Issue" in df.columns
        else None
    )

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

    if "Model" in df.columns:

        model_options = sorted(
            df["Model"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_models = st.sidebar.multiselect(
            "Product Model",
            model_options,
            default=model_options,
        )

        df = df[
            df["Model"].astype(str).isin(selected_models)
        ]

    if failure_column:

        failure_options = sorted(
            df[failure_column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_failures = st.sidebar.multiselect(
            "Failure Mode",
            failure_options,
            default=failure_options,
        )

        df = df[
            df[failure_column].astype(str).isin(selected_failures)
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

    failure_column = (
        "Failure" if "Failure" in df.columns
        else "Issue" if "Issue" in df.columns
        else None
    )

    failure_modes = (
        df[failure_column].nunique()
        if failure_column
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

        if failure_column:

            issue_df = (
                df[failure_column]
                .value_counts()
                .head(10)
                .reset_index()
            )

            issue_df.columns = [
                failure_column,
                "Count",
            ]

            fig = px.bar(
                issue_df,
                x="Count",
                y=failure_column,
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
    # PARETO ANALYSIS
    # ==================================================

    if failure_column:

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-label">PARETO ANALYSIS</div>',
            unsafe_allow_html=True,
        )

        st.markdown("#### Failure Mode Concentration")

        pareto_df = (
            df[failure_column]
            .dropna()
            .astype(str)
            .value_counts()
            .reset_index()
        )

        pareto_df.columns = [failure_column, "Count"]

        pareto_df = pareto_df.sort_values(
            "Count",
            ascending=False,
        ).reset_index(drop=True)

        pareto_df["Cumulative %"] = (
            pareto_df["Count"].cumsum()
            / pareto_df["Count"].sum()
            * 100
        )

        pareto_fig = go.Figure()

        pareto_fig.add_trace(
            go.Bar(
                x=pareto_df[failure_column],
                y=pareto_df["Count"],
                name="Failures",
                marker=dict(color="#4c8dff"),
                yaxis="y1",
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Failures: %{y}"
                    "<extra></extra>"
                ),
            )
        )

        pareto_fig.add_trace(
            go.Scatter(
                x=pareto_df[failure_column],
                y=pareto_df["Cumulative %"],
                name="Cumulative %",
                mode="lines+markers",
                line=dict(color="#ffb52e", width=3),
                marker=dict(size=7),
                yaxis="y2",
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Cumulative: %{y:.1f}%"
                    "<extra></extra>"
                ),
            )
        )

        pareto_fig.add_hline(
            y=80,
            line_dash="dot",
            line_color="#ff5b62",
            annotation_text="80%",
            annotation_position="right",
            yref="y2",
        )

        pareto_fig.update_layout(
            height=400,
            margin=dict(l=10, r=40, t=20, b=10),
            xaxis=dict(title=None),
            yaxis=dict(
                title="Failures",
                side="left",
            ),
            yaxis2=dict(
                title="Cumulative %",
                overlaying="y",
                side="right",
                range=[0, 105],
                showgrid=False,
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
            ),
        )

        st.plotly_chart(
            pareto_fig,
            use_container_width=True,
        )

        vital_few = (
            pareto_df[pareto_df["Cumulative %"] <= 80]
            .shape[0]
        )

        vital_few = max(vital_few, 1)

        st.caption(
            f"The top {vital_few} failure mode"
            f"{'s' if vital_few != 1 else ''} account for "
            "roughly 80% of all recorded failures — "
            "prioritize these for root-cause investigation."
        )

    # ==================================================
    # DRILL-DOWN
    # ==================================================

    if failure_column:

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-label">DRILL-DOWN</div>',
            unsafe_allow_html=True,
        )

        st.markdown("#### Inspect a Failure Mode")

        drilldown_options = ["Select a failure mode..."] + sorted(
            df[failure_column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_mode = st.selectbox(
            "Failure Mode",
            drilldown_options,
            label_visibility="collapsed",
        )

        if selected_mode != "Select a failure mode...":

            drill_df = df[
                df[failure_column].astype(str) == selected_mode
            ]

            st.caption(
                f"{len(drill_df)} record(s) with failure mode "
                f"'{selected_mode}'."
            )

            st.dataframe(
                drill_df,
                use_container_width=True,
                hide_index=True,
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

    if failure_column:

        priority_df = (
            df.groupby(failure_column)
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

            cost_impact = get_cost_impact(
                df,
                st.session_state.get("cost_per_model", {}),
                st.session_state.get("default_cost_per_unit", 0),
            )

            by_mode = cost_impact["by_mode"]

            if not by_mode.empty:

                priority_df = priority_df.merge(
                    by_mode[[failure_column, "Cost"]],
                    on=failure_column,
                    how="left",
                )

                priority_df["Cost"] = (
                    priority_df["Cost"]
                    .fillna(0)
                    .map(lambda x: f"₹{x:,.0f}")
                )

        st.dataframe(
            priority_df.head(10),
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "Priority is based on relative failure concentration "
            "and helps engineering teams focus investigation effort. "
            "Cost reflects estimated impact using each product's "
            "configured cost rate."
        )