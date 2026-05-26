"""Convert copied lab table text into a clean CSV file."""

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
