# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **metpo-kgm-studio**: a collaborative workspace for curating METPO (Microbial Environment and Traits Ontology) terms following OBO Foundry principles. The project uses LLMs with structured prompts to assist in creating ontology definitions, with mandatory human review.

**Key Technologies:**
- Python 3.10+ with `uv` package manager
- `just` command runner for workflow automation
- ROBOT template format (TSV) for ontology curation
- Git-based collaborative workflow with overlapping assignments for inter-curator agreement

## Essential Commands

### Setup and Dependencies
```bash
just setup                    # Initial setup: install deps + create directories
just install                  # Install Python dependencies only (uv sync --group dev)
```

### Assignment Management
```bash
just fetch-assignments        # Download Google Sheet and split into curator assignments
just assignment-stats         # Show class count per curator
```

### Validation
```bash
just validate-file FILE       # Validate specific TSV file against OBO principles
just validate-all            # Validate all assignment files
just validate-reviewed       # Validate reviewed outputs
```

### Testing and Quality
```bash
just test                    # Run pytest + mypy + ruff (full test suite)
just pytest                  # Run pytest unit tests only
just type-check              # Run mypy type checking
just lint                    # Run ruff linting
just format                  # Auto-format code with ruff
just spell-check             # Check spelling with codespell
just pre-commit-all          # Run all pre-commit hooks
```

### Git Workflow Helpers
```bash
just new-branch CURATOR BATCH  # Create branch: curator[N]-batch-[N]
just progress curator1         # Show progress statistics for a curator
just status                    # Git status with workflow reminders
```

## Architecture

### ROBOT Template Format

The project uses ROBOT template TSV files with a specific structure:
- **Row 1**: Human-readable column headers (ID, LABEL, A definition, A definition source)
- **Row 2**: ROBOT markers starting with `>` defining RDF properties (>ID, RDFS:label, IAO:0000115)
- **Row 3**: ROBOT configuration starting with `A` (e.g., SPLIT=|)
- **Row 4+**: Actual ontology class data

**Critical**: The splitter (src/metpo_kgm_studio/splitter.py) and validators must preserve these first 3 rows exactly when processing files.

### Assignment Splitting Strategy

The `splitter.py` module fetches a master ROBOT template from Google Sheets and splits it into overlapping curator assignments:
- Configurable number of curators (default: 6)
- Configurable overlap percentage (default: 20%) for inter-curator agreement assessment
- Random shuffling to distribute classes fairly
- Preserves ROBOT header rows in each output file

**Flow**: Google Sheet → fetch as TSV → parse header vs data rows → create overlapping subsets → write curator[N].tsv files

### Validation System

The `validators.py` module implements OBO Foundry principle checks:

**FP-006 (Textual Definitions):**
- Genus-differentia form: "An [parent class] that [distinguishing characteristics]"
- Length bounds: 20-500 characters
- Circularity detection: term shouldn't appear in its own definition
- Source requirements: PMID:, DOI:, ISBN:, or URL format

**FP-012 (Naming Conventions):**
- Lowercase labels except for proper nouns and acronyms
- Warns about capitalization violations

**ValidationResult dataclass** categorizes issues by severity: error, warning, info

### LLM-Assisted Curation Workflow

The project embraces LLM usage but with strict guardrails:

1. **Approved Templates** (`prompts/templates/`): Pre-defined prompts for definition generation and source finding
2. **Execution Tracking** (`prompts/executed/`): All customized prompts saved with naming: `YYYY-MM-DD_CLASSID_description.md`
3. **Raw Outputs** (`outputs/raw/curator[N]/`): Unedited LLM responses saved as JSON
4. **Reviewed Outputs** (`outputs/reviewed/curator[N]/`): Human-verified and refined definitions

**Critical Philosophy**: LLMs are assistants, not authorities. All outputs require critical human review for scientific accuracy and source verification.

## Key Files and Locations

- `justfile`: All workflow commands and configuration (Google Sheet ID, GID, overlap settings)
- `src/metpo_kgm_studio/splitter.py`: Google Sheets fetching and assignment splitting logic
- `src/metpo_kgm_studio/validators.py`: OBO Foundry principle validators
- `assignments/`: Curator-specific TSV files (curator1.tsv, curator2.tsv, etc.)
- `prompts/templates/`: Approved LLM prompt templates
- `prompts/executed/`: Record of actual prompts used (for reproducibility)
- `outputs/raw/`: Unreviewed LLM outputs
- `outputs/reviewed/`: Human-reviewed and approved definitions
- `pyproject.toml`: Python dependencies, tool configuration (pytest, mypy, ruff, codespell)

## Development Guidelines

### When Modifying Validators

The validation system is central to quality control:
- Add new checks as methods on `DefinitionValidator` or `LabelValidator` classes
- Return `ValidationResult` objects with clear messages
- Set appropriate severity: "error" (blocks), "warning" (advisories), "info" (informational)
- Test thoroughly - false positives frustrate curators

### When Modifying Splitter

The splitter must preserve ROBOT template integrity:
- Always preserve the first 3 header rows verbatim
- The `is_header_row()` method detects ROBOT markers (>, A, SPLIT=|, etc.)
- Overlap logic is in `create_overlapping_subsets()` - changes affect inter-curator agreement
- Changes to Google Sheet URL/GID should update justfile variables

### When Adding New Commands

Add commands to the `justfile` organized by groups:
- `[group('setup')]`: Initial setup commands
- `[group('assignments')]`: Assignment management
- `[group('validation')]`: Validation commands
- `[group('testing')]`: Test and quality commands
- `[group('workflow')]`: Workflow helpers
- `[group('git')]`: Git operations

### Type Checking and Linting

The project enforces strict type checking:
- All functions must have type hints (`disallow_untyped_defs = true`)
- Return types are required
- Tests are exempt from strict typing
- Run `just type-check` before committing

Code style is enforced by ruff:
- Line length: 100 characters
- Python 3.10 target
- Selected rules: pycodestyle, pyflakes, isort, flake8-bugbear, pyupgrade
- Run `just format` to auto-fix most issues

## Curation-Specific Context

### Definition Quality Expectations

Good definitions must:
1. Follow genus-differentia form exactly
2. Be scientifically accurate (verified against literature)
3. Have at least one authoritative source (prefer PMIDs over URLs)
4. Avoid circularity and vagueness
5. Be clear to domain experts (microbiologists)

### Source Verification is Critical

LLMs frequently hallucinate PMIDs and DOIs. Always verify:
```bash
# Example checks:
open "https://pubmed.ncbi.nlm.nih.gov/15073711"
open "https://doi.org/10.1038/nrmicro2386"
```

### Git Workflow Pattern

The project follows **issue → branch → commits → PR**:
1. Create branch: `curator[N]-batch-[N]`
2. Make changes to assignment TSV files
3. Validate: `just validate-file assignments/curator1.tsv`
4. Commit with clear messages: "Add definitions for METPO:XXXXX-YYYYY"
5. Push and create PR
6. Address review feedback

## Testing

Run the full test suite before submitting changes:
```bash
just test  # Runs: pytest + mypy + ruff
```

Test files are in `tests/` with naming convention `test_*.py`. The project uses pytest markers:
- `@pytest.mark.slow`: Long-running tests
- `@pytest.mark.integration`: Integration tests

## Common Pitfalls

1. **Don't skip validation**: Running `just validate-file` before committing prevents broken definitions from entering the codebase
2. **Don't modify ROBOT headers**: The first 3 rows of TSV files are sacred - they define the template structure
3. **Don't trust LLM sources blindly**: Verify every PMID and DOI actually exists and supports the definition
4. **Don't commit without type checking**: Run `just type-check` - the CI will fail otherwise
5. **Remember overlap**: Some classes appear in multiple curator assignments by design (for agreement assessment)

## Support and Questions

- **Ontology/Biology**: Ask Montana or Mark
- **Python/Technical**: Ask Sujay
- **LLM/Prompting**: Ask Chris
- **Detailed Workflow**: See CURATION_GUIDE.md (comprehensive step-by-step guide)
