#!/usr/bin/env python3
"""
Visualize Ontology Source Distribution

Generates a bar chart showing the distribution of ontology prefixes
across the definition sources in the combined curator TSV file.

Usage:
    python scripts/visualize_ontology_sources.py [input_tsv] [output_png]

Default:
    python scripts/visualize_ontology_sources.py
    # Uses: outputs/final/combined_curators_4_5_6.tsv
    # Saves to: outputs/final/ontology_prefix_distribution.png
"""

import re
import sys
from collections import Counter
from pathlib import Path
import matplotlib.pyplot as plt


def extract_ontology_prefixes(tsv_file):
    """Extract ontology prefixes from the definition source column."""
    ontology_prefixes = []
    
    with open(tsv_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        # Skip the two header rows
        for line in lines[2:]:
            parts = line.strip().split('\t')
            if parts and parts[0].startswith('METPO:') and len(parts) > 5:
                sources = parts[5]  # Column 6 is definition source
                if sources:
                    # Extract ontology prefixes (e.g., GO, PATO, ENVO, etc.)
                    matches = re.findall(r'([A-Z]+):', sources)
                    ontology_prefixes.extend(matches)
    
    return ontology_prefixes


def create_chart(prefix_counts, output_file):
    """Create and save the bar chart."""
    # Get all prefixes sorted by count
    sorted_prefixes = prefix_counts.most_common()
    
    # Extract data for plotting
    prefixes = [item[0] for item in sorted_prefixes]
    counts = [item[1] for item in sorted_prefixes]
    
    # Create bar chart
    plt.figure(figsize=(14, 8))
    bars = plt.bar(range(len(prefixes)), counts, color='#4B0082', 
                   edgecolor='#2E0854', linewidth=1.2)
    plt.xticks(range(len(prefixes)), prefixes, rotation=45, ha='right', fontsize=20)
    plt.ylabel('Number of Terms', fontsize=22, fontweight='bold')
    plt.xlabel('Ontology Prefix', fontsize=22, fontweight='bold')
    plt.title('Distribution of Ontology Support for Definitions\n(Combined Curators 4, 5, 6 - 94 Terms)', 
              fontsize=24, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add count labels on top of bars
    for i, count in enumerate(counts):
        plt.text(i, count + 0.3, str(count), ha='center', va='bottom', 
                fontsize=18, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f'✅ Chart saved to: {output_file}')
    
    return sorted_prefixes


def print_summary(prefix_counts):
    """Print summary statistics."""
    sorted_prefixes = prefix_counts.most_common()
    
    print('\nOntology Prefix Distribution:')
    print('=' * 60)
    for i, (prefix, count) in enumerate(sorted_prefixes, 1):
        print(f'{i:2d}. {prefix:15s}: {count:3d} occurrences')
    print('=' * 60)
    print(f'\nTotal unique ontology prefixes: {len(prefix_counts)}')
    print(f'Total ontology references: {sum(prefix_counts.values())}')


def main():
    """Main execution function."""
    # Default file paths
    default_input = 'outputs/final/combined_curators_4_5_6.tsv'
    default_output = 'outputs/final/ontology_prefix_distribution.png'
    
    # Parse command line arguments
    input_file = sys.argv[1] if len(sys.argv) > 1 else default_input
    output_file = sys.argv[2] if len(sys.argv) > 2 else default_output
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f'❌ Error: Input file not found: {input_file}')
        sys.exit(1)
    
    # Extract ontology prefixes
    print(f'📖 Reading TSV from: {input_file}')
    ontology_prefixes = extract_ontology_prefixes(input_file)
    
    # Count frequencies
    prefix_counts = Counter(ontology_prefixes)
    
    # Create chart
    print(f'📊 Creating chart...')
    create_chart(prefix_counts, output_file)
    
    # Print summary
    print_summary(prefix_counts)


if __name__ == '__main__':
    main()
