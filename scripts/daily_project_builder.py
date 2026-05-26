"""Create one small daily biotechnology portfolio project."""

from __future__ import annotations

import csv
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

IST = timezone(timedelta(hours=5, minutes=30))
ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
README_PATH = ROOT / "README.md"

PROJECT_PLAN = [
    {
        "title": "Primer Basics Calculator",
        "track": "Bioinformatics",
        "concept": "Primer length, GC percentage, and basic melting temperature",
        "slug": "primer-basics-calculator",
        "script": "primer_basics_calculator.py",
        "sample": "sample_primers.csv",
        "output": "example_output.txt",
        "sample_text": "name,sequence\nprimer_a,ATGCGTACGTTA\nprimer_b,GGGAAATTTCCC\nprimer_c,ATATATGCGCGC\n",
    },
    {
        "title": "PDF Lab Table Extractor",
        "track": "Productivity/Workflow Helper",
        "concept": "Organizing copied lab table text into structured rows",
        "slug": "pdf-lab-table-extractor",
        "script": "pdf_lab_table_extractor.py",
        "sample": "sample_table_text.txt",
        "output": "example_output.csv",
        "sample_text": "Sample | Reading | Unit\nGlucose | 92 | mg/dL\nProtein | 6.8 | g/dL\npH | 7.2 | pH\n",
    },
    {
        "title": "Biotech Term Chat Helper",
        "track": "AI",
        "concept": "Rule-based educational Q&A for beginner biotechnology terms",
        "slug": "biotech-term-chat-helper",
        "script": "biotech_term_chat_helper.py",
        "sample": "sample_questions.txt",
        "output": "example_output.txt",
        "sample_text": "What is DNA?\nWhat is PCR?\nWhat is plasmid?\n",
    },
    {
        "title": "Gene Expression Mini Summary",
        "track": "Data Analysis",
        "concept": "Simple fold-change style comparison for example gene expression values",
        "slug": "gene-expression-mini-summary",
        "script": "gene_expression_mini_summary.py",
        "sample": "sample_expression.csv",
        "output": "example_output.txt",
        "sample_text": "gene,control,treatment\nGENE_A,10,20\nGENE_B,8,4\nGENE_C,15,18\n",
    },
]


def slugify(text: str) -> str:
    clean = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return clean.strip("-")


def today_ist() -> datetime:
    return datetime.now(IST)


def project_for_day(day_number: int) -> dict[str, str]:
    return PROJECT_PLAN[day_number % len(PROJECT_PLAN)]


def read_existing_project_count() -> int:
    if not PROJECTS_DIR.exists():
        return 0
    return len([path for path in PROJECTS_DIR.iterdir() if path.is_dir()])


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def primer_script() -> str:
    return '''"""Calculate beginner-friendly primer properties from a CSV file."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def gc_content(sequence: str) -> float:
    sequence = sequence.upper()
    if not sequence:
        return 0.0
    gc_count = sequence.count("G") + sequence.count("C")
    return (gc_count / len(sequence)) * 100


def melting_temperature(sequence: str) -> int:
    sequence = sequence.upper()
    return 2 * (sequence.count("A") + sequence.count("T")) + 4 * (sequence.count("G") + sequence.count("C"))


def read_primers(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def build_report(rows: list[dict[str, str]]) -> str:
    lines = ["Primer Basics Calculator", ""]
    for row in rows:
        name = row["name"].strip()
        sequence = row["sequence"].strip().upper()
        lines.append(f"Primer: {name}")
        lines.append(f"Sequence: {sequence}")
        lines.append(f"Length: {len(sequence)} bases")
        lines.append(f"GC Content: {gc_content(sequence):.2f}%")
        lines.append(f"Basic Tm: {melting_temperature(sequence)} C")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate basic primer properties.")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--output", type=Path, default=Path("primer_report.txt"))
    args = parser.parse_args()
    report = build_report(read_primers(args.csv_file))
    args.output.write_text(report, encoding="utf-8")
    print(report, end="")


if __name__ == "__main__":
    main()
'''


def table_script() -> str:
    return '''"""Convert copied lab table text into a clean CSV file."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_table(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        rows.append([cell.strip() for cell in line.split("|")])
    return rows


def write_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert simple copied lab table text into CSV.")
    parser.add_argument("text_file", type=Path)
    parser.add_argument("--output", type=Path, default=Path("clean_lab_table.csv"))
    args = parser.parse_args()
    rows = parse_table(args.text_file.read_text(encoding="utf-8"))
    write_csv(args.output, rows)
    print(f"Saved {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
'''


def chat_script() -> str:
    return '''"""Answer a few beginner biotechnology term questions using a small local dictionary."""

from __future__ import annotations

import argparse
from pathlib import Path

ANSWERS = {
    "dna": "DNA stores genetic information using A, T, G, and C bases.",
    "pcr": "PCR is a method used to make many copies of a selected DNA region.",
    "plasmid": "A plasmid is a small circular DNA molecule often found in bacteria.",
    "enzyme": "An enzyme is a biological catalyst that speeds up reactions.",
}


def answer_question(question: str) -> str:
    lower_question = question.lower()
    for term, answer in ANSWERS.items():
        if term in lower_question:
            return answer
    return "I need to add this term to my study dictionary."


def main() -> None:
    parser = argparse.ArgumentParser(description="Answer beginner biotechnology term questions.")
    parser.add_argument("questions_file", type=Path)
    args = parser.parse_args()
    for question in args.questions_file.read_text(encoding="utf-8").splitlines():
        if question.strip():
            print(f"Q: {question}")
            print(f"A: {answer_question(question)}")
            print()


if __name__ == "__main__":
    main()
'''


def expression_script() -> str:
    return '''"""Summarize simple gene expression changes from a CSV file."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def classify_change(control: float, treatment: float) -> str:
    if treatment > control:
        return "increased"
    if treatment < control:
        return "decreased"
    return "unchanged"


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize example gene expression changes.")
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args()

    with args.csv_file.open("r", encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            control = float(row["control"])
            treatment = float(row["treatment"])
            fold_change = treatment / control if control else 0.0
            change = classify_change(control, treatment)
            print(f"{row['gene']}: {change}, fold change = {fold_change:.2f}")


if __name__ == "__main__":
    main()
'''


SCRIPT_BY_SLUG = {
    "primer-basics-calculator": primer_script,
    "pdf-lab-table-extractor": table_script,
    "biotech-term-chat-helper": chat_script,
    "gene-expression-mini-summary": expression_script,
}


def readme_for(project: dict[str, str], date_text: str) -> str:
    return f"""# {project['title']}

**Date:** {date_text}  
**Track:** {project['track']}  
**Author:** Meena Vignesh M

## Purpose

I built this project as a small portfolio exercise to practice biotechnology concepts with simple Python code.

## Concept

{project['concept']}.

## Features

- Uses a small sample file for practice
- Runs with Python from the command line
- Produces a clear beginner-friendly output
- Keeps the project scope realistic for first-year learning

## Files

- `{project['script']}` - main Python script
- `{project['sample']}` - sample input
- `{project['output']}` - example output or expected output file

## How To Run

```bash
python {project['script']} {project['sample']}
```

## What I Learned

- I practiced connecting a biology topic with a small coding task
- I learned how structured input files make analysis easier
- I improved my confidence with Python project folders

## Next Improvements

- Next I want to add more examples
- Next I want to improve the output formatting
- Next I want to add a simple chart or interface when useful
"""


def example_output_for(project: dict[str, str]) -> str:
    if project["slug"] == "primer-basics-calculator":
        return "Primer Basics Calculator\n\nPrimer: primer_a\nSequence: ATGCGTACGTTA\nLength: 12 bases\nGC Content: 50.00%\nBasic Tm: 36 C\n"
    if project["slug"] == "pdf-lab-table-extractor":
        return "Sample,Reading,Unit\nGlucose,92,mg/dL\nProtein,6.8,g/dL\npH,7.2,pH\n"
    if project["slug"] == "biotech-term-chat-helper":
        return "Q: What is DNA?\nA: DNA stores genetic information using A, T, G, and C bases.\n"
    return "GENE_A: increased, fold change = 2.00\nGENE_B: decreased, fold change = 0.50\nGENE_C: increased, fold change = 1.20\n"


def update_root_readme(project: dict[str, str], folder_name: str, date_text: str) -> None:
    readme = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else "# Daily Biotech Projects\n"
    project_row = f"| {date_text} | {project['title']} | {project['concept']} | [projects/{folder_name}](projects/{folder_name}) |"
    chrono_row = f"| {date_text} | {project['track']} | [{project['title']}](projects/{folder_name}) |"

    if project_row not in readme:
        track_heading = f"### {project['track']}"
        if track_heading in readme:
            section_start = readme.index(track_heading)
            next_section = readme.find("\n### ", section_start + len(track_heading))
            if next_section == -1:
                next_section = readme.find("\n## Chronological Index", section_start)
            section = readme[section_start:next_section]
            if "| Date | Project | Concept | Folder |" in section:
                insert_at = section_start + section.rfind("|") + 1
                readme = readme[:insert_at] + f"\n{project_row}" + readme[insert_at:]

    if chrono_row not in readme and "## Chronological Index" in readme:
        author_index = readme.find("\n## Portfolio Focus")
        if author_index != -1:
            before = readme[:author_index].rstrip()
            after = readme[author_index:]
            readme = before + f"\n{chrono_row}\n" + after

    README_PATH.write_text(readme, encoding="utf-8")


def main() -> None:
    now = today_ist()
    date_text = now.strftime("%Y-%m-%d")
    project = project_for_day(read_existing_project_count())
    folder_name = f"{date_text}-{project['slug']}"
    folder = PROJECTS_DIR / folder_name

    if folder.exists():
        print(f"Project already exists: {folder_name}")
        return

    write_text(folder / "README.md", readme_for(project, date_text))
    write_text(folder / project["sample"], project["sample_text"])
    write_text(folder / project["script"], SCRIPT_BY_SLUG[project["slug"]]())
    write_text(folder / project["output"], example_output_for(project))
    update_root_readme(project, folder_name, date_text)
    print(f"Created project: {folder_name}")


if __name__ == "__main__":
    main()
