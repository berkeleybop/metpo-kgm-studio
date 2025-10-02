"""Split Google Sheets ROBOT template into overlapping curator assignments.

This module fetches a ROBOT template from Google Sheets and splits it into
multiple TSV files for different curators, with configurable overlap for
inter-curator agreement assessment.

Follows OBO Foundry principles and ROBOT template conventions.
"""

from pathlib import Path
from typing import List, Optional
import csv
import random
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobotTemplateRow:
    """Represents a row from a ROBOT template."""

    def __init__(self, data: dict):
        self.data = data
        self.class_id = data.get('ID', '')

    def is_header_row(self) -> bool:
        """Check if this is a ROBOT header row.

        ROBOT headers contain markers like:
        - Columns starting with '>' (e.g., '>A', '>ID')
        - Special values: 'A', 'AI', 'SPLIT=|', 'SC %', 'TYPE'
        - Column names: 'ID', 'LABEL' (first row)
        """
        # Check if any value in the row has ROBOT markers
        robot_markers = ['>', 'A ', 'AI ', 'SPLIT=|', 'SC %', 'TYPE', 'LABEL']
        values = [str(v) for v in self.data.values()]

        # First row often has: ID, LABEL, TYPE, etc.
        # Second row has: ID, LABEL, TYPE, SC %, A IAO:..., >A IAO:..., etc.
        has_markers = any(
            any(marker in str(v) for marker in robot_markers)
            for v in values
        )

        # Also check if first value is exactly 'ID' (common first header)
        first_value = next(iter(self.data.values())) if self.data else ''
        is_id_row = str(first_value).strip() == 'ID'

        return has_markers or is_id_row


def fetch_google_sheet_as_tsv(sheet_id: str, gid: str) -> str:
    """Fetch a Google Sheet as TSV text.

    Args:
        sheet_id: The Google Sheet ID from the URL
        gid: The GID of the specific sheet/tab

    Returns:
        TSV content as string

    Raises:
        requests.HTTPError: If the sheet cannot be fetched
    """
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=tsv&gid={gid}"
    logger.info(f"Fetching Google Sheet: {sheet_id} (gid={gid})")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    logger.info(f"Successfully fetched {len(response.text)} bytes")
    return response.text


def parse_robot_template(tsv_content: str) -> tuple[List[dict], List[str]]:
    """Parse ROBOT template TSV content.

    Args:
        tsv_content: TSV content as string

    Returns:
        Tuple of (header_rows, data_rows) where:
        - header_rows: List of header row dicts (typically first 2 rows)
        - data_rows: List of data row dicts (class definitions)
    """
    reader = csv.DictReader(tsv_content.splitlines(), delimiter='\t')
    rows = list(reader)

    # Identify header rows (first rows that start with > or special markers)
    header_rows = []
    data_rows = []

    for row in rows:
        robot_row = RobotTemplateRow(row)
        if robot_row.is_header_row() and len(header_rows) < 2:
            header_rows.append(row)
        elif not robot_row.is_header_row():
            # Only include rows with actual class IDs
            if robot_row.class_id and robot_row.class_id.strip():
                data_rows.append(row)

    logger.info(f"Parsed {len(header_rows)} header rows and {len(data_rows)} data rows")
    return header_rows, data_rows


def create_overlapping_subsets(
    items: List[any],
    num_subsets: int,
    overlap_percentage: int = 10,
    randomize: bool = True
) -> List[List[any]]:
    """Create overlapping subsets for inter-curator agreement.

    Args:
        items: List of items to split
        num_subsets: Number of subsets to create
        overlap_percentage: Percentage of overlap between subsets (0-50)
        randomize: Whether to randomize before splitting

    Returns:
        List of subsets, each containing items
    """
    if num_subsets < 1:
        raise ValueError("num_subsets must be at least 1")

    if overlap_percentage < 0 or overlap_percentage > 50:
        raise ValueError("overlap_percentage must be between 0 and 50")

    items_copy = items.copy()
    if randomize:
        random.shuffle(items_copy)

    total_items = len(items_copy)
    base_size = total_items // num_subsets
    overlap_size = int(base_size * (overlap_percentage / 100))

    subsets = []
    for i in range(num_subsets):
        start_idx = i * base_size - (overlap_size if i > 0 else 0)
        end_idx = min((i + 1) * base_size + overlap_size, total_items)

        # Ensure last subset gets any remaining items
        if i == num_subsets - 1:
            end_idx = total_items

        subset = items_copy[start_idx:end_idx]
        subsets.append(subset)
        logger.info(f"Subset {i+1}: {len(subset)} items (indices {start_idx}-{end_idx})")

    return subsets


def write_robot_template_tsv(
    filepath: Path,
    header_rows: List[dict],
    data_rows: List[dict],
    fieldnames: Optional[List[str]] = None
) -> None:
    """Write ROBOT template to TSV file.

    Args:
        filepath: Output file path
        header_rows: List of header row dicts
        data_rows: List of data row dicts
        fieldnames: Column names (defaults to header_rows[0] keys)
    """
    if not fieldnames and header_rows:
        fieldnames = list(header_rows[0].keys())

    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')

        # Write column headers
        writer.writeheader()

        # Write ROBOT header rows
        for row in header_rows:
            writer.writerow(row)

        # Write data rows
        for row in data_rows:
            writer.writerow(row)

    logger.info(f"Wrote {len(data_rows)} rows to {filepath}")


def split_assignments(
    sheet_id: str,
    gid: str,
    output_dir: Path,
    num_curators: int = 3,
    overlap_percentage: int = 10,
    curator_names: Optional[List[str]] = None
) -> List[Path]:
    """Fetch Google Sheet and split into curator assignments.

    Args:
        sheet_id: Google Sheet ID
        gid: Google Sheet tab GID
        output_dir: Directory to write assignment files
        num_curators: Number of curator assignment files to create
        overlap_percentage: Overlap percentage for agreement assessment
        curator_names: Optional list of curator names for filenames

    Returns:
        List of output file paths
    """
    # Fetch and parse
    tsv_content = fetch_google_sheet_as_tsv(sheet_id, gid)
    header_rows, data_rows = parse_robot_template(tsv_content)

    if not header_rows:
        raise ValueError("No ROBOT header rows found in template")

    # Create overlapping subsets
    subsets = create_overlapping_subsets(
        data_rows,
        num_curators,
        overlap_percentage,
        randomize=True
    )

    # Generate curator names if not provided
    if not curator_names:
        curator_names = [f"curator{i+1}" for i in range(num_curators)]

    # Write files
    output_files = []
    fieldnames = list(header_rows[0].keys()) if header_rows else None

    for i, (subset, curator_name) in enumerate(zip(subsets, curator_names)):
        output_file = output_dir / f"{curator_name}.tsv"
        write_robot_template_tsv(output_file, header_rows, subset, fieldnames)
        output_files.append(output_file)

    logger.info(f"Created {len(output_files)} assignment files in {output_dir}")
    return output_files


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < 3:
        print("Usage: python splitter.py <sheet_id> <gid> [output_dir]")
        sys.exit(1)

    sheet_id = sys.argv[1]
    gid = sys.argv[2]
    output_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("assignments")

    split_assignments(sheet_id, gid, output_dir)
