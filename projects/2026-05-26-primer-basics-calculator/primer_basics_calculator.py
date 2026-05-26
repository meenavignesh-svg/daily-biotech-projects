"""Calculate beginner-friendly primer properties from a CSV file."""

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
    return "
".join(lines).rstrip() + "
"


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate basic primer properties.")
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args()
    print(build_report(read_primers(args.csv_file)), end="")


if __name__ == "__main__":
    main()
