"""Check simple PCR primer quality rules from a CSV file."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def gc_content(sequence: str) -> float:
    return ((sequence.count("G") + sequence.count("C")) / len(sequence)) * 100 if sequence else 0.0


def melting_temperature(sequence: str) -> int:
    return 2 * (sequence.count("A") + sequence.count("T")) + 4 * (sequence.count("G") + sequence.count("C"))


def review_notes(sequence: str) -> list[str]:
    notes: list[str] = []
    gc = gc_content(sequence)
    tm = melting_temperature(sequence)
    if not 18 <= len(sequence) <= 25:
        notes.append("length outside 18-25 bases")
    if not 40 <= gc <= 60:
        notes.append("GC content outside 40-60%")
    if not 50 <= tm <= 65:
        notes.append("melting temperature outside 50-65 C")
    return notes


def primer_status(sequence: str) -> str:
    return "PASS" if not review_notes(sequence) else "REVIEW"


def main() -> None:
    parser = argparse.ArgumentParser(description="Screen primers using beginner PCR quality rules.")
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args()

    print("Primer Quality Checker")
    with args.csv_file.open("r", encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            sequence = row["sequence"].strip().upper()
            notes = review_notes(sequence)
            note_text = "; ".join(notes) if notes else "basic checks passed"
            print(
                f"{row['primer']}: {primer_status(sequence)} | "
                f"length={len(sequence)} | GC={gc_content(sequence):.1f}% | "
                f"Tm={melting_temperature(sequence)} C | {note_text}"
            )


if __name__ == "__main__":
    main()
