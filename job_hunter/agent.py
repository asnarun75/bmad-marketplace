"""
Daily job-hunting agent.

Run manually:  python -m job_hunter.agent
Runs via:      .github/workflows/daily_job_hunt.yml (scheduled daily)
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
import re

from job_hunter.config import SEARCH_QUERIES, MIN_SALARY_USD, OUTPUT_DIR
from job_hunter.scraper import search_jobs
from job_hunter.resume_tailor import tailor_resume_claude, tailor_resume_openai
from job_hunter.tracker import already_tracked, record_job
from job_hunter.pdf_generator import markdown_to_pdf

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

            stem = (
                f"{datetime.utcnow().strftime('%Y%m%d')}"
                f"_{safe_filename(company)}"
                f"_{safe_filename(title)}"
            )

            saved_any = False

            # ── Claude version ────────────────────────────────────────────
            try:
                claude_md = tailor_resume_claude(
                    master_resume=master_resume,
                    job_title=title, company=company,
                    location=location, job_description=desc,
                )
                claude_md_path  = output_dir / f"{stem}_claude.md"
                claude_pdf_path = output_dir / f"{stem}_claude.pdf"
                claude_md_path.write_text(claude_md, encoding="utf-8")
                try:
                    markdown_to_pdf(claude_md, claude_pdf_path)
                    log.info("  Claude PDF: %s", claude_pdf_path.name)
                except Exception as exc:
                    log.warning("  Claude PDF failed: %s", exc)
                saved_any = True
            except Exception as exc:
                log.error("  Claude API error: %s", exc)

            # ── OpenAI version (if key available) ─────────────────────────
            if os.environ.get("OPENAI_API_KEY"):
                try:
                    oai_md = tailor_resume_openai(
                        master_resume=master_resume,
                        job_title=title, company=company,
                        location=location, job_description=desc,
                    )
                    oai_md_path  = output_dir / f"{stem}_openai.md"
                    oai_pdf_path = output_dir / f"{stem}_openai.pdf"
                    oai_md_path.write_text(oai_md, encoding="utf-8")
                    try:
                        markdown_to_pdf(oai_md, oai_pdf_path)
                        log.info("  OpenAI PDF: %s", oai_pdf_path.name)
                    except Exception as exc:
                        log.warning("  OpenAI PDF failed: %s", exc)
                    saved_any = True
                except Exception as exc:
                    log.error("  OpenAI API error: %s", exc)

            if not saved_any:
                continue

            record_job(
                job_id=job_id,
                title=title,
                company=company,
                location=location,
                salary=f"{sal_min}-{job['salary_max']}",
                url=url,
                resume_file=stem,
            )
            log.info("  Done: %s", stem)
            new_jobs += 1

    log.info("Done. Tailored %d new resume(s).", new_jobs)
    return new_jobs


if __name__ == "__main__":
    sys.exit(0 if run() >= 0 else 1)
