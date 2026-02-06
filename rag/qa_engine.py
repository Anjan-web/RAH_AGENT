import pandas as pd

from typing import List


def build_context(df:pd.DataFrame,question:str,max_rows:int=10)->str:
    """
    Select relevant rows from dataframe based on keywords in question
    and build a textual context for the LLM.
    """

    q=question.lower()
    filtered=df

    if "Critical"in q:
        filtered=filtered[filtered["severity"=="Critical"]]
    if "high"in q:
        filtered = filtered[filtered['severity'].isin(["Critical", "High"])]

    
    if "sla" in q:
        filtered = filtered[filtered["sla_breached"] == 1]

    if "team" in q:
        filtered = filtered.sort_values("risk_score", ascending=False)

    if "log4shell" in q:
        filtered = filtered[filtered["vuln_title"].str.contains("log4shell", case=False)]
    

    filtered=filtered.head(max_rows)

    context_lines: List[str] = []

    for _, row in filtered.iterrows():
        context_lines.append(
            f"""Finding ID: {row['finding_id']}
Severity: {row['severity']}
CVE: {row['cve_id']}
Title: {row['vuln_title']}
Days Open: {row['days_open']}
Owner Team: {row['owner_team']}
Risk Score: {row['risk_score']}
Remediation: {row['remediation']}
"""
        )
    return "\n".join(context_lines  )



def build_prompt(context:str,question:str)->str:
    return f"""
You are a cybersecurity analyst.

Answer the user's question using ONLY the information provided below.
If information is insufficient, say so clearly.

DATA:
{context}

QUESTION:
{question}

Provide:
1. Clear explanation
2. Risk impact
3. Actionable recommendation
"""
    
