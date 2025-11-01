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
# Naming format: YYYY-MM-DD_curatr_output.json
{
    "metadata":  {
                     "total_definitions":  29,
                     "curator":  "curator5",
                     "ontology":  "METPO",
                     "description":  "OBO Foundry-compliant definitions for METPO terms - final version",
                     "generation_date":  "2025-10-09"
                 },
    "definitions":  [
                        {
                            "confidence":  "high",
                            "class_label":  "Acetogenesis",
                            "proposed_definition":  "A metabolic process in which acetate is produced as the primary end product through the reduction of carbon dioxide or other carbon compounds, typically performed by acetogenic bacteria under anaerobic conditions.",
                            "reasoning":  "Follows genus-differentia form by specifying it as a metabolic process with clear distinguishing characteristics (acetate production, CO2 reduction, anaerobic). Distinguished from other metabolic processes by the specific end product.",
                            "sources":  [
                                            "PMID:21183676",
                                            "PMID:25246403",
                                            "DOI:10.1016/j.tim.2016.02.001"
                                        ],
                            "notes":  "",
                            "class_id":  "METPO:1000845",
                            "parent_class":  "metabolism"
                        },
                        {
                            "confidence":  "high",
                            "class_label":  "acidotolerant",
                            "proposed_definition":  "A pH growth preference in which an organism can tolerate and grow in acidic environments (typically pH below 5.5) but exhibits optimal growth at neutral pH.",
                            "reasoning":  "Distinguishes acidotolerant from acidophilic organisms by emphasizing tolerance of acidic conditions while maintaining neutral pH preference for optimal growth.",
                            "sources":  [
                                            "PMID:19270716",
                                            "PMID:16233609",
                                            "DOI:10.1128/MMBR.00010-08"
                                        ],
                            "notes":  "",
                            "class_id":  "METPO:1003008",
                            "parent_class":  "pH growth preference"
                        },
                        {
                            "confidence":  "high",
                            "class_label":  "pleomorphic shaped",
                            "proposed_definition":  "A cell shape in which an organism exhibits variable morphology, with individual cells displaying multiple different shapes or forms under the same environmental conditions.",
                            "reasoning":  "Clearly defines pleomorphism as a cell shape characteristic distinguished by morphological variability, which sets it apart from organisms with consistent, defined shapes.",
                            "sources":  [
                                            "PMID:23161027",
                                            "ISBN:9781555819675",
                                            "DOI:10.1128/MMBR.00020-13"
                                        ],
                            "notes":  "",
                            "class_id":  "METPO:1000679",
                            "parent_class":  "cell shape"
                        }
    ]
}
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
