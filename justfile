# METPO/KG-Microbe Curation Workflow Justfile
# Collaborative workspace for curating METPO terms and experimenting with KG-Microbe ingest with METPO normalization of source data

# ============ Variables ============

# Python executable
shebang := if os() == 'windows' {
  'py'
} else {
  '/usr/bin/env python3'
}

# Google Sheets configuration
SHEET_ID := "1_Lr-9_5QHi8QLvRyTZFSciUhzGKD4DbUObyTpJ16_RU"
SHEET_GID := "355012485"
NUM_CURATORS := "6"
OVERLAP_PCT := "20"

# Directories
ASSIGNMENTS_DIR := "assignments"
OUTPUTS_DIR := "outputs"
PROMPTS_DIR := "prompts"

# ============ Default Command ============

# List all available commands
_default:
    @just --list

# ============ Setup Commands ============

# Initial setup: install dependencies and prepare workspace
[group('setup')]
setup: install create-dirs
    @echo "✓ Setup complete! Ready to start curating."
    @echo ""
    @echo "Next steps:"
    @echo "  1. Run 'just fetch-assignments' to download and split the Google Sheet"
    @echo "  2. Read CURATION_GUIDE.md for workflow instructions"
    @echo "  3. Start curating your assigned classes!"

# Install Python dependencies
[group('setup')]
install:
    uv sync --group dev

# Create necessary directories
[group('setup')]
create-dirs:
    mkdir -p {{ASSIGNMENTS_DIR}}
    mkdir -p {{OUTPUTS_DIR}}/raw/curator1
    mkdir -p {{OUTPUTS_DIR}}/raw/curator2
    mkdir -p {{OUTPUTS_DIR}}/raw/curator3
    mkdir -p {{OUTPUTS_DIR}}/reviewed/curator1
    mkdir -p {{OUTPUTS_DIR}}/reviewed/curator2
    mkdir -p {{OUTPUTS_DIR}}/reviewed/curator3
    mkdir -p {{PROMPTS_DIR}}/executed

# ============ Assignment Management ============

# Fetch Google Sheet and split into curator assignments
[group('assignments')]
fetch-assignments:
    @echo "Fetching ROBOT template from Google Sheets..."
    @echo "Sheet ID: {{SHEET_ID}}"
    @echo "GID: {{SHEET_GID}}"
    @echo "Curators: {{NUM_CURATORS}}, Overlap: {{OVERLAP_PCT}}%"
    uv run python -m metpo_kgm_studio.splitter {{SHEET_ID}} {{SHEET_GID}} {{ASSIGNMENTS_DIR}} {{NUM_CURATORS}} {{OVERLAP_PCT}}
    @echo ""
    @echo "✓ Assignments created in {{ASSIGNMENTS_DIR}}/"
    @echo "  Each curator has overlapping terms for inter-curator agreement"

# Show assignment statistics
[group('assignments')]
assignment-stats:
    #!/usr/bin/env bash
    echo "Assignment Statistics:"
    echo "====================="
    for file in {{ASSIGNMENTS_DIR}}/*.tsv; do
        if [ -f "$file" ]; then
            # Count non-header rows
            count=$(tail -n +4 "$file" | wc -l | tr -d ' ')
            echo "$(basename $file): $count classes"
        fi
    done

# ============ Validation Commands ============

# Validate all definitions in assignments
[group('validation')]
validate-all:
    @echo "Validating all assignment files..."
    @for file in {{ASSIGNMENTS_DIR}}/*.tsv; do \
        if [ -f "$$file" ]; then \
            echo ""; \
            echo "Validating $$file..."; \
            just validate-file "$$file"; \
        fi; \
    done

# Validate a specific TSV file
[group('validation')]
validate-file FILE:
    uv run python -c "from metpo_kgm_studio.validators import validate_definition_file; import sys; results = validate_definition_file('{{FILE}}'); print(f\"Errors: {results['errors']}, Warnings: {results['warnings']}\"); sys.exit(1 if results['errors'] > 0 else 0)"

# Validate definitions in reviewed outputs
[group('validation')]
validate-reviewed:
    @echo "Validating reviewed outputs..."
    @for file in {{OUTPUTS_DIR}}/reviewed/*/*.tsv; do \
        if [ -f "$$file" ]; then \
            echo ""; \
            echo "Validating $$file..."; \
            just validate-file "$$file"; \
        fi; \
    done

# ============ Testing Commands ============

# Run all tests
[group('testing')]
test: pytest type-check lint

# Run pytest unit tests
[group('testing')]
pytest:
    uv run pytest tests/ -v

# Run type checking with mypy
[group('testing')]
type-check:
    uv run mypy src/metpo_kgm_studio

# Run linting with ruff
[group('testing')]
lint:
    uv run ruff check src/ tests/

# Format code with ruff
[group('testing')]
format:
    uv run ruff format src/ tests/

# Check code formatting without making changes
[group('testing')]
format-check:
    uv run ruff format --check src/ tests/

# ============ Quality Checks ============

# Run all pre-commit hooks
[group('quality')]
pre-commit-all:
    uv run pre-commit run --all-files

# Check spelling with codespell
[group('quality')]
spell-check:
    uv run codespell .

# ============ Workflow Helper Commands ============

# Show curation workflow summary
[group('workflow')]
workflow-help:
    @echo "METPO Curation Workflow"
    @echo "======================="
    @echo ""
    @echo "1. GET YOUR ASSIGNMENT"
    @echo "   just fetch-assignments"
    @echo "   → Creates curator1.tsv, curator2.tsv, etc. in assignments/"
    @echo ""
    @echo "2. CREATE A BRANCH"
    @echo "   git checkout -b curator1-batch1"
    @echo ""
    @echo "3. WORK ON DEFINITIONS"
    @echo "   - Use prompts/templates/ for LLM prompts"
    @echo "   - Save executed prompts to prompts/executed/"
    @echo "   - Save raw LLM outputs to outputs/raw/your-name/"
    @echo ""
    @echo "4. VALIDATE YOUR WORK"
    @echo "   just validate-file assignments/curator1.tsv"
    @echo ""
    @echo "5. COMMIT YOUR CHANGES"
    @echo "   git add ."
    @echo "   git commit -m 'Add definitions for METPO:XXX-YYY'"
    @echo ""
    @echo "6. CREATE PULL REQUEST"
    @echo "   git push origin curator1-batch1"
    @echo "   → Create PR on GitHub"
    @echo ""
    @echo "For detailed instructions, see CURATION_GUIDE.md"

# Create a new branch for curation work
[group('workflow')]
new-branch CURATOR BATCH:
    git checkout -b {{CURATOR}}-batch-{{BATCH}}
    @echo "✓ Created branch: {{CURATOR}}-batch-{{BATCH}}"
    @echo "Start working on your assignments!"

# Quick commit with standardized message
[group('workflow')]
quick-commit CLASS_RANGE MESSAGE:
    git add .
    git commit -m "{{MESSAGE}} ({{CLASS_RANGE}})"
    @echo "✓ Committed: {{MESSAGE}}"

# ============ Reporting ============

# Show progress statistics for a curator
[group('reporting')]
progress CURATOR:
    @echo "Progress Report for {{CURATOR}}"
    @echo "==============================="
    @echo ""
    @echo "Assignment:"
    @if [ -f "{{ASSIGNMENTS_DIR}}/{{CURATOR}}.tsv" ]; then \
        total=$(tail -n +4 "{{ASSIGNMENTS_DIR}}/{{CURATOR}}.tsv" | wc -l | tr -d ' '); \
        echo "  Total classes: $$total"; \
    fi
    @echo ""
    @echo "Raw outputs:"
    @if [ -d "{{OUTPUTS_DIR}}/raw/{{CURATOR}}" ]; then \
        count=$(ls -1 "{{OUTPUTS_DIR}}/raw/{{CURATOR}}" 2>/dev/null | wc -l | tr -d ' '); \
        echo "  Files: $$count"; \
    fi
    @echo ""
    @echo "Reviewed outputs:"
    @if [ -d "{{OUTPUTS_DIR}}/reviewed/{{CURATOR}}" ]; then \
        count=$(ls -1 "{{OUTPUTS_DIR}}/reviewed/{{CURATOR}}" 2>/dev/null | wc -l | tr -d ' '); \
        echo "  Files: $$count"; \
    fi

# ============ Maintenance ============

# Update copier template
[group('maintenance')]
update-template:
    copier update --trust --skip-answered

# Clean generated files (WARNING: destructive!)
[group('maintenance')]
clean:
    rm -rf {{ASSIGNMENTS_DIR}}/*.tsv
    rm -rf {{OUTPUTS_DIR}}/raw/*
    rm -rf {{OUTPUTS_DIR}}/reviewed/*
    @echo "⚠️  Cleaned all assignments and outputs"

# ============ Documentation ============

# Serve documentation locally
[group('docs')]
serve-docs:
    @echo "Documentation files:"
    @echo "  README.md - Project overview"
    @echo "  CURATION_GUIDE.md - Detailed workflow guide"
    @echo "  prompts/templates/README.md - LLM prompt guide"

# ============ Git Helpers ============

# Show git status with helpful reminders
[group('git')]
status:
    @git status
    @echo ""
    @echo "Reminder: Follow the issue → branch → commits → PR workflow"

# Sync from upstream (for forks)
[group('git')]
sync-upstream:
    git fetch upstream
    git merge upstream/main
    @echo "✓ Synced with upstream"

# ============ Hidden Internal Commands ============

# Initialize git if not already initialized
_git-init:
    @if [ ! -d .git ]; then git init; fi

# Check if required tools are installed
_check-deps:
    @command -v uv >/dev/null 2>&1 || { echo "Error: uv is not installed"; exit 1; }
    @command -v git >/dev/null 2>&1 || { echo "Error: git is not installed"; exit 1; }
