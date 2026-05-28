"""Build a premium static GitHub Pages site for every portfolio project."""

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
:root { color-scheme: dark; --bg: #061113; --panel: rgba(255,255,255,.065); --panel2: rgba(255,255,255,.035); --ink: #eefcf8; --muted: #a8beba; --line: rgba(196,235,226,.18); --accent: #4de3b6; --blue: #99d7ff; --gold: #f4d06f; --rose: #ff9d9d; }
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Arial, sans-serif; color: var(--ink); background: radial-gradient(circle at 12% 5%, rgba(77,227,182,.20), transparent 30rem), radial-gradient(circle at 90% 12%, rgba(153,215,255,.16), transparent 28rem), linear-gradient(135deg, #061113, #09171d 56%, #061113); line-height: 1.58; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
.wrap { width: min(1180px, calc(100% - 34px)); margin: 0 auto; }
.hero { min-height: 82vh; display: grid; align-items: center; border-bottom: 1px solid var(--line); position: relative; overflow: hidden; }
.hero:after { content: ""; position: absolute; right: -120px; bottom: -180px; width: 520px; height: 520px; border: 1px solid rgba(77,227,182,.24); border-radius: 50%; box-shadow: inset 0 0 80px rgba(77,227,182,.12); }
.kicker { color: var(--accent); font-weight: 850; letter-spacing: .12em; text-transform: uppercase; font-size: 12px; }
h1 { max-width: 990px; margin: 14px 0 18px; font-size: clamp(42px, 8vw, 96px); line-height: .95; letter-spacing: 0; }
.lead { max-width: 800px; color: #cde5e0; font-size: clamp(17px, 2.1vw, 23px); }
.hero-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; }
.button { display: inline-flex; align-items: center; justify-content: center; min-height: 44px; padding: 0 16px; border-radius: 8px; border: 1px solid var(--line); background: rgba(255,255,255,.06); color: var(--ink); font-weight: 760; }
.button.primary { background: var(--accent); color: #04201a; border-color: transparent; }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin-top: 34px; max-width: 850px; }
.stat { border: 1px solid var(--line); background: rgba(255,255,255,.055); border-radius: 8px; padding: 15px; backdrop-filter: blur(10px); }
.stat strong { display: block; font-size: 30px; line-height: 1; color: var(--gold); }
.stat span { color: var(--muted); font-size: 13px; }
main { padding: 58px 0 78px; }
.section-title { display: flex; align-items: end; justify-content: space-between; gap: 18px; margin: 0 0 18px; }
.section-title p { color: var(--muted); max-width: 480px; }
h2 { margin: 0; font-size: clamp(25px, 4vw, 42px); line-height: 1.08; }
h3 { margin: 14px 0 8px; font-size: 22px; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(265px, 1fr)); gap: 16px; }
.card, .panel { position: relative; overflow: hidden; border: 1px solid var(--line); background: linear-gradient(180deg, var(--panel), var(--panel2)); border-radius: 8px; padding: 21px; box-shadow: 0 22px 60px rgba(0,0,0,.25); }
.card { min-height: 218px; }
.card:before, .panel:before { content: ""; position: absolute; inset: 0 0 auto; height: 3px; background: linear-gradient(90deg, var(--accent), var(--blue), var(--gold)); }
.pill { display: inline-flex; padding: 5px 9px; border-radius: 999px; color: #051513; background: var(--accent); font-size: 12px; font-weight: 850; }
.proof { display: grid; grid-template-columns: 1.1fr .9fr; gap: 16px; margin-bottom: 48px; }
.matrix { width: 100%; border-collapse: collapse; overflow: hidden; border-radius: 8px; }
.matrix th, .matrix td { padding: 13px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
.matrix th { color: var(--gold); background: rgba(255,255,255,.045); }
.timeline { display: grid; gap: 10px; }
.step { display: grid; grid-template-columns: 44px 1fr; gap: 12px; align-items: start; }
.num { width: 36px; height: 36px; border-radius: 50%; display: grid; place-items: center; background: rgba(77,227,182,.14); border: 1px solid var(--line); color: var(--accent); font-weight: 850; }
.case-grid { display: grid; grid-template-columns: minmax(0, .92fr) minmax(320px, 1.08fr); gap: 18px; align-items: start; }
ul { padding-left: 20px; }
pre { overflow-x: auto; border: 1px solid rgba(153,215,255,.22); background: #05090d; color: #d8fff2; padding: 18px; border-radius: 8px; box-shadow: inset 0 1px 0 rgba(255,255,255,.06); }
code { font-family: Consolas, Monaco, monospace; font-size: 13px; }
footer { border-top: 1px solid var(--line); padding: 26px 0; color: var(--muted); }
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
<footer><div class="wrap">Meena Vignesh M - Computational biotechnology, bioinformatics, lab data, and healthcare-data portfolio.</div></footer>
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
  <p class="lead">A focused first-year biotechnology portfolio by Meena Vignesh M, built around Python, biological data handling, scientific interpretation, and deployable case studies.</p>
  <div class="hero-actions"><a class="button primary" href="#projects">View projects</a><a class="button" href="https://github.com/meenavignesh-svg/daily-biotech-projects">Open GitHub repo</a></div>
  <div class="stats"><div class="stat"><strong>{project_count}</strong><span>completed case studies</span></div><div class="stat"><strong>{track_count}</strong><span>job-focused tracks</span></div><div class="stat"><strong>10</strong><span>core project roadmap</span></div><div class="stat"><strong>100%</strong><span>documented with sample data</span></div></div>
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
  <div class="panel"><h2>Recruiter Quick Scan</h2><p>This portfolio is designed to prove practical employable behavior: reading scientific data, writing small Python tools, producing clean reports, and explaining biological meaning.</p><table class="matrix"><tr><th>Proof area</th><th>Evidence</th></tr><tr><td>Bioinformatics</td><td>FASTA parsing, nucleotide summaries, protein properties, PCR primer checks</td></tr><tr><td>Lab data analysis</td><td>CSV handling, fold-change analysis, result classification</td></tr><tr><td>Communication</td><td>Every project has purpose, concept, result, output, and code</td></tr></table></div>
  <div class="panel"><h2>How I Build</h2><div class="timeline"><div class="step"><div class="num">1</div><div><strong>Choose a biotech problem</strong><br><span>Sequence, lab table, healthcare-data, or screening task.</span></div></div><div class="step"><div class="num">2</div><div><strong>Create a working tool</strong><br><span>Python script, sample input, and example output.</span></div></div><div class="step"><div class="num">3</div><div><strong>Explain the value</strong><br><span>README, resume bullet, and deployed case-study page.</span></div></div></div></div>
</section>
<div class="section-title"><h2>Skill Tracks</h2><p>Each track maps to an internship conversation: what data I can handle, what tools I can write, and how clearly I can explain results.</p></div>
<div class="grid">
  <div class="card"><span class="pill">Bioinformatics</span><h3>Sequence Workflows</h3><p>FASTA, primers, protein properties, and reproducible command-line reports.</p></div>
  <div class="card"><span class="pill">Lab Data</span><h3>Scientific Tables</h3><p>CSV cleaning, OD readings, expression summaries, and lab report outputs.</p></div>
  <div class="card"><span class="pill">Healthcare Data</span><h3>Structured Mapping</h3><p>Safe educational term mapping and non-clinical healthcare-data summaries.</p></div>
  <div class="card"><span class="pill">Biotech Tools</span><h3>Transparent Scoring</h3><p>Explainable rule-based tools for sample review and learning.</p></div>
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
