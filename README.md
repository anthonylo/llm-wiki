# LLM Wiki

An auto-evolving wiki generation system that ingests structured documents and generates markdown wiki pages using Claude.

The project is designed to:
- convert CSV, TSV, Excel, JSON, and PDF files into linked wiki pages
- validate factual fidelity and consistency before writing pages
- discover related topics and cross-link pages automatically
- persist processing state in `.wiki_store`

## Ingest Mechanism Examples

### Prompt 1

`For each key concept in the pdfs in /inbox, create a markdown in /wiki with a summary, explanation, related links using [[brackets]], and note any contradictions between the papers.`

### Prompt 2

`For each key concept within each pdf in /inbox, create a markdown in /wiki/beer with a summary, explanation, related links using [[brackets]], and note any contradictions between the papers.`

### Prompt 3

`Can you go through the processed AI pdfs again to see if you're not missing anything? Also, please add a section to the iNDEX to identify what pages are linked to the PDFs, add instructinos to add this information going forward.`

## Key features

- `wiki ingest <file>`: ingest a source file and generate wiki pages
- `wiki watch`: monitor an inbox directory for new source files and auto-ingest them
- deduplication with SHA-256 hashing
- embeddings + ChromaDB for semantic related page discovery
- configurable settings via `.env`

## Supported input formats

- `.csv`
- `.tsv`
- `.xlsx`
- `.xls`
- `.json`
- `.pdf`

## Setup

```bash
cd /Users/anthonylo/Projects/llm-wiki
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

Copy the example environment file:

```bash
cp .env.example .env
```

Then add your Anthropic API key to `.env`:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

### Ingest a file

```bash
wiki ingest inbox/VikingMalt_BeerMaltHandbook_Online-1.pdf
```

Force re-ingest of an already processed file:

```bash
wiki ingest inbox/file.csv --force
```

### Watch the inbox directory

```bash
wiki watch
```

Or specify a custom inbox directory:

```bash
wiki watch --inbox inbox
```

Drop supported files into the watched inbox directory and they will be processed automatically.

## Output

Generated wiki pages are written to `wiki/`.

Other important directories:

- `processed/`: archived source files after ingestion
- `.wiki_store/`: internal storage for deduplication, embeddings, and metadata

## Configuration

Environment variables are defined in `.env` and include:

- `ANTHROPIC_API_KEY`
- `WIKI_DIR`
- `INBOX_DIR`
- `STORE_DIR`
- `GENERATION_MODEL`
- `VALIDATION_MODEL`
- `LINKING_MODEL`
- `MAX_ROWS_PER_PROMPT`
- `ARCHIVE_DIR`

Defaults are shown in `.env.example`.

### Convert Excel to wiki markdown

```bash
wiki excel-to-markdown path/to/workbook.xlsx
```

This command writes a markdown summary page under `wiki/excel/`.

For a repository-local skill, use the `.github/excel_to_markdown` agent skill:

```bash
python .github/excel_to_markdown/main.py path/to/workbook.xlsx
```
### Convert CSV to wiki markdown

```bash
wiki csv-to-markdown path/to/data.csv
```

This command writes one markdown page per row under `wiki/csv/`.

For a repository-local skill, use the `.github/csv_to_markdown` agent skill:

```bash
python .github/csv_to_markdown/main.py path/to/data.csv
```
## Testing

```bash
pytest tests/
```

## Project structure

- `wiki_engine/cli.py` — Typer CLI entrypoint
- `wiki_engine/pipeline.py` — central ingestion and generation pipeline
- `wiki_engine/config.py` — settings and environment config
- `wiki_engine/watcher.py` — inbox directory monitor
- `wiki_engine/ingest/` — file adapters for CSV, Excel, JSON, PDF
- `wiki_engine/llm/` — generator, validator, and linker logic
- `wiki_engine/embeddings/` — embedding generation and ChromaDB storage
- `wiki_engine/wiki/` — page writer, index, and changelog management

## Notes

This repository is intended for generating and maintaining a machine-readable wiki from source documents. It is not a general-purpose CMS or page editor.