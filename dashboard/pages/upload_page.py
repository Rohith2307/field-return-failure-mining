"""
Upload Dataset Page
"""

import streamlit as st
import pandas as pd


from src.core.schema import normalize_dataset, get_missing_canonical_columns

def render_upload_page():

    st.title("📂 Upload Dataset")

    st.caption(
        "Upload your field-return dataset to begin reliability analysis."
    )

    # --------------------------------------------------
    # UPLOAD AREA
    # --------------------------------------------------

    uploaded_file = st.file_uploader(
        "Upload Field Return Dataset",
        type=["csv"],
        help="Upload a CSV file containing field-return records.",
    )

    if uploaded_file is None:

        st.info(
            "📌 Upload a CSV file to start the analysis."
        )

        st.markdown(
            """
            ### What happens after upload?

            **01 · Validation**  
            The dataset is checked for missing values and structure.

            **02 · Failure Analysis**  
            Failure modes, severity and affected products are analyzed.

            **03 · Trend Analytics**  
            Failure patterns are visualized and compared.

            **04 · AI Insights**  
            Gemini identifies patterns and engineering recommendations.

            **05 · Engineering Report**  
            Generate a downloadable PDF report.
            """
        )

        return

    # --------------------------------------------------
    # READ DATASET
    # --------------------------------------------------

    try:

        df = pd.read_csv(uploaded_file)

        # Normalize to the canonical InsightForge schema
        df = normalize_dataset(df)

        # Store dataset
        st.session_state["dataset"] = df

        st.success(
            f"✅ Dataset uploaded successfully — "
            f"{len(df):,} records detected."
        )

        missing_columns = get_missing_canonical_columns(df)

        if missing_columns:
            st.warning(
                "⚠ Some expected columns were not found in this dataset: "
                f"**{', '.join(missing_columns)}**. "
                "Pages that rely on these fields will show partial "
                "or N/A results."
            )

        # --------------------------------------------------
        # DATASET OVERVIEW
        # --------------------------------------------------

        st.subheader("📊 Dataset Overview")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Records",
                f"{len(df):,}",
            )

        with c2:
            st.metric(
                "Columns",
                len(df.columns),
            )

        with c3:
            st.metric(
                "Missing Values",
                int(df.isna().sum().sum()),
            )

        with c4:
            st.metric(
                "Duplicate Rows",
                int(df.duplicated().sum()),
            )

        st.divider()

        # --------------------------------------------------
        # DATASET PREVIEW
        # --------------------------------------------------

        st.subheader("👀 Dataset Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        # --------------------------------------------------
        # VALIDATION
        # --------------------------------------------------

        st.subheader("🛡 Dataset Validation")

        missing_values = int(
            df.isna().sum().sum()
        )

        duplicate_rows = int(
            df.duplicated().sum()
        )

        validation_col1, validation_col2 = st.columns(2)

        with validation_col1:

            if missing_values == 0:

                st.success(
                    "✓ No missing values detected"
                )

            else:

                st.warning(
                    f"⚠ {missing_values:,} missing values detected"
                )

        with validation_col2:

            if duplicate_rows == 0:

                st.success(
                    "✓ No duplicate rows detected"
                )

            else:

                st.warning(
                    f"⚠ {duplicate_rows:,} duplicate rows detected"
                )

        # --------------------------------------------------
        # DATASET INFORMATION
        # --------------------------------------------------

        st.divider()

        st.subheader("📋 Dataset Information")

        info_col1, info_col2 = st.columns(2)

        with info_col1:

            st.markdown(
                f"""
                **File:** `{uploaded_file.name}`

                **Rows:** `{len(df):,}`

                **Columns:** `{len(df.columns)}`
                """
            )

        with info_col2:

            st.markdown(
                f"""
                **Memory Usage:** `{df.memory_usage(deep=True).sum() / 1024:.1f} KB`

                **Numeric Columns:** `{len(df.select_dtypes(include="number").columns)}`

                **Text Columns:** `{len(df.select_dtypes(include="object").columns)}`
                """
            )

    except Exception as e:

        st.error(
            f"❌ Error reading CSV: {e}"
        )