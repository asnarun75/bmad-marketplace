import os
import anthropic
from job_hunter.config import CLAUDE_MODEL, CLAUDE_MAX_TOKENS

SYSTEM_PROMPT = """You are an elite Technical Resume Optimizer and ATS Specialist for senior technology executives in financial services.

Rules you MUST follow:
1. NEVER invent, fabricate, or hallucinate job titles, companies, dates, or metrics.
2. Only rephrase, reprioritize, or change emphasis of facts already in the master resume.
3. Mirror the exact technical keywords and skills from the job description.
4. Rewrite the Professional Summary to position the candidate as the ideal match.
5. Reorder and reword bullet points to surface the most relevant experience first.
6. Output ONLY clean Markdown. No preamble, no "Here is your resume", no closing remarks.
"""

USER_TEMPLATE = """## Master Resume
{master_resume}

---

## Target Job Description
**Title:** {job_title}
**Company:** {company}
**Location:** {location}

{job_description}

---

## Task
1. Identify the top 5 hard skills and top 3 soft skills in the job description.
2. Rewrite the Professional Summary (3–4 sentences) to mirror those skills exactly.
3. Reorder experience bullet points to highlight the most relevant work first.
4. Add a "Key Skills Match" section at the top listing the exact keywords from the JD that appear in this resume.
5. Output the complete tailored resume in Markdown.
"""


def tailor_resume(master_resume: str, job_title: str, company: str, location: str, job_description: str) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = USER_TEMPLATE.format(
        master_resume=master_resume,
        job_title=job_title,
        company=company,
        location=location,
        job_description=job_description,
    )

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=CLAUDE_MAX_TOKENS,
        temperature=0.2,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
