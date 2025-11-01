#!/usr/bin/env python3
"""
Convert JSON output from LLM definition generation to ROBOT template TSV format.
Supports v2.1 format (structured sources, parent_class_id, quantitative_values) and legacy formats.

Usage: python json_to_robot_tsv.py input.json output.tsv
"""

import json
import csv
import sys
from pathlib import Path
from typing import Dict, List, Any


def load_json(json_path: str) -> Dict[str, Any]:
    """
    Load JSON file containing LLM-generated definitions.
    
    Args:
        json_path: Path to input JSON file
        
    Returns:
        Dictionary containing metadata and definitions
        
    Raises:
        FileNotFoundError: If JSON file doesn't exist
        JSONDecodeError: If JSON is malformed
    """
    json_file = Path(json_path)
    if not json_file.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data: Dict[str, Any] = json.load(f)

    return data


def convert_sources_to_pipe_separated(sources: List[Any] | None) -> str:
    """
    Convert sources to pipe-separated string for ROBOT template.
    
    Handles both v2.1 format (list of dicts with 'id' field) and 
    legacy format (list of strings).
    
    Args:
        sources: List of source dicts (v2.1) or strings (legacy)
                 v2.1 format: [{"type": "ontology", "id": "GO:0015948", "label": "...", "url": "..."}]
                 Legacy format: ['OLS:GO:0009061', 'PMID:12345']
        
    Returns:
        Pipe-separated string (e.g., 'GO:0015948|ENVO:00002029|PMID:12345678')
    """
    if not sources:
        return ''
    
    # Check if v2.1 format (list of dicts) or legacy format (list of strings)
    if isinstance(sources, list) and len(sources) > 0:
        if isinstance(sources[0], dict):
            # v2.1 format: extract 'id' field from each source dict
            return '|'.join(source.get('id', '') for source in sources if source.get('id'))
        else:
            # Legacy format: join strings directly
            return '|'.join(sources)
    
    return ''


def format_quantitative_values(quant_values: Dict[str, Any] | None) -> str:
    """
    Format quantitative values into a human-readable string for comments field.
    
    Args:
        quant_values: Dictionary of quantitative measurements or None
        
    Returns:
        Formatted string describing the measurements, or empty string if None
    """
    if not quant_values:
        return ''
    
    if isinstance(quant_values, dict):
        # Extract key-value pairs, excluding 'measurement_source'
        measurements = []
        for key, value in quant_values.items():
            if key != 'measurement_source' and value:
                # Format key: replace underscores with spaces, capitalize
                formatted_key = key.replace('_', ' ').title()
                measurements.append(f"{formatted_key}: {value}")
        
        if measurements:
            quant_str = '; '.join(measurements)
            # Add source if present
            if 'measurement_source' in quant_values:
                quant_str += f" (Source: {quant_values['measurement_source']})"
            return quant_str
    
    return ''


def json_to_robot_rows(json_data: Dict[str, Any]) -> List[List[str]]:
    """
    Convert JSON data to ROBOT template rows.
    
    Args:
        json_data: Dictionary containing 'metadata' and 'definitions'
        
    Returns:
        List of rows, where each row is a list of strings
    """
    # ROBOT template header row (column names)
    header_row = [
        'ID',
        'label',
        'TYPE',
        'parent class',
        'description',
        'definition source',
        'comment',
        'biolink equivalent',
        'confirmed exact synonym',
        'literature mining synonyms',
        'madin synonym or field',
        'synonym source',
        'bacdive keyword synonym',
        'bactotraits synonym'
    ]
    
    # ROBOT template annotation row (ROBOT directives)
    annotation_row = [
        'ID',
        'LABEL',
        'TYPE',
        'SC %',  # SubClass Of (%)
        'A IAO:0000115',  # Annotation: definition (IAO:0000115)
        '>A IAO:0000119',  # Multiple annotations: definition source
        'A rdfs:comment',  # Annotation: comment
        'AI skos:closeMatch',  # Annotation with IRI
        'A oboInOwl:hasExactSynonym SPLIT=|',
        'A oboInOwl:hasRelatedSynonym SPLIT=|',
        'A oboInOwl:hasRelatedSynonym SPLIT=|',
        '>AI IAO:0000119',  # Multiple annotation IRIs
        'A oboInOwl:hasRelatedSynonym SPLIT=|',
        'A oboInOwl:hasRelatedSynonym SPLIT=|'
    ]
    
    rows = [header_row, annotation_row]
    
    # Convert each definition to a row
    for definition in json_data.get('definitions', []):
        class_id = definition.get('class_id', '')
        label = definition.get('class_label', '')
        parent_class = definition.get('parent_class', '')
        description = definition.get('proposed_definition', '')
        
        # Convert sources to pipe-separated string (handles both v2.1 and legacy formats)
        sources = definition.get('sources', [])
        definition_sources = convert_sources_to_pipe_separated(sources)
        
        # Build comment field from multiple sources
        comment_parts = []
        
        # Add existing comments/notes
        if definition.get('comments'):
            comment_parts.append(definition.get('comments'))
        elif definition.get('notes'):
            comment_parts.append(definition.get('notes'))
        
        # Add quantitative values if present (v2.1 feature)
        quant_str = format_quantitative_values(definition.get('quantitative_values'))
        if quant_str:
            comment_parts.append(f"Quantitative values: {quant_str}")
        
        # Add reasoning if present (v2.1 feature)
        if definition.get('reasoning'):
            comment_parts.append(f"Reasoning: {definition.get('reasoning')}")
        
        # Add parent class ID if present (v2.1 feature)
        if definition.get('parent_class_id'):
            comment_parts.append(f"Parent class ID: {definition.get('parent_class_id')}")
        
        # Join all comment parts
        comments = ' | '.join(comment_parts) if comment_parts else ''
        
        # Create data row matching the template structure
        data_row = [
            class_id,           # ID
            label,              # label
            'owl:Class',        # TYPE (always owl:Class for these terms)
            parent_class,       # parent class (SubClass Of)
            description,        # description (IAO:0000115 - textual definition)
            definition_sources, # definition source (IAO:0000119)
            comments,           # comment (rdfs:comment) - now includes quantitative values, reasoning, etc.
            '',                 # biolink equivalent (empty for now)
            '',                 # confirmed exact synonym (empty for now)
            '',                 # literature mining synonyms (empty for now)
            '',                 # madin synonym or field (empty for now)
            '',                 # synonym source (empty for now)
            '',                 # bacdive keyword synonym (empty for now)
            ''                  # bactotraits synonym (empty for now)
        ]
        
        rows.append(data_row)
    
    return rows


def write_tsv(rows: List[List[str]], output_path: str) -> None:
    """
    Write rows to TSV file.
    
    Args:
        rows: List of rows to write
        output_path: Path to output TSV file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)
    
    print(f"✅ Successfully wrote {len(rows) - 2} definitions to {output_path}")
    print(f"   (Total rows: {len(rows)} including 2 header rows)")


def convert_json_to_robot_tsv(json_path: str, output_path: str) -> None:
    """
    Main conversion function: JSON to ROBOT template TSV.
    
    Args:
        json_path: Path to input JSON file
        output_path: Path to output TSV file
    """
    print(f"📖 Reading JSON from: {json_path}")
    json_data = load_json(json_path)
    
    # Validate JSON structure
    if 'definitions' not in json_data:
        raise ValueError("JSON must contain 'definitions' key")
    
    metadata = json_data.get('metadata', {})
    total_defs = metadata.get('total_definitions', len(json_data['definitions']))
    prompt_version = metadata.get('prompt_version', 'unknown')
    batch_number = metadata.get('batch_number', '')
    
    print(f"📊 Found {total_defs} definitions in JSON")
    print(f"   Curator: {metadata.get('curator', 'unknown')}")
    print(f"   Date: {metadata.get('generation_date', 'unknown')}")
    print(f"   Ontology: {metadata.get('ontology', 'unknown')}")
    print(f"   Prompt version: {prompt_version}")
    if batch_number:
        print(f"   Batch number: {batch_number}")
    
    print(f"\n🔄 Converting to ROBOT template format...")
    rows = json_to_robot_rows(json_data)
    
    print(f"💾 Writing TSV to: {output_path}")
    write_tsv(rows, output_path)
    
    print(f"\n✨ Conversion complete!")
    
    # Summary of v2.1 features detected
    v21_features = []
    for definition in json_data.get('definitions', []):
        if definition.get('parent_class_id'):
            v21_features.append('parent_class_id')
            break
    for definition in json_data.get('definitions', []):
        if definition.get('quantitative_values'):
            v21_features.append('quantitative_values')
            break
    for definition in json_data.get('definitions', []):
        if definition.get('reasoning'):
            v21_features.append('reasoning')
            break
    
    if v21_features:
        print(f"\n📋 v2.1 features included: {', '.join(v21_features)}")


def main() -> None:
    """Command-line interface."""
    if len(sys.argv) != 3:
        print("Usage: python json_to_robot_tsv.py <input.json> <output.tsv>")
        print("\nExample:")
        print("  python json_to_robot_tsv.py outputs/raw/curator5/2025-10-30_curator5_v2.1_batch1_output.json output.tsv")
        print("\nSupports:")
        print("  - v2.1 format with structured sources, parent_class_id, quantitative_values")
        print("  - Legacy formats with simple source lists")
        sys.exit(1)
    
    json_path = sys.argv[1]
    output_path = sys.argv[2]
    
    try:
        convert_json_to_robot_tsv(json_path, output_path)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
