"""
Trend Analytics Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from src.core.demo_data import trend_data


def render_trends_page():

    st.title("📈 Trend Analytics")

    st.caption(
        "Analyze monthly failure patterns and identify periods requiring attention."
    )

    if "dataset" not in st.session_state:
        st.warning("Please upload a dataset first.")
        return

    # Use the same monthly trend data as the Dashboard
    monthly = trend_data().copy()

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