import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF
import numpy as np

from ingestion.normalize import normalize_data
from scoring.score_engine import compute_scores
from ai_module.remediation_agent import suggest_remediations
from dashboard.visuals import radar_chart, heatmap


def generate_pdf(df):
    from datetime import datetime
    import os
    from io import BytesIO

    class PDFReport(FPDF):
        def header(self):
            # Logo (optional - place logo.png in dashboard/)
            logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
            if os.path.exists(logo_path):
                self.image(logo_path, 10, 8, 20)  # x, y, width

            # Title
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, "Compliance Summary Report", ln=True, align='C')

            # Date
            self.set_font('Arial', '', 10)
            self.cell(0, 5, f"Generated on: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
            self.ln(10)

        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(150)
            self.cell(0, 10, "Confidential - For Internal Use Only", 0, 0, 'C')

    # Create PDF object
    pdf = PDFReport()
    pdf.add_page()

    # Executive Summary
    pdf.set_font("Arial", '', 11)
    summary_text = (
        "This report summarizes the current compliance performance against key ISO controls. "
        "Controls scoring below 70 require immediate attention. Higher scores indicate strong performance."
    )
    pdf.multi_cell(0, 6, summary_text)
    pdf.ln(5)

    # Table Header
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(41, 128, 185)  # Blue header
    pdf.set_text_color(255, 255, 255)
    pdf.cell(60, 8, "Control", 1, 0, 'C', fill=True)
    pdf.cell(30, 8, "Score", 1, 0, 'C', fill=True)
    pdf.cell(100, 8, "Recommendation", 1, 1, 'C', fill=True)

    # Table Rows
    pdf.set_font("Arial", '', 10)
    for _, row in df.iterrows():
        control = str(row.get("Control", ""))
        score = int(row.get("Score", 0))
        recommendation = str(row.get("Remediation", ""))

        # Color code score cell
        if score < 50:
            pdf.set_fill_color(231, 76, 60)  # Red
            score_text_color = (255, 255, 255)
        elif score < 70:
            pdf.set_fill_color(241, 196, 15)  # Yellow
            score_text_color = (0, 0, 0)
        else:
            pdf.set_fill_color(46, 204, 113)  # Green
            score_text_color = (255, 255, 255)

        # Control
        pdf.set_text_color(0, 0, 0)
        pdf.cell(60, 8, control, 1)

        # Score (with background color)
        pdf.set_text_color(*score_text_color)
        pdf.cell(30, 8, str(score), 1, 0, 'C', fill=True)

        # Recommendation
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(100, 8, recommendation, border=1)

    # Output as BytesIO for Streamlit download
    output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    output.write(pdf_bytes)
    output.seek(0)
    return output



def generate_insights(df):
    low_score_controls = df[df['Score'] < 70].sort_values(by='Score')
    weakest_domains = df.groupby('Domain')['Score'].mean().sort_values().head(3)

    insights = []
    if not low_score_controls.empty:
        insights.append("🚨 Top Risky Controls:")
        for _, row in low_score_controls.head(5).iterrows():
            insights.append(f"- {row['Control']} in {row['Domain']} scored {row['Score']}")

    insights.append("\n📉 Weakest Performing Domains:")
    for domain, avg_score in weakest_domains.items():
        insights.append(f"- {domain}: Avg Score {round(avg_score, 2)}")

    return insights


def run_dashboard(_):
    st.set_page_config(page_title="Compliance Dashboard", layout="wide")
    st.sidebar.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/512px-React-icon.svg.png",
        width=80
    )
    st.sidebar.title("🔐 Compliance Portal")
    st.sidebar.markdown("Select a file to begin analysis.")

    st.title("📊 Compliance Posture Dashboard")
    st.markdown(
        "Upload your compliance dataset to begin analysis. The dashboard visualizes KPIs and recommends remediation strategies."
    )

    uploaded_file = st.sidebar.file_uploader("📎 Upload a CSV file", type="csv")
    if uploaded_file is not None:
        df = normalize_data(uploaded_file)
        df = compute_scores(df)

        # ✅ Simulate urgency if not present
        if 'Urgency' not in df.columns:
            df['Urgency'] = np.random.choice(['High', 'Low'], size=len(df))

        df = suggest_remediations(df)

        st.markdown("---")
        framework = st.selectbox("🔍 Select Compliance Framework", sorted(df["Framework"].unique()))
        domain = st.selectbox("📂 Select Domain", sorted(df["Domain"].unique()))
        filtered = df[(df["Framework"] == framework) & (df["Domain"] == domain)]

        st.metric("🔢 Average Compliance Score", round(filtered["Score"].mean(), 2))
        st.bar_chart(filtered.set_index("Control")["Score"])

        with st.expander("📈 Advanced Visualizations"):
            radar_chart(df)
            heatmap(df)

        with st.expander("🧠 Smart Insights"):
            insights = generate_insights(df)
            for tip in insights:
                st.markdown(tip)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="💾 Download CSV",
                data=filtered.to_csv(index=False),
                file_name="compliance_summary.csv",
                mime="text/csv"
            )

        with col2:
            st.download_button(
                label="🧾 Download PDF",
                data=generate_pdf(filtered),
                file_name="compliance_summary.pdf",
                mime="application/pdf"
            )

        st.markdown("---")
        st.subheader("💡 Remediation Suggestions")
        for _, row in filtered.iterrows():
            if row["Score"] < 70:
                st.markdown(f"**{row['Control']}** — {row['Remediation']}")
