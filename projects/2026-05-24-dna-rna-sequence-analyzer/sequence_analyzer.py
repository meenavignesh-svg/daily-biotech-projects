"""Analyze simple DNA and RNA sequences from a FASTA file."""

from __future__ import annotations

import argparse
from pathlib import Path

DNA_BASES = set("ATGC")
RNA_BASES = set("AUGC")
COMPLEMENT = str.maketrans("ATGC", "TACG")


def read_fasta(path: Path) -> list[tuple[str, str]]:
    """Read a FASTA file and return a list of (name, sequence) pairs."""
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
            current_name = line[1:].strip() or "unnamed_sequence"
            current_parts = []
        else:
            current_parts.append(line.replace(" ", ""))

    if current_name is not None:
        records.append((current_name, "".join(current_parts).upper()))

    if not records:
        raise ValueError("No FASTA records were found.")

    return records


def detect_sequence_type(sequence: str) -> str:
    bases = set(sequence)
    if bases <= DNA_BASES:
        return "DNA"
    if bases <= RNA_BASES:
        return "RNA"
    return "Mixed or unknown"


def gc_content(sequence: str) -> float:
    if not sequence:
        return 0.0
    gc_count = sequence.count("G") + sequence.count("C")
    return (gc_count / len(sequence)) * 100


def base_counts(sequence: str) -> dict[str, int]:
    return {base: sequence.count(base) for base in "ATGCU"}


def transcribe_dna(sequence: str) -> str:
    return sequence.replace("T", "U")


def reverse_complement_dna(sequence: str) -> str:
    return sequence.translate(COMPLEMENT)[::-1]


def analyze_record(name: str, sequence: str) -> str:
    sequence_type = detect_sequence_type(sequence)
    counts = base_counts(sequence)

    lines = [
        f"Sequence: {name}",
        f"Type: {sequence_type}",
        f"Length: {len(sequence)} bases",
        "Base Counts: " + ", ".join(f"{base}={counts[base]}" for base in "ATGCU"),
        f"GC Content: {gc_content(sequence):.2f}%",
    ]

    if sequence_type == "DNA":
        lines.append(f"RNA Transcript: {transcribe_dna(sequence)}")
        lines.append(f"Reverse Complement: {reverse_complement_dna(sequence)}")
    elif sequence_type == "RNA":
        lines.append("RNA Transcript: already RNA")
        lines.append("Reverse Complement: not calculated for RNA input")
    else:
        lines.append("Note: sequence contains characters outside standard DNA/RNA bases")

    return "\n".join(lines)


def build_report(records: list[tuple[str, str]]) -> str:
    sections = [analyze_record(name, sequence) for name, sequence in records]
    return "\n\n".join(sections) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze DNA/RNA sequences from a FASTA file.")
    parser.add_argument("fasta_file", type=Path, help="Path to an input FASTA file")
    parser.add_argument("--output", type=Path, help="Optional path to save the report")
    args = parser.parse_args()

    records = read_fasta(args.fasta_file)
    report = build_report(records)

    if args.output:
        args.output.write_text(report, encoding="utf-8")
        print(f"Report saved to {args.output}")
    else:
        print(report, end="")


if __name__ == "__main__":
    main()
