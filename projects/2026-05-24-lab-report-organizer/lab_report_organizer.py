"""Create a clean study index for biotechnology lab report files."""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path


def slugify(text: str) -> str:
    """Convert text into a simple folder-friendly name."""
    cleaned = text.strip().lower()
    cleaned = re.sub(r"[^a-z0-9]+", "-", cleaned)
    return cleaned.strip("-") or "untitled"


def split_file_name(file_name: str) -> tuple[str, str]:
    path = Path(file_name.strip())
    extension = path.suffix.lower()
    stem = path.stem if path.stem else path.name
    return stem, extension


def clean_file_name(file_name: str) -> str:
    stem, extension = split_file_name(file_name)
    clean_stem = slugify(stem)
    return f"{clean_stem}{extension}"


def read_reports(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        required_columns = {"subject", "experiment", "file_name"}
        missing = required_columns - set(reader.fieldnames or [])
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ValueError(f"Missing required column(s): {missing_list}")
        return [row for row in reader]


def build_suggested_path(report: dict[str, str]) -> str:
    subject = report["subject"].strip()
    experiment = report["experiment"].strip()
    file_name = report["file_name"].strip()
    return f"{subject}/{slugify(experiment)}/{clean_file_name(file_name)}"


def group_reports(reports: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for report in reports:
        report = dict(report)
        report["suggested_path"] = build_suggested_path(report)
        grouped[report["subject"].strip()].append(report)
    return dict(sorted(grouped.items()))


def build_index(reports: list[dict[str, str]]) -> str:
    grouped = group_reports(reports)
    lines = [
        "# Lab Report Organizer Index",
        "",
        "This index shows suggested clean folders and file names for my biotechnology lab reports.",
        "",
    ]

    for subject, subject_reports in grouped.items():
        lines.append(f"## {subject}")
        lines.append("")
        for report in sorted(subject_reports, key=lambda item: item["experiment"]):
            experiment = report["experiment"].strip()
            original = report["file_name"].strip()
            suggested = report["suggested_path"]
            lines.append(f"- {experiment}: `{suggested}`")
            lines.append(f"  - Original file: `{original}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a clean index for lab report file names.")
    parser.add_argument("csv_file", type=Path, help="CSV file with subject, experiment, and file_name columns")
    parser.add_argument("--output", type=Path, default=Path("lab_report_index.md"), help="Output Markdown index path")
    args = parser.parse_args()

    reports = read_reports(args.csv_file)
    index = build_index(reports)
    args.output.write_text(index, encoding="utf-8")
    print(f"Index created: {args.output}")


if __name__ == "__main__":
    main()
