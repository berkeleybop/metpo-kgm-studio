# metpo-kgm-studio

Collaborative workspace for curating METPO terms and experimenting with KG-Microbe ingest with METPO normalization of source data

This workspace provides a structured environment for curating definitions and metadata for the METPO (Microbial Environment and Traits Ontology) and KG-Microbe knowledge graph, following OBO Foundry principles and best practices.

## Quick Start

### Prerequisites

Install these tools once (one-time setup):

1. **Python >= 3.10**: Required for all Python tooling
2. **uv**: Python package manager ([installation instructions](https://docs.astral.sh/uv/getting-started/installation/))
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **just**: Command runner ([installation instructions](https://github.com/casey/just))
   ```bash
   uv tool install rust-just
   ```
4. **Git**: Version control (should already be installed)

### Initial Setup

1. Clone this repository (or your fork):
   ```bash
   git clone https://github.com/berkeleybop/metpo-kgm-studio.git
   cd metpo-kgm-studio
   ```

2. Run setup:
   ```bash
   just setup
   ```

3. Fetch your assignments from Google Sheets:
   ```bash
   just fetch-assignments
   ```

4. Read the workflow guide:
   ```bash
   cat CURATION_GUIDE.md
   ```

## Project Structure

```
metpo-kgm-studio/
├── assignments/               # Curator-specific class assignments
│   ├── curator1.tsv          # Classes assigned to curator 1
│   ├── curator2.tsv          # Classes assigned to curator 2
│   └── curator3.tsv          # Classes assigned to curator 3
├── prompts/
│   ├── templates/            # Approved LLM prompt templates
│   │   ├── definition-generation.md
│   │   └── definition-source-finding.md
│   └── executed/             # Record of prompts actually executed
│       └── YYYY-MM-DD_CLASSID_description.md
├── outputs/
│   ├── raw/                  # Raw LLM outputs (before review)
│   │   └── curator1/
│   └── reviewed/             # Reviewed and approved outputs
│       └── curator1/
├── src/metpo_kgm_studio/   # Python curation tools
│   ├── splitter.py           # Google Sheets assignment splitter
│   └── validators.py         # Definition quality validators
├── tests/                    # Unit tests
├── justfile                  # Workflow commands (run `just` to see all)
├── README.md                 # This file
└── CURATION_GUIDE.md        # Detailed workflow documentation
```

## Common Commands

Run `just` to see all available commands. Here are the most important ones:

### Setup & Assignments
```bash
just setup                    # Install dependencies and create directories
just fetch-assignments        # Download and split Google Sheet into assignments
just assignment-stats         # Show how many classes per curator
```

### Validation
```bash
just validate-all            # Validate all assignment files
just validate-file FILE      # Validate a specific TSV file
just validate-reviewed       # Validate reviewed outputs
```

### Testing & Quality
```bash
just test                    # Run all tests (pytest, mypy, ruff)
just lint                    # Check code style
just format                  # Auto-format code
just spell-check             # Check spelling
```

### Workflow Helpers
```bash
just workflow-help           # Show workflow summary
just new-branch NAME BATCH   # Create a new branch for curation work
just progress curator1       # Show progress for a curator
```

### Git Operations
```bash
just status                  # Git status with helpful reminders
just sync-upstream           # Sync fork with upstream (for forks)
```

## Curation Workflow

The recommended workflow follows GitHub's **issue → branch → commits → PR** pattern:

1. **Get Assignment**: `just fetch-assignments`
2. **Create Branch**: `just new-branch curator1 1` or `git checkout -b curator1-batch1`
3. **Curate Definitions**:
   - Use prompts from `prompts/templates/`
   - Save executed prompts to `prompts/executed/`
   - Save LLM outputs to `outputs/raw/your-name/`
4. **Validate**: `just validate-file assignments/curator1.tsv`
5. **Commit**: `git add . && git commit -m "Add definitions for METPO:XXX-YYY"`
6. **Push & PR**: `git push origin curator1-batch1` → Create pull request on GitHub

See `CURATION_GUIDE.md` for detailed step-by-step instructions.

## OBO Foundry Principles

This project follows OBO Foundry principles, especially:

### FP-006: Textual Definitions
- **Genus-Differentia Form**: "An [parent class] that [distinguishing characteristics]"
- **Clear & Unambiguous**: Intelligible to domain experts
- **Avoid Circularity**: Don't use term in its own definition
- **Sources Required**: At least one PMID, DOI, ISBN, or authoritative URL

### FP-012: Naming Conventions
- **Lowercase Labels**: Except for proper nouns and acronyms
- **No Capitalization**: Avoid capitalizing common words
- **Consistent Style**: Follow established patterns in the ontology

Validators automatically check these principles. See `src/metpo_kgm_studio/validators.py`.

## Using LLMs Safely

This project **encourages** LLM use but with **guardrails**:

### ✅ DO:
- Start with approved prompt templates in `prompts/templates/`
- Save all prompts and outputs to git for reproducibility
- **Critically review** all LLM outputs (they can hallucinate!)
- Verify all sources (PMIDs, DOIs) actually exist and support the definition
- Iterate on prompts if quality is poor

### ❌ DON'T:
- Trust LLM outputs blindly
- Use ad-hoc prompts without documenting them
- Skip the review step
- Generate definitions without understanding the biology
- Ignore validation errors

### Recommended LLMs:
- **Claude** (3.5 Sonnet or Opus): Excellent for scientific text
- **ChatGPT** (GPT-4): Good general performance
- **CBORG**: Specialized for biomedical text (if available)

See Chris Mungall's [best practices](https://berkeleybop.org/best_practice/) for more guidance.

## For Interns: Your First Steps

1. **Read This File**: You're doing it! ✓
2. **Read CURATION_GUIDE.md**: Detailed workflow walkthrough
3. **Run Setup**: `just setup`
4. **Get Your Assignment**: `just fetch-assignments`
5. **Find Your File**: `assignments/curator1.tsv` (or curator2, curator3)
6. **Read Prompt Templates**: `prompts/templates/README.md`
7. **Try One Class**: Start small - curate definition for one class
8. **Validate**: `just validate-file assignments/curator1.tsv`
9. **Ask Questions**: Don't hesitate to ask Montana, Mark, Sujay, or Chris!

### Learning Goals

Through this project, you will learn:
- ✅ **Ontology curation**: Following OBO Foundry principles
- ✅ **Git workflow**: Branch, commit, pull request
- ✅ **Python development**: Type hints, testing, linting
- ✅ **LLM best practices**: Prompt engineering, critical evaluation
- ✅ **Scientific literature**: Finding and citing authoritative sources
- ✅ **Collaborative coding**: Code review, issue tracking

These are all **highly marketable skills** for bioinformatics and data science careers!

## Getting Help

- **Ontology Questions**: Ask Montana or Mark
- **Python/Technical Questions**: Ask Sujay
- **LLM/Prompting Questions**: Ask Chris
- **General Questions**: Ask anyone on the team!

## Contributing

See `CURATION_GUIDE.md` for the detailed workflow. In summary:

1. Fork this repo (for interns) or clone directly (for team members)
2. Create a branch for your work
3. Make changes following OBO Foundry principles
4. Validate your work: `just validate-all`
5. Commit with clear messages
6. Push and create a pull request
7. Address review feedback
8. Celebrate when merged! 🎉

## License

BSD-3-Clause

## Acknowledgments

This project was created from the [metpo-kgm-copier](https://github.com/berkeleybop/metpo-kgm-copier) template, based on [monarch-project-copier](https://github.com/monarch-initiative/monarch-project-copier).

Developed as part of the METPO/KG-Microbe project at Lawrence Berkeley National Laboratory.

---

**Generated**: 2025-10-02
