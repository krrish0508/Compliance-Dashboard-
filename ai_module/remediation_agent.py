import os
from dotenv import load_dotenv
import openai
import pandas as pd

# Load API Key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("❌ OPENAI_API_KEY not found. Please set it in .env or Streamlit Secrets.")

def gpt_remediation(control, score, domain):
    """
    Ask GPT for a remediation recommendation and priority.
    """
    prompt = f"""
    You are an ISO 27001 compliance consultant.
    Control: {control}
    Domain: {domain}
    Current Compliance Score: {score}/100

    1. Write a concise remediation recommendation in 1–2 sentences.
    2. Suggest a priority: 'Do First', 'Schedule', 'Delegate', or 'Eliminate'.
    Format your response as:
    Recommendation: <text>
    Priority: <priority>
    """

    try:
        print(f"🔍 Sending request to GPT for control: {control} | Score: {score} | Domain: {domain}")

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Try gpt-3.5-turbo if gpt-4o-mini fails
            messages=[
                {"role": "system", "content": "You are an expert in compliance and security frameworks."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=120
        )

        reply = response.choices[0].message["content"].strip()
        print(f"✅ GPT raw reply: {reply}")

        # Parse GPT's structured output
        recommendation = ""
        priority = ""
        for line in reply.split("\n"):
            if line.lower().startswith("recommendation:"):
                recommendation = line.split(":", 1)[1].strip()
            elif line.lower().startswith("priority:"):
                priority = line.split(":", 1)[1].strip()

        return recommendation, priority

    except Exception as e:
        error_message = f"❌ GPT request failed: {str(e)}"
        print(error_message)
        return (error_message, "Schedule")


def suggest_remediations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enhance the DataFrame with GPT‑generated remediation recommendations & priorities.
    """
    remediations = []
    priorities = []

    for _, row in df.iterrows():
        control = row.get("Control", "")
        score = row.get("Score", 0)
        domain = row.get("Domain", "")

        recommendation, priority = gpt_remediation(control, score, domain)

        remediations.append(recommendation)
        priorities.append(priority)

    df["Remediation"] = remediations
    df["Priority"] = priorities
    return df
