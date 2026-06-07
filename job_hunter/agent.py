"""
Daily job-hunting agent.

Run manually:  python -m job_hunter.agent
Runs via:      .github/workflows/daily_job_hunt.yml (scheduled daily)
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
import re

from job_hunter.config import SEARCH_QUERIES, MIN_SALARY_USD, OUTPUT_DIR
from job_hunter.scraper import search_jobs
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

    new_jobs = 0

    for query in SEARCH_QUERIES:
        log.info("Searching: %s", query)
        jobs = search_jobs(query)

        if not jobs:
            log.info("  No results.")
            continue

        log.info("  Found %d listings.", len(jobs))

        for job in jobs:
            job_id   = job["job_id"]
            title    = job["title"]
            company  = job["company"]
            location = job["location"]
            url      = job["url"]
            desc     = job["description"]
            sal_min  = job["salary_min"]

            if not job_id or not desc:
                continue

            if already_tracked(job_id):
                log.debug("  Skip (seen): %s @ %s", title, company)
                continue

            # Skip if salary data available and below floor
            if sal_min and sal_min < MIN_SALARY_USD:
                log.info("  Skip (salary $%s < $%s): %s @ %s",
                         f"{sal_min:,.0f}", f"{MIN_SALARY_USD:,.0f}", title, company)
                continue

            log.info("  Tailoring resume → %s @ %s", title, company)
            try:
                tailored = tailor_resume(
                    master_resume=master_resume,
                    job_title=title,
                    company=company,
                    location=location,
                    job_description=desc,
                )
            except Exception as exc:
                log.error("  Claude API error: %s", exc)
                continue

            fname = (
                f"{datetime.utcnow().strftime('%Y%m%d')}"
                f"_{safe_filename(company)}"
                f"_{safe_filename(title)}.md"
            )
            fpath = output_dir / fname
            fpath.write_text(tailored, encoding="utf-8")

            record_job(
                job_id=job_id,
                title=title,
                company=company,
                location=location,
                salary=f"{sal_min}-{job['salary_max']}",
                url=url,
                resume_file=str(fpath),
            )
            log.info("  Saved: %s", fname)
            new_jobs += 1

    log.info("Done. Tailored %d new resume(s).", new_jobs)
    return new_jobs


if __name__ == "__main__":
    sys.exit(0 if run() >= 0 else 1)
