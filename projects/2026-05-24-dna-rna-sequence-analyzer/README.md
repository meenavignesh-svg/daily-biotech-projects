# DNA/RNA Sequence Analyzer

**Date:** 2026-05-24  
**Author:** Meena Vignesh M

## Purpose

This beginner-friendly bioinformatics project analyzes short DNA or RNA sequences and reports useful sequence properties such as length, base composition, GC content, transcription, and reverse complement.

It is designed as an early biotechnology learning project to connect molecular biology concepts with simple Python programming.

## Biotech Concept

DNA and RNA sequences are made of nucleotide bases. By counting bases and calculating GC content, we can understand basic sequence composition. GC content is commonly used in molecular biology because G-C pairs have three hydrogen bonds, while A-T pairs have two, which can affect sequence stability.

## Features

- Reads sequences from a FASTA file
- Supports DNA and RNA-style input
- Calculates sequence length
- Counts A, T, G, C, and U bases
- Calculates GC content percentage
- Converts DNA to RNA by transcription
- Generates reverse complement for DNA sequences
- Writes a clear text report

## Files

- `sequence_analyzer.py` - main Python script
- `sample_sequences.fasta` - sample input sequences
- `example_report.txt` - sample output report

## How To Run

From this project folder, run:

```bash
python sequence_analyzer.py sample_sequences.fasta
```

To save the report:

```bash
python sequence_analyzer.py sample_sequences.fasta --output my_report.txt
```

## Sample Input

```fasta
>sample_dna_1
ATGCGTACGTTAGC
```

## Sample Output

```text
Sequence: sample_dna_1
Type: DNA
Length: 14 bases
GC Content: 50.00%
RNA Transcript: AUGCGUACGUUAGC
Reverse Complement: GCTAACGTACGCAT
```

## What I Learned

- How biological sequences can be stored in FASTA format
- How to calculate nucleotide composition
- Why GC content is useful in sequence analysis
- How transcription changes DNA sequence notation into RNA notation
- How Python can support basic bioinformatics workflows

## Possible Improvements

- Add amino acid translation from coding DNA
- Add charts for base composition
- Support larger FASTA files
- Add primer melting temperature estimation
