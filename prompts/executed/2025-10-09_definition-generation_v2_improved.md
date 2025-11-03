# Definition Generation Prompt Template - Version 2.0 (IMPROVED)

**Version:** 2.0
**Purpose:** Generate textual definitions for METPO ontology classes following OBO Foundry principles
**Date Executed:** 2025-10-09
**Curator:** curator5
**Improvements:** Added batch processing, domain-specific guidelines, validation checklist, and enhanced examples

---

## Instructions for LLM

You are helping curate definitions for the METPO (Microbial Environment and Traits Ontology) and KG-Microbe knowledge graph. Your task is to generate high-quality textual definitions that follow OBO Foundry principles.

### Requirements (OBO Foundry FP-006)

1. **Genus-Differentia Form**: Definitions must follow the pattern:
   - "An [parent class] that [distinguishing characteristics]"
   - "A [parent class] in which [distinguishing characteristics]"
   - NOT: "Acetogenesis is..." or "Methanogenesis produces..." (avoid starting with the term being defined)

2. **Definition Quality**:
   - Must be clear, concise, and unambiguous
   - Must be intelligible to a biologist or microbiologist
   - Should reference parent classes from the ontology hierarchy
   - Should specify what makes this class distinct from sibling classes
   - Should be scientifically accurate and current

3. **Avoid Circularity**: Do not use the term being defined (or its synonyms) in its own definition

4. **Scientific Accuracy**: Base definitions on established scientific knowledge from peer-reviewed sources

### Common Mistakes to Avoid

❌ **Circular Definition**:
- Bad: "Methanogenesis is a process of producing methane by methanogens"
- Good: "A metabolic process in which methane is produced as the primary end product..."

❌ **Too Vague**:
- Bad: "A cell shape found in some bacteria"
- Good: "A cell shape in which an organism has a spherical or nearly spherical morphology, with roughly equal dimensions in all directions"

❌ **Wrong Pattern**:
- Bad: "Acetogenesis produces acetate through reduction of CO2"
- Good: "A metabolic process in which acetate is produced as the primary end product through the reduction of carbon dioxide..."

❌ **Missing Distinguishing Features**:
- Bad: "A type of respiration"
- Good: "A respiration process in which molecular oxygen serves as the terminal electron acceptor..."

### Input Format

For each term, you will receive:
- **Class ID**: e.g., METPO:1234567
- **Class Label**: e.g., "anaerobic respiration"
- **Parent Class(es)**: e.g., "cellular respiration" or "respiration"
- **Existing Definition** (if any): Current definition that may need improvement
- **Known Synonyms** (optional): Related terms or alternate labels
- **Sibling Classes** (optional): Other terms with the same parent class

### METPO-Specific Guidelines

#### 1. For Metabolic Processes (metabolism, respiration, fermentation, etc.)
- **Specify substrates and products**: What compounds are consumed and produced?
- **Specify conditions**: Aerobic, anaerobic, microaerobic?
- **Specify electron donors/acceptors** when relevant
- **Mention taxonomic restrictions** if process is limited to specific groups (e.g., "exclusively performed by methanogenic archaea")
- **Examples**: Acetogenesis, Methanogenesis, Aerobic respiration, Disproportionation

#### 2. For Morphological Terms (cell shape, colony morphology)
- **Provide geometric/spatial description**: Shape, dimensions, proportions
- **Distinguish from similar shapes**: How is "helical" different from "spirochete"?
- **Be specific about characteristics**: "spherical or nearly spherical" not just "round"
- **Examples**: coccus shaped, helical shaped, pleomorphic shaped, ellipsoidal

#### 3. For Growth Preferences (pH, temperature, salinity, nutrient)
- **Specify quantitative ranges** when possible (pH 5.5, 15-30% NaCl)
- **Distinguish obligate vs. facultative**: Can only grow vs. can also grow
- **Define tolerance vs. preference**: "tolerates acidic" vs. "requires acidic"
- **Examples**: acidotolerant, obligately acidophilic, extremely halophilic, oligotrophic

#### 4. For Trophic Types (autotrophic, heterotrophic, etc.)
- **Clearly state BOTH energy source AND carbon source**
- **Energy source**: Light (photo-) or chemical (chemo-)
- **Carbon source**: Organic (organo-/hetero-) or inorganic (litho-/auto-)
- **Avoid ambiguity** between energy and carbon metabolism
- **Examples**: chemoorganotrophic, photolithotrophic, lithoheterotrophic, hydrogenotrophic

#### 5. For Phenotypic Traits (motility, gram stain, etc.)
- **Describe the observable characteristic**
- **Mention underlying mechanism** when relevant (e.g., cell wall structure for gram stain)
- **Distinguish from related traits**
- **Examples**: motility, gram stain, cell shape

### Output Format

#### For Single Term:
```json
{
  "class_id": "METPO:1234567",
  "class_label": "anaerobic respiration",
  "parent_class": "cellular respiration",
  "proposed_definition": "A cellular respiration process that occurs in the absence of oxygen, using alternative electron acceptors such as nitrate, sulfate, or carbon dioxide.",
  "confidence": "high|medium|low",
  "reasoning": "Brief explanation of why this definition is appropriate and how it distinguishes from related terms",
  "sources": [
    "PMID:12345678",
    "PMID:23456789",
    "DOI:10.1234/example"
  ],
  "notes": "Any additional context, alternative phrasings considered, or edge cases"
}
```

#### For Multiple Terms (Batch Processing):
```json
{
  "metadata": {
    "curator": "curator5",
    "generation_date": "2025-10-09",
    "ontology": "METPO",
    "description": "OBO Foundry-compliant definitions for METPO terms following FP-006 principles",
    "total_definitions": 26
  },
  "definitions": [
    {
      "class_id": "METPO:1000845",
      "class_label": "Acetogenesis",
      "parent_class": "metabolism",
      "proposed_definition": "A metabolic process in which acetate is produced as the primary end product...",
      "confidence": "high",
      "reasoning": "...",
      "sources": ["PMID:12345678"],
      "notes": ""
    },
    {
      "class_id": "METPO:1000806",
      "class_label": "Disproportionation",
      "parent_class": "metabolism",
      "proposed_definition": "A metabolic process in which...",
      "confidence": "high",
      "reasoning": "...",
      "sources": ["PMID:23456789"],
      "notes": ""
    }
  ]
}
```

### Suggested Sources Requirements

**Acceptable Sources** (in order of preference):
1. **Peer-reviewed journal articles**: PMID:12345678
2. **Authoritative textbooks**: ISBN:9781555819675
3. **Published reviews**: DOI:10.1234/example
4. **Official manuals**: CDC Biosafety Manual, Bergey's Manual

**NOT Acceptable**:
- Wikipedia or general encyclopedias
- Non-peer-reviewed blogs or websites
- Unpublished materials
- Sources without proper citations

**Minimum**: Provide at least 2-3 credible sources per definition

**Note**: Sources should be provided in the `sources` field as an array of source identifiers.

### Confidence Levels

- **high**: Definition is scientifically accurate, follows all OBO principles, has strong source support, clearly distinguishes from siblings
- **medium**: Definition is accurate but may be broad, has some source support, could benefit from refinement
- **low**: Definition needs significant work, limited sources, may have ambiguity or circularity issues

### Self-Check Before Submitting

Before providing your response, verify:
- [ ] Definition starts with parent class (genus-differentia form)
- [ ] Term being defined does NOT appear in its own definition (check synonyms too!)
- [ ] Distinguishing characteristics are specific and measurable
- [ ] Definition would be clear to a microbiologist without additional context
- [ ] At least 2 credible sources provided with proper identifiers
- [ ] Confidence level accurately reflects definition quality
- [ ] For metabolic terms: substrates/products and conditions specified
- [ ] For morphological terms: geometric/spatial description provided
- [ ] For preference terms: quantitative ranges included when possible
- [ ] For trophic types: both energy and carbon sources clearly stated

### Special Cases

1. **Broad Parent Classes** (e.g., "phenotype", "metabolism"):
   - Definitions may be intentionally broad but should still specify what the class encompasses
   - Example: "cell shape" is a phenotype that describes morphological form

2. **Terms with Multiple Parents**:
   - Reference the most specific or most relevant parent class in the definition
   - Can mention other relationships in notes

3. **Taxonomically Restricted Terms**:
   - When a process/trait is limited to specific taxa, include this restriction
   - Example: "exclusively performed by methanogenic archaea"

4. **Overlapping Concepts**:
   - Clearly distinguish from siblings by specifying key differences
   - Example: Distinguish "facultatively acidophilic" from "obligately acidophilic" and "acidotolerant"

---

## Example 1: Metabolic Process

**Input:**
- Class ID: METPO:1000844
- Class Label: Methanogenesis
- Parent Class: metabolism
- Existing Definition: None
- Synonyms: Carbonate respiration, Biomethanation, Biological methanation

**Expected Output:**
```json
{
  "class_id": "METPO:1000844",
  "class_label": "Methanogenesis",
  "parent_class": "metabolism",
  "proposed_definition": "A metabolic process in which methane is produced as the primary end product through the reduction of carbon-containing compounds such as carbon dioxide, formate, methanol, or acetate, exclusively performed by methanogenic archaea under strictly anaerobic conditions.",
  "confidence": "high",
  "reasoning": "Definition follows genus-differentia form, clearly distinguishes methanogenesis from other metabolic processes by specifying: (1) unique end product (methane), (2) specific substrates, (3) taxonomic restriction to archaea, and (4) obligate anaerobic nature. This distinguishes it from other anaerobic processes and fermentations.",
  "sources": [
    "PMID:15073711",
    "PMID:23645609",
    "DOI:10.1038/nrmicro.2016.79"
  ],
  "notes": "Synonyms like 'carbonate respiration' emphasize the CO2 reduction pathway. The taxonomic restriction to archaea is critical as it distinguishes true methanogenesis from methane production by other means."
}
```

## Example 2: Cell Shape

**Input:**
- Class ID: METPO:1000668
- Class Label: coccus shaped
- Parent Class: cell shape
- Existing Definition: None
- Synonyms: coccus

**Expected Output:**
```json
{
  "class_id": "METPO:1000668",
  "class_label": "coccus shaped",
  "parent_class": "cell shape",
  "proposed_definition": "A cell shape in which an organism has a spherical or nearly spherical morphology, with roughly equal dimensions in all directions.",
  "confidence": "high",
  "reasoning": "Definition follows genus-differentia form and provides clear geometric description that distinguishes coccus shape from other shapes. The key distinguishing feature is spherical geometry with equal dimensions, which contrasts with elongated shapes (bacillus, vibrio) or irregular shapes (pleomorphic).",
  "sources": [
    "ISBN:9781555819675",
    "PMID:24478428",
    "DOI:10.1038/nrmicro.2016.172"
  ],
  "notes": "Classic bacterial morphology term. 'Nearly spherical' accounts for slight variations while maintaining the essential spherical character."
}
```

## Example 3: pH Growth Preference

**Input:**
- Class ID: METPO:1003006
- Class Label: obligately acidophilic
- Parent Class: pH growth preference
- Existing Definition: None
- Synonyms: obligate acidophile
- Sibling Classes: facultatively acidophilic, acidotolerant

**Expected Output:**
```json
{
  "class_id": "METPO:1003006",
  "class_label": "obligately acidophilic",
  "parent_class": "pH growth preference",
  "proposed_definition": "A pH growth preference in which an organism requires acidic conditions (typically pH below 5.5) for growth and cannot grow at neutral pH.",
  "confidence": "high",
  "reasoning": "Definition follows genus-differentia form and clearly distinguishes obligate acidophiles from: (1) facultative acidophiles (which CAN grow at neutral pH), and (2) acidotolerant organisms (which prefer neutral but tolerate acidic). The quantitative threshold (pH 5.5) and absolute requirement are key distinguishing features.",
  "sources": [
    "PMID:19270716",
    "PMID:17223624",
    "DOI:10.1111/j.1574-6976.2007.00077.x"
  ],
  "notes": "The 'obligate' nature is critical - these organisms fail to grow at neutral pH, unlike facultative forms. The pH 5.5 threshold is a commonly used criterion in microbiology."
}
```

## Example 4: Trophic Type

**Input:**
- Class ID: METPO:1000648
- Class Label: lithoheterotrophic
- Parent Class: trophic type
- Existing Definition: None
- Synonyms: lithoheterotroph

**Expected Output:**
```json
{
  "class_id": "METPO:1000648",
  "class_label": "lithoheterotrophic",
  "parent_class": "trophic type",
  "proposed_definition": "A trophic type in which an organism obtains energy from the oxidation of inorganic compounds while using organic compounds as the primary carbon source for biosynthesis.",
  "confidence": "high",
  "reasoning": "Definition follows genus-differentia form and clearly specifies BOTH energy source (inorganic compounds = litho-) AND carbon source (organic compounds = hetero-). This distinguishes lithoheterotrophy from: (1) chemoorganotrophy (organic energy + organic carbon), (2) photoautotrophy/chemolithoautotrophy (inorganic/light energy + inorganic carbon), and (3) photoheterotrophy (light energy + organic carbon).",
  "sources": [
    "PMID:16933922",
    "PMID:19270710",
    "DOI:10.1128/MMBR.00008-10"
  ],
  "notes": "This is a less common trophic strategy but important for certain sulfur and iron oxidizers. The combination of inorganic energy source with organic carbon source is the key distinguishing characteristic."
}
```

---

## Template Variables

Replace these before sending to LLM:

- `{CLASS_ID}`: The ontology class ID (e.g., METPO:1000845)
- `{CLASS_LABEL}`: The human-readable label (e.g., "Acetogenesis")
- `{PARENT_CLASSES}`: Comma-separated list of parent classes (e.g., "metabolism")
- `{EXISTING_DEFINITION}`: Current definition if available, or "None"
- `{SYNONYMS}`: Known synonyms if available (optional)
- `{SIBLING_CLASSES}`: Related terms with same parent (optional)

**For Batch Processing**, provide a list of terms in structured format (TSV, JSON, or table).

---


---

## Execution Log

**Date Executed:** 2025-10-09
**Curator:** curator5
**Terms Processed:** 26 METPO terms
**Input Source:** assignments/curator5.tsv
**Output Location:** outputs/raw/curator5/2025-10-09_all_terms_output.json
**Status:** Completed - Definitions generated for all 26 terms
**Notes:**
- Used batch processing format
- All definitions follow genus-differentia form
- 25 high confidence, 1 medium confidence (Electron transfer - intentionally broad)
- Focused on distinguishing metabolic processes, cell shapes, pH preferences, and trophic types
- Sources include PMIDs, DOIs, and ISBNs from authoritative microbiology literature
