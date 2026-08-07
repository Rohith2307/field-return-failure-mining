import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )

client = genai.Client(api_key=api_key)


def generate_insights(df):

    sample = df.head(30).to_csv(index=False)

    prompt = f"""
You are a Senior Reliability Engineer.

Analyze the following field-return dataset.

{sample}

Generate:

1. Executive Summary

2. Top Failure Patterns

3. Root Cause Analysis

4. Engineering Recommendations

5. Preventive Actions

Keep the response concise.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    return response.text