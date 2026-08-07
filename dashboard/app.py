"""
InsightForge AI

Main Application
"""

import streamlit as st

from styles.css import load_css

from components.header import render_header

from components.sidebar import render_sidebar

from components.metric_card import metric_card


# -------------------------------------------------

st.set_page_config(

    page_title="InsightForge AI",

    page_icon="🛠️",

    layout="wide",

    initial_sidebar_state="expanded",

)

# -------------------------------------------------

st.markdown(

    load_css(),

    unsafe_allow_html=True,

)

# -------------------------------------------------

page = render_sidebar()

render_header()

# -------------------------------------------------

if page == "Dashboard":

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        metric_card(

            "Health Score",

            "84",

            "+5%"

        )

    with c2:

        metric_card(

            "Repair Logs",

            "18,423",

            "+12%"

        )

    with c3:

        metric_card(

            "Failure Modes",

            "17",

            "+2"

        )

    with c4:

        metric_card(

            "Products",

            "42",

            "+1"

        )

    st.divider()

    left, right = st.columns([2, 1])

    with left:

        st.subheader(

            "Failure Distribution"

        )

        st.info(

            "Charts will appear here."

        )

    with right:

        st.subheader(

            "AI Summary"

        )

        st.success(

            """

Most issues relate to

• Overheating

• Battery

• Display

"""

        )

else:

    st.info(

        f"{page} page coming soon."

    )