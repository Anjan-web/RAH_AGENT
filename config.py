import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR=Path(__file__).resolve().parent

DATA_DIR=BASE_DIR/"data"
RAW_DATA_DIR=DATA_DIR / "raw"
PROCESSED_DATA_DIR=DATA_DIR/"processed"
VULNERABILITIES_CSV=RAW_DATA_DIR/"vulnerabilities.csv"

LOG_DIR=BASE_DIR/"logs"


for path in[DATA_DIR,RAW_DATA_DIR,PROCESSED_DATA_DIR,LOG_DIR]:
    path.mkdir(parents=True,exist_ok=True)