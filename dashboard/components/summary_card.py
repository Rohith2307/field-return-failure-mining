import streamlit as st


def render_summary():

    st.markdown("### 🤖 AI Executive Summary")

    st.markdown(
        """
<div style="
padding:20px;
border-radius:15px;
border:1px solid #444;
background-color:rgba(100,100,100,0.05);
">

<b>Key Findings</b>

<br><br>

• Overheating continues to be the dominant issue.

• Failure rate increased during the last quarter.

• Most failures appear on premium models.

<br>

<b>Recommendation</b>

Review thermal assembly and fan design.

</div>
""",
        unsafe_allow_html=True,
    )