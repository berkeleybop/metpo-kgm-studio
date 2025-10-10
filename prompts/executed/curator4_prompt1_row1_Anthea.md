Model: Claude 4.5
------------------------------------------------------------------------
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
--------------------------------------------------------------------------------------------------------------------------------------------
Claude responded:
I'm ready to help curate definitions for METPO following OBO Foundry principles. I understand the requirements:

1. **Genus-Differentia Form**: Definitions should follow "An [parent class] that [distinguishing characteristics]"
2. **Quality Standards**: Clear, concise, unambiguous, and intelligible to microbiologists
3. **No Circularity**: Don't use the term being defined in its definition
4. **Scientific Accuracy**: Based on established knowledge

I'll provide responses in the specified JSON format with:
- Proposed definition following OBO Foundry FP-006
- Confidence level (high/medium/low)
- Reasoning for the definition
- Suggested scientific sources (PMIDs, DOIs, ISBNs)

Please provide the term(s) you'd like me to define, including:
- Class ID
- Class Label
- Parent Class(es)
- Existing Definition (if any)
- Any additional context about sibling classes or related terms

I'm ready to begin! What term would you like me to work on first?
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Followup:
I need you to generate a textual definition for an ontology class following the requirements above.
ID: METPO:1000059 label: phenotype TYPE: owl:Class parent class: quality description: A (combination of) quality(ies) of an organism determined by the interaction of its genetic make-up and environment that differentiates specific instances of a species from other instances of the same species. definition source: OGMS:0000023 comment:  biolink equivalent: https://biolink.github.io/biolink-model/PhenotypicQuality confirmed exact synonym:  literature mining synonyms:  madin synonym or field:  synonym source:  bacdive keyword synonym:  bactotraits synonym: 

Note that some columns are empty. Here are all of the columns: ID label TYPE parent class description definition source comment biolink equivalent confirmed exact synonym literature mining synonyms madin synonym or field synonym source bacdive keyword synonym bactotraits synonym

Please provide a definition following the OBO Foundry principles outlined above, formatted as JSON.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------

{
  "class_id": "METPO:1000059",
  "class_label": "phenotype",
  "proposed_definition": "A quality or combination of qualities of an organism that results from the interaction between its genotype and environment, and that distinguishes individual organisms or strains within a species from one another.",
  "confidence": "high",
  "reasoning": "This definition follows the genus-differentia form starting with the parent class 'quality'. It distinguishes phenotype from other qualities by specifying: (1) it pertains to organisms, (2) it arises from genotype-environment interaction, and (3) it creates observable variation within a species. The definition avoids circularity by not using 'phenotype' or 'phenotypic' in the definition itself. It is appropriate for METPO's microbial context while remaining general enough for broader biological applications.",
  "suggested_sources": [
    "PMID:18460186",
    "PMID:11337588",
    "DOI:10.1038/nrg1606"
  ],
  "notes": "The existing description from OGMS:0000023 is well-structured but could be streamlined. The proposed definition maintains the key concepts (quality, genotype-environment interaction, intraspecific variation) while using clearer language. 'Genetic make-up' is replaced with 'genotype' for precision, and 'differentiates specific instances' is simplified to 'distinguishes individual organisms or strains' for better clarity in microbial contexts."
}

------------------------------------------------------------------------------------------------------------------------------------------------------------------------
...continues: https://claude.ai/share/4d25ca86-909c-4870-afbe-ac75ac76c434
