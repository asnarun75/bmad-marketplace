"""
Converts a tailored markdown resume into a clean, professional PDF.
Designed to look like a real submitted resume, not a converted document.
"""

from pathlib import Path
import markdown2
from weasyprint import HTML


RESUME_CSS = """
@page {
    margin: 0.65in 0.7in 0.65in 0.7in;
    size: letter;
}

* { box-sizing: border-box; }

body {
    font-family: "Calibri", "Georgia", serif;
    font-size: 10.5pt;
    line-height: 1.4;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
}

/* ── Name (h1) ─────────────────────────────────────────── */
h1 {
    font-family: "Calibri", "Arial", sans-serif;
    font-size: 22pt;
    font-weight: 700;
    color: #1a1a1a;
    text-align: center;
    margin: 0 0 3px 0;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    border: none;
}

/* ── Contact line (paragraph immediately after h1) ─────── */
h1 + p {
    text-align: center;
    font-size: 9.5pt;
    color: #444;
    margin: 0 0 10px 0;
    border-bottom: 1.5px solid #1a1a1a;
    padding-bottom: 7px;
}

/* ── Section headers (h2) ──────────────────────────────── */
h2 {
    font-family: "Calibri", "Arial", sans-serif;
    font-size: 10pt;
    font-weight: 700;
    color: #1a1a1a;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 11px 0 3px 0;
    border-bottom: 1px solid #1a1a1a;
    padding-bottom: 1px;
}

/* ── Role / company lines (h3) ─────────────────────────── */
h3 {
    font-size: 10.5pt;
    font-weight: 700;
    color: #1a1a1a;
    margin: 7px 0 1px 0;
}

/* ── Bullet points ─────────────────────────────────────── */
ul {
    margin: 2px 0 5px 0;
    padding-left: 15px;
}

li {
    margin-bottom: 2px;
    line-height: 1.4;
}

/* ── Inline code (used for skill tags — hide styling) ──── */
code {
    font-family: inherit;
    font-size: inherit;
    background: none;
    border: none;
    padding: 0;
}

/* ── Paragraphs ────────────────────────────────────────── */
p {
    margin: 3px 0;
}

/* ── Horizontal rules ──────────────────────────────────── */
hr {
    display: none;
}

/* ── Bold text ─────────────────────────────────────────── */
strong {
    color: #1a1a1a;
}

/* ── Hide blockquotes (Claude instruction notes) ───────── */
blockquote {
    display: none;
}

/* ── Tables ────────────────────────────────────────────── */
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 9.5pt;
    margin: 4px 0;
}
td, th {
    padding: 2px 6px;
    border: 1px solid #ccc;
}
th {
    background: #f5f5f5;
    font-weight: 600;
}
"""


def _clean_markdown(md: str) -> str:
    lines = md.splitlines()
    # Drop any leading heading that starts with "# Tailored Resume"
    if lines and lines[0].startswith("# Tailored Resume"):
        lines = lines[1:]
    # Collapse leading blank lines
    while lines and not lines[0].strip():
        lines = lines[1:]
    return "\n".join(lines)


def markdown_to_pdf(markdown_content: str, output_path: str | Path) -> Path:
    cleaned = _clean_markdown(markdown_content)

    html_body = markdown2.markdown(
        cleaned,
        extras=["tables", "fenced-code-blocks", "strike"],
    )

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>{RESUME_CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    out = Path(output_path)
    HTML(string=full_html).write_pdf(str(out))
    return out
