"""Answer beginner biotechnology term questions using a small dictionary."""

from __future__ import annotations

import argparse
from pathlib import Path

ANSWERS = {
    "dna": "DNA stores genetic information using A, T, G, and C bases.",
    "pcr": "PCR makes many copies of a selected DNA region.",
    "plasmid": "A plasmid is a small circular DNA molecule often found in bacteria.",
}


def answer_question(question: str) -> str:
    lower_question = question.lower()
    for term, answer in ANSWERS.items():
        if term in lower_question:
            return answer
    return "I need to add this term to my study dictionary."


def main() -> None:
    parser = argparse.ArgumentParser(description="Answer beginner biotechnology term questions.")
    parser.add_argument("questions_file", type=Path)
    args = parser.parse_args()
    for question in args.questions_file.read_text(encoding="utf-8").splitlines():
        if question.strip():
            print(f"Q: {question}")
            print(f"A: {answer_question(question)}")
            print()


if __name__ == "__main__":
    main()
