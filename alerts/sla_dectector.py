import pandas as pd



def detect_sla_breaches(df:pd.DataFrame)->pd.DataFrame:
    """
    Detect SLA-breached vulnerabilities that require alerts....
    """

    if df.empty:
        return pd.DataFrame()
    
    alerts_df=df.copy()

    alerts_df["severity"]=alerts_df["severity"].str.strip()

    alerts_df["sla_breached"]=alerts_df["sla_breached"].astype(bool)

    alerts_df=alerts_df[
        (alerts_df["sla_breached"]==True)&
        (alerts_df["severity"].isin(["Critical","High"]))
    ]

    alerts_df=alerts_df.sort_values(
        by=["severity","days_open","risk_score"],
        ascending=[True,False,False]
    )

    alert_columns = [
    "finding_id",
    "severity",
    "hostname",
    "vuln_title",
    "cve_id",
    "days_open",
    "sla_days",
    "owner_team",
    "owner_email",
    "remediation"]

    return alerts_df[alert_columns].reset_index(drop=True)
