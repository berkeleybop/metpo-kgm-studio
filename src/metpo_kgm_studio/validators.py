"""Validators for ontology definitions following OBO Foundry principles.

This module provides validators to check definition quality, including:
- Genus-differentia form checking
- Definition source validation
- Naming convention compliance (FP-012)
- General quality checks

References:
- FP-006: https://obofoundry.org/principles/fp-006-textual-definitions.html
- FP-012: https://obofoundry.org/principles/fp-012-naming-conventions.html
"""

from dataclasses import dataclass
from typing import List, Optional, Pattern
import re
from pathlib import Path

# Common problematic patterns in definitions
CIRCULAR_PATTERNS = [
    r"is a \w+ that is",  # "X is a process that is X"
]

# Patterns that suggest poor genus-differentia form
POOR_GENUS_DIFFERENTIA = [
    r"^A[n]?\s+\w+\s+(process|activity|pathway|system|function)\s+that",  # Too generic
    r"^The\s+",  # Starts with "The"
]

# Valid source identifier patterns
SOURCE_PATTERNS = {
    'pmid': re.compile(r'^PMID:\d+$', re.IGNORECASE),
    'doi': re.compile(r'^DOI:10\.\d+/\S+$', re.IGNORECASE),
    'isbn': re.compile(r'^ISBN:[\d\-]+$', re.IGNORECASE),
    'url': re.compile(r'^https?://\S+$', re.IGNORECASE),
}


@dataclass
class ValidationResult:
    """Result of a validation check."""
    passed: bool
    message: str
    severity: str = "error"  # "error", "warning", "info"
    field: Optional[str] = None

    def __str__(self) -> str:
        prefix = "✓" if self.passed else "✗"
        severity_marker = "" if self.severity == "error" else f" [{self.severity.upper()}]"
        field_info = f" ({self.field})" if self.field else ""
        return f"{prefix}{severity_marker}{field_info}: {self.message}"


class DefinitionValidator:
    """Validator for ontology class definitions."""

    def __init__(self):
        self.results: List[ValidationResult] = []

    def validate_all(
        self,
        definition: str,
        class_id: str,
        class_label: str,
        sources: Optional[List[str]] = None
    ) -> List[ValidationResult]:
        """Run all validation checks on a definition.

        Args:
            definition: The textual definition
            class_id: Ontology class ID (e.g., METPO:1234567)
            class_label: Human-readable label
            sources: List of definition sources

        Returns:
            List of validation results
        """
        self.results = []

        # Required field checks
        self.check_definition_exists(definition)
        self.check_class_id_format(class_id)
        self.check_label_exists(class_label)

        if definition:
            # Definition quality checks
            self.check_definition_length(definition)
            self.check_starts_with_article(definition, class_label)
            self.check_circularity(definition, class_label)
            self.check_genus_differentia_form(definition)
            self.check_special_characters(definition)

        if sources:
            self.check_sources(sources)

        return self.results

    def check_definition_exists(self, definition: str) -> None:
        """Check if definition is provided and non-empty."""
        if not definition or not definition.strip():
            self.results.append(ValidationResult(
                passed=False,
                message="Definition is required but missing or empty",
                severity="error",
                field="definition"
            ))
        else:
            self.results.append(ValidationResult(
                passed=True,
                message="Definition is present",
                severity="info",
                field="definition"
            ))

    def check_definition_length(self, definition: str, min_length: int = 20, max_length: int = 500) -> None:
        """Check if definition is within reasonable length bounds."""
        length = len(definition.strip())

        if length < min_length:
            self.results.append(ValidationResult(
                passed=False,
                message=f"Definition too short ({length} chars, minimum {min_length})",
                severity="warning",
                field="definition"
            ))
        elif length > max_length:
            self.results.append(ValidationResult(
                passed=False,
                message=f"Definition too long ({length} chars, maximum {max_length})",
                severity="warning",
                field="definition"
            ))
        else:
            self.results.append(ValidationResult(
                passed=True,
                message=f"Definition length appropriate ({length} chars)",
                severity="info",
                field="definition"
            ))

    def check_starts_with_article(self, definition: str, class_label: str) -> None:
        """Check if definition avoids starting with 'A/An [class_label]'."""
        # Pattern: "A/An <class_label>"
        label_words = class_label.lower().split()
        definition_lower = definition.lower().strip()

        # Check if starts with "A/An <first word of label>"
        if label_words and definition_lower.startswith(f"a {label_words[0]}"):
            self.results.append(ValidationResult(
                passed=False,
                message=f"Definition should not start with 'A {label_words[0]}' (avoid article + class name)",
                severity="warning",
                field="definition"
            ))
        elif label_words and definition_lower.startswith(f"an {label_words[0]}"):
            self.results.append(ValidationResult(
                passed=False,
                message=f"Definition should not start with 'An {label_words[0]}' (avoid article + class name)",
                severity="warning",
                field="definition"
            ))
        else:
            self.results.append(ValidationResult(
                passed=True,
                message="Definition does not start with article + class name",
                severity="info",
                field="definition"
            ))

    def check_circularity(self, definition: str, class_label: str) -> None:
        """Check for circular definitions."""
        definition_lower = definition.lower()
        label_lower = class_label.lower()

        # Check if label appears in definition (excluding parent class references)
        if label_lower in definition_lower:
            self.results.append(ValidationResult(
                passed=False,
                message=f"Definition may be circular - contains class label '{class_label}'",
                severity="warning",
                field="definition"
            ))
        else:
            self.results.append(ValidationResult(
                passed=True,
                message="No obvious circular definition detected",
                severity="info",
                field="definition"
            ))

    def check_genus_differentia_form(self, definition: str) -> None:
        """Check if definition follows genus-differentia form."""
        # Look for "A/An [parent] that [differentia]"
        genus_diff_pattern = r'^An?\s+\w+(\s+\w+)*\s+that\s+\w+'

        if re.match(genus_diff_pattern, definition):
            self.results.append(ValidationResult(
                passed=True,
                message="Definition appears to follow genus-differentia form",
                severity="info",
                field="definition"
            ))
        else:
            self.results.append(ValidationResult(
                passed=False,
                message="Definition may not follow genus-differentia form (should be 'An [parent] that [characteristics]')",
                severity="warning",
                field="definition"
            ))

    def check_special_characters(self, definition: str) -> None:
        """Check for problematic special characters or formatting."""
        issues = []

        if definition.startswith(' ') or definition.endswith(' '):
            issues.append("has leading/trailing whitespace")

        if '  ' in definition:
            issues.append("contains double spaces")

        if not definition.endswith('.'):
            issues.append("does not end with period")

        if issues:
            self.results.append(ValidationResult(
                passed=False,
                message=f"Formatting issues: {', '.join(issues)}",
                severity="warning",
                field="definition"
            ))
        else:
            self.results.append(ValidationResult(
                passed=True,
                message="No formatting issues detected",
                severity="info",
                field="definition"
            ))

    def check_class_id_format(self, class_id: str) -> None:
        """Check if class ID follows expected format."""
        # Expected format: PREFIX:1234567
        id_pattern = r'^[A-Z]+:\d+$'

        if re.match(id_pattern, class_id):
            self.results.append(ValidationResult(
                passed=True,
                message=f"Class ID format valid: {class_id}",
                severity="info",
                field="class_id"
            ))
        else:
            self.results.append(ValidationResult(
                passed=False,
                message=f"Class ID format invalid: {class_id} (expected PREFIX:1234567)",
                severity="error",
                field="class_id"
            ))

    def check_label_exists(self, class_label: str) -> None:
        """Check if class label is provided."""
        if not class_label or not class_label.strip():
            self.results.append(ValidationResult(
                passed=False,
                message="Class label is required but missing",
                severity="error",
                field="class_label"
            ))
        else:
            self.results.append(ValidationResult(
                passed=True,
                message="Class label is present",
                severity="info",
                field="class_label"
            ))

    def check_sources(self, sources: List[str]) -> None:
        """Validate definition sources."""
        if not sources:
            self.results.append(ValidationResult(
                passed=False,
                message="No definition sources provided (at least one required)",
                severity="error",
                field="sources"
            ))
            return

        valid_sources = 0
        for source in sources:
            source_valid = False
            for _source_type, pattern in SOURCE_PATTERNS.items():
                if pattern.match(source):
                    source_valid = True
                    valid_sources += 1
                    break

            if not source_valid:
                self.results.append(ValidationResult(
                    passed=False,
                    message=f"Invalid source format: {source} (expected PMID:, DOI:, ISBN:, or URL)",
                    severity="error",
                    field="sources"
                ))

        if valid_sources > 0:
            self.results.append(ValidationResult(
                passed=True,
                message=f"{valid_sources} valid source(s) found",
                severity="info",
                field="sources"
            ))


class LabelValidator:
    """Validator for class label naming conventions (FP-012)."""

    def __init__(self):
        self.results: List[ValidationResult] = []

    def validate_label_case(self, label: str) -> List[ValidationResult]:
        """Check label follows lowercase convention for multi-word terms.

        OBO Foundry FP-012: Labels should be lowercase except for proper nouns
        and acronyms.

        Args:
            label: The class label to validate

        Returns:
            List of validation results
        """
        self.results = []

        # Check if label is all lowercase (allowing for proper nouns/acronyms)
        words = label.split()

        uppercase_words = [w for w in words if w[0].isupper() and len(w) > 1]

        if uppercase_words and not all(w.isupper() for w in uppercase_words):
            # Has capitalized words that aren't acronyms
            self.results.append(ValidationResult(
                passed=False,
                message=f"Label may violate FP-012 case convention: '{label}'. Check if capitalized words are proper nouns.",
                severity="warning",
                field="class_label"
            ))
        else:
            self.results.append(ValidationResult(
                passed=True,
                message="Label case follows FP-012 convention",
                severity="info",
                field="class_label"
            ))

        return self.results


def validate_definition_file(
    tsv_path: Path,
    id_column: str = "ID",
    label_column: str = "LABEL",
    definition_column: str = "A definition",
    source_column: str = "A definition source"
) -> dict:
    """Validate all definitions in a ROBOT template TSV file.

    Args:
        tsv_path: Path to TSV file
        id_column: Name of ID column
        label_column: Name of label column
        definition_column: Name of definition column
        source_column: Name of source column

    Returns:
        Dictionary with validation results and statistics
    """
    import csv

    results = {
        'total_rows': 0,
        'validated_rows': 0,
        'errors': 0,
        'warnings': 0,
        'row_results': []
    }

    with open(tsv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')

        for i, row in enumerate(reader, 1):
            # Skip ROBOT header rows
            if row.get(id_column, '').startswith('>'):
                continue

            results['total_rows'] += 1

            class_id = row.get(id_column, '')
            class_label = row.get(label_column, '')
            definition = row.get(definition_column, '')
            sources = row.get(source_column, '').split('|') if row.get(source_column) else []

            validator = DefinitionValidator()
            validation_results = validator.validate_all(definition, class_id, class_label, sources)

            label_validator = LabelValidator()
            validation_results.extend(label_validator.validate_label_case(class_label))

            # Count errors and warnings
            row_errors = sum(1 for r in validation_results if not r.passed and r.severity == "error")
            row_warnings = sum(1 for r in validation_results if not r.passed and r.severity == "warning")

            results['errors'] += row_errors
            results['warnings'] += row_warnings
            results['validated_rows'] += 1

            results['row_results'].append({
                'row': i,
                'class_id': class_id,
                'class_label': class_label,
                'results': validation_results,
                'errors': row_errors,
                'warnings': row_warnings
            })

    return results


if __name__ == "__main__":
    # Example usage
    validator = DefinitionValidator()
    results = validator.validate_all(
        definition="A cellular respiration process that occurs without oxygen.",
        class_id="METPO:0000123",
        class_label="anaerobic respiration",
        sources=["PMID:12345678", "DOI:10.1234/example"]
    )

    for result in results:
        print(result)
