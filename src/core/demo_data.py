import pandas as pd
import streamlit as st


def get_dataset():

    if "dataset" in st.session_state:
        return st.session_state["dataset"]

    return pd.DataFrame({
        "Month": ["Jan","Feb","Mar","Apr","May","Jun"],
        "Failures": [105,118,143,166,195,214],
        "Failure": [
            "Overheating",
            "Battery",
            "Display",
            "Charging",
            "Keyboard",
            "Battery",
        ],
        "Severity": [
            "High",
            "Medium",
            "Low",
            "High",
            "Medium",
            "High",
        ],
        "Model": [
            "Latitude",
            "Inspiron",
            "XPS",
            "Precision",
            "Latitude",
            "XPS",
        ],
        "Issue": [
            "Overheating",
            "Battery Drain",
            "Display Flicker",
            "Charging Failure",
            "Keyboard Fault",
            "Thermal Shutdown",
        ],
    })


def repair_logs():
    return get_dataset()


def trend_data():

    df = get_dataset()

    if "Month" in df.columns and "Failures" in df.columns:

        month_order = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ]

        trend = (
            df.groupby("Month", as_index=False)["Failures"]
            .sum()
        )

        trend["Month"] = pd.Categorical(
            trend["Month"],
            categories=month_order,
            ordered=True,
        )

        trend = trend.sort_values("Month")

        return trend

    return pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Failures": [105, 118, 143, 166, 195, 214],
    })


def distribution_data():

    df = get_dataset()

    if "Failure" in df.columns:
        return (
            df.groupby("Failure")
            .size()
            .reset_index(name="Count")
        )

    return pd.DataFrame({
        "Failure":[
            "Overheating",
            "Battery",
            "Display",
            "Charging",
            "Keyboard"
        ],
        "Count":[41,25,17,10,7],
    })

def calculate_health_score():

    df = get_dataset()

    if len(df) == 0:
        return 0

    score = 100

    if "Severity" in df.columns:

        high = (df["Severity"] == "High").sum()
        medium = (df["Severity"] == "Medium").sum()
        low = (df["Severity"] == "Low").sum()

        score -= high * 2.5
        score -= medium * 1
        score -= low * 0.25

    score = max(0, min(100, round(score)))

    return score