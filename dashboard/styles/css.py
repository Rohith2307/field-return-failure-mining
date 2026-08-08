"""
Global UI styling for InsightForge AI
"""


def load_css() -> str:

    return """
<style>

:root {
    --if-blue: #2563EB;
    --if-indigo: #6366F1;
    --if-cyan: #06B6D4;
    --if-green: #22C55E;
}


/* =========================================================
   GLOBAL
   ========================================================= */

html {
    scroll-behavior: smooth;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 4rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(37, 99, 235, 0.06),
            transparent 28%
        ),
        radial-gradient(
            circle at 10% 80%,
            rgba(99, 102, 241, 0.045),
            transparent 25%
        );
}


/* =========================================================
   TYPOGRAPHY
   ========================================================= */

h1,
h2,
h3,
h4 {
    color: var(--text-color) !important;
    font-weight: 700 !important;
}

h1 {
    letter-spacing: -1.5px;
}

h2 {
    letter-spacing: -0.7px;
}

h3 {
    letter-spacing: -0.3px;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128, 128, 128, 0.16);

    background:
        linear-gradient(
            180deg,
            rgba(99, 102, 241, 0.045),
            transparent 45%
        );
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

section[data-testid="stSidebar"] .stRadio label {
    border-radius: 10px;
    padding: 6px 8px;
    transition: all 0.18s ease;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(37, 99, 235, 0.08);
    transform: translateX(3px);
}


/* =========================================================
   HERO
   ========================================================= */

.hero-section {
    position: relative;
    overflow: hidden;

    padding: 42px 46px;
    margin-bottom: 28px;

    border-radius: 26px;

    background:
        linear-gradient(
            135deg,
            rgba(37, 99, 235, 0.16),
            rgba(99, 102, 241, 0.10),
            rgba(6, 182, 212, 0.05)
        );

    border: 1px solid rgba(99, 102, 241, 0.20);

    box-shadow:
        0 15px 45px rgba(15, 23, 42, 0.10);

    animation: ifFadeUp 0.6s ease;
}

.hero-section::before {
    content: "";

    position: absolute;

    width: 280px;
    height: 280px;

    right: -80px;
    top: -120px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(59, 130, 246, 0.24),
            transparent 68%
        );

    pointer-events: none;
}

.hero-section::after {
    content: "";

    position: absolute;

    width: 180px;
    height: 180px;

    right: 170px;
    bottom: -130px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(6, 182, 212, 0.10),
            transparent 70%
        );

    pointer-events: none;
}

.hero-section h1 {
    position: relative;

    font-size: 42px !important;

    margin: 8px 0 !important;

    z-index: 2;
}

.hero-section p {
    position: relative;

    max-width: 760px;

    font-size: 16px;

    line-height: 1.65;

    opacity: 0.72;

    z-index: 2;
}

.hero-badge {
    position: relative;

    display: inline-block;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.6px;

    color: var(--if-blue);

    z-index: 2;
}


/* =========================================================
   SECTION LABELS
   ========================================================= */

.section-label {
    margin-top: 10px;
    margin-bottom: 12px;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.7px;

    opacity: 0.48;

    animation: ifFadeUp 0.45s ease;
}


/* =========================================================
   METRIC CARDS
   ========================================================= */

div[data-testid="stMetric"] {
    position: relative;
    overflow: hidden;

    min-height: 112px;

    padding: 20px !important;

    border-radius: 18px !important;

    background:
        linear-gradient(
            145deg,
            var(--secondary-background-color),
            rgba(37, 99, 235, 0.025)
        ) !important;

    border: 1px solid rgba(128, 128, 128, 0.17);

    box-shadow:
        0 5px 20px rgba(15, 23, 42, 0.055);

    transition:
        transform 0.22s ease,
        box-shadow 0.22s ease,
        border-color 0.22s ease;

    animation: ifFadeUp 0.55s ease;
}

div[data-testid="stMetric"]::after {
    content: "";

    position: absolute;

    width: 80px;
    height: 80px;

    right: -35px;
    top: -35px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(37, 99, 235, 0.12),
            transparent 70%
        );
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-5px);

    border-color:
        rgba(37, 99, 235, 0.28);

    box-shadow:
        0 14px 32px rgba(15, 23, 42, 0.11);
}

div[data-testid="stMetric"] label {
    color: var(--text-color) !important;

    opacity: 0.62;

    font-size: 12px !important;

    font-weight: 600 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--text-color) !important;

    font-size: 29px !important;

    font-weight: 750 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-size: 11px !important;
}


/* =========================================================
   HEALTH BANNER
   ========================================================= */

.health-banner {
    display: flex;

    align-items: center;

    gap: 18px;

    padding: 18px 22px;

    margin: 5px 0 20px 0;

    border-radius: 17px;

    background:
        linear-gradient(
            110deg,
            var(--secondary-background-color),
            rgba(34, 197, 94, 0.035)
        );

    border: 1px solid rgba(128, 128, 128, 0.16);

    box-shadow:
        0 6px 20px rgba(15, 23, 42, 0.055);

    animation: ifFadeUp 0.7s ease;
}

.health-icon {
    width: 44px;
    height: 44px;

    min-width: 44px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 50%;

    font-size: 19px;

    font-weight: 800;
}

.health-good .health-icon {
    background: rgba(34, 197, 94, 0.15);
}

.health-warning .health-icon {
    background: rgba(234, 179, 8, 0.15);
}

.health-critical .health-icon {
    background: rgba(239, 68, 68, 0.15);
}

.health-title {
    font-size: 16px;
    font-weight: 700;
}

.health-description {
    margin-top: 4px;

    font-size: 13px;

    opacity: 0.62;
}


/* =========================================================
   CHART CONTAINERS
   ========================================================= */

div[data-testid="stPlotlyChart"] {
    padding: 8px;

    border-radius: 18px;

    background:
        var(--secondary-background-color);

    border: 1px solid rgba(128, 128, 128, 0.13);

    box-shadow:
        0 5px 18px rgba(15, 23, 42, 0.045);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;

    animation: ifFadeUp 0.65s ease;
}

div[data-testid="stPlotlyChart"]:hover {
    transform: translateY(-2px);

    box-shadow:
        0 10px 28px rgba(15, 23, 42, 0.075);
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    border-radius: 10px !important;

    min-height: 42px;

    font-weight: 650 !important;

    border: 1px solid rgba(128, 128, 128, 0.20);

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 7px 18px rgba(37, 99, 235, 0.18);
}


/* =========================================================
   FILE UPLOADER
   ========================================================= */

div[data-testid="stFileUploader"] {
    padding: 8px;

    border-radius: 18px;

    border: 1px dashed rgba(37, 99, 235, 0.30);

    background:
        rgba(37, 99, 235, 0.025);

    transition:
        border-color 0.2s ease,
        background 0.2s ease;
}

div[data-testid="stFileUploader"]:hover {
    border-color: rgba(37, 99, 235, 0.60);

    background:
        rgba(37, 99, 235, 0.055);
}


/* =========================================================
   INPUTS
   ========================================================= */

div[data-baseweb="select"] > div {
    border-radius: 10px !important;
}

div[data-testid="stTextInput"] input {
    border-radius: 10px !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: var(--if-blue) !important;

    box-shadow:
        0 0 0 2px rgba(37, 99, 235, 0.12) !important;
}


/* =========================================================
   ALERTS
   ========================================================= */

div[data-testid="stAlert"] {
    border-radius: 15px !important;

    background:
        var(--secondary-background-color) !important;

    color:
        var(--text-color) !important;

    border: 1px solid rgba(128, 128, 128, 0.16) !important;

    box-shadow:
        0 4px 16px rgba(15, 23, 42, 0.045);
}

div[data-testid="stAlert"] p {
    color: var(--text-color) !important;
}


/* =========================================================
   DATA TABLES
   ========================================================= */

div[data-testid="stDataFrame"] {
    border-radius: 15px;

    overflow: hidden;

    border: 1px solid rgba(128, 128, 128, 0.15);

    box-shadow:
        0 5px 18px rgba(15, 23, 42, 0.045);
}


/* =========================================================
   DIVIDERS
   ========================================================= */

hr {
    margin-top: 1.7rem;
    margin-bottom: 1.7rem;

    opacity: 0.18;
}


/* =========================================================
   PLOTLY MODEBAR
   ========================================================= */

div.modebar {
    opacity: 1 !important;
}

div.modebar-group {
    opacity: 1 !important;
}

.modebar-btn {
    opacity: 1 !important;
}

.modebar-btn svg {
    fill: currentColor !important;
}

.modebar-btn:hover svg {
    fill: #2563EB !important;
}

.js-plotly-plot .plotly .modebar {
    background:
        var(--secondary-background-color) !important;

    border-radius: 8px;
}


/* =========================================================
   FOOTER
   ========================================================= */

.dashboard-footer {
    margin-top: 55px;

    padding: 25px 0;

    text-align: center;

    border-top: 1px solid rgba(128, 128, 128, 0.14);

    opacity: 0.50;

    font-size: 10px;

    letter-spacing: 1.5px;
}

.dashboard-footer span {
    display: block;

    margin-top: 6px;

    font-size: 11px;

    letter-spacing: 0;
}


/* =========================================================
   ANIMATIONS
   ========================================================= */

@keyframes ifFadeUp {

    from {
        opacity: 0;

        transform:
            translateY(14px);
    }

    to {
        opacity: 1;

        transform:
            translateY(0);
    }
}

@keyframes ifPulse {

    0%, 100% {
        opacity: 0.65;
    }

    50% {
        opacity: 1;
    }
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 900px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero-section {
        padding: 30px 25px;
    }

    .hero-section h1 {
        font-size: 32px !important;
    }
}



/* =========================================================
   INSIGHTFORGE PREMIUM SIDEBAR
   ========================================================= */

.if-sidebar-brand {
    padding: 18px 4px 12px 4px;
}

.if-brand-title {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -0.8px;
}

.if-brand-subtitle {
    margin-top: 8px;
    font-size: 12px;
    opacity: 0.55;
}

.if-sidebar-divider {
    height: 1px;

    margin:
        20px 0 28px 0;

    background:
        rgba(128, 128, 128, 0.15);
}


/* ---------------------------------------------------------
   Navigation Buttons
   --------------------------------------------------------- */

section[data-testid="stSidebar"]
.stButton {
    margin-bottom: 12px;
}


section[data-testid="stSidebar"]
.stButton > button {

    position: relative;

    height: 64px !important;

    padding:
        0 20px !important;

    border-radius: 18px !important;

    border:
        1px solid rgba(128, 128, 128, 0.14) !important;

    background:
        rgba(128, 128, 128, 0.025) !important;

    font-size: 16px !important;

    font-weight: 650 !important;

    text-align: left !important;

    transition:
        transform 0.2s ease,
        background 0.2s ease,
        border-color 0.2s ease,
        box-shadow 0.2s ease !important;
}


/* ---------------------------------------------------------
   Hover
   --------------------------------------------------------- */

section[data-testid="stSidebar"]
.stButton > button:hover {

    transform:
        translateX(4px);

    background:
        rgba(37, 99, 235, 0.08) !important;

    border-color:
        rgba(37, 99, 235, 0.30) !important;

    box-shadow:
        0 8px 24px
        rgba(37, 99, 235, 0.08) !important;
}


/* ---------------------------------------------------------
   Primary = Active Page
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
        inset 4px 0 0 #2563EB,
        0 10px 30px
        rgba(37, 99, 235, 0.10) !important;
}


/* ---------------------------------------------------------
   Active Glow
   --------------------------------------------------------- */

section[data-testid="stSidebar"]
.stButton > button[kind="primary"]::after {

    content: "";

    position: absolute;

    right: 18px;

    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #3B82F6;

    box-shadow:
        0 0 12px
        rgba(59, 130, 246, 0.75);

    animation:
        sidebarGlow 2s ease-in-out infinite;
}


/* ---------------------------------------------------------
   Button Text
   --------------------------------------------------------- */

section[data-testid="stSidebar"]
.stButton > button p {

    font-size: 16px !important;

    font-weight: 650 !important;

    letter-spacing: -0.15px;
}


/* ---------------------------------------------------------
   Remove Streamlit Focus Outline
   --------------------------------------------------------- */

section[data-testid="stSidebar"]
.stButton > button:focus {

    box-shadow:
        inset 4px 0 0 #2563EB,
        0 10px 30px
        rgba(37, 99, 235, 0.10) !important;
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