"""
Converts a tailored markdown resume into a clean, ATS-ready PDF.
Uses weasyprint (HTML/CSS → PDF) for professional formatting.
"""

import re
from pathlib import Path

import markdown2
from weasyprint import HTML


RESUME_CSS = """
@page {
    margin: 0.7in 0.75in 0.7in 0.75in;
    size: letter;
}

body {
    font-family: "Arial", "Helvetica Neue", Helvetica, sans-serif;
    font-size: 10.5pt;
    line-height: 1.45;
    color: #1a1a1a;
}

/* Name / title line at the top */
h1 {
    font-size: 20pt;
    font-weight: 700;
    color: #0a2342;
    margin: 0 0 2px 0;
    letter-spacing: 0.5px;
    border-bottom: 2.5px solid #0a2342;
    padding-bottom: 4px;
}

/* Contact line (italicised paragraph right after h1) */
h1 + p {
    font-size: 9.5pt;
    color: #444;
    margin: 3px 0 12px 0;
}

/* Section headers */
h2 {
    font-size: 11pt;
    font-weight: 700;
    color: #0a2342;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin: 14px 0 4px 0;
    border-bottom: 1px solid #b0bec5;
    padding-bottom: 2px;
}

/* Role / company headers */
h3 {
    font-size: 10.5pt;
    font-weight: 700;
    color: #1a1a1a;
    margin: 8px 0 2px 0;
}

/* Bullet points */
ul {
    margin: 3px 0 6px 0;
    padding-left: 16px;
}

li {
    margin-bottom: 2px;
}

/* Key skills match section — highlight box */
h2:first-of-type + p,
p strong {
    color: #0a2342;
}

/* Horizontal rule */
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 10px 0;
}

/* Blockquote — instruction to Claude, hidden from output */
blockquote {
    display: none;
}

/* Tables (impact metrics) */
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 9.5pt;
    margin: 6px 0;
}
td, th {
    padding: 3px 8px;
    border: 1px solid #ddd;
}
th {
    background: #f0f4f8;
    font-weight: 600;
}

p { margin: 4px 0; }
"""


def _strip_front_matter(md: str) -> str:
    """Remove the '# Tailored Resume — ...' heading line used as a filename hint."""
    lines = md.splitlines()
    if lines and lines[0].startswith("# Tailored Resume"):
        lines = lines[1:]
    return "\n".join(lines)


def markdown_to_pdf(markdown_content: str, output_path: str | Path) -> Path:
    """Convert a tailored markdown resume to a PDF file."""
    cleaned = _strip_front_matter(markdown_content)

    html_body = markdown2.markdown(
        cleaned,
        extras=["tables", "fenced-code-blocks", "strike", "header-ids"],
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
