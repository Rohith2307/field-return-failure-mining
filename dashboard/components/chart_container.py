"""
Reusable Plotly Chart Container
"""

import streamlit as st
import plotly.graph_objects as go


def render_chart(
    figure: go.Figure,
    title: str,
) -> None:
    """
    Render a Plotly chart inside
    a styled container.
    """

    st.markdown(f"### {title}")

    st.plotly_chart(
    figure,
    use_container_width=True,
    config={
        "displaylogo": False,
        "displayModeBar": "hover",
        "scrollZoom": True,
        "responsive": True,
        "modeBarButtonsToRemove": [
            "lasso2d",
            "select2d",
            "autoScale2d",
            "toggleSpikelines"
        ],
        "toImageButtonOptions": {
            "format": "png",
            "filename": "insightforge_chart",
            "scale": 2,
        },
    },
)