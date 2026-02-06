import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd

def build_vulnerability_text(row:pd.Series)->str:
    """
    Convert a vulnerability row into rich natural-language text.
    """ 

    return f"""
    Vulnerability Title: {row['vuln_title']}
    Severity: {row['severity']}
    CVE: {row['cve_id']}
    Asset: {row['hostname']}
    Asset Type: {row['asset_type']}
    Operating System: {row['os_family']}
    Days Open: {row['days_open']}
    Region: {row['region']}
    MITRE Tactic: {row['mitre_tactic']}
    Exploited in Wild: {row['exploited_in_wild']}
    Remediation: {row['remediation']}"""


def build_faiss_index(df:pd.DataFrame):

    model=SentenceTransformer("all-MiniLM-L6-v2")

    texts=df.apply(build_vulnerability_text,axis=1).to_list()

    embedings=model.encode(texts,
                           convert_to_numpy=True,
                           show_progress_bar=True)
    
    dimensions=embedings.shape[1]

    index=faiss.IndexFlatL2(dimensions)

    index.add(np.array(embedings))

    return index,texts,model
