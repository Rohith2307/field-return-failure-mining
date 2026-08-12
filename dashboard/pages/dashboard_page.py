"""
InsightForge AI
Main Dashboard Page
"""

from pathlib import Path
import base64

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.core import demo_data
from src.core.schema import get_cost_impact


# ============================================================
# PROJECT / ASSET PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"


# ============================================================
# ASSET HELPERS
# ============================================================

def load_asset_base64(filename: str) -> str:
    """
    Load an image from the assets folder and convert it to base64.
    """

    file_path = ASSETS_DIR / filename

    if not file_path.exists():
        return ""

    try:
        return base64.b64encode(
            file_path.read_bytes()
        ).decode("utf-8")
    except Exception:
        return ""


# ============================================================
# DATA HELPERS
# ============================================================

def _get_demo_value(name, default=None):
    """
    Safely retrieve a value from src.core.demo_data.

    This avoids importing specific names such as `months`,
    `failures`, etc. directly. Your demo_data.py can therefore
    change its internal structure without breaking this page.
    """

    try:
        value = getattr(demo_data, name, None)

        if value is None:
            return default

        if callable(value):
            return value()

        return value

    except Exception:
        return default


def get_dashboard_data():
    """
    Build dashboard data directly from the uploaded dataset.

    Expected columns:
        Month
        Failures
        Failure
        Severity
        Model
        Issue
        Repair Date
        Status
    """

    # --------------------------------------------------------
    # GET UPLOADED DATASET
    # --------------------------------------------------------

    df = st.session_state.get("dataset")

    if df is None or df.empty:
        return (
            [],
            [],
            pd.DataFrame(
                columns=["Category", "Count"]
            ),
            pd.DataFrame(),
        )

    # Work on a copy so the uploaded dataframe is not modified.
    df = df.copy()

    # --------------------------------------------------------
    # NORMALIZE COLUMN NAMES
    # --------------------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # MONTHLY FAILURE TREND
    # --------------------------------------------------------

    if "Month" in df.columns:

        month_order = [
            "Jan", "Feb", "Mar", "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec",
        ]

        trend = (
            df.groupby("Month", sort=False)["Failures"]
            .sum()
            if "Failures" in df.columns
            else df.groupby("Month", sort=False)
            .size()
        )

        trend = trend.reindex(
            [
                month
                for month in month_order
                if month in trend.index
            ]
        )

        months = trend.index.astype(str).tolist()
        failures = trend.tolist()

    else:

        months = []
        failures = []

    # --------------------------------------------------------
    # FAILURE DISTRIBUTION
    # --------------------------------------------------------

    if "Failure" in df.columns:

        distribution = (
            df["Failure"]
            .dropna()
            .astype(str)
            .str.strip()
            .value_counts()
            .rename_axis("Category")
            .reset_index(name="Count")
        )

    elif "Issue" in df.columns:

        distribution = (
            df["Issue"]
            .dropna()
            .astype(str)
            .str.strip()
            .value_counts()
            .rename_axis("Category")
            .reset_index(name="Count")
        )

    else:

        distribution = pd.DataFrame(
            columns=["Category", "Count"]
        )

    # --------------------------------------------------------
    # REPAIR LOGS
    # --------------------------------------------------------

    repair_logs = df.copy()

    if "Repair Date" in repair_logs.columns:

        repair_logs["Repair Date"] = pd.to_datetime(
            repair_logs["Repair Date"],
            errors="coerce",
        )

        repair_logs = repair_logs.sort_values(
            "Repair Date",
            ascending=False,
            na_position="last",
        )

    if "Date" in repair_logs.columns:

        repair_logs["Date"] = pd.to_datetime(
            repair_logs["Date"],
            errors="coerce",
        )

    return (
        months,
        failures,
        distribution,
        repair_logs,
    )


# ============================================================
# HEALTH SCORE
# ============================================================

def get_health_score(logs: pd.DataFrame) -> int:
    """
    Calculate a simple dashboard health score.
    """

    try:

        if logs is None or logs.empty:
            return 90

        if "Severity" not in logs.columns:
            return 90

        total = len(logs)

        high_count = (
            logs["Severity"]
            .astype(str)
            .str.lower()
            .eq("high")
            .sum()
        )

        medium_count = (
            logs["Severity"]
            .astype(str)
            .str.lower()
            .eq("medium")
            .sum()
        )

        score = 100 - (
            (high_count / max(total, 1)) * 30
            + (medium_count / max(total, 1)) * 10
        )

        return max(
            0,
            min(
                100,
                round(score),
            ),
        )

    except Exception:
        return 90


# ============================================================
# SYSTEM HEALTH STATUS
# ============================================================

def get_system_health_status(
    logs: pd.DataFrame,
    health_score: int,
    critical_failures: int,
    total_returns: int,
    months: list,
    failures: list,
    risk_threshold: float = 0.3,
) -> dict:
    """
    Derive System Health Overview panel values from the
    actual dataset instead of static demo values.
    """

    # ----- Health Score KPI bucket (score gauge only) -----
    if health_score >= 80:
        score_class = "green"
        score_label = "Excellent"
    elif health_score >= 60:
        score_class = "orange"
        score_label = "Good"
    else:
        score_class = "red"
        score_label = "Needs Attention"

    # ----- Risk / Reliability bucket (based on critical failure share) -----
    critical_ratio = (
        critical_failures / total_returns
        if total_returns
        else 0
    )

    if critical_ratio == 0:
        risk_class = "green"
        risk_level = "Low"
        reliability = "High"
    elif critical_ratio < risk_threshold:
        risk_class = "orange"
        risk_level = "Medium"
        reliability = "Medium"
    else:
        risk_class = "red"
        risk_level = "High"
        reliability = "Low"

    # ----- Performance (trend direction) -----
    if len(failures) >= 2 and failures[0]:
        change = ((failures[-1] - failures[0]) / failures[0]) * 100

        if change > 10:
            performance = "Degrading"
            performance_class = "red"
        elif change < -10:
            performance = "Improving"
            performance_class = "green"
        else:
            performance = "Stable"
            performance_class = "green"
    else:
        performance = "N/A"
        performance_class = "green"

    # ----- Resolution rate (replaces "Uptime") -----
    if logs is not None and "Status" in logs.columns and total_returns:
        repaired = (
            logs["Status"]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("repaired")
            .sum()
        )
        resolution_rate = f"{(repaired / total_returns) * 100:.1f}%"
    else:
        resolution_rate = "N/A"

    # ----- Health banner text (driven by the same risk bucket) -----
    if risk_class == "green":
        health_state = "ok"
        health_icon = "✓"
        health_title = "All systems operational"
        health_description = (
            "No critical issues detected. System performing "
            "within normal parameters."
        )
    elif risk_class == "orange":
        health_state = "warning"
        health_icon = "⚠"
        health_title = "Attention needed"
        health_description = (
            f"{critical_failures} high-severity failure(s) detected "
            f"({critical_ratio * 100:.0f}% of records). Review affected "
            "products before they escalate."
        )
    else:
        health_state = "critical"
        health_icon = "!"
        health_title = "Critical issues detected"
        health_description = (
            f"{critical_failures} high-severity failures detected out of "
            f"{total_returns} records ({critical_ratio * 100:.0f}%). "
            "Immediate engineering review recommended."
        )

    return {
        "score_class": score_class,
        "score_label": score_label,
        "risk_class": risk_class,
        "risk_level": risk_level,
        "reliability": reliability,
        "performance": performance,
        "performance_class": performance_class,
        "resolution_rate": resolution_rate,
        "health_state": health_state,
        "health_icon": health_icon,
        "health_title": health_title,
        "health_description": health_description,
    }


# ============================================================
# DASHBOARD CSS
# ============================================================

def load_dashboard_css() -> None:
    """
    Load dashboard-specific styling.
    """

    watermark_data = load_asset_base64(
        "insightforge-watermark.png"
    )

    watermark_css = ""

    if watermark_data:
        watermark_css = f"""
        .if-dashboard-watermark {{
            position: fixed;
            top: 50%;
            left: 58%;
            transform: translate(-50%, -50%);
            width: 420px;
            opacity: 0.035;
            pointer-events: none;
            user-select: none;
            z-index: 0;
        }}

        .if-dashboard-watermark img {{
            width: 100%;
            height: auto;
        }}
        """

    css = f"""
    <style>

    /* ==================================================
       GLOBAL
       ================================================== */

    .stApp {{
        background:
            radial-gradient(
                circle at 70% 20%,
                rgba(37, 99, 235, 0.06),
                transparent 30%
            ),
            #070d19;
    }}

    .main .block-container {{
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        position: relative;
    }}

    /* ==================================================
       WATERMARK
       ================================================== */

    {watermark_css}

    /* ==================================================
       PAGE HEADER
       ================================================== */

    .if-page-header {{
        margin-bottom: 26px;
        position: relative;
        z-index: 2;
    }}

    .if-page-title {{
        font-size: 34px;
        font-weight: 700;
        line-height: 1.15;
        color: #f5f7fb;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }}

    .if-page-subtitle {{
        color: #9aa6b8;
        font-size: 15px;
        line-height: 1.5;
    }}

    /* ==================================================
       KPI GRID
       ================================================== */

    .if-kpi-grid {{
        display: grid;
        grid-template-columns:
            repeat(6, minmax(0, 1fr));
        gap: 14px;
        margin-bottom: 18px;
        position: relative;
        z-index: 2;
    }}

    .if-kpi {{
        background:
            linear-gradient(
                145deg,
                rgba(15, 29, 52, 0.98),
                rgba(8, 17, 31, 0.98)
            );

        border: 1px solid
            rgba(91, 112, 145, 0.28);

        border-radius: 14px;
        min-height: 158px;
        padding: 21px;
        position: relative;
        overflow: hidden;
    }}

    .if-kpi::after {{
        content: "";
        position: absolute;
        width: 110px;
        height: 110px;
        right: -45px;
        bottom: -45px;
        border-radius: 50%;
        background: rgba(37, 99, 235, 0.07);
    }}

    .if-kpi-label {{
        color: #b6c0d0;
        font-size: 14px;
        margin-bottom: 18px;
    }}

    .if-kpi-value {{
        color: #f4f7fb;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
    }}

    .if-kpi-value.green {{
        color: #45d483;
    }}

    .if-kpi-value.orange {{
        color: #ffb52e;
    }}

    .if-kpi-value.red {{
        color: #ff5b62;
    }}

    .if-kpi-change {{
        font-size: 13px;
        color: #7f8da2;
    }}

    .if-kpi-change.blue {{
        color: #4c8dff;
    }}

    .if-kpi-change.green {{
        color: #45d483;
    }}

    .if-kpi-change.red {{
        color: #ff5b62;
    }}

    .if-kpi-change.orange {{
        color: #ffb52e;
    }}

    .if-kpi-change.purple {{
        color: #b279ff;
    }}

    /* ==================================================
       PANELS
       ================================================== */

    .if-panel {{
        background:
            linear-gradient(
                145deg,
                rgba(11, 23, 41, 0.96),
                rgba(7, 15, 28, 0.96)
            );

        border: 1px solid
            rgba(91, 112, 145, 0.25);

        border-radius: 14px;
        padding: 20px;
        position: relative;
        z-index: 2;
    }}

    .if-panel-title {{
        color: #f2f5fa;
        font-size: 17px;
        font-weight: 600;
        margin-bottom: 4px;
    }}

    .if-panel-subtitle {{
        color: #7f8da2;
        font-size: 12px;
        margin-bottom: 12px;
    }}

    /* ==================================================
       HEALTH PANEL
       ================================================== */

    .if-health {{
        background:
            linear-gradient(
                135deg,
                rgba(20, 76, 58, 0.30),
                rgba(8, 30, 29, 0.50)
            );

        border: 1px solid
            rgba(59, 205, 128, 0.28);

        border-radius: 14px;
        padding: 20px;
        margin-top: 16px;
        margin-bottom: 18px;
    }}

    .if-health-top {{
        display: flex;
        align-items: center;
        gap: 15px;
    }}

    .if-health-icon {{
        width: 46px;
        height: 46px;
        border-radius: 50%;
        border: 2px solid #45d483;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #45d483;
        font-size: 25px;
        font-weight: 700;
        flex-shrink: 0;
    }}

    .if-health-title {{
        color: #45d483;
        font-size: 16px;
        font-weight: 600;
    }}

    .if-health-description {{
        color: #c3ccd8;
        font-size: 13px;
        line-height: 1.6;
        margin-top: 5px;
    }}

    .if-health.warning {{
        background:
            linear-gradient(
                135deg,
                rgba(120, 76, 20, 0.30),
                rgba(40, 26, 8, 0.50)
            );
        border: 1px solid rgba(255, 181, 46, 0.30);
    }}

    .if-health.critical {{
        background:
            linear-gradient(
                135deg,
                rgba(120, 30, 30, 0.30),
                rgba(40, 10, 10, 0.50)
            );
        border: 1px solid rgba(255, 91, 98, 0.30);
    }}

    .if-health-icon.warning {{
        border-color: #ffb52e;
        color: #ffb52e;
    }}

    .if-health-icon.critical {{
        border-color: #ff5b62;
        color: #ff5b62;
    }}

    .if-health-title.warning {{
        color: #ffb52e;
    }}

    .if-health-title.critical {{
        color: #ff5b62;
    }}

    .if-mini-grid {{
        display: grid;
        grid-template-columns:
            repeat(4, 1fr);
        margin-top: 22px;
        border-top: 1px solid
            rgba(91, 112, 145, 0.20);
        padding-top: 18px;
    }}

    .if-mini-item {{
        text-align: center;
        border-right: 1px solid
            rgba(91, 112, 145, 0.20);
    }}

    .if-mini-item:last-child {{
        border-right: none;
    }}

    .if-mini-label {{
        color: #8996a9;
        font-size: 12px;
        margin-bottom: 7px;
    }}

    .if-mini-value {{
        font-size: 16px;
        font-weight: 600;
    }}

    .if-mini-value.green {{
        color: #45d483;
    }}

    .if-mini-value.orange {{
        color: #ffb52e;
    }}

    .if-mini-value.red {{
        color: #ff5b62;
    }}
    /* ==================================================
       REPAIR TABLE
       ================================================== */

    .if-table-wrapper {{
        overflow-x: auto;
        margin-top: 16px;
    }}

    .if-table {{
        width: 100%;
        border-collapse: collapse;
        color: #dce3ed;
        font-size: 13px;
    }}

    .if-table th {{
        text-align: left;
        color: #98a5b7;
        font-weight: 500;
        padding: 12px 10px;
        border-bottom: 1px solid
            rgba(91, 112, 145, 0.30);
        white-space: nowrap;
    }}

    .if-table td {{
        padding: 13px 10px;
        border-bottom: 1px solid
            rgba(91, 112, 145, 0.14);
        white-space: nowrap;
    }}

    .if-severity-high {{
        color: #ff5b62;
        font-weight: 600;
    }}

    .if-severity-medium {{
        color: #ffb52e;
        font-weight: 600;
    }}

    .if-severity-low {{
        color: #45d483;
        font-weight: 600;
    }}

    .if-status {{
        display: inline-block;
        padding: 4px 9px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
    }}

    .if-status-repaired {{
        background: rgba(52, 211, 119, 0.12);
        color: #45d483;
    }}

    .if-status-pending {{
        background: rgba(255, 181, 46, 0.12);
        color: #ffb52e;
    }}

    .if-status-open {{
        background: rgba(255, 91, 98, 0.12);
        color: #ff5b62;
    }}

    /* ==================================================
       LINKS
       ================================================== */

    .if-view-link {{
        text-align: right;
        color: #4285ff;
        font-size: 13px;
        padding-top: 10px;
    }}

    /* ==================================================
       FOOTER
       ================================================== */

    .if-footer {{
        margin-top: 28px;
        padding-top: 20px;
        border-top: 1px solid
            rgba(91, 112, 145, 0.18);

        color: #6e7b8e;
        font-size: 12px;
        text-align: center;
    }}

    .if-footer strong {{
        color: #a8b4c5;
    }}

    /* ==================================================
       RESPONSIVE
       ================================================== */

    @media (max-width: 1100px) {{

        .if-kpi-grid {{
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }}

    }}

    @media (max-width: 700px) {{

        .if-kpi-grid {{
            grid-template-columns: 1fr;
        }}

        .if-page-title {{
            font-size: 28px;
        }}

        .if-mini-grid {{
            grid-template-columns:
                repeat(2, 1fr);
            row-gap: 18px;
        }}

        .if-mini-item:nth-child(2) {{
            border-right: none;
        }}

    }}

    </style>
    """

    st.html(css)


# ============================================================
# CHART: MONTHLY FAILURE TREND
# ============================================================

def create_trend_chart(months, failures):
    """
    Create the monthly failure trend chart.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=months,
            y=failures,
            mode="lines+markers",
            line=dict(
                width=3,
                color="#3f82ff",
            ),
            marker=dict(
                size=7,
                color="#3f82ff",
            ),
            fill="tozeroy",
            fillcolor="rgba(63,130,255,0.13)",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Failures: %{y}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        height=340,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#aeb9c9",
            size=12,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(120,140,170,0.12)",
            zeroline=False,
            title=None,
        ),
        showlegend=False,
    )

    return fig


# ============================================================
# CHART: FAILURE DISTRIBUTION
# ============================================================

def create_distribution_chart(distribution):
    """
    Create the failure distribution donut chart.
    Returns None if there is no real data to show.
    """

    labels = []
    values = []

    try:

        if isinstance(distribution, pd.DataFrame):

            category_column = None

            for candidate in [
                "Category",
                "Failure",
                "Failure Mode",
                "Type",
            ]:

                if candidate in distribution.columns:
                    category_column = candidate
                    break

            count_column = None

            for candidate in [
                "Count",
                "count",
                "Frequency",
                "frequency",
            ]:

                if candidate in distribution.columns:
                    count_column = candidate
                    break

            if (
                category_column is not None
                and count_column is not None
            ):

                labels = (
                    distribution[category_column]
                    .astype(str)
                    .tolist()
                )

                values = (
                    pd.to_numeric(
                        distribution[count_column],
                        errors="coerce",
                    )
                    .fillna(0)
                    .tolist()
                )

    except Exception:
        pass

    if not labels or not values or sum(values) == 0:
        return None

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.62,
                textinfo="percent",
                textposition="inside",
                marker=dict(
                    colors=[
                        "#2864d7",
                        "#f59e0b",
                        "#36a269",
                        "#8b5cc7",
                        "#d84b50",
                    ],
                    line=dict(
                        color="#08101e",
                        width=2,
                    ),
                ),
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "%{percent}"
                    "<extra></extra>"
                ),
            )
        ]
    )

    fig.update_layout(
        height=340,
        margin=dict(
            l=0,
            r=0,
            t=5,
            b=0,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#dce3ed",
            size=12,
        ),
        legend=dict(
            orientation="v",
            x=0.95,
            y=0.5,
            xanchor="left",
            yanchor="middle",
        ),
        showlegend=True,
    )

    return fig


# ============================================================
# REPAIR LOG TABLE
# ============================================================

def render_repair_table(data: pd.DataFrame) -> None:
    """
    Render recent repair logs.
    """

    if data is None or data.empty:

        st.info(
            "No repair records found."
        )

        return

    rows = []

    for index, row in data.head(5).iterrows():

        record_id = row.get("ID", "—")

        model = row.get(
            "Product Model",
            row.get("Model", "—"),
        )

        issue = row.get(
            "Failure Mode",
            row.get("Issue", "—"),
        )

        severity = str(
            row.get("Severity", "—")
        )

        repair_date = row.get("Repair Date", "—")

        if pd.isna(repair_date):
            repair_date = "—"

        status = str(
            row.get("Status", "—")
        )

        severity_lower = severity.lower()

        if severity_lower == "high":

            severity_class = (
                "if-severity-high"
            )

        elif severity_lower == "medium":

            severity_class = (
                "if-severity-medium"
            )

        else:

            severity_class = (
                "if-severity-low"
            )

        status_lower = status.lower()

        if status_lower == "repaired":

            status_class = (
                "if-status-repaired"
            )

        elif status_lower == "pending":

            status_class = (
                "if-status-pending"
            )

        else:

            status_class = (
                "if-status-open"
            )

        rows.append(
            f"""
            <tr>

                <td>{record_id}</td>

                <td>{model}</td>

                <td>{issue}</td>

                <td class="{severity_class}">
                    {severity}
                </td>

                <td>{repair_date}</td>

                <td>
                    <span class="if-status {status_class}">
                        {status}
                    </span>
                </td>

            </tr>
            """
        )

    table_html = f"""
    <div class="if-table-wrapper">

        <table class="if-table">

            <thead>

                <tr>
                    <th>ID</th>
                    <th>Product Model</th>
                    <th>Failure Mode</th>
                    <th>Severity</th>
                    <th>Repair Date</th>
                    <th>Status</th>
                </tr>

            </thead>

            <tbody>
                {"".join(rows)}
            </tbody>

        </table>

    </div>
    """

    st.html(table_html)


# ============================================================
# MAIN DASHBOARD
# ============================================================

def render_dashboard() -> None:
    """
    Render the complete InsightForge AI dashboard.
    """

    # --------------------------------------------------------
    # LOAD CSS
    # --------------------------------------------------------

    load_dashboard_css()

    # --------------------------------------------------------
    # WATERMARK
    # --------------------------------------------------------

    watermark_data = load_asset_base64(
        "insightforge-watermark.png"
    )

    if watermark_data:

        st.html(
            f"""
            <div class="if-dashboard-watermark">

                <img
                    src="data:image/png;base64,{watermark_data}"
                    alt=""
                >

            </div>
            """
        )

    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    st.html(
        """
        <div class="if-page-header">

            <div class="if-page-title">
                Dashboard
            </div>

            <div class="if-page-subtitle">
                Welcome back! Here's your
                failure intelligence overview.
            </div>

        </div>
        """
    )

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    (
        months,
        failures,
        distribution,
        logs,
    ) = get_dashboard_data()

    # --------------------------------------------------------
    # HEALTH
    # --------------------------------------------------------

    health_score = get_health_score(logs)

    # --------------------------------------------------------
    # TOTAL RETURNS
    # --------------------------------------------------------

    total_returns = len(logs)

    # --------------------------------------------------------
    # FAILURE MODE COUNT
    # --------------------------------------------------------

    failure_mode_column = (
        "Failure" if "Failure" in logs.columns
        else "Issue" if "Issue" in logs.columns
        else None
    )

    failure_mode_count = (
        logs[failure_mode_column]
        .dropna()
        .astype(str)
        .str.strip()
        .nunique()
        if failure_mode_column
        else 0
    )

    # --------------------------------------------------------
    # OTHER KPI VALUES
    # --------------------------------------------------------

    # Critical failures are records marked High severity.
    if "Severity" in logs.columns:

        critical_failures = (
            logs["Severity"]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("high")
            .sum()
        )

    else:

        critical_failures = 0

    has_date = "Date" in logs.columns
    has_repair_date = "Repair Date" in logs.columns

    if not has_date and not has_repair_date:

        mttr = "N/A"
        mttr_note = "Missing Date & Repair Date"

    elif not has_date:

        mttr = "N/A"
        mttr_note = "Missing failure Date column"

    elif not has_repair_date:

        mttr = "N/A"
        mttr_note = "Missing Repair Date column"

    else:

        resolution_days = (
            logs["Repair Date"] - logs["Date"]
        ).dt.days

        valid_days = resolution_days.dropna()
        valid_days = valid_days[valid_days >= 0]

        if valid_days.empty:

            mttr = "N/A"

            mttr_note = (
                "Dates present but unusable"
                if not resolution_days.dropna().empty
                else "No valid date pairs found"
            )

        else:

            mttr = f"{valid_days.mean():.1f}d"
            mttr_note = f"Across {len(valid_days)} repaired records"

    # --------------------------------------------------------
    # SYSTEM HEALTH STATUS
    # --------------------------------------------------------

    status = get_system_health_status(
        logs,
        health_score,
        critical_failures,
        total_returns,
        months,
        failures,
        st.session_state.get("risk_threshold_pct", 30) / 100,
    )

    cost_impact = get_cost_impact(
        logs,
        st.session_state.get("cost_per_model", {}),
        st.session_state.get("default_cost_per_unit", 0),
    )

    health_state_class = (
        "" if status["health_state"] == "ok"
        else status["health_state"]
    )

    # --------------------------------------------------------
    # KPI ROW

    st.html(
        f"""
        <div class="if-kpi-grid">

            <div class="if-kpi">

                <div class="if-kpi-label">
                    🛡️ &nbsp; System Health Score
                </div>

                <div class="if-kpi-value {status['score_class']}">
                    {health_score}%
                </div>

                <div class="if-kpi-change {status['score_class']}">
                    {status['score_label']}
                </div>

            </div>


            <div class="if-kpi">

                <div class="if-kpi-label">
                    📦 &nbsp; Total Field Returns
                </div>

                <div class="if-kpi-value">
                    {total_returns:,}
                </div>

                <div class="if-kpi-change blue">
                    Based on uploaded dataset
                </div>

            </div>


            <div class="if-kpi">

                <div class="if-kpi-label">
                    ⚠️ &nbsp; Failure Modes
                </div>

                <div class="if-kpi-value">
                    {failure_mode_count}
                </div>

                <div class="if-kpi-change orange">
                    Unique failure categories
                </div>

            </div>


            <div class="if-kpi">

                <div class="if-kpi-label">
                    🔴 &nbsp; Critical Failures
                </div>

                <div class="if-kpi-value">
                    {critical_failures}
                </div>

                <div class="if-kpi-change red">
                    High severity records
                </div>

            </div>


            <div class="if-kpi">

                <div class="if-kpi-label">
                    🕒 &nbsp; MTTR (avg)
                </div>

                <div class="if-kpi-value">
                    {mttr}
                </div>

                <div class="if-kpi-change purple">
                    {mttr_note}
                </div>

            </div>


            <div class="if-kpi">

                <div class="if-kpi-label">
                    💰 &nbsp; Estimated Cost Impact
                </div>

                <div class="if-kpi-value">
                    ₹{cost_impact['total_cost']:,.0f}
                </div>

                <div class="if-kpi-change orange">
                    Based on per-model cost rates
                </div>

            </div>

        </div>
        """
    )

    # --------------------------------------------------------
    # CHART ROW
    # --------------------------------------------------------

    chart_left, chart_right = st.columns(
        [2, 1]
    )

    # --------------------------------------------------------
    # MONTHLY FAILURE TREND
    # --------------------------------------------------------

    with chart_left:

        st.html(
            """
            <div class="if-panel">

                <div class="if-panel-title">
                    Monthly Failure Trend
                </div>

                <div class="if-panel-subtitle">
                    Field return failures over time
                </div>

            </div>
            """
        )

        st.plotly_chart(
            create_trend_chart(
                months,
                failures,
            ),
            width="stretch",
            config={
                "displayModeBar": False,
            },
        )

    # --------------------------------------------------------
    # FAILURE DISTRIBUTION
    # --------------------------------------------------------

    with chart_right:

        st.html(
            """
            <div class="if-panel">

                <div class="if-panel-title">
                    Failure Distribution
                </div>

                <div class="if-panel-subtitle">
                    Distribution by failure category
                </div>

            </div>
            """
        )

        distribution_fig = create_distribution_chart(
            distribution
        )

        if distribution_fig is not None:

            st.plotly_chart(
                distribution_fig,
                width="stretch",
                config={
                    "displayModeBar": False,
                },
            )

            st.html(
                """
                <div class="if-view-link">
                    View detailed analysis →
                </div>
                """
            )

        else:

            st.info(
                "No failure distribution data available. "
                "Upload a dataset to see this chart."
            )

    # --------------------------------------------------------
    # LOWER ROW
    # --------------------------------------------------------

    summary_col, logs_col = st.columns(
        [1, 1.55]
    )

    # --------------------------------------------------------
    # SYSTEM HEALTH OVERVIEW
    # --------------------------------------------------------

    with summary_col:

        st.html(
            f"""
            <div class="if-panel">

                <div class="if-panel-title">
                    System Health Overview
                </div>

                <div class="if-health {health_state_class}">

                    <div class="if-health-top">

                        <div class="if-health-icon {health_state_class}">
                            {status['health_icon']}
                        </div>

                        <div>

                            <div class="if-health-title {health_state_class}">
                                {status['health_title']}
                            </div>

                            <div class="if-health-description">
                                {status['health_description']}
                            </div>

                        </div>

                    </div>

                </div>

                <div class="if-mini-grid">

                    <div class="if-mini-item">

                        <div class="if-mini-label">
                            Resolution Rate
                        </div>

                        <div class="if-mini-value green">
                            {status['resolution_rate']}
                        </div>

                    </div>


                    <div class="if-mini-item">

                        <div class="if-mini-label">
                            Reliability
                        </div>

                        <div class="if-mini-value {status['risk_class']}">
                            {status['reliability']}
                        </div>

                    </div>


                    <div class="if-mini-item">

                        <div class="if-mini-label">
                            Performance
                        </div>

                        <div class="if-mini-value {status['performance_class']}">
                            {status['performance']}
                        </div>

                    </div>


                    <div class="if-mini-item">

                        <div class="if-mini-label">
                            Risk Level
                        </div>

                        <div class="if-mini-value {status['risk_class']}">
                            {status['risk_level']}
                        </div>

                    </div>

                </div>

            </div>
            """
        )

    # --------------------------------------------------------
    # RECENT REPAIR LOGS
    # --------------------------------------------------------

    with logs_col:

        st.html(
            """
            <div class="if-panel">

                <div class="if-panel-title">
                    Recent Repair Logs
                </div>

            </div>
            """
        )

        render_repair_table(logs)

        st.html(
            """
            <div class="if-view-link">
                View all logs →
            </div>
            """
        )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.html(
        """
        <div class="if-footer">

            <strong>
                INSIGHTFORGE AI
            </strong>

            &nbsp; • &nbsp;

            Field Return Failure Intelligence Platform

        </div>
        """
    )


# ============================================================
# END OF FILE
# ============================================================