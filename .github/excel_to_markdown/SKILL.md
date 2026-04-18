---
name: excel-to-markdown
description: "Convert an Excel workbook into a markdown wiki page inside the llm-wiki repository."
---

This local skill converts `.xlsx` files into wiki-ready markdown summary pages under `wiki/excel/`.

## Usage

- `python .github/excel_to_markdown/main.py path/to/workbook.xlsx`
- `python .github/excel_to_markdown/main.py path/to/workbook.xlsx --sheet "Sheet1"`
- `python .github/excel_to_markdown/main.py path/to/workbook.xlsx --output-dir wiki/`

## Notes

- If `--output-dir` is omitted, the skill uses `WIKI_DIR` from `.env` or the default `wiki/` directory.
- Use this skill from the repository root so Python can import `wiki_engine`.
- Requires the repository dependencies installed in the active Python environment.
