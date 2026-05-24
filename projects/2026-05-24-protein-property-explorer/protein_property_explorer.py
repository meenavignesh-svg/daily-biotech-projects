"""Explore beginner-friendly properties of protein sequences from FASTA files."""

from __future__ import annotations

import argparse
from pathlib import Path

AMINO_ACID_MASSES = {
    "A": 89.09,
    "R": 174.20,
    "N": 132.12,
    "D": 133.10,
    "C": 121.16,
    "E": 147.13,
    "Q": 146.15,
    "G": 75.07,
    "H": 155.16,
    "I": 131.17,
    "L": 131.17,
    "K": 146.19,
    "M": 149.21,
    "F": 165.19,
    "P": 115.13,
    "S": 105.09,
    "T": 119.12,
    "W": 204.23,
    "Y": 181.19,
    "V": 117.15,
}

AROMATIC_AMINO_ACIDS = {"F", "W", "Y"}
WATER_MASS = 18.015


def read_fasta(path: Path) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    current_name: str | None = None
    current_parts: list[str] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if current_name is not None:
                records.append((current_name, "".join(current_parts).upper()))
            current_name = line[1:].strip() or "unnamed_protein"
            current_parts = []
        else:
            current_parts.append(line.replace(" ", ""))

    if current_name is not None:
        records.append((current_name, "".join(current_parts).upper()))

    if not records:
        raise ValueError("No FASTA protein records were found.")

    return records


def amino_acid_counts(sequence: str) -> dict[str, int]:
    return {aa: sequence.count(aa) for aa in AMINO_ACID_MASSES}


def estimate_molecular_weight(sequence: str) -> float:
    known_masses = [AMINO_ACID_MASSES[aa] for aa in sequence if aa in AMINO_ACID_MASSES]
    if not known_masses:
        return 0.0
    return sum(known_masses) - (len(known_masses) - 1) * WATER_MASS


def composition_lines(sequence: str, counts: dict[str, int]) -> list[str]:
    if not sequence:
        return ["  no amino acids found"]

    lines = []
    for aa in sorted(AMINO_ACID_MASSES):
        count = counts[aa]
        if count:
            percentage = (count / len(sequence)) * 100
            lines.append(f"  {aa}: {count} ({percentage:.1f}%)")
    return lines


def analyze_protein(name: str, sequence: str) -> str:
    counts = amino_acid_counts(sequence)
    unknown = sorted(set(sequence) - set(AMINO_ACID_MASSES))
    aromatic_count = sum(sequence.count(aa) for aa in AROMATIC_AMINO_ACIDS)

    lines = [
        f"Protein: {name}",
        f"Length: {len(sequence)} amino acids",
        f"Estimated Molecular Weight: {estimate_molecular_weight(sequence):.2f} Da",
        f"Aromatic Amino Acids: {aromatic_count}",
        "Unknown Characters: " + (", ".join(unknown) if unknown else "none"),
        "Amino Acid Composition:",
    ]
    lines.extend(composition_lines(sequence, counts))
    return "\n".join(lines)


def build_report(records: list[tuple[str, str]]) -> str:
    return "\n\n".join(analyze_protein(name, sequence) for name, sequence in records) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Explore basic properties of protein FASTA sequences.")
    parser.add_argument("fasta_file", type=Path, help="Path to a protein FASTA file")
    parser.add_argument("--output", type=Path, help="Optional path to save the report")
    args = parser.parse_args()

    report = build_report(read_fasta(args.fasta_file))

    if args.output:
        args.output.write_text(report, encoding="utf-8")
        print(f"Report saved to {args.output}")
    else:
        print(report, end="")


if __name__ == "__main__":
    main()
