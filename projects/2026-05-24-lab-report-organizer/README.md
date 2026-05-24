# Lab Report Organizer

**Date:** 2026-05-24  
**Track:** Productivity/Workflow Helper  
**Author:** Meena Vignesh M

## Purpose

I built this project to organize biotechnology lab report files into clean folders and create a simple index. As a first-year biotechnology student, I want my practical work, observations, and report drafts to stay easy to find.

## Biotech Concept

Good lab documentation is important in biotechnology because experiments need clear records. Even a small practical class can create many files: observation notes, raw readings, final reports, and reference PDFs. A clean folder system helps avoid confusion and makes revision easier.

## Features

- Reads a list of lab report file names from a CSV file
- Cleans messy file names into a consistent format
- Groups reports by subject or practical topic
- Creates suggested folder paths
- Builds a Markdown index for quick revision
- Keeps the original file names in the output for checking

## Files

- `lab_report_organizer.py` - main Python script
- `sample_reports.csv` - sample lab report file list
- `example_index.md` - sample organized index

## How To Run

From this project folder, run:

```bash
python lab_report_organizer.py sample_reports.csv
```

To save the index with a custom name:

```bash
python lab_report_organizer.py sample_reports.csv --output my_lab_index.md
```

## Sample Input

```csv
subject,experiment,file_name
Microbiology,Gram Staining,gram staining final report.docx
Biochemistry,Protein Estimation,protein_estimation readings.pdf
Cell Biology,Microscopy,cell  microscopy observations.txt
```

## Sample Output

```text
## Microbiology

- Gram Staining: `Microbiology/gram-staining/gram-staining-final-report.docx`
```

## What I Learned

- I learned why clean file naming matters for lab work
- I practiced reading CSV files in Python
- I learned how to convert messy names into consistent names
- I understood how a simple index can make lab revision easier

## Possible Improvements

- Add real file moving after a preview step
- Add date-based folders
- Add support for PDF summaries
- Create a small desktop or web interface
