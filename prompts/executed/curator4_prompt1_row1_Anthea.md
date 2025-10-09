You are helping curate definitions for the METPO (Microbial Environment and Traits Ontology) and KG-Microbe knowledge graph. Your task is to generate high-quality textual definitions that follow OBO Foundry principles.
Requirements (OBO Foundry FP-006)
1. Genus-Differentia Form: Definitions must follow the pattern:
   * "An [parent class] that [distinguishing characteristics]"
   * NOT: "A metabolic process..." (avoid starting with article + class name)
2. Definition Quality:
   * Must be clear, concise, and unambiguous
   * Must be intelligible to a biologist or microbiologist
   * Should reference parent classes from the ontology hierarchy
   * Should specify what makes this class distinct from siblings
3. Avoid Circularity: Do not use the term being defined in its own definition
4. Scientific Accuracy: Base definitions on established scientific knowledge
Input Format
For each term, you will receive:
* Class ID: e.g., METPO:1234567
* Class Label: e.g., "anaerobic respiration"
* Parent Class(es): e.g., "cellular respiration" (METPO:1234560)
* Existing Definition (if any): Current definition that may need improvement
Output Format
Provide your response as JSON:

```
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

Example
Input:
* Class ID: METPO:0000123
* Class Label: methanogenesis
* Parent Class: anaerobic respiration (METPO:0000120)
* Existing Definition: None
Expected Output:

```
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

<data>

ID	label	TYPE	parent class	description	definition source	comment	biolink equivalent	confirmed exact synonym	literature mining synonyms	madin synonym or field	synonym source	bacdive keyword synonym	bactotraits synonym
ID	LABEL	TYPE	SC %	A IAO:0000115	>A IAO:0000119	A rdfs:comment	AI skos:closeMatch	A oboInOwl:hasExactSynonym SPLIT=|	A oboInOwl:hasRelatedSynonym SPLIT=|	A oboInOwl:hasRelatedSynonym SPLIT=|	>AI IAO:0000119	A oboInOwl:hasRelatedSynonym SPLIT=|	A oboInOwl:hasRelatedSynonym SPLIT=|
METPO:1000059	phenotype	owl:Class	quality	A (combination of) quality(ies) of an organism determined by the interaction of its genetic make-up and environment that differentiates specific instances of a species from other instances of the same species.	OGMS:0000023		https://biolink.github.io/biolink-model/PhenotypicQuality						

<data>
