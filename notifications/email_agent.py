
from rag.llm import ask_llm

def generate_email(alert_row:dict)->dict:
    """
    Generate AI-written email for a vulnerability alert.
    """

    context=f"""Finding ID: {alert_row['finding_id']}
Severity: {alert_row['severity']}
CVE: {alert_row['cve_id']}
Days Open: {alert_row['days_open']}
SLA Days: {alert_row['sla_days']}
Owner Team: {alert_row['owner_team']}
Remediation: {alert_row['remediation']}
"""
    prompt=f"""
You are a cybersecurity incident response analyst.

Write a professional, concise email to the responsible engineering team.

Include:
- Why this is critical
- Business risk
- Clear remediation steps
- Urgency (SLA breached)

DATA:
{context}"""
    email_body=ask_llm(prompt)
    return{"to": alert_row["owner_email"],
        "subject": f"[ACTION REQUIRED] {alert_row['severity']} Vulnerability – {alert_row['cve_id']}",
        "body": email_body}
    
