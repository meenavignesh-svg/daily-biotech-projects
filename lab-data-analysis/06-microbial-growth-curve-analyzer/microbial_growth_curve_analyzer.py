"""Summarize a microbial OD600 growth curve from CSV data."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> None:
  parser = argparse.ArgumentParser(description="Analyze a simple microbial growth curve.")
  parser.add_argument("csv_file", type=Path)
  args = parser.parse_args()
  points: list[tuple[float, float]] = []
  with args.csv_file.open("r", encoding="utf-8", newline="") as file:
    for row in csv.DictReader(file):
      points.append((float(row["hour"]), float(row["od600"])))
  peak_hour, peak_od = max(points, key=lambda point: point[1])
  fastest = max(zip(points, points[1:]), key=lambda pair: pair[1][1] - pair[0][1])
  print("Microbial Growth Curve Analyzer")
  print(f"Peak OD600: {peak_od:.2f} at {peak_hour:.1f} hours")
  print(f"Fastest increase: hour {fastest[0][0]:.1f} to {fastest[1][0]:.1f}")


if __name__ == "__main__":
  main()