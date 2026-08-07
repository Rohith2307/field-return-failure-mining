import streamlit as st

from src.ai.gemini_client import generate_insights


def render_ai_page():

    st.title("🤖 AI Insights")

    if "dataset" not in st.session_state:

        st.warning("Please upload a dataset first.")

        return

    if st.button("Generate AI Insights"):

        with st.spinner("Analyzing dataset..."):

            result = generate_insights(
                st.session_state["dataset"]
            )

        st.markdown(result)