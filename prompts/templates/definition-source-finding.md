# Definition Source Finding Prompt Template

**Version:** 1.0
**Purpose:** Find authoritative sources for METPO ontology class definitions
**Last Updated:** {% now 'utc', '%Y-%m-%d' %}

---

## Instructions for LLM

You are helping find authoritative literature sources that support textual definitions for METPO (Microbial Environment and Traits Ontology) classes.

### Requirements

1. **Source Types (in order of preference)**:
   - PubMed IDs (PMID:12345678)
   - DOIs (DOI:10.1234/example)
   - ISBNs for textbooks (ISBN:1234567890)
   - Authoritative web resources (URL with access date)

2. **Source Quality**:
   - Must be peer-reviewed or from authoritative textbooks
   - Should be recent (prefer last 10 years unless classic reference)
   - Must directly support the definition provided
   - Prefer review articles over primary research when available

3. **Citation Format**:
   - Use standard identifiers (PMID, DOI, ISBN)
   - For URLs, include the access date
   - Provide full citation details for verification

### Input Format

You will receive:
- **Class ID**: e.g., METPO:1234567
- **Class Label**: e.g., "methanogenesis"
- **Definition**: The textual definition needing sources

### Output Format

Provide your response as JSON:

```json
{
  "class_id": "METPO:1234567",
  "class_label": "methanogenesis",
  "definition": "An anaerobic respiration process...",
  "sources": [
    {
      "identifier": "PMID:12345678",
      "type": "pubmed",
      "title": "Article title here",
      "authors": "Smith et al.",
      "year": "2020",
      "relevance": "Provides comprehensive review of methanogenic pathways",
      "confidence": "high"
    },
    {
      "identifier": "DOI:10.1234/example",
      "type": "doi",
      "title": "Another relevant article",
      "authors": "Jones et al.",
      "year": "2019",
      "relevance": "Describes electron acceptors in methanogenesis",
      "confidence": "high"
    }
  ],
  "search_terms_used": ["methanogenesis", "anaerobic respiration", "methane production"],
  "notes": "Both sources are recent review articles that comprehensively support the definition."
}
```

### Example

**Input:**
- Class ID: METPO:0000123
- Class Label: methanogenesis
- Definition: "An anaerobic respiration process in which methane is produced as the primary metabolic end product, typically using carbon dioxide or acetic acid as terminal electron acceptors."

**Expected Output:**
```json
{
  "class_id": "METPO:0000123",
  "class_label": "methanogenesis",
  "definition": "An anaerobic respiration process in which methane is produced as the primary metabolic end product, typically using carbon dioxide or acetic acid as terminal electron acceptors.",
  "sources": [
    {
      "identifier": "PMID:15073711",
      "type": "pubmed",
      "title": "Methanogenic archaea: ecologically relevant differences in energy conservation",
      "authors": "Thauer RK et al.",
      "year": "2008",
      "relevance": "Comprehensive review of methanogenic pathways and energy conservation mechanisms",
      "confidence": "high"
    },
    {
      "identifier": "PMID:23645609",
      "type": "pubmed",
      "title": "Diversity and evolution of methanogenic archaea",
      "authors": "Evans PN et al.",
      "year": "2015",
      "relevance": "Describes diversity of substrates and electron acceptors in methanogenesis",
      "confidence": "high"
    }
  ],
  "search_terms_used": ["methanogenesis", "methanogenic archaea", "methane production"],
  "notes": "Both are highly cited review articles from leaders in the field. The 2008 Thauer review is considered a classic reference."
}
```

---

## Usage Notes for Curators

1. **Verify Sources**: Always check that PMIDs and DOIs are correct
2. **Read Abstracts**: Confirm the source actually supports the definition
3. **Check Access**: Ensure sources are accessible (open access preferred)
4. **Multiple Sources**: Aim for 2-3 high-quality sources per definition
5. **Track Searches**: Record your search strategy for reproducibility

## Template Variables

Replace these before sending to LLM:

- `{CLASS_ID}`: The ontology class ID
- `{CLASS_LABEL}`: The human-readable label
- `{DEFINITION}`: The definition needing sources

---

## Actual Prompt (Copy below this line)

I need you to find authoritative literature sources for an ontology class definition following the requirements above.

**Class ID:** {CLASS_ID}
**Class Label:** {CLASS_LABEL}
**Definition:** {DEFINITION}

Please find 2-3 high-quality sources that support this definition, formatted as JSON according to the template above.
