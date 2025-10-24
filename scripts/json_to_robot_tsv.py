#!/usr/bin/env python3
"""
Convert JSON output from LLM definition generation to ROBOT template TSV format.

This script transforms the JSON output containing ontology term definitions
into a TSV file compatible with ROBOT template format for ontology editing.

Usage:
    python json_to_robot_tsv.py input.json output.tsv
    
    Or import as module:
    from json_to_robot_tsv import convert_json_to_robot_tsv
    convert_json_to_robot_tsv('input.json', 'output.tsv')
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
        data = json.load(f)
    
    return data


def convert_sources_to_pipe_separated(sources: List[str]) -> str:
    """
    Convert list of sources to pipe-separated string for ROBOT template.
    
    Args:
        sources: List of source identifiers (e.g., ['OLS:GO:0009061', 'PMID:12345'])
        
    Returns:
        Pipe-separated string (e.g., 'OLS:GO:0009061|PMID:12345')
    """
    return '|'.join(sources) if sources else ''


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
        
        # Convert sources list to pipe-separated string
        sources = definition.get('sources', [])
        definition_sources = convert_sources_to_pipe_separated(sources)
        
        # Get notes if present (this goes in the comment field)
        notes = definition.get('notes', '')
        
        # Create data row matching the template structure
        data_row = [
            class_id,           # ID
            label,              # label
            'owl:Class',        # TYPE (always owl:Class for these terms)
            parent_class,       # parent class (SubClass Of)
            description,        # description (IAO:0000115 - textual definition)
            definition_sources, # definition source (IAO:0000119)
            notes,              # comment (rdfs:comment)
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
    print(f"📊 Found {total_defs} definitions in JSON")
    print(f"   Curator: {metadata.get('curator', 'unknown')}")
    print(f"   Date: {metadata.get('generation_date', 'unknown')}")
    print(f"   Ontology: {metadata.get('ontology', 'unknown')}")
    
    print(f"\n🔄 Converting to ROBOT template format...")
    rows = json_to_robot_rows(json_data)
    
    print(f"💾 Writing TSV to: {output_path}")
    write_tsv(rows, output_path)
    
    print(f"\n✨ Conversion complete!")


def main():
    """Command-line interface."""
    if len(sys.argv) != 3:
        print("Usage: python json_to_robot_tsv.py <input.json> <output.tsv>")
        print("\nExample:")
        print("  python json_to_robot_tsv.py outputs/reviewed/curator5/2025-10-17_curator5_v3_output.json output.tsv")
        sys.exit(1)
    
    json_path = sys.argv[1]
    output_path = sys.argv[2]
    
    try:
        convert_json_to_robot_tsv(json_path, output_path)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
