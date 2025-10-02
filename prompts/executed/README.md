# Executed Prompts

This directory stores the actual prompts that were sent to LLMs during curation.

## Purpose

Tracking executed prompts allows us to:
- **Reproduce results**: Re-run the same prompt if needed
- **Improve prompts**: Learn what works and what doesn't
- **Share knowledge**: Help others learn effective prompting
- **Audit trail**: Understand how definitions were generated

## Naming Convention

```
YYYY-MM-DD_CLASSID_description.md
```

Examples:
- `2025-10-02_METPO_0000123_definition-generation.md`
- `2025-10-02_METPO_0000123_source-finding.md`
- `2025-10-02_METPO_0000124_definition-revision-v2.md`

## Content

Each file should contain:
1. The complete prompt sent to the LLM
2. Which LLM was used (Claude, ChatGPT, etc.)
3. Date/time of execution
4. Link to the raw output file

Example:

```markdown
# Definition Generation for METPO:0000123

**Date**: 2025-10-02 14:30 UTC
**LLM**: Claude 3.5 Sonnet
**Output**: outputs/raw/curator1/2025-10-02_METPO_0000123_output.json

## Prompt

[Full prompt text here...]

## Notes

- First attempt produced a circular definition
- This is the revised version with better parent class specification
```

## Workflow

1. Start with a template from `prompts/templates/`
2. Customize with your class-specific information
3. **Save the customized prompt here BEFORE executing**
4. Execute the prompt with your LLM
5. Save output to `outputs/raw/`
6. Update this file with any notes about the results

## Tips

- **Save before executing**: Don't forget to save the prompt before sending to LLM
- **Include context**: Note any special considerations or challenges
- **Version iterations**: If you revise a prompt, create a new file with v2, v3, etc.
- **Share successes**: If a prompt works really well, tell the team!
