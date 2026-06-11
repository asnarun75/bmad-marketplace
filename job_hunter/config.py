"""
User preferences — edit these before running.
"""

# ── Your location ────────────────────────────────────────────────────────────
LOCATION = "Jersey City, NJ"          # City, State (or "remote")
COUNTRY  = "US"
MAX_COMMUTE_MINUTES = 45

# ── Target roles ──────────────────────────────────────────────────────────────
# These run against JOB TITLE only (Adzuna title_only=1) so keep them concise.
# JSearch also uses these as queries but ranks by relevance.
SEARCH_QUERIES = [
    "Senior Director Technology",
    "Senior Director Engineering",
    "VP Technology",
    "VP Engineering Financial",
    "Managing Director Technology",
    "Head of Technology",
    "Director Capital Markets Technology",
    "Chief Technology Officer",
    "VP Software Engineering",
]

# ── Filters ───────────────────────────────────────────────────────────────────
# Salary filter disabled: Adzuna salary estimates for senior roles are unreliable
# (same posting can show $176K one day and $329K the next). Filter by title instead.
MIN_SALARY_USD      = 0
HOURS_SINCE_POSTED  = 72          # Look back 3 days to avoid missing any postings
MAX_JOBS_PER_QUERY  = 10          # Cap per search term to control API costs

# ── Claude model ──────────────────────────────────────────────────────────────
CLAUDE_MODEL     = "claude-sonnet-4-6"
CLAUDE_MAX_TOKENS = 4000

# ── Output ────────────────────────────────────────────────────────────────────
OUTPUT_DIR    = "job_hunter/output"
TRACKER_CSV   = "job_hunter/output/job_tracker.csv"
