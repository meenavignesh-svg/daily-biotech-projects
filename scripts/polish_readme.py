"""Build the root README for the computational biotechnology portfolio."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
PAGES_BASE_URL = "https://meenavignesh-svg.github.io/daily-biotech-projects"
TRACKS = {
    "bioinformatics": "Bioinformatics",
    "lab-data-analysis": "Lab Data Analysis",
    "medical-coding-healthcare-data": "Medical Coding / Healthcare Data",
    "biotech-ai-tools": "Biotech AI Tools",
}

ROADMAP = [
    ("bioinformatics", "01 DNA FASTA analyzer"),
    ("bioinformatics", "02 Protein property calculator"),
    ("bioinformatics", "03 Primer quality checker"),
    ("lab-data-analysis", "04 Gene expression fold-change analysis"),
    ("lab-data-analysis", "05 ELISA/OD data analyzer"),
    ("lab-data-analysis", "06 Microbial growth curve analyzer"),
    ("lab-data-analysis", "07 Lab report table cleaner"),
    ("medical-coding-healthcare-data", "08 Medical coding term mapper"),
    ("medical-coding-healthcare-data", "09 Drug prescription data dashboard"),
    ("biotech-ai-tools", "10 BioSentinel risk-screening demo"),
    ("bioinformatics", "11 Sequence variant impact annotator"),
    ("bioinformatics", "12 Pairwise sequence alignment scorer"),
    ("bioinformatics", "13 ORF finder and translation reporter"),
    ("lab-data-analysis", "14 qPCR delta-delta Ct analyzer"),
    ("lab-data-analysis", "15 LIMS sample tracker quality audit"),
    ("lab-data-analysis", "16 Antibiotic zone of inhibition analyzer"),
    ("medical-coding-healthcare-data", "17 Clinical lab reference range flagger"),
    ("medical-coding-healthcare-data", "18 Diagnosis keyword triage classifier"),
    ("biotech-ai-tools", "19 Adverse event signal counter"),
    ("biotech-ai-tools", "20 Bioreactor batch anomaly screener"),
]


def clean_text(value: str) -> str:
    return " ".join(value.replace("|", "/").split())


def project_dirs(folder: str) -> list[Path]:
    root = ROOT / folder
    if not root.exists():
        return []
    return [path for path in sorted(root.iterdir()) if path.is_dir()]


def extract_section(text: str, name: str) -> str:
    match = re.search(rf"## {re.escape(name)}\s+(.+?)(?:\n## |\Z)", text, flags=re.DOTALL)
    return clean_text(match.group(1)) if match else ""


def project_meta(folder_name: str, path: Path) -> dict[str, str]:
    readme = path / "README.md"
    text = readme.read_text(encoding="utf-8") if readme.exists() else ""
    title_match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    title = clean_text(title_match.group(1)) if title_match else clean_text(path.name)
    skill = extract_section(text, "What I Practiced") or extract_section(text, "Biology / Data Concept")
    if skill.startswith("-"):
        skill = clean_text(skill.replace("-", " "))
    path_text = f"{folder_name}/{path.name}"
    return {
        "folder": folder_name,
        "path": path_text,
        "live": f"{PAGES_BASE_URL}/{path_text}/",
        "title": title,
        "skill": skill or "Computational biotechnology project with reproducible Python output",
    }


def all_projects() -> list[dict[str, str]]:
    projects: list[dict[str, str]] = []
    for folder in TRACKS:
        projects.extend(project_meta(folder, path) for path in project_dirs(folder))
    return projects


def roadmap_status(projects: list[dict[str, str]]) -> list[str]:
    existing_paths = {project["path"].split("/", 1)[1] for project in projects}
    lines = ["| Track | Target project | Status |", "| --- | --- | --- |"]
    for folder, title in ROADMAP:
        number = title.split(" ", 1)[0]
        status = "Done" if any(path.startswith(number + "-") for path in existing_paths) else "Planned"
        lines.append(f"| {TRACKS[folder]} | {title} | {status} |")
    return lines


def build_readme(projects: list[dict[str, str]]) -> str:
    lines = [
        "# Computational Biotechnology Portfolio",
        "",
        "A focused biotechnology, bioinformatics, and healthcare-data portfolio by **Meena Vignesh M**, Biotechnology student at **Sethu Institute of Technology, Kariapatti**.",
        "",
        f"**Live portfolio site:** {PAGES_BASE_URL}/",
        "",
        "## Why this portfolio matters",
        "",
        "This repository shows my ability to use Python for biotechnology, bioinformatics, lab data cleaning, healthcare data handling, and scientific reporting.",
        "",
        "I am targeting entry-level roles/internships in:",
        "- Bioinformatics",
        "- Biotechnology data analysis",
        "- Medical coding / healthcare data",
        "- Lab informatics",
        "- AI-assisted biotech tools",
        "",
        "## Portfolio Tracks",
        "",
        "| Track | Folder | Purpose |",
        "| --- | --- | --- |",
        "| Bioinformatics | `bioinformatics/` | Sequence analysis, primers, proteins, FASTA workflows |",
        "| Lab Data Analysis | `lab-data-analysis/` | CSV cleaning, OD readings, growth curves, expression summaries |",
        "| Medical Coding / Healthcare Data | `medical-coding-healthcare-data/` | Safe educational healthcare-data mapping and summaries |",
        "| Biotech AI Tools | `biotech-ai-tools/` | Transparent biotech decision-support demos for learning |",
        "",
        "## Project Roadmap",
        "",
    ]
    lines.extend(roadmap_status(projects))
    lines.extend(["", "## Completed Portfolio Projects", ""])
    for folder, label in TRACKS.items():
        folder_projects = [project for project in projects if project["folder"] == folder]
        lines.extend([f"### {label}", ""])
        if not folder_projects:
            lines.extend(["Projects will be added here as this portfolio grows.", ""])
            continue
        lines.extend(["| Project | Live page | Skill shown |", "| --- | --- | --- |"])
        for project in folder_projects:
            lines.append(f"| [{project['title']}]({project['path']}) | [View page]({project['live']}) | {project['skill']} |")
        lines.append("")
    lines.extend([
        "## Project Standard",
        "",
        "Each main project is expected to include:",
        "- A working Python script",
        "- Sample biological, lab, or healthcare-data input",
        "- Example output",
        "- A README with job skill, result, and interview explanation value",
        "- A deployed GitHub Pages project page",
        "- A resume bullet collected in [RESUME_BULLETS.md](RESUME_BULLETS.md)",
        "",
        "## Author",
        "",
        "**Meena Vignesh M**  ",
        "Biotechnology student  ",
        "Sethu Institute of Technology, Kariapatti",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    README_PATH.write_text(build_readme(all_projects()), encoding="utf-8")


if __name__ == "__main__":
    main()
