# METPO/KG-Microbe Curation Guide

**Detailed step-by-step instructions for ontology curation workflow**

This guide walks you through the complete curation workflow, from getting your assignment to submitting a pull request. Follow these steps carefully, especially if you're new to ontology curation or Git workflows.

---

## Table of Contents

1. [One-Time Setup](#one-time-setup)
2. [Getting Your Assignment](#getting-your-assignment)
3. [Understanding Your Assignment](#understanding-your-assignment)
4. [Creating Definitions with LLMs](#creating-definitions-with-llms)
5. [Finding Definition Sources](#finding-definition-sources)
6. [Validating Your Work](#validating-your-work)
7. [Git Workflow](#git-workflow)
8. [Syncing Your Fork](#syncing-your-fork)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## One-Time Setup

These steps only need to be done once.

### 1. Install Required Tools

```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install just (command runner)
uv tool install just

# Verify installations
uv --version
just --version
git --version  # Should already be installed
```

### 2. Clone or Fork the Repository

**For Interns** (using forks):
```bash
# 1. Fork the repo on GitHub (click "Fork" button)
# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/metpo-kgm-studio.git
cd metpo-kgm-studio

# 3. Add upstream remote
git remote add upstream https://github.com/berkeleybop/metpo-kgm-studio.git
git remote -v  # Verify
```

**For Team Members** (direct access):
```bash
git clone https://github.com/berkeleybop/metpo-kgm-studio.git
cd metpo-kgm-studio
```

### 3. Run Initial Setup

```bash
just setup
```

This will:
- Install Python dependencies
- Create necessary directories
- Verify everything is working

---

## Getting Your Assignment

### 1. Fetch Assignments from Google Sheets

The METPO class definitions are stored in a [Google Sheet](https://docs.google.com/spreadsheets/d/1_Lr-9_5QHi8QLvRyTZFSciUhzGKD4DbUObyTpJ16_RU/edit).

To split this into individual curator assignments:

```bash
just fetch-assignments
```

This will:
- Download the current ROBOT template from Google Sheets
- Split it into 3 overlapping assignments
- Save files as `assignments/curator1.tsv`, `assignments/curator2.tsv`, etc.
- Include 30% overlap for inter-curator agreement assessment

### 2. Check Assignment Statistics

```bash
just assignment-stats
```

Output example:
```
Assignment Statistics:
=====================
curator1.tsv: 45 classes
curator2.tsv: 47 classes
curator3.tsv: 46 classes
```

### 3. Find Your Assignment File

Determine which curator you are (curator1, curator2, or curator3) and open your file:

```bash
cat assignments/curator1.tsv | head -20  # Preview first 20 lines
```

---

## Understanding Your Assignment

### ROBOT Template Format

Your assignment file is a TSV (tab-separated values) file following ROBOT template conventions.

**Structure:**
```
ID              LABEL                       A definition                    A definition source
>ID             RDFS:label                  IAO:0000115                     ...
A               SPLIT=|                     SPLIT=|                         ...
METPO:0000123   methanogenesis             [TO BE FILLED]                  [TO BE FILLED]
METPO:0000124   anaerobic respiration      [TO BE FILLED]                  [TO BE FILLED]
...
```

**Key columns:**
- **Row 1 (header)**: Human-readable column names
- **Row 2 (ROBOT markers)**: Starts with `>`, defines RDF properties
- **Row 3 (ROBOT config)**: Starts with `A`, configuration options
- **Row 4+**: Actual class data

**Your task**: Fill in the `A definition` and `A definition source` columns for each class.

### What Classes Need Curation?

Classes may be:
1. **Missing definitions**: Blank `A definition` column
2. **Missing sources**: Definition exists but no `A definition source`
3. **Poor quality definitions**: Don't follow OBO Foundry principles

Focus on these in order of priority (ask your supervisor for specific priorities).

---

## Creating Definitions with LLMs

### Step 1: Choose a Class to Work On

Pick a class from your assignment file. Example:
- **Class ID**: METPO:0000123
- **Class Label**: methanogenesis
- **Current Definition**: [blank or needs improvement]

### Step 2: Understand the Class

Before using an LLM:
1. **Research the term**: Read about it in Wikipedia, textbooks, or papers
2. **Understand the biology**: What is this process/trait/environment?
3. **Identify parent classes**: Where does this fit in the ontology hierarchy?

**Never blindly trust an LLM without understanding the domain!**

### Step 3: Use the Definition Generation Template

1. Open `prompts/templates/definition-generation.md`
2. Copy the template
3. Fill in the template variables:
   - `{CLASS_ID}`: METPO:0000123
   - `{CLASS_LABEL}`: methanogenesis
   - `{PARENT_CLASSES}`: anaerobic respiration (METPO:0000120)
   - `{EXISTING_DEFINITION}`: [current definition or "None"]

4. Save your customized prompt to `prompts/executed/`:
   ```bash
   # Naming format: YYYY-MM-DD_CLASSID_description.md
   cp prompts/templates/definition-generation.md \
      prompts/executed/2025-10-02_METPO_0000123_definition-generation.md
   # Edit to fill in variables
   ```

### Step 4: Execute the Prompt with Your LLM

Copy your customized prompt and paste it into:
- **Claude** (recommended): https://claude.ai
- **ChatGPT**: https://chat.openai.com
- **CBORG** (if available): Ask your supervisor for access

### Step 5: Save the Raw Output

Copy the LLM's response and save it to `outputs/raw/[your-name]/`:

```bash
# Create JSON file with output
cat > outputs/raw/curator1/2025-10-02_METPO_0000123_output.json << 'EOF'
{
  "class_id": "METPO:0000123",
  "class_label": "methanogenesis",
  "proposed_definition": "An anaerobic respiration process in which methane is produced as the primary metabolic end product, typically using carbon dioxide or acetic acid as terminal electron acceptors.",
  "confidence": "high",
  "reasoning": "...",
  "suggested_sources": ["PMID:15073711", "PMID:23645609"]
}
EOF
```

### Step 6: Review the Output Critically

**Ask yourself:**
1. ✅ Does this definition make biological sense?
2. ✅ Does it follow genus-differentia form ("An [parent] that [characteristics]")?
3. ✅ Is it clear and unambiguous?
4. ✅ Does it avoid circularity?
5. ✅ Are the suggested sources real and relevant?

**If NO to any question**: Revise the prompt or definition!

---

## Finding Definition Sources

Good definitions need authoritative sources. Use the `definition-source-finding.md` template if the LLM didn't suggest good sources.

### Valid Source Types (in order of preference):

1. **PubMed IDs**: `PMID:12345678`
   - Search: https://pubmed.ncbi.nlm.nih.gov/
   - Verify: Open the paper and check it supports your definition

2. **DOIs**: `DOI:10.1234/example`
   - Search: https://doi.org/ or journal websites
   - Verify: Read abstract/methods

3. **ISBNs**: `ISBN:1234567890` (for textbooks)
   - Example: Madigan's *Brock Biology of Microorganisms*

4. **URLs**: `https://example.com` (only for highly authoritative sources)
   - Include access date in notes

### Source Quality Checklist:

✅ **DO USE:**
- Peer-reviewed journal articles
- Review articles (preferred over primary research)
- Standard microbiology textbooks
- Authoritative databases (e.g., KEGG, MetaCyc)

❌ **DON'T USE:**
- Wikipedia
- Non-peer-reviewed sources
- Preprints (unless exceptional)
- Blog posts or forums

### Verifying Sources

**CRITICAL**: Always verify that PMIDs and DOIs exist and support your definition!

```bash
# Example: Verify PMID
open "https://pubmed.ncbi.nlm.nih.gov/15073711"

# Example: Verify DOI
open "https://doi.org/10.1038/nrmicro2386"
```

---

## Validating Your Work

### Automatic Validation

Run validators to check your definitions against OBO Foundry principles:

```bash
# Validate your assignment file
just validate-file assignments/curator1.tsv
```

**Output example:**
```
✓ Definition is present
✓ Definition length appropriate (127 chars)
✗ [WARNING]: Definition may not follow genus-differentia form
✓ No obvious circular definition detected
✓ Class ID format valid: METPO:0000123
✓ 2 valid source(s) found
```

### Common Validation Errors

| Error | Meaning | How to Fix |
|-------|---------|------------|
| "Definition too short" | < 20 characters | Add more detail about distinguishing characteristics |
| "Definition too long" | > 500 characters | Make more concise; split into multiple sentences if needed |
| "Does not follow genus-differentia form" | Missing "An [X] that..." pattern | Rewrite as "An [parent class] that [characteristics]" |
| "Definition may be circular" | Uses term in its own definition | Remove term name from definition text |
| "Invalid source format" | Wrong PMID/DOI format | Check format: `PMID:12345678` or `DOI:10.1234/example` |
| "Label violates FP-012" | Incorrect capitalization | Change to lowercase unless proper noun/acronym |

### Manual Review

Beyond automated checks, ask yourself:
1. Would a microbiologist understand this definition?
2. Is it scientifically accurate?
3. Does it clearly distinguish this class from siblings?
4. Are the sources authoritative and accessible?

---

## Git Workflow

Follow the **issue → branch → commits → PR** workflow.

### 1. Create a Branch

**Naming convention**: `curator[number]-batch[number]` or `curator[number]-CLASSID`

```bash
# Create and switch to new branch
just new-branch curator1 1

# Or manually:
git checkout -b curator1-batch1
```

### 2. Make Your Changes

Edit your assignment file (`assignments/curator1.tsv`) to add:
- Definitions in the `A definition` column
- Sources in the `A definition source` column (use `|` to separate multiple sources)

**Example row after curation:**
```
METPO:0000123   methanogenesis   An anaerobic respiration process in which methane is produced as the primary metabolic end product, typically using carbon dioxide or acetic acid as terminal electron acceptors.   PMID:15073711|PMID:23645609
```

### 3. Validate Before Committing

```bash
just validate-file assignments/curator1.tsv
```

Only commit if validation passes or you understand and accept the warnings!

### 4. Stage Your Changes

```bash
# Add all changes
git add .

# Or selectively:
git add assignments/curator1.tsv
git add prompts/executed/2025-10-02_METPO_0000123_*.md
git add outputs/raw/curator1/
```

### 5. Commit with a Clear Message

**Good commit messages:**
```bash
git commit -m "Add definitions for METPO:0000123-0000130 (methanogenesis pathway)"
git commit -m "Fix definition sources for METPO:0000145"
git commit -m "Improve genus-differentia form for respiratory processes"
```

**Bad commit messages:**
```bash
git commit -m "updates"
git commit -m "stuff"
git commit -m "fixed things"
```

### 6. Push to Remote

```bash
# For forks:
git push origin curator1-batch1

# For direct access:
git push origin curator1-batch1
```

### 7. Create a Pull Request

1. Go to GitHub: https://github.com/berkeleybop/metpo-kgm-studio
2. Click "Pull requests" → "New pull request"
3. Select your branch
4. Write a clear PR description:

```markdown
## Summary
Added definitions for 10 methanogenesis-related classes (METPO:0000123-0000132)

## Changes
- Added genus-differentia definitions following FP-006
- Included PubMed sources for all definitions
- Validated with `just validate-file`

## Notes
- Some warnings about definition length, but necessary for accuracy
- Used Thauer et al. 2008 review as primary source (PMID:15073711)

## Checklist
- [x] Definitions follow genus-differentia form
- [x] All sources verified
- [x] Validation passes
- [x] Prompt templates saved to prompts/executed/
```

5. Request review from Montana, Mark, or supervisor
6. Address any feedback
7. Celebrate when merged! 🎉

---

## Syncing Your Fork

**For interns using forks**: Regularly sync with the main repository to get updates.

```bash
# Fetch upstream changes
git fetch upstream

# Switch to main branch
git checkout main

# Merge upstream changes
git merge upstream/main

# Or use the helper command:
just sync-upstream

# Push to your fork
git push origin main
```

**When to sync:**
- Before starting new work
- When main repository has updates
- Weekly (to avoid large divergence)

---

## Troubleshooting

### "Permission denied" when pushing

**Problem**: You don't have write access to the repository.

**Solution (for interns)**:
1. Make sure you forked the repository
2. Check your remote URLs: `git remote -v`
3. `origin` should point to YOUR fork, not the main repo
4. If wrong: `git remote set-url origin https://github.com/YOUR-USERNAME/metpo-kgm-studio.git`

### "Validation failed" on commit

**Problem**: Pre-commit hooks failed.

**Solution**:
1. Read the error messages carefully
2. Fix the issues (usually formatting, spelling, or linting)
3. Run `just format` to auto-fix some issues
4. Try committing again

### "Merge conflict" when syncing

**Problem**: Your changes conflict with upstream changes.

**Solution**:
1. Don't panic! This is normal.
2. Git will mark conflicts in files with `<<<<<<<`, `=======`, `>>>>>>>`
3. Edit files to resolve conflicts
4. `git add` the resolved files
5. `git commit` to complete the merge
6. Ask for help if stuck!

### "ModuleNotFoundError" when running commands

**Problem**: Dependencies not installed.

**Solution**:
```bash
just install
# Or:
uv sync --group dev
```

### LLM generated hallucinated sources

**Problem**: PMID or DOI doesn't exist or doesn't support the definition.

**Solution**:
1. Search PubMed/DOI yourself for the topic
2. Find real sources that support the definition
3. Update the LLM prompt to be more specific about verifiable sources
4. **Never use fake sources**

---

## Best Practices

### Scientific Accuracy
- ✅ Understand the biology before using LLMs
- ✅ Verify all facts against authoritative sources
- ✅ Ask domain experts (Montana, Mark, Chris) if unsure
- ✅ Prefer review articles over primary research for sources

### LLM Usage
- ✅ Start with approved prompt templates
- ✅ Save all prompts and outputs to git
- ✅ Critically review all LLM outputs
- ✅ Iterate on prompts if quality is poor
- ❌ Never trust LLM outputs blindly
- ❌ Never use LLM-suggested sources without verifying they exist

### Git Hygiene
- ✅ Commit often with clear messages
- ✅ One logical change per commit
- ✅ Validate before committing
- ✅ Keep branches focused and short-lived
- ✅ Sync regularly with upstream
- ❌ Don't commit broken code
- ❌ Don't commit huge batches without validation

### Collaboration
- ✅ Ask questions early and often
- ✅ Review others' PRs when asked
- ✅ Give constructive feedback
- ✅ Document your decisions (commit messages, PR descriptions)
- ✅ Communicate blockers or challenges
- ❌ Don't struggle silently
- ❌ Don't submit PRs without review

### Time Management
- ✅ Start with easier classes to build confidence
- ✅ Break work into small batches (5-10 classes)
- ✅ Take breaks between batches
- ✅ Track your progress: `just progress curator1`
- ✅ Set realistic goals (quality over quantity)

---

## Getting Help

**Stuck? Confused? Not sure if something is right?**

### Ask for Help!

- **Ontology/Biology Questions**: Montana or Mark
- **Python/Technical Questions**: Sujay
- **LLM/Prompting Questions**: Chris
- **Git/GitHub Questions**: Anyone on the team
- **General Workflow**: This guide or README.md

**How to ask for help:**
1. Describe what you're trying to do
2. Describe what's happening (include error messages)
3. Show what you've tried
4. Ask a specific question

**Good example:**
> "I'm trying to create a definition for METPO:0000145 (sulfate reduction). The LLM suggested 'A process that reduces sulfate' but validation says it doesn't follow genus-differentia form. Should I include the parent class 'anaerobic respiration' in the definition?"

**Less helpful:**
> "The validator doesn't like my definition. Help?"

---

## Additional Resources

- **OBO Foundry Principles**:
  - [FP-006: Textual Definitions](https://obofoundry.org/principles/fp-006-textual-definitions.html)
  - [FP-012: Naming Conventions](https://obofoundry.org/principles/fp-012-naming-conventions.html)

- **Chris Mungall's Best Practices**: https://berkeleybop.org/best_practice/

- **ROBOT Documentation**: http://robot.obolibrary.org/

- **Git Tutorials**:
  - [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
  - [GitHub Flow](https://guides.github.com/introduction/flow/)

- **Python Type Hints**: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html

---

**Questions? Suggestions for improving this guide?**

Open an issue or ask in your next team meeting!

---

**Last Updated**: 2025-10-02
