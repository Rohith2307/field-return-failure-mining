"""
Trend Analytics Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px




def render_trends_page():

    st.title("📈 Trend Analytics")

    st.caption(
        "Analyze monthly failure patterns and identify periods requiring attention."
    )

    if "dataset" not in st.session_state:
        st.warning("Please upload a dataset first.")
        return

    df = st.session_state["dataset"].copy()

    if "Month" not in df.columns:
        st.warning("No trend data available.")
        return

    if "Failures" in df.columns:
        monthly = (
            df.groupby("Month", as_index=False)["Failures"]
            .sum()
        )
    else:
        monthly = (
            df.groupby("Month")
            .size()
            .reset_index(name="Failures")
        )

    if monthly.empty:
        st.warning("No trend data available.")
        return

    # --------------------------------------------------
    # PROPER MONTH ORDER
    # --------------------------------------------------

    month_order = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]

    monthly["Month"] = pd.Categorical(
        monthly["Month"],
        categories=month_order,
        ordered=True,
    )

    monthly = monthly.sort_values("Month")

    # --------------------------------------------------
    # METRICS
    # --------------------------------------------------

    total_failures = int(monthly["Failures"].sum())

    peak_row = monthly.loc[
        monthly["Failures"].idxmax()
    ]

    peak_month = peak_row["Month"]
    peak_failures = int(peak_row["Failures"])

    if len(monthly) >= 2:

        first_value = monthly.iloc[0]["Failures"]
        last_value = monthly.iloc[-1]["Failures"]

        if first_value != 0:
            change = (
                (last_value - first_value)
                / first_value
            ) * 100
        else:
            change = 0

    else:
        change = 0

    # --------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Failures",
        f"{total_failures:,}",
    )

    c2.metric(
        "Peak Month",
        str(peak_month),
    )

    c3.metric(
        "Peak Failures",
        f"{peak_failures:,}",
    )

    c4.metric(
        "Period Change",
        f"{change:+.1f}%",
    )

    st.divider()

    # --------------------------------------------------
    # MONTHLY TREND
    # --------------------------------------------------

    st.subheader("📊 Monthly Failure Trend")

    fig = px.line(
        monthly,
        x="Month",
        y="Failures",
        markers=True,
    )

    fig.update_layout(
        height=420,
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10,
        ),
        xaxis_title=None,
        yaxis_title="Number of Failures",
        hovermode="x unified",
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # --------------------------------------------------
    # PRODUCT / MODEL TREND
    # --------------------------------------------------

    if "Model" in df.columns:

        st.divider()

        st.subheader("🧩 Failure Trend by Product Model")

        if "Failures" in df.columns:
            model_monthly = (
                df.groupby(["Month", "Model"], as_index=False)["Failures"]
                .sum()
            )
        else:
            model_monthly = (
                df.groupby(["Month", "Model"])
                .size()
                .reset_index(name="Failures")
            )

        model_monthly["Month"] = pd.Categorical(
            model_monthly["Month"],
            categories=month_order,
            ordered=True,
        )

        model_monthly = model_monthly.sort_values("Month")

        model_fig = px.line(
            model_monthly,
            x="Month",
            y="Failures",
            color="Model",
            markers=True,
        )

        model_fig.update_layout(
            height=420,
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis_title=None,
            yaxis_title="Number of Failures",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
            ),
        )

        model_fig.update_traces(
            line=dict(width=2.5),
            marker=dict(size=6),
        )

        st.plotly_chart(
            model_fig,
            use_container_width=True,
        )

    # --------------------------------------------------
    # TREND INTERPRETATION
    # --------------------------------------------------

    st.divider()

    st.subheader("🔎 Trend Interpretation")

    if change > 10:

        st.error(
            f"⚠️ Failures increased by {change:.1f}% "
            "from the beginning to the end of the observed period."
        )

    elif change < -10:

        st.success(
            f"✅ Failures decreased by {abs(change):.1f}% "
            "from the beginning to the end of the observed period."
        )

    else:

        st.info(
            "ℹ️ Failure volume remained relatively stable "
            "across the observed period."
        )

    st.info(
        f"Peak failure activity occurred in **{peak_month}** "
        f"with **{peak_failures} failures**."
    )

    # --------------------------------------------------
    # SEVERITY TREND
    # --------------------------------------------------

    if "Severity" in df.columns:

        st.divider()

        st.subheader("🚦 Severity Trend Over Time")

        severity_monthly = (
            df.groupby(["Month", "Severity"])
            .size()
            .reset_index(name="Failures")
        )

        severity_monthly["Month"] = pd.Categorical(
            severity_monthly["Month"],
            categories=month_order,
            ordered=True,
        )

        severity_monthly = severity_monthly.sort_values("Month")

        severity_colors = {
            "High": "#ff5b62",
            "Medium": "#ffb52e",
            "Low": "#3ecf8e",
        }

        severity_fig = px.area(
            severity_monthly,
            x="Month",
            y="Failures",
            color="Severity",
            color_discrete_map=severity_colors,
            category_orders={
                "Severity": ["Low", "Medium", "High"]
            },
        )

        severity_fig.update_layout(
            height=420,
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis_title=None,
            yaxis_title="Number of Failures",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
            ),
        )

        st.plotly_chart(
            severity_fig,
            use_container_width=True,
        )

        # Flag if High-severity share is growing over time
        high_share = (
            severity_monthly[severity_monthly["Severity"] == "High"]
            .set_index("Month")["Failures"]
        )

        totals_by_month = (
            severity_monthly.groupby("Month")["Failures"].sum()
        )

        if len(high_share) >= 2 and not totals_by_month.empty:

            first_month = totals_by_month.index[0]
            last_month = totals_by_month.index[-1]

            first_ratio = (
                high_share.get(first_month, 0) / totals_by_month[first_month]
                if totals_by_month[first_month] else 0
            )

            last_ratio = (
                high_share.get(last_month, 0) / totals_by_month[last_month]
                if totals_by_month[last_month] else 0
            )

            if last_ratio > first_ratio + 0.1:
                st.error(
                    "⚠️ The share of High-severity failures is "
                    "trending upward — quality may be degrading "
                    "over time, not just volume."
                )
            elif last_ratio < first_ratio - 0.1:
                st.success(
                    "✅ The share of High-severity failures is "
                    "trending downward relative to total volume."
                )

   

    # --------------------------------------------------
    # MONTHLY SUMMARY
    # --------------------------------------------------

    st.divider()

    st.subheader("📋 Monthly Failure Summary")

    display_monthly = monthly.copy()

    display_monthly["Change"] = (
        display_monthly["Failures"]
        .pct_change()
        .mul(100)
        .round(1)
    )

    display_monthly["Change"] = (
        display_monthly["Change"]
        .fillna(0)
        .map(lambda x: f"{x:+.1f}%")
    )

    st.dataframe(
        display_monthly,
        use_container_width=True,
        hide_index=True,
    )