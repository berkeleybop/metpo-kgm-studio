# Curator Assignments

This directory contains TSV files with class assignments for each curator.

## Files

- `curator1.tsv`: Classes assigned to curator 1
- `curator2.tsv`: Classes assigned to curator 2
- `curator3.tsv`: Classes assigned to curator 3

## Format

Each file is a ROBOT template with these columns:
- **ID**: Ontology class ID (e.g., METPO:0000123)
- **LABEL**: Human-readable class label
- **A definition**: Textual definition (to be filled in)
- **A definition source**: Source citations (PMID, DOI, etc.)

## Overlap

Assignments have {{ overlap_percentage }}% overlap for inter-curator agreement assessment.
This means some classes appear in multiple curator files - this is intentional!

## Refreshing Assignments

To re-fetch assignments from Google Sheets:

```bash
just fetch-assignments
```

**Warning**: This will overwrite existing assignment files!

## Working with Assignments

1. Open your assignment file (e.g., `curator1.tsv`)
2. Fill in definitions and sources for each class
3. Validate: `just validate-file assignments/curator1.tsv`
4. Commit your changes

See `CURATION_GUIDE.md` for detailed instructions.
