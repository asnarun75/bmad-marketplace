"""
Job scrapers — two sources for better senior-role coverage:

1. Adzuna API (title-only search, IT category)
   Free tier 1000 calls/month. Register at: https://developer.adzuna.com

2. JSearch via RapidAPI (pulls from LinkedIn + Indeed + Google Jobs)
   Free tier 200 requests/month. Register at: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
   Add JSEARCH_API_KEY to GitHub Secrets.
"""

import os
import logging
import requests
from job_hunter.config import LOCATION, COUNTRY, HOURS_SINCE_POSTED, MAX_JOBS_PER_QUERY

log = logging.getLogger(__name__)

ADZUNA_BASE  = "https://api.adzuna.com/v1/api/jobs"
JSEARCH_BASE = "https://jsearch.p.rapidapi.com/search"
COUNTRY_MAP  = {"US": "us", "GB": "gb", "CA": "ca", "AU": "au"}


# ── Shared job-dict normaliser ────────────────────────────────────────────────

def _job(job_id, title, company, location, url, description, salary_min, salary_max, date_posted=""):
    return {
        "job_id":      str(job_id),
        "title":       title,
        "company":     company,
        "location":    location,
        "url":         url,
        "description": description,
        "salary_min":  float(salary_min) if salary_min else 0,
        "salary_max":  float(salary_max) if salary_max else 0,
        "date_posted": date_posted,
    }


# ── Adzuna ────────────────────────────────────────────────────────────────────

def _adzuna_credentials():
    app_id  = os.environ.get("ADZUNA_APP_ID")
    app_key = os.environ.get("ADZUNA_API_KEY")
    if not app_id or not app_key:
        raise EnvironmentError("ADZUNA_APP_ID and ADZUNA_API_KEY must be set.")
    return app_id, app_key


def _search_adzuna(query: str) -> list[dict]:
    app_id, app_key = _adzuna_credentials()
    region     = COUNTRY_MAP.get(COUNTRY.upper(), "us")
    city       = LOCATION.split(",")[0].strip()
    cutoff_days = max(1, HOURS_SINCE_POSTED // 24)

    params = {
        "app_id":          app_id,
        "app_key":         app_key,
        "results_per_page": MAX_JOBS_PER_QUERY,
        "what_and":        query,       # ALL words must appear
        "title_only":      1,           # match in JOB TITLE only — eliminates most noise
        "category":        "it-jobs",   # IT category only
        "where":           city,
        "distance":        50,
        "max_days_old":    cutoff_days,
        "content-type":    "application/json",
        "sort_by":         "date",
    }

    url = f"{ADZUNA_BASE}/{region}/search/1"
    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code == 403:
            log.error("Adzuna 403 — expected when running locally; use GitHub Actions.")
            return []
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as exc:
        log.warning("Adzuna request failed for '%s': %s", query, exc)
        return []

    jobs = []
    for item in data.get("results", []):
        jobs.append(_job(
            job_id      = item.get("id", ""),
            title       = item.get("title", ""),
            company     = item.get("company", {}).get("display_name", ""),
            location    = item.get("location", {}).get("display_name", ""),
            url         = item.get("redirect_url", ""),
            description = item.get("description", ""),
            salary_min  = item.get("salary_min") or 0,
            salary_max  = item.get("salary_max") or 0,
            date_posted = item.get("created", ""),
        ))
    return jobs


# ── JSearch (LinkedIn + Indeed + Google Jobs) ─────────────────────────────────

def _search_jsearch(query: str) -> list[dict]:
    api_key = os.environ.get("JSEARCH_API_KEY")
    if not api_key:
        return []   # key not configured — skip silently

    city  = LOCATION.split(",")[0].strip()
    state = LOCATION.split(",")[1].strip() if "," in LOCATION else ""

    params = {
        "query":            f"{query} {city} {state}".strip(),
        "num_pages":        "1",
        "date_posted":      "week",     # last 7 days
        "employment_types": "FULLTIME",
        "job_requirements": "senior_level,director,vp,executive",
    }
    headers = {
        "X-RapidAPI-Key":  api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    }

    try:
        resp = requests.get(JSEARCH_BASE, params=params, headers=headers, timeout=20)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as exc:
        log.warning("JSearch request failed for '%s': %s", query, exc)
        return []

    jobs = []
    for item in data.get("data", []):
        location = ", ".join(filter(None, [
            item.get("job_city"), item.get("job_state")
        ]))
        jobs.append(_job(
            job_id      = item.get("job_id", ""),
            title       = item.get("job_title", ""),
            company     = item.get("employer_name", ""),
            location    = location,
            url         = item.get("job_apply_link") or item.get("job_google_link", ""),
            description = item.get("job_description", ""),
            salary_min  = item.get("job_min_salary") or 0,
            salary_max  = item.get("job_max_salary") or 0,
            date_posted = item.get("job_posted_at_datetime_utc", ""),
        ))
    return jobs


# ── Public interface ──────────────────────────────────────────────────────────

def search_jobs(query: str) -> list[dict]:
    """Search all configured sources and return deduplicated results."""
    seen_ids: set[str] = set()
    results: list[dict] = []

    for job in _search_adzuna(query) + _search_jsearch(query):
        if job["job_id"] and job["job_id"] not in seen_ids:
            seen_ids.add(job["job_id"])
            results.append(job)

    return results
