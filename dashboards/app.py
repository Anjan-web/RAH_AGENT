# =============================
# Path fix for Streamlit
# =============================
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# =============================
# Imports
# =============================
import streamlit as st
import pandas as pd

from config import VULNERABILITIES_CSV
from alerts.sla_dectector import detect_sla_breaches
from rag.qa_engine import build_context, build_prompt
from rag.llm import ask_llm
from notifications.email_agent import generate_email
from rag.faiss_index import build_faiss_index
from rag.semantic_qa import semantic_rag_answer


# =============================
# Page config
# =============================
st.set_page_config(
    page_title="Cybersecurity AI SOC Dashboard",
    layout="wide"
)

st.title("🛡️ Cybersecurity Vulnerability Intelligence")
st.caption("Analytics + RAG + AI Automation")

# =============================
# Load data (cached)
# =============================
@st.cache_data
def load_data():
    return pd.read_csv(VULNERABILITIES_CSV)

# -----------------------------
# 🔥 LOAD DATA & DERIVED DATASETS
# -----------------------------
df = load_data()

# SLA alerts derived ONCE
alerts_df = detect_sla_breaches(df)


@st.cache_resource
def load_faiss(df):
    return build_faiss_index(df)

faiss_index, faiss_texts, embedding_model = load_faiss(df)


# =============================
# 📊 DASHBOARD KPIs
# =============================
st.divider()
st.subheader("📊 Key Risk Metrics")

total_vulns = len(df)
critical_count = (df["severity"] == "Critical").sum()
high_count = (df["severity"] == "High").sum()
sla_breached_count = (df["sla_breached"] == 1).sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Vulnerabilities", f"{total_vulns:,}")
c2.metric("Critical", f"{critical_count:,}")
c3.metric("High", f"{high_count:,}")
c4.metric("SLA Breached", f"{sla_breached_count:,}")

st.divider()
st.subheader("📊 Severity Distribution")

severity_counts = (
    df["severity"]
    .value_counts()
    .reindex(["Critical", "High", "Medium", "Low"])
    .fillna(0)
)

st.bar_chart(severity_counts)

st.subheader("⏳ Vulnerability Aging (Days Open)")

df["aging_bucket"] = pd.cut(
    df["days_open"],
    bins=[-1, 30, 60, 90, 9999],
    labels=["0–30", "31–60", "61–90", ">90"]
)

aging_counts = df["aging_bucket"].value_counts().sort_index()

st.bar_chart(aging_counts)

st.subheader("🏭 Top Risky Owner Teams (Critical + High)")

top_teams = (
    df[df["severity"].isin(["Critical", "High"])]
    .groupby("owner_team")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_teams)


# =============================
# 🚨 SLA ALERTS SECTION
# =============================
st.divider()
st.subheader("🚨 SLA Breach Alerts")

st.metric("Active SLA Breaches", len(alerts_df))

if len(alerts_df) > 0:
    st.dataframe(alerts_df, use_container_width=True)
else:
    st.success("No SLA breaches detected 🎉")

# =============================
# 📧 AI-GENERATED EMAIL PREVIEW
# =============================
st.divider()
st.subheader("📧 AI-Generated Remediation Emails (Preview)")

if len(alerts_df) > 0:
    selected_index = st.selectbox(
        "Select an alert",
        alerts_df.index
    )

    alert_row = alerts_df.loc[selected_index].to_dict()

    if st.button("✉️ Generate AI Email"):
        with st.spinner("AI drafting remediation email..."):
            email = generate_email(alert_row)

        st.markdown("### 📬 To")
        st.code(email["to"])

        st.markdown("### 📝 Subject")
        st.code(email["subject"])

        st.markdown("### 📄 Email Body")
        st.text_area(
            "Email Content",
            email["body"],
            height=300
        )
else:
    st.info("No alerts available for email generation.")

# =============================
# 🤖 AI SECURITY ANALYST (RAG)
# =============================
st.divider()
st.markdown("## 🤖 AI Security Analyst (RAG-powered)")
st.caption("Ask questions in natural language. AI answers using live vulnerability data.")

question = st.text_input(
    "Ask the AI",
    placeholder="Why are SLA breaches high? Which team should fix issues first?"
)

if question:
    with st.spinner("🧠 AI analyzing your security posture..."):
        context = build_context(df, question)
        prompt = build_prompt(context, question)
        answer = ask_llm(prompt)

    st.markdown("### 🧠 AI Analysis & Recommendation")
    st.write(answer)

st.divider()
st.markdown("## 🧠 Semantic AI Analyst (FAISS-powered)")
st.caption("Ask high-level or vague questions. AI finds relevant vulnerabilities semantically.")

semantic_question = st.text_input(
    "Ask a semantic security question",
    placeholder="e.g. authentication related vulnerabilities"
)

if semantic_question:
    with st.spinner("🔍 Searching vulnerabilities semantically..."):
        semantic_answer = semantic_rag_answer(
            semantic_question,
            faiss_index,
            faiss_texts,
            embedding_model
        )

    st.markdown("### 🧠 AI Semantic Analysis")
    st.write(semantic_answer)

