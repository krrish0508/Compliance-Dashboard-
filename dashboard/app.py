import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF
from ingestion.normalize import normalize_data
from scoring.score_engine import compute_scores
from ai_module.remediation_agent import suggest_remediations
from dashboard.visuals import radar_chart, heatmap

def generate_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Compliance Summary", ln=True, align="C")
    for index, row in df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Control']}: Score {row['Score']} - {row['Remediation']}", ln=True)
    output = BytesIO()
    pdf.output(name=output, dest='S')
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
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/512px-React-icon.svg.png", width=80)
    st.sidebar.title("🔐 Compliance Portal")
    st.sidebar.markdown("Select a file to begin analysis.")

    st.title("📊 Compliance Posture Dashboard")
    st.markdown("Upload your compliance dataset to begin analysis. The dashboard visualizes KPIs and recommends remediation strategies.")

    uploaded_file = st.sidebar.file_uploader("📎 Upload a CSV file", type="csv")
    if uploaded_file is not None:
        df = normalize_data(uploaded_file)
        df = compute_scores(df)
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