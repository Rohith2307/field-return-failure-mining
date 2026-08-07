"""
Custom Metric Card Component
"""

import streamlit as st


def metric_card(
    title: str,
    value: str,
    delta: str,
    delta_positive: bool = True,
) -> None:
    """
    Render a custom metric card.
    """

    delta_color = "#22C55E" if delta_positive else "#EF4444"
    arrow = "▲" if delta_positive else "▼"

    st.markdown(
        f"""
        <div style="
            background: var(--secondary-background-color);
            border:1px solid rgba(128,128,128,0.15);
            border-radius:18px;
            padding:18px;
            min-height:130px;
            box-shadow:0 2px 10px rgba(0,0,0,0.08);
        ">

        <p style="
            margin:0;
            font-size:14px;
            color:var(--text-color);
            opacity:0.75;
        ">
        {title}
        </p>

        <h2 style="
            margin-top:10px;
            margin-bottom:10px;
            color:var(--text-color);
        ">
        {value}
        </h2>

        <span style="
            color:{delta_color};
            font-weight:600;
            font-size:14px;
        ">
        {arrow} {delta}
        </span>

        </div>
        """,
        unsafe_allow_html=True,
    )