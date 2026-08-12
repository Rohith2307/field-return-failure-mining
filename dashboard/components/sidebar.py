"""
InsightForge AI — Sidebar Navigation
"""
import streamlit as st
def render_sidebar() -> str:
    """Render the InsightForge AI sidebar and return the active page."""
    # --------------------------------------------------
    # Sidebar Branding
    # --------------------------------------------------
    st.sidebar.markdown(
        '<div class="if-sidebar-brand">'
        '<div class="if-brand-mark">◆</div>'
        '<div class="if-brand-content">'
        '<div class="if-brand-title">Insight<span>Forge</span><sup>AI</sup></div>'
        '<div class="if-brand-subtitle">Failure Intelligence Platform</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    # --------------------------------------------------
    # Navigation
    # --------------------------------------------------
    pages = [
        ("⌂", "Dashboard"),
        ("↑", "Upload Dataset"),
        ("⚠", "Failure Analysis"),
        ("↗", "Trend Analytics"),
        ("💥", "Blast Radius"),
        ("✦", "AI Insights"),
        ("▣", "Engineering Report"),
    ]
    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "Dashboard"
    for icon, page_name in pages:
        active = st.session_state["active_page"] == page_name
        button_label = f"{icon}    {page_name}    ›"
        if st.sidebar.button(
            button_label,
            key=f"nav_{page_name}",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            st.session_state["active_page"] = page_name
            st.rerun()
    # --------------------------------------------------
    # Sidebar Bottom Controls
    # --------------------------------------------------
    st.sidebar.markdown(
        '<div class="if-sidebar-spacer"></div>',
        unsafe_allow_html=True,
    )

    if "default_cost_per_unit" not in st.session_state:
        st.session_state["default_cost_per_unit"] = 2500

    if "cost_per_model" not in st.session_state:
        st.session_state["cost_per_model"] = {}

    dataset = st.session_state.get("dataset")

    models = []

    if (
        dataset is not None
        and not dataset.empty
        and "Model" in dataset.columns
    ):
        models = sorted(
            dataset["Model"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    default_cost = st.sidebar.number_input(
        "Default Cost per Failure (₹)",
        min_value=0,
        value=st.session_state["default_cost_per_unit"],
        step=100,
        help=(
            "Used for any model without its own cost set below."
        ),
    )

    st.session_state["default_cost_per_unit"] = default_cost

    if "risk_threshold_pct" not in st.session_state:
        st.session_state["risk_threshold_pct"] = 30

    risk_threshold_pct = st.sidebar.slider(
        "Risk Sensitivity",
        min_value=5,
        max_value=75,
        value=st.session_state["risk_threshold_pct"],
        step=5,
        format="%d%%",
        help=(
            "Share of High-severity records at which the "
            "dashboard flags High risk. Lower = stricter."
        ),
    )

    st.session_state["risk_threshold_pct"] = risk_threshold_pct

    if models:

        with st.sidebar.expander(
            f"Cost per Model ({len(models)})",
            expanded=False,
        ):

            for model in models:

                current_value = st.session_state[
                    "cost_per_model"
                ].get(model, default_cost)

                model_cost = st.number_input(
                    model,
                    min_value=0,
                    value=int(current_value),
                    step=100,
                    key=f"cost_model_{model}",
                )

                st.session_state["cost_per_model"][model] = (
                    model_cost
                )

    
    # --------------------------------------------------
    # Footer
    # --------------------------------------------------
    st.sidebar.markdown(
        """
<div class="if-sidebar-footer">
    <div>InsightForge AI © 2026</div>
    <div>All rights reserved.</div>
</div>
        """,
        unsafe_allow_html=True,
    )
    return st.session_state["active_page"]