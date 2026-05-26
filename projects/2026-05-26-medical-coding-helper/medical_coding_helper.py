"""Study helper for organizing educational medical and laboratory terms."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REQUIRED_COLUMNS = {"term", "category", "example_code", "meaning"}


def read_terms(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            missing_text = ", ".join(sorted(missing))
            raise ValueError(f"Missing required column(s): {missing_text}")
        return [{key: value.strip() for key, value in row.items()} for row in reader]


def filter_terms(
    terms: list[dict[str, str]],
    search: str | None = None,
    category: str | None = None,
) -> list[dict[str, str]]:
    results = terms

    if search:
        search_text = search.lower()
        results = [
            term
            for term in results
            if search_text in term["term"].lower()
            or search_text in term["meaning"].lower()
            or search_text in term["example_code"].lower()
        ]

    if category:
        category_text = category.lower()
        results = [term for term in results if category_text in term["category"].lower()]

    return results


def build_table(terms: list[dict[str, str]]) -> str:
    lines = [
        "Medical Coding Helper - Study Output",
        "Learning note: for education only, not for clinical or billing use.",
        "",
    ]

    if not terms:
        lines.append("No matching study terms found.")
        return "\n".join(lines) + "\n"

    term_width = max(len("Term"), *(len(item["term"]) for item in terms))
    category_width = max(len("Category"), *(len(item["category"]) for item in terms))
    code_width = max(len("Code"), *(len(item["example_code"]) for item in terms))

    lines.append(f"{'Term':<{term_width}}  {'Category':<{category_width}}  {'Code':<{code_width}}  Meaning")
    lines.append(f"{'-' * term_width}  {'-' * category_width}  {'-' * code_width}  {'-' * 7}")

    for item in terms:
        lines.append(
            f"{item['term']:<{term_width}}  "
            f"{item['category']:<{category_width}}  "
            f"{item['example_code']:<{code_width}}  "
            f"{item['meaning']}"
        )

    return "\n".join(lines) + "\n"


def write_csv(path: Path, terms: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["term", "category", "example_code", "meaning"])
        writer.writeheader()
        writer.writerows(terms)


def main() -> None:
    parser = argparse.ArgumentParser(description="Search educational medical and lab coding terms.")
    parser.add_argument("csv_file", type=Path, help="CSV file with term, category, example_code, and meaning columns")
    parser.add_argument("--search", help="Keyword to search in term, meaning, or code")
    parser.add_argument("--category", help="Category filter, such as Biochemistry or Microbiology")
    parser.add_argument("--output", type=Path, help="Optional CSV file to save matching rows")
    args = parser.parse_args()

    terms = read_terms(args.csv_file)
    results = filter_terms(terms, search=args.search, category=args.category)
    print(build_table(results), end="")

    if args.output:
        write_csv(args.output, results)
        print(f"\nSaved matching rows to {args.output}")


if __name__ == "__main__":
    main()
