"""
Upload Dataset Page
"""

import streamlit as st
import pandas as pd


def render_upload_page():

    st.title("📂 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Upload Field Return Dataset (.csv)",
        type=["csv"],
    )

    if uploaded_file is None:
        st.info("Please upload a CSV file to begin.")
        return

    try:

        df = pd.read_csv(uploaded_file)

        st.success("Dataset uploaded successfully!")

        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True,
            hide_index=True,
        )
        st.divider()

        st.subheader("📊 Dataset Validation")

        missing_values = int(df.isna().sum().sum())

        duplicate_rows = int(df.duplicated().sum())

        quality_score = max(
            0,
            round(
                (
                    1
                    - (
                        (missing_values + duplicate_rows)
                        / max(len(df), 1)
                    )
                )
                * 100,
                1,
            ),
        )

        required_columns = [
            "Model",
            "Issue",
            "Severity",
        ]

        missing_columns = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Quality Score", f"{quality_score}%")

        with c2:
            st.metric("Duplicate Rows", duplicate_rows)

        with c3:
            st.metric("Required Columns", f"{len(required_columns) - len(missing_columns)}/{len(required_columns)}")

        if missing_columns:
            st.warning(
                "Missing columns: " + ", ".join(missing_columns)
            )
        else:
            st.success("✅ Required columns detected.")

        st.subheader("Dataset Information")

        c1, c2, c3 = st.columns(3)

        c1.metric("Rows", len(df))
        c2.metric("Columns", len(df.columns))
        c3.metric("Missing Values", int(df.isna().sum().sum()))

        st.session_state["dataset"] = df

    except Exception as e:
        st.error(f"Error reading CSV: {e}")