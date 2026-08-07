"""
Reusable Section Header
"""

import streamlit as st


def section_header(
    title: str,
    subtitle: str,
) -> None:

    st.markdown(
        f"""
        <h2 style="
            margin-bottom:0;
        ">
            {title}
        </h2>

        <p style="
            color:gray;
            margin-top:2px;
        ">
            {subtitle}
        </p>
        """,
        unsafe_allow_html=True,
    )