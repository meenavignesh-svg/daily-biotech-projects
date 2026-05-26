# Medical Coding Helper

**Date:** 2026-05-26  
**Track:** Productivity/Workflow Helper  
**Author:** Meena Vignesh M

## Purpose

I built this project as a simple learning tool to organize basic medical and laboratory terms with beginner-friendly code labels. This is only for education and revision, not for diagnosis, billing, or clinical decision-making.

## Biotech Concept

Biotechnology students often read lab reports, case examples, diagnostic test names, and research notes. A coding helper can make terms easier to search and group. This project shows how structured data can connect a term, category, simple description, and example code in one table.

## Features

- Reads a CSV file of educational medical/lab terms
- Searches terms by keyword
- Filters terms by category
- Prints a clean study table
- Exports search results to a CSV file
- Keeps a safe learning-only note in the output

## Files

- `medical_coding_helper.py` - main Python script
- `sample_terms.csv` - sample study terms
- `example_output.txt` - sample output

## How To Run

```bash
python medical_coding_helper.py sample_terms.csv --search glucose
```

Filter by category:

```bash
python medical_coding_helper.py sample_terms.csv --category Biochemistry
```

Export results:

```bash
python medical_coding_helper.py sample_terms.csv --search blood --output results.csv
```

## Sample Input

```csv
term,category,example_code,meaning
Blood Glucose Test,Biochemistry,LAB-GLU,Measures glucose level in blood sample
Complete Blood Count,Hematology,LAB-CBC,Counts major blood cell types
```

## Sample Output

```text
Medical Coding Helper - Study Output
Learning note: for education only, not for clinical or billing use.

Term                  Category       Code
Blood Glucose Test    Biochemistry   LAB-GLU
```

## What I Learned

- I learned how structured CSV data can support study tools
- I practiced filtering rows with Python
- I learned why healthcare-related tools need clear safety limits
- I understood how simple labels can make lab terms easier to revise

## Next Improvements

- Next I want to add more biotechnology lab terms
- Next I want to add a small web interface
- Next I want to support notes for each term
