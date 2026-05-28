"""Calculate treatment versus control fold change from gene expression CSV data."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def classify(fold_change: float) -> str:
    if fold_change >= 1.5:
        return "upregulated"
    if fold_change <= 0.67:
        return "downregulated"
    return "similar"


def safe_fold_change(control: float, treatment: float) -> float:
    return treatment / control if control else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize gene expression fold change.")
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args()

    print("Gene Expression Fold-Change Analysis")
    with args.csv_file.open("r", encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            control = float(row["control"])
            treatment = float(row["treatment"])
            fold_change = safe_fold_change(control, treatment)
            print(
                f"{row['gene']}: control={control:.2f}, treatment={treatment:.2f}, "
                f"fold_change={fold_change:.2f}, status={classify(fold_change)}"
            )


if __name__ == "__main__":
    main()
