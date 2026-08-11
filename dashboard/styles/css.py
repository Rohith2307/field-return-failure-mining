"""
Global UI styling for InsightForge AI
"""


def load_css() -> str:
    """Return the global InsightForge AI stylesheet."""

    return """
    <style>

    /* =========================================================
       INSIGHTFORGE AI — GLOBAL UI
       ========================================================= */

    /* ---------------------------------------------------------
       Sidebar
       --------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.14);
    }

    .if-sidebar-brand {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 18px 4px 20px 4px;
    }

    .if-brand-mark {
        display: flex;
        align-items: center;
        justify-content: center;

        width: 36px;
        height: 36px;

        color: #3b82f6;
        font-size: 28px;
        line-height: 1;
    }

    .if-brand-content {
        min-width: 0;
    }

    .if-brand-title {
        font-size: 21px;
        font-weight: 800;
        letter-spacing: -0.7px;
        white-space: nowrap;
    }

    .if-brand-title span {
        color: #f59e0b;
    }

    .if-brand-title sup {
        color: #f59e0b;
        font-size: 9px;
        margin-left: 2px;
        vertical-align: top;
    }

    .if-brand-subtitle {
        margin-top: 5px;
        font-size: 10px;
        opacity: 0.5;
        white-space: nowrap;
    }

    /* ---------------------------------------------------------
       Sidebar Navigation
       --------------------------------------------------------- */

    section[data-testid="stSidebar"] .stButton {
        margin-bottom: 12px;
    }

    section[data-testid="stSidebar"] .stButton > button {
        position: relative;

        width: 100%;
        min-height: 58px;

        padding: 0 18px !important;

        border-radius: 16px !important;

        border: 1px solid rgba(128, 128, 128, 0.14) !important;

        background: rgba(128, 128, 128, 0.025) !important;

        font-size: 15px !important;
        font-weight: 650 !important;

        text-align: left !important;

        transition:
            transform 0.2s ease,
            background 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease !important;
    }

    /* ---------------------------------------------------------
       Navigation Hover
       --------------------------------------------------------- */

    section[data-testid="stSidebar"] .stButton > button:hover {
        transform: translateX(3px);

        background: rgba(37, 99, 235, 0.08) !important;

        border-color: rgba(37, 99, 235, 0.30) !important;

        box-shadow:
            0 8px 24px rgba(37, 99, 235, 0.08) !important;
    }

    /* ---------------------------------------------------------
       Active Navigation Item
       --------------------------------------------------------- */

    section[data-testid="stSidebar"]
    .stButton > button[kind="primary"] {

        background:
            linear-gradient(
                100deg,
                rgba(37, 99, 235, 0.25),
                rgba(99, 102, 241, 0.12)
            ) !important;

        border:
            1px solid rgba(37, 99, 235, 0.40) !important;

        box-shadow:
            inset 4px 0 0 #2563eb,
            0 10px 30px rgba(37, 99, 235, 0.10) !important;
    }

    /* ---------------------------------------------------------
       Active Indicator
       --------------------------------------------------------- */

    section[data-testid="stSidebar"]
    .stButton > button[kind="primary"]::after {

        content: "";

        position: absolute;

        right: 18px;

        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #3b82f6;

        box-shadow:
            0 0 12px rgba(59, 130, 246, 0.75);

        animation:
            sidebarGlow 2s ease-in-out infinite;
    }

    /* ---------------------------------------------------------
       Sidebar Button Text
       --------------------------------------------------------- */

    section[data-testid="stSidebar"] .stButton > button p {
        font-size: 15px !important;
        font-weight: 650 !important;
        letter-spacing: -0.15px;
    }

    /* ---------------------------------------------------------
       Focus State
       --------------------------------------------------------- */

    section[data-testid="stSidebar"]
    .stButton > button:focus {

        box-shadow:
            inset 4px 0 0 #2563eb,
            0 10px 30px rgba(37, 99, 235, 0.10) !important;
    }

    /* ---------------------------------------------------------
       Sidebar Spacer
       --------------------------------------------------------- */

    .if-sidebar-spacer {
        height: 24px;
    }

    /* ---------------------------------------------------------
       Sidebar Footer
       --------------------------------------------------------- */

    .if-sidebar-footer {
        margin-top: 24px;
        padding: 18px 4px 8px 4px;

        border-top:
            1px solid rgba(128, 128, 128, 0.12);

        text-align: center;
    }

    .if-sidebar-footer div {
        font-size: 11px;
        opacity: 0.45;
        line-height: 1.6;
    }

    /* ---------------------------------------------------------
       General Application
       --------------------------------------------------------- */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------------------------------------------------------
       Cards
       --------------------------------------------------------- */

    .if-card {
        padding: 20px;

        border-radius: 18px;

        border:
            1px solid rgba(128, 128, 128, 0.16);

        background:
            linear-gradient(
                165deg,
                rgba(59, 130, 246, 0.06),
                rgba(128, 128, 128, 0.02) 55%
            );

        box-shadow:
            0 1px 0 rgba(255, 255, 255, 0.04) inset,
            0 10px 30px rgba(0, 0, 0, 0.05),
            0 2px 8px rgba(0, 0, 0, 0.03);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;
    }

    .if-card:hover {
        transform: translateY(-3px);

        border-color: rgba(59, 130, 246, 0.28);

        box-shadow:
            0 1px 0 rgba(255, 255, 255, 0.05) inset,
            0 18px 40px rgba(0, 0, 0, 0.08),
            0 4px 14px rgba(37, 99, 235, 0.08);
    }

    /* ---------------------------------------------------------
       Metric Cards
       --------------------------------------------------------- */

    .if-metric-card {
        padding: 20px;

        border-radius: 18px;

        border:
            1px solid rgba(128, 128, 128, 0.16);

        background:
            linear-gradient(
                165deg,
                rgba(245, 158, 11, 0.05),
                rgba(128, 128, 128, 0.02) 60%
            );

        box-shadow:
            0 1px 0 rgba(255, 255, 255, 0.04) inset,
            0 8px 24px rgba(0, 0, 0, 0.05);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;
    }

    .if-metric-card:hover {
        transform: translateY(-3px);

        border-color: rgba(245, 158, 11, 0.30);

        box-shadow:
            0 1px 0 rgba(255, 255, 255, 0.05) inset,
            0 16px 34px rgba(0, 0, 0, 0.08),
            0 4px 12px rgba(245, 158, 11, 0.08);
    }

    .if-metric-label {
        font-size: 12px;
        font-weight: 600;
        opacity: 0.55;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    .if-metric-value {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.8px;

        background:
            linear-gradient(
                135deg,
                currentColor,
                currentColor 60%,
                rgba(245, 158, 11, 0.9)
            );

        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;

        transition: letter-spacing 0.25s ease;
    }s

    .if-metric-card:hover .if-metric-value {
        letter-spacing: -0.6px;
    }

    /* ---------------------------------------------------------
       Section Headers
       --------------------------------------------------------- */

    .if-section-header {
        margin-top: 28px;
        margin-bottom: 16px;
    }

    .if-section-title {
        font-size: 20px;
        font-weight: 750;
        letter-spacing: -0.4px;
    }

    .if-section-subtitle {
        margin-top: 4px;
        font-size: 13px;
        opacity: 0.55;
    }

    /* ---------------------------------------------------------
       Animation
       --------------------------------------------------------- */

    @keyframes sidebarGlow {

        0%,
        100% {
            opacity: 0.45;
            transform: scale(0.85);
        }

        50% {
            opacity: 1;
            transform: scale(1.15);
        }
    }

    </style>
    """