import pandas as pd

def compute_scores(df):
    risk_weights = {
        "Access Control": 1.2,
        "Identity Management": 1.1,
        "Network Security": 1.3,
        "Monitoring & Detection": 1.2,
        "Vulnerability Management": 1.4,
        "Policy Compliance": 1.0,
        "Audit & Assurance": 1.0,
        "Risk Management": 1.3,
        "Business Continuity": 1.1,
        "Incident Response": 1.2,
        "Data Privacy": 1.3,
        "DevSecOps": 1.2
    }
    df['Score'] = df.apply(lambda row: round(row['Value'] * 100 * risk_weights.get(row['Domain'], 1.0)), axis=1)
    return df