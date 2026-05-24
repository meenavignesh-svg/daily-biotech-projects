# Protein Property Explorer

**Date:** 2026-05-24  
**Track:** Bioinformatics  
**Author:** Meena Vignesh M

## Purpose

This project analyzes protein sequences and reports beginner-friendly biochemical properties such as amino acid composition, estimated molecular weight, and aromatic amino acid count.

It is designed for a first-year biotechnology student learning how protein sequences can be studied with simple computational tools.

## Biotech Concept

Proteins are made of amino acids. Each amino acid has a one-letter code, such as A for alanine and G for glycine. By counting amino acids and estimating molecular weight, we can begin to understand protein composition and connect sequence data with biochemical properties.

## Features

- Reads protein sequences from a FASTA file
- Counts each amino acid
- Calculates sequence length
- Estimates molecular weight in Daltons
- Calculates percentage composition for each amino acid present
- Counts aromatic amino acids: F, W, and Y
- Flags unknown or non-standard characters

## Files

- `protein_property_explorer.py` - main Python script
- `sample_proteins.fasta` - sample protein sequences
- `example_report.txt` - sample output report

## How To Run

From this project folder, run:

```bash
python protein_property_explorer.py sample_proteins.fasta
```

To save the report:

```bash
python protein_property_explorer.py sample_proteins.fasta --output protein_report.txt
```

## Sample Input

```fasta
>insulin_fragment
GIVEQCCTSICSLYQLENYCN
```

## Sample Output

```text
Protein: insulin_fragment
Length: 21 amino acids
Estimated Molecular Weight: 2381.66 Da
Aromatic Amino Acids: 3
Unknown Characters: none
```

## What I Learned

- Protein sequences can be analyzed using one-letter amino acid codes
- Molecular weight can be estimated from amino acid masses
- Amino acid composition helps describe protein character
- Aromatic amino acids are important in protein structure and absorbance

## Possible Improvements

- Add isoelectric point estimation
- Add hydrophobicity scoring
- Create a bar chart of amino acid composition
- Compare two protein sequences side by side
