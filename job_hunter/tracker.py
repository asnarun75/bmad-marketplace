import csv
import os
from datetime import datetime
from job_hunter.config import TRACKER_CSV


FIELDS = ["date", "job_id", "title", "company", "location", "salary", "url", "resume_file", "status"]


def _ensure_csv():
    os.makedirs(os.path.dirname(TRACKER_CSV), exist_ok=True)
    if not os.path.exists(TRACKER_CSV):
        with open(TRACKER_CSV, "w", newline="") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()


def already_tracked(job_id: str) -> bool:
    _ensure_csv()
    with open(TRACKER_CSV, "r") as f:
        return any(row["job_id"] == job_id for row in csv.DictReader(f))


def record_job(job_id: str, title: str, company: str, location: str,
               salary: str, url: str, resume_file: str):
    _ensure_csv()
    with open(TRACKER_CSV, "a", newline="") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerow({
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "job_id": job_id,
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "url": url,
            "resume_file": resume_file,
            "status": "tailored",
        })
