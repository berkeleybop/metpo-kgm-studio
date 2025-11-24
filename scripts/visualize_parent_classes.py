#!/usr/bin/env python3
"""
Visualize Parent Class Distribution

Generates a horizontal bar chart showing the distribution of parent classes
across the METPO definitions in the combined curator TSV file.

Usage:
    python scripts/visualize_parent_classes.py [input_tsv] [output_png]

Default:
    python scripts/visualize_parent_classes.py
    # Uses: outputs/final/combined_curators_4_5_6.tsv
    # Saves to: outputs/final/parent_class_distribution.png
"""

import sys
import re
from collections import Counter, defaultdict
from pathlib import Path
import matplotlib.pyplot as plt


def extract_parent_classes_with_ontologies(tsv_file, top_n=None):
    """Extract parent classes and their most dominant ontology prefix."""
    parent_classes = []
    parent_to_ontologies = defaultdict(lambda: Counter())
    
    with open(tsv_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        # Skip the two header rows
        for line in lines[2:]:
            parts = line.strip().split('\t')
            if parts and parts[0].startswith('METPO:') and len(parts) > 3:
                parent_class = parts[3]  # Column 4 is parent class
                if parent_class:
                    parent_classes.append(parent_class)
                    
                    # Extract ontology prefixes from sources (column 6)
                    if len(parts) > 5:
                        sources = parts[5]
                        if sources:
                            ontology_matches = re.findall(r'([A-Z]+):', sources)
                            for onto in ontology_matches:
                                parent_to_ontologies[parent_class][onto] += 1
    
    # Count frequencies
    parent_counts = Counter(parent_classes)
    
    # Get top N if specified, otherwise all
    if top_n:
        top_parents = parent_counts.most_common(top_n)
    else:
        top_parents = parent_counts.most_common()
    
    # Add most dominant ontology to parent data
    parent_data_with_ontologies = []
    for parent, count in top_parents:
        # Get the most common ontology for this parent class
        if parent_to_ontologies[parent]:
            dominant_ontology = parent_to_ontologies[parent].most_common(1)[0][0]
        else:
            dominant_ontology = None
        parent_data_with_ontologies.append((parent, count, dominant_ontology))
    
    return parent_data_with_ontologies


def create_chart(parent_data, output_file):
    """Create and save the horizontal bar chart with ontology labels."""
    # Reverse order so highest is at top
    parent_classes = [item[0] for item in reversed(parent_data)]
    counts = [item[1] for item in reversed(parent_data)]
    ontologies = [item[2] for item in reversed(parent_data)]
    
    # Create horizontal bar chart
    plt.figure(figsize=(14, 8))
    bars = plt.barh(range(len(parent_classes)), counts, color='steelblue', 
                    edgecolor='navy', linewidth=1.2)
    plt.yticks(range(len(parent_classes)), parent_classes, fontsize=20)
    plt.xlabel('Number of Terms', fontsize=22, fontweight='bold')
    plt.ylabel('Parent Class', fontsize=22, fontweight='bold')
    plt.title('Distribution of Parent Classes\n(Combined Curators 4, 5, 6 - 94 Terms)', 
              fontsize=24, fontweight='bold')
    plt.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add ontology labels inside bars and count labels outside
    for i, (count, ontology) in enumerate(zip(counts, ontologies)):
        # Ontology label inside the bar (white text) - only the most dominant one
        if ontology:
            plt.text(count * 0.5, i, ontology, va='center', ha='center',
                    fontsize=24, fontweight='bold', color='white')
        
        # Count label outside the bar
        plt.text(count + 0.3, i, str(count), va='center', fontsize=18, 
                fontweight='bold', color='black')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f'✅ Chart saved to: {output_file}')


def print_summary(parent_data, total_terms):
    """Print summary statistics."""
    print('\nParent Class Distribution:')
    print('=' * 60)
    for i, (parent, count) in enumerate(parent_data, 1):
        percentage = (count / total_terms) * 100
        print(f'{i}. {parent:30s}: {count:2d} terms ({percentage:5.1f}%)')
    print('=' * 60)
    total_shown = sum(count for _, count in parent_data)
    print(f'\nTotal terms shown: {total_shown}')
    print(f'Total unique parent classes: {len(parent_data)}')


def main():
    """Main execution function."""
    # Default file paths
    default_input = 'outputs/final/combined_curators_4_5_6.tsv'
    default_output = 'outputs/final/parent_class_distribution.png'
    
    # Parse command line arguments
    input_file = sys.argv[1] if len(sys.argv) > 1 else default_input
    output_file = sys.argv[2] if len(sys.argv) > 2 else default_output
    top_n = int(sys.argv[3]) if len(sys.argv) > 3 else 6  # Default to top 6
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f'❌ Error: Input file not found: {input_file}')
        sys.exit(1)
    
    # Extract parent classes with ontologies
    print(f'📖 Reading TSV from: {input_file}')
    parent_data = extract_parent_classes_with_ontologies(input_file, top_n=top_n)
    
    # Calculate total for percentages
    total_terms = sum(count for _, count, _ in parent_data)
    
    # Create chart
    print(f'📊 Creating chart for top {len(parent_data)} parent classes...')
    create_chart(parent_data, output_file)
    
    # Print summary (extract just parent and count for print_summary)
    parent_count_data = [(parent, count) for parent, count, _ in parent_data]
    print_summary(parent_count_data, total_terms)


if __name__ == '__main__':
    main()
