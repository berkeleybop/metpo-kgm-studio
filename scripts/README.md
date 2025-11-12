# JSON to ROBOT TSV Converter

Convert LLM-generated JSON ontology definitions to ROBOT template TSV format for ontology integration.

## Requirements

**Python 3.6+** - No external dependencies required! Uses only Python standard library.

## Quick Start

### 1. Check Python Installation

```bash
python --version
```

or

```bash
python3 --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/)

### 2. Run the Converter

```bash
python scripts/json_to_robot_tsv.py <input.json> <output.tsv>
```

## Usage Examples

### Convert a single batch file:

```bash
python scripts/json_to_robot_tsv.py \
    outputs/raw/curator5/2025-10-30_curator5_v2.1_batch1_output.json \
    outputs/batch1_robot.tsv
```

### Convert multiple batches:

```bash
# Batch 1
python scripts/json_to_robot_tsv.py \
    outputs/raw/curator5/2025-10-30_curator5_v2.1_batch1_output.json \
    outputs/batch1_robot.tsv

# Batch 2
python scripts/json_to_robot_tsv.py \
    outputs/raw/curator5/2025-10-30_curator5_v2.1_batch2_output.json \
    outputs/batch2_robot.tsv

# Batch 3
python scripts/json_to_robot_tsv.py \
    outputs/raw/curator5/2025-10-30_curator5_v2.1_batch3_output.json \
    outputs/batch3_robot.tsv

# Batch 4
python scripts/json_to_robot_tsv.py \
    outputs/raw/curator5/2025-10-30_curator5_v2.1_batch4_output.json \
    outputs/batch4_robot.tsv
```

## What It Does

The script performs the following operations:

1. **Reads** JSON file with ontology term definitions
2. **Validates** JSON structure (checks for 'definitions' key)
3. **Extracts** term information:
   - Class IDs (e.g., `METPO:1000845`)
   - Labels (e.g., "Acetogenesis")
   - Parent classes
   - Definitions
   - Sources (ontology references and literature)
   - Quantitative values (if present)
   - Reasoning and comments
4. **Converts** structured sources to pipe-separated format:
   - v2.1 format: `[{"type": "ontology", "id": "GO:0015948", ...}]` → `GO:0015948|ENVO:00002029`
   - Legacy format: `["OLS:GO:0009061", "PMID:12345"]` → `OLS:GO:0009061|PMID:12345`
5. **Combines** metadata into comment field:
   - Original comments/notes
   - Quantitative values with measurement sources
   - Reasoning from LLM
   - Parent class IDs
6. **Writes** ROBOT template TSV file with:
   - Header row (column names)
   - Annotation row (ROBOT directives)
   - Data rows (one per definition)

## Output Format

The script generates a TSV file ready for ROBOT with:

- **Column 1 (ID):** Class identifier (e.g., `METPO:1000845`)
- **Column 2 (label):** Human-readable label
- **Column 3 (TYPE):** Always `owl:Class`
- **Column 4 (parent class):** Parent class name
- **Column 5 (description):** Textual definition (IAO:0000115)
- **Column 6 (definition source):** Pipe-separated source IDs (IAO:0000119)
- **Column 7 (comment):** Combined comments, reasoning, quantitative values
- **Columns 8-14:** Empty (reserved for synonyms and other annotations)

### Example Output:

```
✅ Wrote 8 definitions to outputs/batch1_robot.tsv
✨ Conversion complete!
```

## Dependencies

All dependencies are Python standard library (included with Python):

- `json` - JSON parsing
- `csv` - TSV file writing
- `sys` - Command-line arguments
- `pathlib` - File path handling
- `typing` - Type hints

**No pip install required!** 🎉

## Supported Input Formats

### v2.1 Format (Recommended)
JSON with structured sources including URLs and metadata:

```json
{
    "metadata": {
        "prompt_version": "2.1",
        "curator": "curator5",
        ...
    },
    "definitions": [
        {
            "class_id": "METPO:1000845",
            "class_label": "Acetogenesis",
            "parent_class": "metabolism",
            "parent_class_id": "GO:0008152",
            "proposed_definition": "A metabolic process...",
            "quantitative_values": {...},
            "reasoning": "...",
            "sources": [
                {
                    "type": "ontology",
                    "id": "GO:0019413",
                    "label": "acetate biosynthetic process",
                    "url": "http://purl.obolibrary.org/obo/GO_0019413"
                }
            ]
        }
    ]
}
```

### Legacy Format
JSON with simple source arrays:

```json
{
    "definitions": [
        {
            "class_id": "METPO:1000845",
            "class_label": "Acetogenesis",
            "parent_class": "metabolism",
            "proposed_definition": "A metabolic process...",
            "sources": ["OLS:GO:0019413", "PMID:21183676"],
            "notes": "..."
        }
    ]
}
```

## Using Output with ROBOT

Once you have the TSV file, use it with ROBOT to update your ontology:

```bash
robot template \
    --template outputs/batch1_robot.tsv \
    --ontology-iri http://purl.obolibrary.org/obo/metpo.owl \
    --output metpo_updated.owl
```

## Troubleshooting

### "Python was not found"
- Install Python from [python.org](https://www.python.org/downloads/)
- On some systems, use `python3` instead of `python`

### "JSON file not found"
- Check that the file path is correct
- Use absolute paths if relative paths don't work
- Ensure you're running the command from the repository root directory

### "JSON must contain 'definitions' key"
- Verify your JSON file has the correct structure
- Check that it's a valid JSON file (use a JSON validator)

## Platform-Specific Notes

### Windows (PowerShell/CMD)
```powershell
python scripts\json_to_robot_tsv.py input.json output.tsv
```

### macOS/Linux
```bash
python3 scripts/json_to_robot_tsv.py input.json output.tsv
```

## Script Version

**Version:** 2.1 (2025-10-30)

**Features:**
- ✅ Supports v2.1 format with structured sources
- ✅ Supports legacy format with simple source lists
- ✅ Extracts parent class IDs
- ✅ Formats quantitative values with measurement sources
- ✅ Combines comments, reasoning, and metadata
- ✅ Minimal output for clean execution
- ✅ Zero external dependencies

## Questions or Issues?

If you encounter any problems or have questions:

1. Verify Python 3.6+ is installed
2. Check that your JSON file is valid
3. Ensure all file paths are correct
4. Review the error message for specific issues

## License

See repository LICENSE file for details.
