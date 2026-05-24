# Simple Sequence Alignment

**Date:** 2026-05-24  
**Track:** Bioinformatics  
**Author:** Meena Vignesh M

## Purpose

This project compares two short biological sequences and creates a simple pairwise alignment report. It is designed to explain matches, mismatches, gaps, and percent identity in a beginner-friendly way.

## Biotech Concept

Sequence alignment is a basic bioinformatics method used to compare DNA, RNA, or protein sequences. Similar sequences may suggest related function, shared ancestry, or conserved biological regions. This project uses a simple global alignment approach to introduce the concept without advanced algorithms becoming overwhelming.

## Features

- Reads two sequences from a FASTA file
- Performs simple global pairwise alignment
- Uses beginner-friendly scoring: match, mismatch, and gap
- Reports alignment score
- Calculates percent identity
- Counts matches, mismatches, and gaps
- Shows a visual alignment line using `|` for matches

## Files

- `simple_sequence_alignment.py` - main Python script
- `sample_pair.fasta` - sample input containing two DNA sequences
- `example_report.txt` - sample alignment output

## How To Run

From this project folder, run:

```bash
python simple_sequence_alignment.py sample_pair.fasta
```

To save the report:

```bash
python simple_sequence_alignment.py sample_pair.fasta --output alignment_report.txt
```

## Sample Input

```fasta
>sequence_a
ATGCTAGCTAG
>sequence_b
ATGCGAGCTAG
```

## Sample Output

```text
sequence_a  ATGCTAGCTAG
            |||| ||||||
sequence_b  ATGCGAGCTAG

Percent Identity: 90.91%
```

## What I Learned

- Sequence alignment compares biological sequences position by position
- Matches increase similarity, while mismatches and gaps reduce it
- Percent identity is a simple way to describe sequence similarity
- Alignment is a foundation for many bioinformatics workflows

## Possible Improvements

- Add local alignment
- Add custom scoring from command-line options
- Support protein alignment examples
- Export alignment results as CSV
