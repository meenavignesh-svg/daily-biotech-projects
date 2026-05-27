"""Calculate beginner-friendly protein sequence properties."""

from __future__ import annotations

import argparse
from pathlib import Path

AMINO_ACID_MASS = {
    "A": 89.09, "R": 174.20, "N": 132.12, "D": 133.10, "C": 121.15,
    "E": 147.13, "Q": 146.15, "G": 75.07, "H": 155.16, "I": 131.17,
    "L": 131.17, "K": 146.19, "M": 149.21, "F": 165.19, "P": 115.13,
    "S": 105.09, "T": 119.12, "W": 204.23, "Y": 181.19, "V": 117.15,
}

HYDROPHOBIC = set("AILMFWYV")
CHARGED = set("RHKDE")


def clean_sequence(text: str) -> str:
    return "".join(char for char in text.upper() if char in AMINO_ACID_MASS)


def molecular_weight(sequence: str) -> float:
    return sum(AMINO_ACID_MASS[amino_acid] for amino_acid in sequence)


def percent(part: int, total: int) -> float:
    return (part / total) * 100 if total else 0.0


def composition(sequence: str) -> dict[str, int]:
    return {amino_acid: sequence.count(amino_acid) for amino_acid in sorted(set(sequence))}


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate simple protein properties.")
    parser.add_argument("sequence_file", type=Path)
    args = parser.parse_args()

    sequence = clean_sequence(args.sequence_file.read_text(encoding="utf-8"))
    hydrophobic_count = sum(1 for amino_acid in sequence if amino_acid in HYDROPHOBIC)
    charged_count = sum(1 for amino_acid in sequence if amino_acid in CHARGED)

    print("Protein Property Calculator")
    print(f"Length: {len(sequence)} amino acids")
    print(f"Approximate molecular weight: {molecular_weight(sequence):.2f} Da")
    print(f"Hydrophobic residues: {hydrophobic_count} ({percent(hydrophobic_count, len(sequence)):.1f}%)")
    print(f"Charged residues: {charged_count} ({percent(charged_count, len(sequence)):.1f}%)")
    print("Composition:")
    for amino_acid, count in composition(sequence).items():
        print(f"  {amino_acid}: {count}")


if __name__ == "__main__":
    main()
