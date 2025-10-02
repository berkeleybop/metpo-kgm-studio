# LLM Prompt Templates

This directory contains approved prompt templates for using LLMs in METPO/KG-Microbe curation.

## Available Templates

### 1. `definition-generation.md`
Generate textual definitions for ontology classes following OBO Foundry principles (FP-006).

**When to use:**
- Creating new definitions for classes that lack them
- Improving existing definitions that don't follow best practices
- Getting initial draft definitions that you will then refine

**Remember:** Always review and verify LLM-generated definitions for scientific accuracy.

### 2. `definition-source-finding.md`
Find authoritative literature sources (PMIDs, DOIs) to support definitions.

**When to use:**
- After creating or improving a definition
- When existing definitions lack proper citations
- To find additional supporting evidence

**Remember:** Verify that sources actually support the definition and are accessible.

## Usage Workflow

1. **Select Template**: Choose the appropriate template for your task

2. **Customize**: Fill in the template variables:
   - `{CLASS_ID}`: e.g., METPO:1234567
   - `{CLASS_LABEL}`: e.g., "methanogenesis"
   - `{PARENT_CLASSES}`: Parent class information
   - `{EXISTING_DEFINITION}`: Current definition if any
   - `{DEFINITION}`: For source-finding template

3. **Save Your Prompt**: Copy the customized prompt to `prompts/executed/` with naming format:
   ```
   YYYY-MM-DD_CLASSID_task-description.md
   ```
   Example: `2025-10-02_METPO_0000123_definition-generation.md`

4. **Execute**: Send the prompt to your LLM of choice (Claude, ChatGPT, etc.)

5. **Save Output**: Save the raw LLM response to `outputs/raw/[your-name]/` as JSON:
   ```
   YYYY-MM-DD_CLASSID_output.json
   ```

6. **Review and Refine**: Critically review the output:
   - Check scientific accuracy
   - Verify sources exist and support the definition
   - Ensure OBO Foundry principles are followed
   - Refine as needed

7. **Record Reviewed Version**: Save your final, reviewed version to `outputs/reviewed/[your-name]/`:
   ```
   CLASSID_reviewed.tsv
   ```

8. **Commit**: Commit both the executed prompt and outputs to git with a descriptive message

## Best Practices

### DO:
✅ Start with these approved templates
✅ Save all prompts and outputs to git for reproducibility
✅ Review LLM outputs critically - they can hallucinate!
✅ Verify all sources (PMIDs, DOIs) are real and relevant
✅ Iterate on prompts if outputs are poor quality
✅ Ask for help if you're unsure about a definition

### DON'T:
❌ Use ad-hoc prompts without documenting them
❌ Trust LLM outputs without verification
❌ Skip saving intermediate steps
❌ Generate definitions without understanding the underlying biology
❌ Copy definitions from other ontologies without attribution

## Improving Templates

If you find these templates produce poor results or you develop better prompts:

1. Create a new version of the template (e.g., `definition-generation-v2.md`)
2. Document what changed and why
3. Discuss with the team before making it the default
4. Update this README to reflect changes

## Questions?

- See `CURATION_GUIDE.md` for detailed workflow documentation
- Ask Sujay for Python/technical questions
- Ask Montana/Mark for ontology principles questions
- Ask Chris for LLM best practices and advanced prompting
