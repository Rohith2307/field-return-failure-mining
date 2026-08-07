"""
Enterprise Data Table
"""

import pandas as pd
import streamlit as st

from st_aggrid import AgGrid
from st_aggrid import GridOptionsBuilder
from st_aggrid.shared import JsCode


def render_table(df: pd.DataFrame):

    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_default_column(
        sortable=True,
        filter=True,
        resizable=True,
    )

    severity_sort = JsCode(
        """
        function(valueA, valueB){

            const order = {
                "High":3,
                "Medium":2,
                "Low":1
            };

            return order[valueA]-order[valueB];
        }
        """
    )

    gb.configure_column(

        "Severity",

        comparator=severity_sort,

    )

    gb.configure_pagination(
        enabled=True,
        paginationPageSize=10,
    )

    gb.configure_grid_options(
        animateRows=True,
    )

    gridOptions = gb.build()

    st.markdown("### 📋 Recent Repair Logs")

    AgGrid(

        df,

        gridOptions=gridOptions,

        fit_columns_on_grid_load=True,

        height=320,

        allow_unsafe_jscode=True,

    )