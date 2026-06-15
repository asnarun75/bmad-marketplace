"""
User preferences — edit these before running.
"""

# ── Your location ────────────────────────────────────────────────────────────
LOCATION = "Jersey City, NJ"          # City, State (or "remote")
COUNTRY  = "US"
MAX_COMMUTE_MINUTES = 45

# ── Target roles ──────────────────────────────────────────────────────────────
# Keep to 6 queries: 6 × 30 days = 180 JSearch calls/month (free tier cap: 200).
# Adzuna uses what_or + title_only so shorter phrases yield more hits.
SEARCH_QUERIES = [
    "VP Technology",
    "VP Engineering",
    "Senior Director Technology",
    "Managing Director Technology",
    "Head of Technology",
    "Chief Technology Officer",
]

# ── Filters ───────────────────────────────────────────────────────────────────
# Salary filter disabled: Adzuna salary estimates for senior roles are unreliable
# (same posting can show $176K one day and $329K the next). Filter by title instead.
MIN_SALARY_USD      = 0
HOURS_SINCE_POSTED  = 168         # 7-day lookback — scraper enforces minimum 7 days
MAX_JOBS_PER_QUERY  = 10          # Cap per search term to control API costs

# ── Claude model ──────────────────────────────────────────────────────────────
CLAUDE_MODEL     = "claude-sonnet-4-6"
CLAUDE_MAX_TOKENS = 4000

# ── Output ────────────────────────────────────────────────────────────────────
OUTPUT_DIR    = "job_hunter/output"
TRACKER_CSV   = "job_hunter/output/job_tracker.csv"
