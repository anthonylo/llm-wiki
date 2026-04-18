# CSV-to-Markdown Agent Skill

This local skill is a repository-backed tool for converting CSV files into markdown wiki pages, creating one page per row.

## Run

```bash
python .github/csv_to_markdown/main.py path/to/data.csv
```

## Options

- `--output-dir`: write output to a custom wiki directory

## Requirements

- Run from the repository root
- Install dependencies with `pip install -e .`
