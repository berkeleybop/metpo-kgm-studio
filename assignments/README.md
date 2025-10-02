# Curator Assignments

This directory contains TSV files with class assignments for each curator.

## Files

- `marcin.tsv`: Classes assigned to Marcin (28 classes)
- `mark.tsv`: Classes assigned to Mark (32 classes)
- `sujay.tsv`: Classes assigned to Sujay (32 classes)
- `curator4.tsv`: Classes assigned to intern 1 (32 classes)
- `curator5.tsv`: Classes assigned to intern 2 (32 classes)
- `curator6.tsv`: Classes assigned to intern 3 (31 classes)

**Total**: 147 unique classes from METPO ontology

## Format

Each file is a ROBOT template with these columns:
- **ID**: Ontology class ID (e.g., METPO:1000059)
- **LABEL**: Human-readable class label
- **TYPE**: owl:Class
- **parent class**: Parent class in the hierarchy
- **description**: Short description of the class
- **definition source**: Source citations (PMID, DOI, ontology IDs, etc.)
- **comment**: Additional notes
- Plus synonym columns for cross-referencing

## Overlap

Assignments have **20% overlap** for inter-curator agreement assessment.
This means some classes appear in multiple curator files - this is intentional!

Adjacent curators share overlapping classes to measure consistency in curation decisions.

## Flexibility

**Note**: Class assignments are not fixed! We can move classes between curators if:
- Someone needs to complete an entire subclass hierarchy
- Workload needs rebalancing (e.g., reducing Sujay's assignment)
- Specialized knowledge makes one person better suited

When moving classes, ensure non-overlapping (unique) assignments are redistributed to maintain coverage.

## Refreshing Assignments

To re-fetch assignments from Google Sheets:

```bash
just fetch-assignments
```

**Warning**: This will overwrite existing assignment files!

## Working with Assignments

1. Open your assignment file (e.g., `marcin.tsv`)
2. Fill in definitions and sources for each class
3. Validate: `just validate-file assignments/marcin.tsv`
4. Commit your changes

See `CURATION_GUIDE.md` for detailed instructions.

## Current Statistics

Run `just assignment-stats` to see current class counts per curator.
