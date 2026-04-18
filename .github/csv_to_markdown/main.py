from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Any

from wiki_engine.config import get_settings


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


def dump_csv_to_markdown(file_path: Path, wiki_dir: Path) -> list[Path]:
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a CSV file into markdown wiki pages (one per row)."
    )
    parser.add_argument("file", type=Path, help="Path to the CSV file to convert")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Optional wiki output directory. Defaults to WIKI_DIR from .env or wiki/.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.file.exists():
        raise SystemExit(f"Error: file not found: {args.file}")

    settings = get_settings()
    wiki_dir = args.output_dir or settings.wiki_dir

    output_paths = dump_csv_to_markdown(args.file, wiki_dir)
    if output_paths:
        print(f"Wrote {len(output_paths)} markdown pages:")
        for path in output_paths:
            print(f"  {path.resolve()}")
    else:
        print("No valid rows found in CSV.")


if __name__ == "__main__":
    main()
