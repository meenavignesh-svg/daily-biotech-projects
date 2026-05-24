"""Create a beginner-friendly global alignment for two FASTA sequences."""

from __future__ import annotations

import argparse
from pathlib import Path

MATCH_SCORE = 1
MISMATCH_SCORE = -1
GAP_SCORE = -2


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
            current_name = line[1:].strip() or "unnamed_sequence"
            current_parts = []
        else:
            current_parts.append(line.replace(" ", ""))

    if current_name is not None:
        records.append((current_name, "".join(current_parts).upper()))

    if len(records) != 2:
        raise ValueError("This beginner tool expects exactly two FASTA sequences.")

    return records


def score_pair(base_a: str, base_b: str) -> int:
    return MATCH_SCORE if base_a == base_b else MISMATCH_SCORE


def global_align(seq_a: str, seq_b: str) -> tuple[str, str, int]:
    rows = len(seq_a) + 1
    cols = len(seq_b) + 1
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    for row in range(1, rows):
        matrix[row][0] = row * GAP_SCORE
    for col in range(1, cols):
        matrix[0][col] = col * GAP_SCORE

    for row in range(1, rows):
        for col in range(1, cols):
            diagonal = matrix[row - 1][col - 1] + score_pair(seq_a[row - 1], seq_b[col - 1])
            up = matrix[row - 1][col] + GAP_SCORE
            left = matrix[row][col - 1] + GAP_SCORE
            matrix[row][col] = max(diagonal, up, left)

    aligned_a: list[str] = []
    aligned_b: list[str] = []
    row = len(seq_a)
    col = len(seq_b)

    while row > 0 or col > 0:
        if row > 0 and col > 0:
            diagonal_score = matrix[row - 1][col - 1] + score_pair(seq_a[row - 1], seq_b[col - 1])
            if matrix[row][col] == diagonal_score:
                aligned_a.append(seq_a[row - 1])
                aligned_b.append(seq_b[col - 1])
                row -= 1
                col -= 1
                continue

        if row > 0 and matrix[row][col] == matrix[row - 1][col] + GAP_SCORE:
            aligned_a.append(seq_a[row - 1])
            aligned_b.append("-")
            row -= 1
        else:
            aligned_a.append("-")
            aligned_b.append(seq_b[col - 1])
            col -= 1

    return "".join(reversed(aligned_a)), "".join(reversed(aligned_b)), matrix[-1][-1]


def summarize_alignment(aligned_a: str, aligned_b: str) -> dict[str, float | int | str]:
    matches = 0
    mismatches = 0
    gaps = 0
    visual = []

    for base_a, base_b in zip(aligned_a, aligned_b):
        if base_a == "-" or base_b == "-":
            gaps += 1
            visual.append(" ")
        elif base_a == base_b:
            matches += 1
            visual.append("|")
        else:
            mismatches += 1
            visual.append(" ")

    alignment_length = len(aligned_a)
    percent_identity = (matches / alignment_length) * 100 if alignment_length else 0.0

    return {
        "matches": matches,
        "mismatches": mismatches,
        "gaps": gaps,
        "percent_identity": percent_identity,
        "visual": "".join(visual),
    }


def build_report(records: list[tuple[str, str]]) -> str:
    (name_a, seq_a), (name_b, seq_b) = records
    aligned_a, aligned_b, score = global_align(seq_a, seq_b)
    summary = summarize_alignment(aligned_a, aligned_b)

    return (
        "Simple Sequence Alignment Report\n"
        "================================\n\n"
        f"Sequence A: {name_a}\n"
        f"Sequence B: {name_b}\n"
        f"Scoring: match={MATCH_SCORE}, mismatch={MISMATCH_SCORE}, gap={GAP_SCORE}\n\n"
        f"{name_a:<12} {aligned_a}\n"
        f"{'':<12} {summary['visual']}\n"
        f"{name_b:<12} {aligned_b}\n\n"
        f"Alignment Score: {score}\n"
        f"Matches: {summary['matches']}\n"
        f"Mismatches: {summary['mismatches']}\n"
        f"Gaps: {summary['gaps']}\n"
        f"Percent Identity: {summary['percent_identity']:.2f}%\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Align two short FASTA sequences.")
    parser.add_argument("fasta_file", type=Path, help="Path to a FASTA file with exactly two sequences")
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
