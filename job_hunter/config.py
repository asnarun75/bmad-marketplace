"""
User preferences — edit these before running.
"""

# ── Your location ────────────────────────────────────────────────────────────
LOCATION = "New York, NY"          # City, State (or "remote")
COUNTRY  = "US"
MAX_COMMUTE_MINUTES = 45

# ── Target roles ──────────────────────────────────────────────────────────────
SEARCH_QUERIES = [
    "Senior Director Technology",
    "Senior Director Engineering",
    "VP Technology Financial Services",
    "Head of Technology Banking",
    "Chief Architect Financial Services",
]

# ── Filters ───────────────────────────────────────────────────────────────────
MIN_SALARY_USD      = 285_000
HOURS_SINCE_POSTED  = 24          # Only jobs posted in the last N hours
MAX_JOBS_PER_QUERY  = 10          # Cap per search term to control API costs

# ── Claude model ──────────────────────────────────────────────────────────────
CLAUDE_MODEL     = "claude-sonnet-4-6"
CLAUDE_MAX_TOKENS = 4000

# ── Output ────────────────────────────────────────────────────────────────────
OUTPUT_DIR    = "job_hunter/output"
TRACKER_CSV   = "job_hunter/output/job_tracker.csv"
