import os
import pandas as pd
from ingestion.normalize import normalize_data
from scoring.score_engine import compute_scores
from ai_module.remediation_agent import suggest_remediations
from dashboard.app import run_dashboard

def main():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/normalized", exist_ok=True)
    print("[+] Starting dashboard...")
    run_dashboard(None)

if __name__ == "__main__":
    main()