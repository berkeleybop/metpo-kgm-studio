# Curation Outputs

This directory stores LLM outputs and reviewed curation results.

## Structure

```
outputs/
├── raw/              # Raw LLM outputs before review
│   ├── curator1/
│   ├── curator2/
│   └── curator3/
└── reviewed/         # Reviewed and approved outputs
    ├── curator1/
    ├── curator2/
    └── curator3/
```

## Workflow

### 1. Save Raw Outputs

After getting an LLM response, save it to `raw/[your-name]/`:

```bash
# Naming format: YYYY-MM-DD_CLASSID_output.json
cat > outputs/raw/curator1/2025-10-02_METPO_0000123_output.json << 'EOF'
{
  "class_id": "METPO:0000123",
  "class_label": "methanogenesis",
  "proposed_definition": "...",
  "suggested_sources": ["PMID:12345678"]
}
EOF
```

### 2. Review and Refine

- Read the output critically
- Verify scientific accuracy
- Check sources exist and are relevant
- Revise if needed

### 3. Save Reviewed Outputs

After review, save the final version to `reviewed/[your-name]/`:

You can save as:
- TSV files matching ROBOT template format
- JSON files with structured data
- Whatever format works for merging back to assignments

### 4. Commit to Git

Both raw and reviewed outputs should be committed to git for:
- Reproducibility
- Tracking what LLM suggested vs. what you approved
- Inter-curator agreement analysis
- Learning from past work

## Tips

- **Don't skip the raw output step**: It's important to track what the LLM originally suggested
- **Review thoroughly**: LLMs can hallucinate sources and make scientific errors
- **Document changes**: If you modify LLM output significantly, note why in commit message
- **Share good examples**: If an LLM gives excellent output, share the prompt with the team!
