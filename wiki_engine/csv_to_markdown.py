from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Any, List


def _slugify(text: str) -> str:
    import re
    text = text.strip().lower().replace(" ", "-")
    text = re.sub(r"[^a-z0-9\-]", "", text)
    return text or "entry"


def _format_row_markdown(row: Dict[str, Any], csv_path: Path, row_number: int) -> str:
    """Generate markdown content for a single CSV row."""
    # Use first column as identifier
    identifier = str(row[list(row.keys())[0]])
    title = identifier
    
    # Tags: csv + identifier slug
    tags = ["csv", _slugify(identifier)]
    
    sources = [csv_path.name]
    
    # Summary: basic description
    name_field = row.get("name", identifier)
    summary = f"This entry describes {name_field}."
    
    # Data Points section
    data_points = []
    for key, value in row.items():
        data_points.append(f"- **{key}**: {value}")
    
    content_lines = [
        "---",
        f"title: {title}",
        f"tags: [{', '.join(tags)}]",
        f"sources: {sources}",
        f"row number: {row_number}",
        "---",
        "",
        "## Summary",
        "",
        summary,
        "",
        "## Data Points",
        "",
        "\n".join(data_points),
    ]
    
    return "\n".join(content_lines).strip() + "\n"


def dump_csv_to_markdown(file_path: Path, wiki_dir: Path) -> List[Path]:
    """Read a CSV file and write markdown pages for each row."""
    output_paths = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=1):
            # Skip empty rows
            if not any(row.values()):
                continue
            
            identifier = str(row[list(row.keys())[0]])
            slug = _slugify(identifier)
            
            content = _format_row_markdown(row, file_path, row_num)
            
            output_dir = wiki_dir / "csv"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{slug}.md"
            output_path.write_text(content, encoding="utf-8")
            
            output_paths.append(output_path)
    
    return output_paths