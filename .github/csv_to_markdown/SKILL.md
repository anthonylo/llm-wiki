---
name: csv-to-markdown
description: "Convert a CSV file into markdown wiki pages, creating one page per row."
---

This local skill converts `.csv` files into wiki-ready markdown pages under `wiki/csv/`, with one page generated for each data row.

## Usage

- `python .github/csv_to_markdown/main.py path/to/data.csv`
- `python .github/csv_to_markdown/main.py path/to/data.csv --output-dir wiki/`

## Notes

- If `--output-dir` is omitted, the skill uses `WIKI_DIR` from `.env` or the default `wiki/` directory.
- Run from the repository root so Python can import `wiki_engine`.
- Requires the repository dependencies installed in the active Python environment.
- Each row becomes a separate markdown page, using the first column value as the identifier.
