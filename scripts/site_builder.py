"""Build a static GitHub Pages site for every portfolio project."""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BASE_URL = "https://meenavignesh-svg.github.io/daily-biotech-projects"
TRACKS = {
    "bioinformatics": "Bioinformatics",
    "lab-data-analysis": "Lab Data Analysis",
    "medical-coding-healthcare-data": "Medical Coding / Healthcare Data",
    "biotech-ai-tools": "Biotech AI Tools",
}


def clean(value: str) -> str:
    return " ".join(value.split())


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def title_from_readme(text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    return clean(match.group(1)) if match else fallback.replace("-", " ").title()


def section(text: str, name: str) -> str:
    match = re.search(rf"## {re.escape(name)}\s+(.+?)(?:\n## |\Z)", text, flags=re.DOTALL)
    return match.group(1).strip() if match else ""


def paragraphize(markdown: str) -> str:
    lines = []
    in_list = False
    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            if in_list:
                lines.append("</ul>")
                in_list = False
            continue
        if line.startswith("-"):
            if not in_list:
                lines.append("<ul>")
                in_list = True
            lines.append(f"<li>{html.escape(line[1:].strip())}</li>")
        else:
            if in_list:
                lines.append("</ul>")
                in_list = False
            lines.append(f"<p>{html.escape(line)}</p>")
    if in_list:
        lines.append("</ul>")
    return "\n".join(lines)


def page_shell(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{ color-scheme: light; --ink: #17202a; --muted: #536271; --line: #d9e2ec; --accent: #0f766e; --soft: #eef8f6; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; color: var(--ink); background: #f8fafc; line-height: 1.55; }}
    header {{ background: #ffffff; border-bottom: 1px solid var(--line); }}
    .wrap {{ width: min(1080px, calc(100% - 32px)); margin: 0 auto; }}
    .top {{ padding: 28px 0 22px; }}
    .brand {{ font-size: 14px; color: var(--accent); font-weight: 700; text-transform: uppercase; letter-spacing: 0; }}
    h1 {{ margin: 8px 0 8px; font-size: clamp(30px, 5vw, 52px); line-height: 1.05; }}
    h2 {{ margin-top: 30px; font-size: 22px; }}
    p {{ margin: 10px 0; }}
    a {{ color: var(--accent); }}
    main {{ padding: 28px 0 48px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; margin-top: 18px; }}
    .card {{ background: #ffffff; border: 1px solid var(--line); border-radius: 8px; padding: 16px; }}
    .card h3 {{ margin: 0 0 8px; font-size: 18px; }}
    .pill {{ display: inline-block; padding: 4px 8px; background: var(--soft); color: var(--accent); border-radius: 999px; font-size: 12px; font-weight: 700; }}
    pre {{ overflow-x: auto; background: #0f172a; color: #e2e8f0; padding: 16px; border-radius: 8px; }}
    code {{ font-family: Consolas, Monaco, monospace; }}
    table {{ width: 100%; border-collapse: collapse; background: #ffffff; }}
    th, td {{ padding: 10px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    footer {{ color: var(--muted); border-top: 1px solid var(--line); padding: 22px 0; background: #ffffff; }}
  </style>
</head>
<body>
<header><div class="wrap top"><div class="brand">Computational Biotechnology Portfolio</div><h1>{html.escape(title)}</h1><p>Meena Vignesh M</p></div></header>
<main><div class="wrap">{body}</div></main>
<footer><div class="wrap">Bioinformatics, lab data analysis, healthcare data, and biotech tools portfolio.</div></footer>
</body>
</html>
"""


def project_records() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for folder, track in TRACKS.items():
        root = ROOT / folder
        if not root.exists():
            continue
        for project_dir in sorted(path for path in root.iterdir() if path.is_dir()):
            readme = read_file(project_dir / "README.md")
            records.append({
                "track_folder": folder,
                "track": track,
                "slug": project_dir.name,
                "title": title_from_readme(readme, project_dir.name),
                "purpose": section(readme, "Purpose"),
                "concept": section(readme, "Biology / Data Concept"),
                "skill": section(readme, "Job Skill Demonstrated"),
                "result": section(readme, "Result"),
                "practiced": section(readme, "What I Practiced"),
                "code": read_file(next(project_dir.glob("*.py"), project_dir / "missing.py")),
                "output": read_file(project_dir / "example_output.txt"),
            })
    return records


def build_project_page(record: dict[str, str]) -> str:
    body = f"""
<p><span class="pill">{html.escape(record['track'])}</span></p>
<h2>Purpose</h2>
{paragraphize(record['purpose'])}
<h2>Biology / Data Concept</h2>
{paragraphize(record['concept'])}
<h2>Job Skill Demonstrated</h2>
{paragraphize(record['skill'])}
<h2>Result</h2>
{paragraphize(record['result'])}
<h2>What I Practiced</h2>
{paragraphize(record['practiced'])}
<h2>Example Output</h2>
<pre><code>{html.escape(record['output'])}</code></pre>
<h2>Main Python Code</h2>
<pre><code>{html.escape(record['code'])}</code></pre>
<p><a href="../../">Back to portfolio home</a></p>
"""
    return page_shell(record["title"], body)


def build_home(records: list[dict[str, str]]) -> str:
    cards = []
    for record in records:
        url = f"{record['track_folder']}/{record['slug']}/"
        cards.append(f"""
<div class="card">
  <span class="pill">{html.escape(record['track'])}</span>
  <h3><a href="{html.escape(url)}">{html.escape(record['title'])}</a></h3>
  <p>{html.escape(clean(record['concept'])[:180])}</p>
</div>
""")
    body = """
<p>This portfolio shows practical Python work for biotechnology, bioinformatics, lab data cleaning, healthcare data handling, and scientific reporting.</p>
<h2>Project Tracks</h2>
<table>
<tr><th>Track</th><th>Focus</th></tr>
<tr><td>Bioinformatics</td><td>Sequence analysis, primers, proteins, FASTA workflows</td></tr>
<tr><td>Lab Data Analysis</td><td>CSV cleaning, OD readings, growth curves, expression summaries</td></tr>
<tr><td>Medical Coding / Healthcare Data</td><td>Safe educational healthcare-data mapping and summaries</td></tr>
<tr><td>Biotech AI Tools</td><td>Transparent biotech decision-support demos for learning</td></tr>
</table>
<h2>Projects</h2>
<div class="grid">
""" + "\n".join(cards) + "\n</div>"
    return page_shell("Computational Biotechnology Portfolio", body)


def main() -> None:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)
    records = project_records()
    (DOCS / "index.html").write_text(build_home(records), encoding="utf-8")
    for record in records:
        out_dir = DOCS / record["track_folder"] / record["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(build_project_page(record), encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built GitHub Pages site with {len(records)} projects.")


if __name__ == "__main__":
    main()
