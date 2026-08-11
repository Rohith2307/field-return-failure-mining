"""
AI Insights Page
"""

import re

import streamlit as st

from src.ai.gemini_client import generate_insights


def render_ai_page():

    st.title("🤖 AI Insights")

    st.caption(
        "AI-powered reliability analysis based on the uploaded field-return dataset."
    )

    if "dataset" not in st.session_state:
        st.warning("Please upload a dataset first.")
        return

    df = st.session_state["dataset"]

    # Dataset summary
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Records Analyzed",
        f"{len(df):,}",
    )

    failure_column = (
        "Failure" if "Failure" in df.columns
        else "Issue" if "Issue" in df.columns
        else None
    )

    c2.metric(
        "Failure Modes",
        df[failure_column].nunique()
        if failure_column
        else "N/A",
    )

    c3.metric(
        "Products",
        df["Model"].nunique()
        if "Model" in df.columns
        else "N/A",
    )

    st.divider()

    if st.button(
        "✨ Generate AI Insights",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner(
            "Analyzing failure patterns and engineering trends..."
        ):

            try:

                result = generate_insights(
                    df,
                    st.session_state.get("cost_per_model", {}),
                    st.session_state.get("default_cost_per_unit", 0),
                )

                st.session_state["ai_insights"] = result

            except Exception as e:

                st.error(
                    f"Unable to generate AI insights: {e}"
                )

                return

    if "ai_insights" not in st.session_state:

        st.subheader("What the AI analyzes")

        col1, col2 = st.columns(2)

        with col1:

            st.info(
                """
                **🔎 Failure Patterns**

                Identifies the most frequent failure modes
                and affected products.
                """
            )

            st.info(
                """
                **⚠️ Severity Analysis**

                Examines High, Medium and Low severity
                failure distribution.
                """
            )

            st.info(
                """
                **🧩 Root Cause Hypotheses**

                Identifies possible engineering causes
                from observed failure patterns.
                """
            )

        with col2:

            st.info(
                """
                **📈 Trend Analysis**

                Examines changes in failure frequency
                over time.
                """
            )

            st.info(
                """
                **🛠 Engineering Recommendations**

                Suggests practical reliability improvements.
                """
            )

            st.info(
                """
                **🛡 Preventive Actions**

                Recommends actions to reduce future
                field failures.
                """
            )

        return

    # --------------------------------------------------
    # AI RESULTS
    # --------------------------------------------------

    result = st.session_state["ai_insights"]

    st.divider()

    st.subheader("🔎 Engineering Analysis")

    # Remove markdown heading symbols so we can
    # create our own clean section headers.
    cleaned_result = result.replace("\r", "")

    sections = re.split(
        r"(?m)^#{1,6}\s+",
        cleaned_result,
    )

    sections = [
        section.strip()
        for section in sections
        if section.strip()
    ]

    for section in sections:

        lines = section.split("\n")

        heading = lines[0].strip()

        content = "\n".join(
            lines[1:]
        ).strip()

        # Identify important sections
        heading_lower = heading.lower()

        if "executive" in heading_lower:

            st.markdown(
                "### 🎯 Executive Summary"
            )

            st.success(content)

        elif "failure" in heading_lower:

            st.markdown(
                "### 🔥 Top Failure Patterns"
            )

            st.warning(content)

        elif "root cause" in heading_lower:

            st.markdown(
                "### 🧩 Root Cause Hypotheses"
            )

            st.info(content)

        elif "recommendation" in heading_lower:

            st.markdown(
                "### 🛠 Engineering Recommendations"
            )

            st.info(content)

        elif "preventive" in heading_lower:

            st.markdown(
                "### 🛡 Preventive Actions"
            )

            st.success(content)

        elif "takeaway" in heading_lower:

            st.markdown(
                "### 📌 Key Takeaways"
            )

            st.markdown(content)

        else:

            st.markdown(
                f"### {heading}"
            )

            st.markdown(content)

    st.divider()

    st.caption(
        "AI-generated analysis is based on the uploaded dataset. "
        "Engineering teams should validate recommendations before implementation."
    )