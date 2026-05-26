"""Summarize simple gene expression changes from a CSV file."""

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
            print(f"{row['gene']}: {classify_change(control, treatment)}, fold change = {fold_change:.2f}")


if __name__ == "__main__":
    main()
