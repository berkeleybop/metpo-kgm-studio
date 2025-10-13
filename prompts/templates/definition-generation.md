# Definition Generation Prompt Template

**Version:** 1.0
**Purpose:** Generate textual definitions for METPO ontology classes following OBO Foundry principles
**Last Updated:** 2025-10-13


---

## Instructions for LLM

You are assisting in identifying **authoritative ontology or curated reference sources** that support or verify textual definitions for METPO ontology classes which will later be used to curate the knowledge graph.  
An entire TSV or CSV file containing multiple class records will be provided as input.


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


## Input Format

Each row in the TSV/CSV input will include:
- **Class ID** — e.g., `METPO:1234567`  
- **Class Label** — e.g., `methanogenesis`  
- **Definition** — The textual definition requiring authoritative ontology or literature support  

Your task is to process each row and return ontology-aligned definitions and sources following the specifications below.

---

## Requirements (OBO Foundry FP-006)

### **Genus–Differentia Form**
Definitions must follow the logical pattern:
> **"An [parent class] that [distinguishing characteristics]"**

- ❌ Do **not** start with "A metabolic process..." or any article + class name phrasing  
- ✅ Example:  
  *"An anaerobic metabolic process that produces methane as a primary end product."*

### **Definition Quality**
Definitions must:
- Be **clear**, **concise**, and **unambiguous**
- Be **intelligible** to a biologist or microbiologist
- Reference **parent classes** from the ontology hierarchy
- Specify **what distinguishes** the term from sibling classes
- **Avoid circularity** (do not use the term being defined within the definition)
- Ensure **scientific accuracy** — all statements must align with established, peer-reviewed or ontology-backed knowledge

---

## Source Prioritization Hierarchy

### **1. Preferred Sources (Ontology-based)**
- OBO Foundry ontologies (e.g., **OBMS**, **ENVO**, **PATO**, **GO**, **CHEBI**, **MEO**, **BTO**, **PO**, **NCIT**, **ECO**)
- Curated microbiology vocabularies: **GOLD**, **BacDive**, **MIxS**
- Ontology URIs or IDs (e.g., `"ENVO:00002002"`, `"GO:0015948"`)

### **2. Secondary Sources (if no ontology match)**
- **PubMed IDs (PMID)** — review or canonical articles  
- **DOIs** — peer-reviewed scientific literature  
- **ISBNs** — authoritative textbooks  
- **Stable URLs** — from recognized research organizations (include access date)

### **3. Source Quality Rules**
- Prefer **OBO Foundry** or **peer-reviewed** resources  
- Sources must describe the **same conceptual scope** as the METPO definition  
- Prefer **recent ontology versions or reviews** (last 10 years unless classic)

---
## Output Format (JSON)

```json
{
    "metadata": {
        "total_definitions": 1,
        "curator": "curator_name_here",
        "ontology": "METPO",
        "description": "OBO Foundry-compliant definitions for METPO terms",
        "generation_date": "2025-10-09"
    },
    "definitions": [
        {
            "class_id": "METPO:0000123",
            "class_label": "methanogenesis",
            "proposed_definition": "An anaerobic metabolic process that produces methane as the primary end product, typically using carbon dioxide or acetate as electron acceptors.",
            "reasoning": "Definition follows genus-differentia pattern, aligns with GO:0015948 (methanogenesis) and ENVO:00002029 (methanogenic environment). Clarifies distinguishing metabolic characteristics.",
            "sources": [
                "GO:0015948 (methanogenesis)",
                "ENVO:00002029 (methanogenic environment)",
                "MEO:0000111 (methanogenic bacterium)"
            ],
            "confidence": "high"
        }
    ]
}
```
---
```
{
    "metadata": {
        "total_definitions": 2,
        "curator": "curator5",
        "ontology": "METPO",
        "description": "OBO Foundry-compliant definitions for METPO terms - final version",
        "generation_date": "2025-10-09"
    },
    "definitions": [
        {
            "class_id": "METPO:1000845",
            "class_label": "Acetogenesis",
            "proposed_definition": "A metabolic process that produces acetate as the primary end product through the reduction of carbon dioxide or other carbon compounds, typically performed by acetogenic bacteria under anaerobic conditions.",
            "reasoning": "Uses genus-differentia form. Aligns with GO:0015946 (acetate biosynthetic process) and ENVO:00002002 (acetogenic environment) for acetogenic metabolism.",
            "sources": [
                "GO:0015946 (acetate biosynthetic process)",
                "ENVO:00002002 (acetogenic environment)",
                "MEO:0000134 (acetogenic bacterium)"
            ],
            "confidence": "high"
        },
        {
            "class_id": "METPO:2000543",
            "class_label": "acidotolerant",
            "proposed_definition": "An organism trait that enables tolerance to acidic environments (typically pH below 5.5) while maintaining optimal growth near neutral pH.",
            "reasoning": "Distinguishes acidotolerant from acidophilic by emphasizing tolerance vs preference. Matches PATO pH tolerance traits.",
            "sources": [
                "PATO:0001796 (pH tolerance)",
                "ENVO:01000240 (acidic environment)",
                "BTO:0000148 (acid-tolerant bacterium)"
            ],
            "confidence": "high"
        }
    ]
}
```
## Usage Notes for Curators

1. **Save Prompts**: When you execute this prompt, copy it to `prompts/executed/` with a timestamp
2. **Record Output**: Save the LLM output to `outputs/raw/[your-name]/` as JSON
3. **Review Carefully**: The LLM can make mistakes - always verify scientific accuracy
4. **Check Sources**: Verify that suggested sources actually support the definition
5. **Iterate**: If the output is poor, revise this template and try again

## 📄 Note

When the TSV/CSV file is uploaded, the LLM should:

- Parse all rows (class_id, class_label, definition)
- Generate ontology-aligned definitions using genus–differentia structure
- Retrieve ontology cross-references and compile the output into the JSON structure above
