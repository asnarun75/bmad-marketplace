"""
Daily job-hunting agent.

Run manually:  python -m job_hunter.agent
Runs via:      .github/workflows/daily_job_hunt.yml (scheduled)
"""

import os
import re
import sys
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

from jobspy import scrape_jobs
import pandas as pd

from job_hunter.config import (
    LOCATION, COUNTRY, HOURS_SINCE_POSTED, MAX_JOBS_PER_QUERY,
    MIN_SALARY_USD, SEARCH_QUERIES, OUTPUT_DIR,
)
from job_hunter.resume_tailor import tailor_resume
from job_hunter.tracker import already_tracked, record_job

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

MASTER_RESUME_PATH = Path(__file__).parent / "master_resume.md"


def load_master_resume() -> str:
    return MASTER_RESUME_PATH.read_text(encoding="utf-8")


def safe_filename(text: str) -> str:
    return re.sub(r"[^\w\-]", "_", text)[:60]


def run():
    master_resume = load_master_resume()
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    cutoff = datetime.now(timezone.utc) - timedelta(hours=HOURS_SINCE_POSTED)
    new_jobs_processed = 0

    for query in SEARCH_QUERIES:
        log.info("Searching: %s @ %s", query, LOCATION)
        try:
            jobs: pd.DataFrame = scrape_jobs(
                site_name=["indeed", "linkedin", "glassdoor"],
                search_term=query,
                location=LOCATION,
                results_wanted=MAX_JOBS_PER_QUERY,
                hours_old=HOURS_SINCE_POSTED,
                country_indeed=COUNTRY,
            )
        except Exception as exc:
            log.warning("Scrape failed for '%s': %s", query, exc)
            continue

        if jobs.empty:
            log.info("  No results.")
            continue

        log.info("  Found %d listings.", len(jobs))

        for _, row in jobs.iterrows():
            job_id    = str(row.get("id") or row.get("job_url", ""))
            title     = str(row.get("title", ""))
            company   = str(row.get("company", ""))
            location  = str(row.get("location", ""))
            url       = str(row.get("job_url", ""))
            salary    = str(row.get("min_amount") or row.get("salary_source") or "")
            desc      = str(row.get("description", ""))
            date_posted = row.get("date_posted")

            if not job_id or not desc:
                continue

            # Skip already processed
            if already_tracked(job_id):
                log.debug("  Skip (already tracked): %s @ %s", title, company)
                continue

            # Skip if salary info available and below minimum
            if row.get("min_amount"):
                try:
                    if float(row["min_amount"]) < MIN_SALARY_USD:
                        log.debug("  Skip (salary too low): %s @ %s", title, company)
                        continue
                except (ValueError, TypeError):
                    pass

            log.info("  Tailoring resume for: %s @ %s", title, company)
            try:
                tailored = tailor_resume(
                    master_resume=master_resume,
                    job_title=title,
                    company=company,
                    location=location,
                    job_description=desc,
                )
            except Exception as exc:
                log.error("  Claude API error for %s @ %s: %s", title, company, exc)
                continue

            fname = f"{datetime.utcnow().strftime('%Y%m%d')}_{safe_filename(company)}_{safe_filename(title)}.md"
            fpath = output_dir / fname
            fpath.write_text(tailored, encoding="utf-8")

            record_job(
                job_id=job_id,
                title=title,
                company=company,
                location=location,
                salary=salary,
                url=url,
                resume_file=str(fpath),
            )
            log.info("  Saved: %s", fpath.name)
            new_jobs_processed += 1

    log.info("Done. Tailored resumes for %d new job(s).", new_jobs_processed)
    return new_jobs_processed


if __name__ == "__main__":
    sys.exit(0 if run() >= 0 else 1)
