"""Convert a copied lab report table into a clean CSV file."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_table(text: str) -> list[list[str]]:
  rows: list[list[str]] = []
  for line in text.splitlines():
    if line.strip():
      rows.append([cell.strip() for cell in line.split("|")])
  return rows


def main() -> None:
  parser = argparse.ArgumentParser(description="Clean copied lab table text into CSV.")
  parser.add_argument("text_file", type=Path)
  parser.add_argument("--output", type=Path, default=Path("clean_lab_table.csv"))
  args = parser.parse_args()
  rows = parse_table(args.text_file.read_text(encoding="utf-8"))
  with args.output.open("w", encoding="utf-8", newline="") as file:
    csv.writer(file).writerows(rows)
  print(f"Saved {len(rows)} cleaned rows to {args.output}")


if __name__ == "__main__":
  main()