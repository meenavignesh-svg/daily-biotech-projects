"""Create one small daily biotechnology portfolio project."""

from __future__ import annotations

import csv
import os
import re
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
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


def today_ist() -> datetime:
    return datetime.now(IST)


def read_existing_project_count() -> int:
    if not PROJECTS_DIR.exists():
        return 0
    return len([path for path in PROJECTS_DIR.iterdir() if path.is_dir()])


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def code_for(slug: str) -> str:
    if slug == "primer-basics-calculator":
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
    if slug == "pdf-lab-table-extractor":
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
    if slug == "biotech-term-chat-helper":
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


def example_output_for(slug: str) -> str:
    if slug == "primer-basics-calculator":
        return "Primer Basics Calculator\n\nPrimer: primer_a\nSequence: ATGCGTACGTTA\nLength: 12 bases\nGC Content: 50.00%\nBasic Tm: 36 C\n"
    if slug == "pdf-lab-table-extractor":
        return "Sample,Reading,Unit\nGlucose,92,mg/dL\nProtein,6.8,g/dL\npH,7.2,pH\n"
    if slug == "biotech-term-chat-helper":
        return "Q: What is DNA?\nA: DNA stores genetic information using A, T, G, and C bases.\n"
    return "GENE_A: increased, fold change = 2.00\nGENE_B: decreased, fold change = 0.50\nGENE_C: increased, fold change = 1.20\n"


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


def update_root_readme(project: dict[str, str], folder_name: str, date_text: str) -> None:
    readme = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else "# Daily Biotech Projects\n"
    project_row = f"| {date_text} | {project['title']} | {project['concept']} | [projects/{folder_name}](projects/{folder_name}) |"
    chrono_row = f"| {date_text} | {project['track']} | [{project['title']}](projects/{folder_name}) |"

    if project_row not in readme:
        heading = f"### {project['track']}"
        heading_index = readme.find(heading)
        if heading_index != -1:
            next_heading = readme.find("\n### ", heading_index + len(heading))
            if next_heading == -1:
                next_heading = readme.find("\n## Chronological Index", heading_index)
            if next_heading != -1:
                before = readme[:next_heading].rstrip()
                after = readme[next_heading:]
                readme = before + f"\n{project_row}\n" + after

    if chrono_row not in readme and "\n## Portfolio Focus" in readme:
        marker = readme.find("\n## Portfolio Focus")
        before = readme[:marker].rstrip()
        after = readme[marker:]
        readme = before + f"\n{chrono_row}\n" + after

    README_PATH.write_text(readme, encoding="utf-8")


def line_explanation(code: str) -> str:
    lines = ["Line-by-Line Code Explanation:", ""]
    for number, text in enumerate(code.splitlines(), start=1):
        stripped = text.strip()
        if not stripped:
            meaning = "This blank line separates parts of the code so it is easier to read."
        elif stripped.startswith('"""'):
            meaning = "This line is part of the file description, explaining the purpose of the script."
        elif stripped.startswith("from __future__"):
            meaning = "This keeps newer Python type-hint behavior consistent."
        elif stripped.startswith("import ") or stripped.startswith("from "):
            meaning = "This brings in a Python module needed by the script."
        elif stripped.startswith("def "):
            meaning = "This starts a function, which is a reusable block of code."
        elif stripped.startswith("return "):
            meaning = "This sends a result back from the function."
        elif stripped.startswith("if __name__"):
            meaning = "This makes the script run main() only when opened directly."
        elif "argparse" in stripped or "add_argument" in stripped:
            meaning = "This helps the script accept command-line input."
        elif "print(" in stripped:
            meaning = "This displays information for the user."
        else:
            meaning = "This line supports the main project logic."
        lines.append(f"Line {number}: `{text}`")
        lines.append(f"Explanation: {meaning}")
        lines.append("")
    return "\n".join(lines)


def lesson_email(project: dict[str, str], folder_name: str, date_text: str, code: str) -> str:
    link = f"https://github.com/meenavignesh-svg/daily-biotech-projects/tree/main/projects/{folder_name}"
    return f"""Project Generated: {project['title']}

Repository:
{link}

Date:
{date_text}

Track:
{project['track']}

Today's Lesson:
Today I practiced {project['concept'].lower()}. This matters because small coding tools can make biotechnology study more organized and easier to revise.

Key Terms To Remember:
- Input file: The sample file read by the program.
- Output: The result printed or saved by the program.
- Function: A reusable block of Python code.

Tech Stack:
- Python

Features Added:
- Sample input file
- Main Python script
- Example output
- Clear project notes

Files Added or Updated:
- README.md
- {project['script']}
- {project['sample']}
- {project['output']}

Biotech/Bioinformatics Concept:
{project['concept']}. I connected this concept with a small beginner-level program so I can understand both the biology idea and the coding logic.

How The Code Works:
The script reads a simple input file, processes the content using functions, and prints or saves a clear result. Each function handles one part of the task so the code is easier to understand.

How To Run:
python {project['script']} {project['sample']}

Sample Input:
{project['sample_text']}

Sample Output:
{example_output_for(project['slug'])}

How To Read The Output:
The output shows the processed result in a simple format. I can compare it with the input to understand how the program changed raw data into useful study information.

Issues Found:
- No major issues found in this beginner version.
- This is a small learning version and can be improved with more examples.

Commits Today:
1 commit from the daily cloud run

Estimated Skill Areas Improved:
- Python basics
- File handling
- Biotechnology data thinking
- GitHub portfolio documentation

What I Learned Today:
- I learned how to connect a biology concept with a small Python project.
- I practiced reading simple input files.
- I improved my ability to explain code clearly.

Revision Questions:
- What input does this script read?
- What biology concept does this project practice?
- Which function would I improve first?

Next Improvements:
- Next I want to add more sample data.
- Next I want to improve the output formatting.
- Next I want to add simple checks for invalid input.

Full Code:
```python
{code}
```

{line_explanation(code)}
"""


def send_lesson(subject: str, body: str) -> None:
    to_email = os.getenv("LESSON_EMAIL_TO")
    host = os.getenv("SMTP_HOST")
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    port = int(os.getenv("SMTP_PORT", "587"))

    if not all([to_email, host, username, password]):
        print("Email settings are incomplete; skipping lesson email.")
        return

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = username
    message["To"] = to_email
    message.set_content(body)

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(message)


def main() -> None:
    date_text = today_ist().strftime("%Y-%m-%d")
    project = PROJECT_PLAN[read_existing_project_count() % len(PROJECT_PLAN)]
    folder_name = f"{date_text}-{project['slug']}"
    folder = PROJECTS_DIR / folder_name

    if folder.exists():
        print(f"Project already exists: {folder_name}")
        return

    code = code_for(project["slug"])
    write_text(folder / "README.md", readme_for(project, date_text))
    write_text(folder / project["sample"], project["sample_text"])
    write_text(folder / project["script"], code)
    write_text(folder / project["output"], example_output_for(project["slug"]))
    update_root_readme(project, folder_name, date_text)
    send_lesson(f"Daily Biotech Project Lesson - {project['title']}", lesson_email(project, folder_name, date_text, code))
    print(f"Created project: {folder_name}")


if __name__ == "__main__":
    main()
