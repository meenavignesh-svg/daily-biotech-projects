"""Build a polished portfolio README from project folders."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
README_PATH = ROOT / "README.md"
TRACKS = ["Bioinformatics", "Productivity/Workflow Helper", "AI", "Data Analysis"]

SKILL_FALLBACKS = {
    "dna-rna-sequence-analyzer": "FASTA parsing, base counts, GC content, transcription",
    "protein-property-explorer": "Amino acid composition, molecular weight, protein basics",
    "simple-sequence-alignment": "Pairwise alignment, matches, mismatches, percent identity",
    "primer-basics-calculator": "Primer length, GC percentage, basic melting temperature",
    "lab-report-organizer": "Clean file naming, lab report indexing, Markdown output",
    "medical-coding-helper": "Educational lab term search, CSV filtering, safe healthcare wording",
    "pdf-lab-table-extractor": "Cleaning copied lab table text into structured data",
    "biotech-term-chat-helper": "Beginner biotechnology Q&A and dictionary-style responses",
    "gene-expression-mini-summary": "CSV analysis, fold-change comparison, gene expression summary",
}


def project_dirs() -> list[Path]:
    if not PROJECTS_DIR.exists():
        return []
    return [path for path in sorted(PROJECTS_DIR.iterdir()) if path.is_dir()]


def clean_text(value: str) -> str:
    return " ".join(value.replace("|", "/").split())


def extract_section(text: str, names: tuple[str, ...]) -> str:
    for name in names:
        match = re.search(rf"## {re.escape(name)}\s+(.+?)(?:\n## |\Z)", text, flags=re.DOTALL)
        if match:
            return clean_text(match.group(1))
    return ""


def skill_focus(folder_name: str, concept: str) -> str:
    for key, value in SKILL_FALLBACKS.items():
        if key in folder_name:
            return value
    if concept:
        sentence = re.split(r"(?<=[.!?])\s+", concept)[0]
        return clean_text(sentence)[:130]
    return "Student biotechnology portfolio project"


def project_meta(folder: Path) -> dict[str, str]:
    readme_path = folder / "README.md"
    text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    title_match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    track_match = re.search(r"\*\*Track:\*\*\s*(.+?)\s*(?:\n|$)", text)
    title = clean_text(title_match.group(1)) if title_match else folder.name
    track = clean_text(track_match.group(1)) if track_match else "Bioinformatics"
    if track not in TRACKS:
        track = "Bioinformatics"
    concept = extract_section(text, ("Concept", "Biotech Concept"))
    date = folder.name[:10] if re.match(r"\d{4}-\d{2}-\d{2}", folder.name) else "Unknown"
    return {
        "date": date,
        "title": title,
        "track": track,
        "focus": skill_focus(folder.name, concept),
        "folder": folder.name,
    }


def build_readme(projects: list[dict[str, str]]) -> str:
    counts = {track: sum(1 for project in projects if project["track"] == track) for track in TRACKS}
    total = len(projects)

    lines = [
        "# Daily Biotech Projects",
        "",
        "A growing biotechnology and bioinformatics portfolio by **Meena Vignesh M**, first-year Biotechnology student at **Sethu Institute of Technology, Kariapatti**.",
        "",
        "## Portfolio Goal",
        "",
        "I am building small, practical projects that connect biotechnology concepts with programming, data handling, and scientific documentation. Each project is kept beginner-friendly, but the portfolio is structured to show steady growth across bioinformatics, productivity tools, AI-style learning utilities, and data analysis.",
        "",
        "## Current Snapshot",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Total projects | {total} |",
    ]
    for track in TRACKS:
        lines.append(f"| {track} | {counts[track]} |")

    lines.extend(["", "## Learning Tracks", ""])
    for track in TRACKS:
        lines.extend([f"### {track}", ""])
        track_projects = [project for project in projects if project["track"] == track]
        if not track_projects:
            lines.extend(["Projects will be added here as the portfolio grows.", ""])
            continue
        lines.extend(["| Date | Project | Skill Focus |", "| --- | --- | --- |"])
        for project in track_projects:
            title = project["title"]
            if project["folder"].endswith("-2"):
                title += " 2"
            elif project["folder"].endswith("-3"):
                title += " 3"
            lines.append(f"| {project['date']} | [{title}](projects/{project['folder']}) | {project['focus']} |")
        lines.append("")

    lines.extend([
        "## Project Standards",
        "",
        "Each project aims to include:",
        "",
        "- A clear README written in my learning voice",
        "- A small working Python script or notebook",
        "- Sample input data",
        "- Example output",
        "- A short explanation of the biotechnology concept",
        "- Notes on what I learned and what I want to improve next",
        "",
        "## Chronological Index",
        "",
        "| Date | Track | Project |",
        "| --- | --- | --- |",
    ])
    for project in projects:
        title = project["title"]
        if project["folder"].endswith("-2"):
            title += " 2"
        elif project["folder"].endswith("-3"):
            title += " 3"
        lines.append(f"| {project['date']} | {project['track']} | [{title}](projects/{project['folder']}) |")

    lines.extend([
        "",
        "## Author",
        "",
        "**Meena Vignesh M**  ",
        "First-year Biotechnology student  ",
        "Sethu Institute of Technology, Kariapatti",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    projects = [project_meta(path) for path in project_dirs()]
    README_PATH.write_text(build_readme(projects), encoding="utf-8")


if __name__ == "__main__":
    main()
