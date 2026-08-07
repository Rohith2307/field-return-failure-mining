"""
Global CSS for InsightForge AI.
"""


def load_css() -> str:
    return """
    <style>

    .block-container{
        padding-top:2rem;
        padding-bottom:2rem;
        padding-left:3rem;
        padding-right:3rem;
    }

    div[data-testid="stMetric"]{
        background:white;
        border-radius:18px;
        padding:20px;
        box-shadow:0px 4px 14px rgba(15,23,42,0.08);
    }

    h1,h2,h3{
        color:#0F172A;
    }

    </style>
    """