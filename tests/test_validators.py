"""Tests for definition validators."""

import pytest
from metpo_kgm_studio.validators import (
    DefinitionValidator,
    LabelValidator,
    ValidationResult,
)


class TestDefinitionValidator:
    """Tests for DefinitionValidator class."""

    def test_definition_exists(self) -> None:
        """Test that validator detects missing definitions."""
        validator = DefinitionValidator()
        validator.check_definition_exists("")

        assert len(validator.results) == 1
        assert not validator.results[0].passed
        assert validator.results[0].severity == "error"

    def test_definition_length_valid(self) -> None:
        """Test that validator accepts appropriate definition lengths."""
        validator = DefinitionValidator()
        definition = "A cellular respiration process that occurs without oxygen."
        validator.check_definition_length(definition)

        assert len(validator.results) == 1
        assert validator.results[0].passed

    def test_definition_length_too_short(self) -> None:
        """Test that validator flags very short definitions."""
        validator = DefinitionValidator()
        validator.check_definition_length("Too short", min_length=20)

        assert len(validator.results) == 1
        assert not validator.results[0].passed
        assert validator.results[0].severity == "warning"

    def test_starts_with_article_detection(self) -> None:
        """Test detection of definitions starting with article + class name."""
        validator = DefinitionValidator()
        validator.check_starts_with_article(
            "A methanogenesis process that produces methane",
            "methanogenesis"
        )

        assert len(validator.results) == 1
        assert not validator.results[0].passed

    def test_genus_differentia_form_valid(self) -> None:
        """Test recognition of valid genus-differentia form."""
        validator = DefinitionValidator()
        definition = "An anaerobic process that produces methane."
        validator.check_genus_differentia_form(definition)

        assert len(validator.results) == 1
        assert validator.results[0].passed

    def test_class_id_format_valid(self) -> None:
        """Test validation of class ID format."""
        validator = DefinitionValidator()
        validator.check_class_id_format("METPO:0000123")

        assert len(validator.results) == 1
        assert validator.results[0].passed

    def test_class_id_format_invalid(self) -> None:
        """Test detection of invalid class ID format."""
        validator = DefinitionValidator()
        validator.check_class_id_format("invalid-id")

        assert len(validator.results) == 1
        assert not validator.results[0].passed

    def test_sources_valid_pmid(self) -> None:
        """Test validation of PMID sources."""
        validator = DefinitionValidator()
        validator.check_sources(["PMID:12345678"])

        # Should have one valid source result
        valid_results = [r for r in validator.results if r.passed]
        assert len(valid_results) > 0

    def test_sources_invalid_format(self) -> None:
        """Test detection of invalid source format."""
        validator = DefinitionValidator()
        validator.check_sources(["invalid source"])

        # Should have error for invalid format
        error_results = [r for r in validator.results if not r.passed and r.severity == "error"]
        assert len(error_results) > 0

    def test_validate_all_integration(self) -> None:
        """Integration test for complete validation."""
        validator = DefinitionValidator()
        results = validator.validate_all(
            definition="An anaerobic respiration process that produces methane.",
            class_id="METPO:0000123",
            class_label="methanogenesis",
            sources=["PMID:12345678", "DOI:10.1234/example"]
        )

        assert len(results) > 0
        # Should have mix of passed and potentially some warnings
        assert any(r.passed for r in results)


class TestLabelValidator:
    """Tests for LabelValidator class."""

    def test_label_case_lowercase_valid(self) -> None:
        """Test that lowercase labels pass validation."""
        validator = LabelValidator()
        results = validator.validate_label_case("anaerobic respiration")

        assert len(results) == 1
        assert results[0].passed

    def test_label_case_with_acronym(self) -> None:
        """Test that acronyms in labels are accepted."""
        validator = LabelValidator()
        results = validator.validate_label_case("DNA replication")

        assert len(results) == 1
        # This should pass as DNA is an acronym
        assert results[0].passed


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_validation_result_str_passed(self) -> None:
        """Test string representation of passed result."""
        result = ValidationResult(
            passed=True,
            message="Test passed",
            severity="info"
        )

        assert "✓" in str(result)
        assert "Test passed" in str(result)

    def test_validation_result_str_failed(self) -> None:
        """Test string representation of failed result."""
        result = ValidationResult(
            passed=False,
            message="Test failed",
            severity="error"
        )

        assert "✗" in str(result)
        assert "Test failed" in str(result)
