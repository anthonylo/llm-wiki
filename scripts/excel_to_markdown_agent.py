from __future__ import annotations

import argparse
from pathlib import Path

from wiki_engine.config import get_settings
from wiki_engine.excel_to_markdown import dump_excel_to_markdown


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Local Excel-to-markdown agent for the llm-wiki project."
    )
    parser.add_argument("file", type=Path, help="Path to the Excel workbook to convert")
    parser.add_argument(
        "--sheet",
        type=str,
        default=None,
        help="Optional sheet name to export. If omitted, exports all non-empty sheets.",
    )
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

    output_path = dump_excel_to_markdown(args.file, wiki_dir, sheet_name=args.sheet)
    print(f"Wrote markdown page: {output_path.resolve()}")


if __name__ == "__main__":
    main()
