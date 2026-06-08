"""
Job scraper using Adzuna API — works reliably from server/cloud IPs.
Free tier: 1000 calls/month. Register at: https://developer.adzuna.com
"""

import os
import logging
import requests
from datetime import datetime, timezone, timedelta
from job_hunter.config import LOCATION, COUNTRY, HOURS_SINCE_POSTED, MAX_JOBS_PER_QUERY

log = logging.getLogger(__name__)

ADZUNA_BASE = "https://api.adzuna.com/v1/api/jobs"

# Map country codes to Adzuna region slugs
COUNTRY_MAP = {"US": "us", "GB": "gb", "CA": "ca", "AU": "au"}


def _adzuna_credentials():
    app_id  = os.environ.get("ADZUNA_APP_ID")
    app_key = os.environ.get("ADZUNA_API_KEY")
    if not app_id or not app_key:
        raise EnvironmentError(
            "ADZUNA_APP_ID and ADZUNA_API_KEY must be set. "
            "Register free at https://developer.adzuna.com"
        )
    return app_id, app_key


def search_jobs(query: str) -> list[dict]:
    """Return list of job dicts matching query, posted within HOURS_SINCE_POSTED."""
    app_id, app_key = _adzuna_credentials()
    region = COUNTRY_MAP.get(COUNTRY.upper(), "us")

    # Adzuna uses city name; strip state portion
    city = LOCATION.split(",")[0].strip()

    cutoff_days = max(1, HOURS_SINCE_POSTED // 24)

    params = {
        "app_id":        app_id,
        "app_key":       app_key,
        "results_per_page": MAX_JOBS_PER_QUERY,
        "what":          query,
        "where":         city,
        "distance":      50,          # km radius
        "max_days_old":  cutoff_days,
        "content-type":  "application/json",
        "sort_by":       "date",
    }

    url = f"{ADZUNA_BASE}/{region}/search/1"
    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code == 403:
            log.error(
                "Adzuna API blocked (403). If running locally, this is expected — "
                "cloud container IPs are blocked. Run via GitHub Actions instead. "
                "Response: %s", resp.text[:200]
            )
            return []
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as exc:
        log.warning("Adzuna request failed for '%s': %s", query, exc)
        return []

    jobs = []
    for item in data.get("results", []):
        salary_min = item.get("salary_min") or 0
        jobs.append({
            "job_id":       item.get("id", ""),
            "title":        item.get("title", ""),
            "company":      item.get("company", {}).get("display_name", ""),
            "location":     item.get("location", {}).get("display_name", ""),
            "url":          item.get("redirect_url", ""),
            "description":  item.get("description", ""),
            "salary_min":   salary_min,
            "salary_max":   item.get("salary_max") or 0,
            "date_posted":  item.get("created", ""),
        })

    return jobs
