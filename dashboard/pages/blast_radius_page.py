"""
Blast Radius Page
"""

import streamlit as st
import pandas as pd

from src.core.schema import get_blast_radius


def render_blast_radius_page():

    st.title("💥 Blast Radius")

    st.caption(
        "Estimate future failure risk per product based on an "
        "assumed fleet size — how many more failures should we "
        "expect from units still in the field, at the current "
        "failure rate."
    )

    if "dataset" not in st.session_state:
        st.warning("Please upload a dataset first.")
        return

    df = st.session_state["dataset"].copy()

    if "Model" not in df.columns:
        st.warning(
            "This dataset has no Model column, so per-product "
            "risk can't be estimated."
        )
        return

    st.divider()

    st.subheader("🚢 Fleet Size by Model")

    st.caption(
        "Enter your best estimate of total units currently in "
        "the field for each product model. Everything below "
        "updates live as you edit these numbers."
    )

    models = sorted(
        df["Model"].dropna().astype(str).unique().tolist()
    )

    if "fleet_sizes" not in st.session_state:
        st.session_state["fleet_sizes"] = {
            model: 1000 for model in models
        }

    for model in models:
        if model not in st.session_state["fleet_sizes"]:
            st.session_state["fleet_sizes"][model] = 1000

    fleet_input_df = pd.DataFrame(
        {
            "Model": models,
            "Fleet Size": [
                st.session_state["fleet_sizes"][model]
                for model in models
            ],
        }
    )

    edited_fleet_df = st.data_editor(
        fleet_input_df,
        column_config={
            "Model": st.column_config.TextColumn(
                "Model",
                disabled=True,
            ),
            "Fleet Size": st.column_config.NumberColumn(
                "Fleet Size",
                min_value=0,
                step=100,
            ),
        },
        hide_index=True,
        use_container_width=True,
        key="fleet_size_editor",
    )

    for _, row in edited_fleet_df.iterrows():
        st.session_state["fleet_sizes"][row["Model"]] = row["Fleet Size"]

    st.divider()

    st.subheader("📊 Projected Risk")

    blast_df = get_blast_radius(
        df,
        st.session_state["fleet_sizes"],
    )

    if blast_df.empty:
        st.info(
            "Enter fleet sizes above to see projected risk."
        )
        return

    total_projected = blast_df["Projected Additional Failures"].sum()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Highest-Risk Model",
        str(blast_df.iloc[0]["Model"]),
    )

    c2.metric(
        "Projected Additional Failures",
        f"{total_projected:,.0f}",
    )

    c3.metric(
        "Models Analyzed",
        len(blast_df),
    )

    st.dataframe(
        blast_df,
        use_container_width=True,
        hide_index=True,
    )

    top_risk = blast_df.iloc[0]

    st.error(
        f"⚠️ At the current failure rate, **{top_risk['Model']}** "
        f"is projected to see **~{top_risk['Projected Additional Failures']:.0f} "
        "more failures** from units still in the field if uncorrected."
    )

    st.caption(
        "Projections assume the historical failure rate holds "
        "steady going forward. Fleet size figures are user "
        "estimates, not measured data."
    )