# Definition Generation Prompt Template

**Version:** 1.0
**Purpose:** Generate textual definitions for METPO ontology classes following OBO Foundry principles
**Last Updated:** {% now 'utc', '%Y-%m-%d' %}

---

## Instructions for LLM

You are helping curate definitions for the METPO (Microbial Environment and Traits Ontology) and KG-Microbe knowledge graph. Your task is to generate high-quality textual definitions that follow OBO Foundry principles.

### Requirements (OBO Foundry FP-006)

1. **Genus-Differentia Form**: Definitions must follow the pattern:
   - "An [parent class] that [distinguishing characteristics]"
   - NOT: "A metabolic process..." (avoid starting with article + class name)

2. **Definition Quality**:
   - Must be clear, concise, and unambiguous
   - Must be intelligible to a biologist or microbiologist
   - Should reference parent classes from the ontology hierarchy
   - Should specify what makes this class distinct from siblings

3. **Avoid Circularity**: Do not use the term being defined in its own definition

4. **Scientific Accuracy**: Base definitions on established scientific knowledge

### Input Format

For each term, you will receive:
- **Class ID**: e.g., METPO:1234567
- **Class Label**: e.g., "anaerobic respiration"
- **Parent Class(es)**: e.g., "cellular respiration" (METPO:1234560)
- **Existing Definition** (if any): Current definition that may need improvement

### Output Format

Provide your response as JSON:

```json
{
  "class_id": "METPO:1234567",
  "class_label": "anaerobic respiration",
  "proposed_definition": "A cellular respiration process that occurs in the absence of oxygen, using alternative electron acceptors such as nitrate, sulfate, or carbon dioxide.",
  "confidence": "high|medium|low",
  "reasoning": "Brief explanation of why this definition is appropriate",
  "suggested_sources": [
    "PMID:12345678",
    "DOI:10.1234/example",
    "ISBN:1234567890"
  ]
}
```

### Example

**Input:**
- Class ID: METPO:0000123
- Class Label: methanogenesis
- Parent Class: anaerobic respiration (METPO:0000120)
- Existing Definition: None

**Expected Output:**
```json
{
  "class_id": "METPO:0000123",
  "class_label": "methanogenesis",
  "proposed_definition": "An anaerobic respiration process in which methane is produced as the primary metabolic end product, typically using carbon dioxide or acetic acid as terminal electron acceptors.",
  "confidence": "high",
  "reasoning": "Definition follows genus-differentia form, clearly distinguishes methanogenesis from other anaerobic respiration types by specifying methane production and typical electron acceptors.",
  "suggested_sources": [
    "PMID:15073711",
    "PMID:23645609"
  ]
}
```

---

## Usage Notes for Curators

1. **Save Prompts**: When you execute this prompt, copy it to `prompts/executed/` with a timestamp
2. **Record Output**: Save the LLM output to `outputs/raw/[your-name]/` as JSON
3. **Review Carefully**: The LLM can make mistakes - always verify scientific accuracy
4. **Check Sources**: Verify that suggested sources actually support the definition
5. **Iterate**: If the output is poor, revise this template and try again

## Template Variables

Replace these before sending to LLM:

- `{CLASS_ID}`: The ontology class ID
- `{CLASS_LABEL}`: The human-readable label
- `{PARENT_CLASSES}`: Comma-separated list of parent classes
- `{EXISTING_DEFINITION}`: Current definition if available

---

## Actual Prompt (Copy below this line)

I need you to generate a textual definition for an ontology class following the requirements above.

**Class ID:** {CLASS_ID}
**Class Label:** {CLASS_LABEL}
**Parent Class(es):** {PARENT_CLASSES}
**Existing Definition:** {EXISTING_DEFINITION}

Please provide a definition following the OBO Foundry principles outlined above, formatted as JSON.
