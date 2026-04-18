# Excel-to-Markdown Agent Skill

This local skill is a repository-backed tool for converting Excel workbooks into markdown wiki pages.

## Run

```bash
python .github/excel_to_markdown/main.py path/to/workbook.xlsx
```

## Options

- `--sheet`: export only a specific worksheet
- `--output-dir`: write output to a custom wiki directory

## Requirements

- Run from the repository root
- Install dependencies with `pip install -e .`
