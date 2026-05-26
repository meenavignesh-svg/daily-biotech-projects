"""Analyze a small DNA FASTA file and print a clean sequence report."""

from __future__ import annotations

import argparse
from pathlib import Path


def read_fasta(path: Path) -> dict[str, str]:
    records: dict[str, str] = {}
    current_name = ""
    parts: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if current_name:
                records[current_name] = "".join(parts).upper()
            current_name = line[1:].strip()
            parts = []
        else:
            parts.append(line)
    if current_name:
        records[current_name] = "".join(parts).upper()
    return records


def gc_content(sequence: str) -> float:
    if not sequence:
        return 0.0
    gc_count = sequence.count("G") + sequence.count("C")
    return (gc_count / len(sequence)) * 100


def transcribe(sequence: str) -> str:
    return sequence.replace("T", "U")


def summarize(records: dict[str, str]) -> str:
    lines = ["DNA FASTA Analyzer", ""]
    for name, sequence in records.items():
        counts = {base: sequence.count(base) for base in "ATGC"}
        lines.append(f"Sequence: {name}")
        lines.append(f"Length: {len(sequence)} bases")
        lines.append(f"A={counts['A']} T={counts['T']} G={counts['G']} C={counts['C']}")
        lines.append(f"GC content: {gc_content(sequence):.2f}%")
        lines.append(f"RNA transcript: {transcribe(sequence)}")
        lines.append("")
    return "\n".join(lines).rstrip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize DNA sequences from a FASTA file.")
    parser.add_argument("fasta_file", type=Path)
    args = parser.parse_args()
    print(summarize(read_fasta(args.fasta_file)))


if __name__ == "__main__":
    main()
