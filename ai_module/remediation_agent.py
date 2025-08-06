import os
from dotenv import load_dotenv
import openai
import pandas as pd

# Load API Key from Streamlit secrets or .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY in your environment variables or Streamlit secrets.")

# Create OpenAI client
client = openai.OpenAI(api_key=api_key)


def gpt_remediation(control, score, domain):
    """
    Ask GPT for a remediation recommendation and priority using the new OpenAI API.
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
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Small & fast GPT model
            messages=[
                {"role": "system", "content": "You are an expert in compliance and security frameworks."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=120
        )

        reply = response.choices[0].message.content.strip()

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
        return (
            f"Unable to generate recommendation. Error: {str(e)}",
            "Schedule"
        )



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
