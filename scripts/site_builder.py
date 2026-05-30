"""Build a clean static GitHub Pages site for every portfolio project."""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TRACKS = {
    "bioinformatics": "Bioinformatics",
    "lab-data-analysis": "Lab Data Analysis",
    "medical-coding-healthcare-data": "Medical Coding / Healthcare Data",
    "biotech-ai-tools": "Biotech AI Tools",
}

CSS = """
:root { color-scheme: light; --bg: #f7faf9; --paper: #ffffff; --soft: #edf7f4; --ink: #12201d; --muted: #5d6f69; --line: #dbe7e3; --accent: #087f68; --blue: #2563eb; --gold: #946200; }
* { box-sizing: border-box; }
body { margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Arial, sans-serif; color: var(--ink); background: linear-gradient(180deg, #f7faf9, #eef6f3); line-height: 1.58; }
a { color: var(--accent); text-decoration: none; } a:hover { text-decoration: underline; }
.wrap { width: min(1180px, calc(100% - 34px)); margin: 0 auto; }
.hero { min-height: 70vh; display: grid; align-items: center; border-bottom: 1px solid var(--line); background: radial-gradient(circle at 86% 18%, #dff3ee 0, transparent 24rem), linear-gradient(135deg, #ffffff, #f3faf7); }
.kicker { color: var(--accent); font-weight: 850; letter-spacing: .11em; text-transform: uppercase; font-size: 12px; }
h1 { max-width: 990px; margin: 14px 0 18px; font-size: clamp(40px, 7.2vw, 86px); line-height: .98; letter-spacing: 0; }
.lead { max-width: 830px; color: #41524d; font-size: clamp(17px, 2.1vw, 22px); }
.hero-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; }
.button { display: inline-flex; align-items: center; justify-content: center; min-height: 44px; padding: 0 16px; border-radius: 8px; border: 1px solid var(--line); background: var(--paper); color: var(--ink); font-weight: 760; box-shadow: 0 8px 22px rgba(20,50,43,.08); }
.button.primary { background: var(--accent); color: #ffffff; border-color: transparent; }
.stats, .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
.stats { margin-top: 34px; max-width: 920px; }
.stat, .card, .panel { border: 1px solid var(--line); background: var(--paper); border-radius: 8px; box-shadow: 0 14px 42px rgba(20,50,43,.08); }
.stat { padding: 15px; } .stat strong { display: block; font-size: 30px; line-height: 1; color: var(--accent); } .stat span { color: var(--muted); font-size: 13px; }
main { padding: 58px 0 78px; }
.section-title { display: flex; align-items: end; justify-content: space-between; gap: 18px; margin: 0 0 18px; }
.section-title p { color: var(--muted); max-width: 540px; }
h2 { margin: 0; font-size: clamp(25px, 4vw, 42px); line-height: 1.08; } h3 { margin: 14px 0 8px; font-size: 22px; }
.card, .panel { position: relative; overflow: hidden; padding: 21px; }
.card { min-height: 218px; } .card:before, .panel:before { content: ""; position: absolute; inset: 0 0 auto; height: 3px; background: linear-gradient(90deg, var(--accent), var(--blue), #d9a441); }
.pill { display: inline-flex; padding: 5px 9px; border-radius: 999px; color: var(--accent); background: var(--soft); font-size: 12px; font-weight: 850; }
.proof, .case-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 48px; }
ul { padding-left: 20px; } pre { overflow-x: auto; border: 1px solid #cfdcd8; background: #0f172a; color: #e2f7ef; padding: 18px; border-radius: 8px; } code { font-family: Consolas, Monaco, monospace; font-size: 13px; }
footer { border-top: 1px solid var(--line); padding: 26px 0; color: var(--muted); background: #ffffff; }
@media (max-width: 860px) { .case-grid, .proof { grid-template-columns: 1fr; } .hero { min-height: auto; padding: 72px 0; } .section-title { display: block; } }
"""


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
    lines: list[str] = []
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


def shell(title: str, hero: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>{CSS}</style>
</head>
<body>
{hero}
<main><div class="wrap">{body}</div></main>
<footer><div class="wrap">Meena Vignesh M - Biotechnology, bioinformatics, lab data, and healthcare-data portfolio.</div></footer>
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
            code_path = next(project_dir.glob("*.py"), project_dir / "missing.py")
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
                "code": read_file(code_path),
                "output": read_file(project_dir / "example_output.txt"),
            })
    return records


def build_home(records: list[dict[str, str]]) -> str:
    project_count = len(records)
    track_count = sum(1 for folder in TRACKS if (ROOT / folder).exists())
    hero = f"""
<header class="hero"><div class="wrap">
  <div class="kicker">Computational Biotechnology Portfolio</div>
  <h1>Biotech data problems solved with code, evidence, and clear reporting.</h1>
  <p class="lead">A focused biotechnology portfolio by Meena Vignesh M, built for bioinformatics, lab informatics, healthcare-data, and research-grade learning opportunities.</p>
  <div class="hero-actions"><a class="button primary" href="#projects">View projects</a><a class="button" href="https://github.com/meenavignesh-svg/daily-biotech-projects">Open GitHub repo</a></div>
  <div class="stats"><div class="stat"><strong>{project_count}</strong><span>completed case studies</span></div><div class="stat"><strong>{track_count}</strong><span>job-focused tracks</span></div><div class="stat"><strong>30</strong><span>project roadmap</span></div><div class="stat"><strong>100%</strong><span>documented with sample data</span></div></div>
</div></header>
"""
    cards = []
    for record in records:
        url = f"{record['track_folder']}/{record['slug']}/"
        cards.append(f"""
<article class="card">
  <span class="pill">{html.escape(record['track'])}</span>
  <h3><a href="{html.escape(url)}">{html.escape(record['title'])}</a></h3>
  <p>{html.escape(clean(record['concept'])[:220])}</p>
</article>
""")
    body = """
<section class="proof">
  <div class="panel"><h2>For Recruiters, Labs, and Data Teams</h2><p>I am looking for internship, trainee, junior assistant, or project-based learning opportunities in biotechnology, bioinformatics, lab informatics, and healthcare data.</p></div>
  <div class="panel"><h2>Portfolio Direction</h2><p>The roadmap moves from fundamentals to intermediate tools and then research-grade inspired prototypes: multi-omics, CRISPR review, digital-twin bioprocessing, cohort stratification, and regulatory readiness.</p></div>
</section>
<div class="section-title"><h2>Skill Tracks</h2><p>Each track maps to an internship conversation: what data I can handle, what tools I can write, and how clearly I can explain results.</p></div>
<div class="grid">
  <div class="card"><span class="pill">Bioinformatics</span><h3>Sequence and Omics Workflows</h3><p>FASTA, primers, variants, ORFs, multi-omics, CRISPR, surveillance, and protein-domain logic.</p></div>
  <div class="card"><span class="pill">Lab Data</span><h3>Scientific and Bioprocess Tables</h3><p>CSV cleaning, OD readings, expression summaries, qPCR, screening, and bioreactor analysis.</p></div>
  <div class="card"><span class="pill">Healthcare Data</span><h3>Structured Review</h3><p>Medical coding data, reference ranges, cohort logic, and pharmacovigilance signal triage.</p></div>
  <div class="card"><span class="pill">Biotech Tools</span><h3>Explainable Decision Support</h3><p>Transparent scoring, biomarker ranking, and regulatory-readiness checks.</p></div>
</div>
<div class="section-title" id="projects" style="margin-top:52px"><h2>Featured Case Studies</h2><p>Each page includes the science concept, job skill, result, sample output, and Python code.</p></div>
<div class="grid">
""" + "\n".join(cards) + "\n</div>"
    return shell("Computational Biotechnology Portfolio", hero, body)


def build_project(record: dict[str, str]) -> str:
    hero = f"""
<header class="hero"><div class="wrap">
  <div class="kicker">{html.escape(record['track'])}</div>
  <h1>{html.escape(record['title'])}</h1>
  <p class="lead">{html.escape(clean(record['concept']))}</p>
  <div class="hero-actions"><a class="button primary" href="https://github.com/meenavignesh-svg/daily-biotech-projects/tree/main/{record['track_folder']}/{record['slug']}">View source files</a><a class="button" href="../../">Portfolio home</a></div>
</div></header>
"""
    body = f"""
<div class="case-grid">
  <section class="panel"><h2>Case Study</h2><h3>Purpose</h3>{paragraphize(record['purpose'])}<h3>Result</h3>{paragraphize(record['result'])}<h3>Skills Demonstrated</h3>{paragraphize(record['skill'])}</section>
  <section class="panel"><h2>Scientific Context</h2>{paragraphize(record['concept'])}<h3>What I Practiced</h3>{paragraphize(record['practiced'])}</section>
</div>
<section class="panel"><h2>Example Output</h2><pre><code>{html.escape(record['output'])}</code></pre></section>
<section class="panel"><h2>Main Python Code</h2><pre><code>{html.escape(record['code'])}</code></pre></section>
"""
    return shell(record["title"], hero, body)


def main() -> None:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)
    records = project_records()
    (DOCS / "index.html").write_text(build_home(records), encoding="utf-8")
    for record in records:
        out_dir = DOCS / record["track_folder"] / record["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(build_project(record), encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built GitHub Pages site with {len(records)} projects.")


if __name__ == "__main__":
    main()
