import os
import anthropic
from openai import OpenAI
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
Internally identify the top skills required by this job description, then produce a tailored resume.
The output must be a COMPLETE, READY-TO-SEND resume with ONLY these sections in this order:

1. Candidate name and contact line
2. Professional Summary (3–4 sentences, rewritten to mirror the JD's exact language and priorities)
3. Signature Impact (keep the 4 bullet metrics exactly as-is)
4. Core Capabilities (reorder and reword to front-load the most JD-relevant skills)
5. Professional Experience (reorder bullet points to surface the most relevant work first)
6. AI & Innovation
7. Education
8. Skills

DO NOT include any analysis, commentary, skills-match tables, internal notes, or section headers
that would not appear on a real resume submitted to an employer.
Output ONLY the resume — no preamble, no explanation, no closing remarks.
"""


def _build_prompt(master_resume: str, job_title: str, company: str,
                  location: str, job_description: str) -> str:
    return USER_TEMPLATE.format(
        master_resume=master_resume,
        job_title=job_title,
        company=company,
        location=location,
        job_description=job_description,
    )


def tailor_resume_claude(master_resume: str, job_title: str, company: str,
                         location: str, job_description: str) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=CLAUDE_MAX_TOKENS,
        temperature=0.2,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": _build_prompt(
            master_resume, job_title, company, location, job_description)}],
    )
    return message.content[0].text


def tailor_resume_openai(master_resume: str, job_title: str, company: str,
                         location: str, job_description: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        max_tokens=CLAUDE_MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": _build_prompt(
                master_resume, job_title, company, location, job_description)},
        ],
    )
    return response.choices[0].message.content


# Convenience wrapper — kept for backward compatibility
def tailor_resume(master_resume: str, job_title: str, company: str,
                  location: str, job_description: str) -> str:
    return tailor_resume_claude(master_resume, job_title, company, location, job_description)
