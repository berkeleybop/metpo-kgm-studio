# Definition Generation Prompt Template

**Version: 2.1**
**Purpose:** Generate textual definitions for METPO ontology classes following OBO Foundry principles
**Last Updated:** 2025-10-24

## Instructions for LLM

You are assisting in identifying authoritative ontology or curated reference sources that support or verify textual definitions for METPO ontology classes which will later be used to curate the knowledge graph.

A TSV file or pasted table containing records to process will be provided as input. Process the records so as to ensure accuracy and prevent hallucinations. 

## Requirements (OBO Foundry FP-006)

### 1\. Genus-Differentia Form

Definitions must follow the pattern:

* "An \[parent class\] that \[distinguishing characteristics\]"
* NOT: "A metabolic process..." (avoid starting with article \+ class name)

### 2\. Definition Quality

* Must be clear, concise, and unambiguous
* Must be intelligible to a biologist or microbiologist
* Should reference parent classes from the ontology hierarchy
* Should specify what makes this class distinct from siblings

### 3\. Avoid Circularity

Do not use the term being defined in its own definition

### 4\. Scientific Accuracy

Base definitions on established scientific knowledge

### 5\. Data Integrity Rules

* **To prevent hallucinations if information cannot be verified, respond with null and explain why in the comments field**
* Never fabricate or guess information that cannot be confirmed through authoritative sources
* Include quantitative values or ranges ONLY if they are grounded in real, published measurements with a citation source
* When including quantitative data, provide reasoning in the comments field

## Input Format

Each row in the TSV/CSV input will include:

* Class ID — e.g., `METPO:1234567`
* Class Label — e.g., `methanogenesis`
* Definition — The textual definition requiring authoritative ontology or literature support

Your task is to process each row and return ontology-aligned definitions and sources following the specifications below.

## Source Requirements and Prioritization

### Source Prioritization Hierarchy

1. **Primary Sources (Ontology-based) \- STRONGLY PREFERRED**

   * OBO Foundry ontologies (e.g., OBMS, ENVO, PATO, GO, CHEBI, MEO, BTO, PO, NCIT, ECO)
   * Curated microbiology vocabularies: GOLD, BacDive, MIxS
   * Must include full ontology URLs when available (e.g., `http://purl.obolibrary.org/obo/GO_0015948`)



2. **Secondary Sources (fallback if no ontology match)**

   * PubMed IDs (PMID) with URLs (e.g., `https://pubmed.ncbi.nlm.nih.gov/12345678/`)
   * DOIs with URLs — peer-reviewed scientific literature
   * ISBNs — authoritative textbooks
   * Stable URLs — from recognized research organizations (include access date)

### Source Quality Rules

* Prefer OBO Foundry or peer-reviewed resources
* Sources must describe the same conceptual scope as the METPO definition
* Prefer recent ontology versions or reviews (last 5 years unless classic)
* **Always retrieve and include the actual URL for each source for manual verification**

## Output Format (JSON)

```json
{
    "metadata": {
        "total_definitions": 1,
        "batch_size_limit": "5-10 terms per batch",
        "curator": "curator_name_here",
        "ontology": "METPO",
        "description": "OBO Foundry-compliant definitions for METPO terms",
        "generation_date": "2025-10-24"
    },
    "definitions": [
        {
            "class_id": "METPO:0000123",
            "class_label": "methanogenesis",
            "parent_class": "anaerobic metabolic process",
            "parent_class_id": "GO:0009061",
            "proposed_definition": "An anaerobic metabolic process that produces methane as the primary end product, typically using carbon dioxide or acetate as electron acceptors.",
            "quantitative_values": {
                "temperature_range": "15-110°C",
                "optimal_pH_range": "6.8-7.2",
                "measurement_source": "PMID:28792873"
            },
            "reasoning": "Definition follows genus-differentia pattern, aligns with GO:0015948 (methanogenesis) and ENVO:00002029 (methanogenic environment). Clarifies distinguishing metabolic characteristics. Temperature range based on published measurements from thermophilic and mesophilic methanogens.",
            "sources": [
                {
                    "type": "ontology",
                    "id": "GO:0015948",
                    "label": "methanogenesis",
                    "url": "http://purl.obolibrary.org/obo/GO_0015948"
                },
                {
                    "type": "ontology",
                    "id": "ENVO:00002029",
                    "label": "methanogenic environment",
                    "url": "http://purl.obolibrary.org/obo/ENVO_00002029"
                },
                {
                    "type": "ontology",
                    "id": "MEO:0000111",
                    "label": "methanogenic bacterium",
                    "url": "http://purl.obolibrary.org/obo/MEO_0000111"
                }
            ],
            "confidence": "high",
            "comments": "Parent class retrieved from GO hierarchy. Quantitative temperature values based on published ranges for known methanogenic archaea. If unable to verify specific values, would mark as null."
        }
    ]
}
```

## Critical Instructions for Verification

1. **Verification**: If you cannot verify information through authoritative sources, use `null` values and explain in the `comments` field
2. **URLs Required**: Always include full URLs for all sources to enable manual verification
3. **Parent Classes**: Always include both the human-readable parent class label AND its ID
4. **Quantitative Data**: Include measurement min/max ranges only when supported by published data; cite the source
5. **Source Preference**: Always prioritize ontology terms over publications when both are available

**Example of handling unverifiable information:**

```json
{
    "quantitative_values": null,
    "comments": "Unable to verify specific temperature ranges from authoritative sources. Recommend manual curation from primary literature."
}
```
