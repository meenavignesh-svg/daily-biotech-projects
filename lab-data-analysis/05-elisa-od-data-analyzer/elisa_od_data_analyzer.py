"""Average ELISA OD readings from replicate sample rows."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def main() -> None:
  parser = argparse.ArgumentParser(description="Summarize ELISA OD values by sample.")
  parser.add_argument("csv_file", type=Path)
  args = parser.parse_args()
  readings: dict[str, list[float]] = defaultdict(list)
  with args.csv_file.open("r", encoding="utf-8", newline="") as file:
    for row in csv.DictReader(file):
      readings[row["sample"]].append(float(row["od450"]))
  print("ELISA OD Data Analyzer")
  for sample, values in sorted(readings.items(), key=lambda item: sum(item[1]) / len(item[1]), reverse=True):
    average = sum(values) / len(values)
    print(f"{sample}: average OD450={average:.3f} from {len(values)} replicates")


if __name__ == "__main__":
  main()