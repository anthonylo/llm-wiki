# LLM Wiki — Developer Guide

## Setup

```bash
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
uv sync
```

## Usage

### Ingest a file
```bash
uv run wiki ingest tests/fixtures/sample.csv
uv run wiki ingest tests/fixtures/sample.xlsx
uv run wiki ingest path/to/data.json
```

### Force re-ingest (bypass deduplication)
```bash
uv run wiki ingest tests/fixtures/sample.csv --force
```

### Watch inbox directory for new files
```bash
uv run wiki watch
# Drop any CSV, TSV, XLSX, XLS, or JSON file into inbox/ to auto-process
```

## Testing

```bash
uv run pytest tests/                    # Run all tests
uv run pytest tests/test_ingest.py      # Run single test file
uv run pytest -v                        # Verbose output
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | *(required)* | Your Anthropic API key |
| `WIKI_DIR` | `wiki` | Output directory for markdown pages |
| `INBOX_DIR` | `inbox` | Watched directory for auto-ingest |
| `STORE_DIR` | `.wiki_store` | Internal state (ChromaDB, hashes) |
| `GENERATION_MODEL` | `claude-opus-4-6` | Model for page generation |
| `VALIDATION_MODEL` | `claude-opus-4-6` | Model for fidelity/consistency checks |
| `LINKING_MODEL` | `claude-haiku-4-5-20251001` | Model for cross-link discovery |
| `MAX_ROWS_PER_PROMPT` | `200` | Max rows sent to LLM per section |

## Architecture

### Data Flow

```
FILE (CLI or inbox/)
      │
      ▼
WikiPipeline.run(file_path)
      │
      ├─ [1] Dedup: SHA-256 hash → .wiki_store/processed/
      ├─ [2] IngestAdapter.parse() → List[SourceSection]
      ├─ [3] MarkdownGenerator.generate() → WikiPage draft
      ├─ [4] WikiValidator.check_fidelity() — regenerate once on fail
      ├─ [5] EmbeddingStore.query_similar() — find related pages
      ├─ [6] WikiValidator.check_consistency() — block on contradiction
      ├─ [7] CrossLinker.find_links() — discover Related Pages
      ├─ [8] WikiWriter.write() → wiki/{slug}.md
      ├─ [9] EmbeddingStore.upsert() — index for future queries
      └─ [10] IndexManager.update() + ChangelogManager.append()
```

### Package Structure

```
wiki_engine/
├── cli.py          # Typer CLI: wiki ingest / wiki watch
├── watcher.py      # Watchdog inbox monitor
├── pipeline.py     # Central orchestrator
├── config.py       # Pydantic Settings
├── ingest/         # CSV, TSV, Excel, JSON adapters
├── llm/            # generator, validator, linker
├── embeddings/     # sentence-transformers + ChromaDB
└── wiki/           # page, writer, index, changelog
```

### Supported File Types

| Extension | Adapter | Sections Generated |
|-----------|---------|-------------------|
| `.csv`, `.tsv` | CSVAdapter | 1 per file |
| `.xlsx`, `.xls` | ExcelAdapter | 1 per non-empty sheet + 1 workbook index |
| `.json` | JSONAdapter | 1 per top-level key (dict) or 1 (array) |

### LLM Models

| Task | Model | Reason |
|------|-------|--------|
| Page generation | `claude-opus-4-6` | Highest quality markdown |
| Fidelity validation | `claude-opus-4-6` | Critical correctness |
| Consistency check | `claude-opus-4-6` | Nuanced contradiction detection |
| Cross-link discovery | `claude-haiku-4-5-20251001` | Cost-sensitive JSON extraction |

### Validation Behavior

- **Fidelity fail**: Regenerate once with feedback → re-check → log `REJECTED` if still fails
- **Consistency fail**: Immediately log `BLOCKED` — human must resolve before re-ingesting
- All validation calls use `temperature=0.0`

### Embeddings

- Model: `all-MiniLM-L6-v2` (sentence-transformers, 384-dim, CPU, ~5ms/doc)
- Store: ChromaDB persisted to `.wiki_store/chroma/` (cosine similarity)
- No external embedding API required

### Output Files

- `wiki/{slug}.md` — Generated wiki pages with YAML front-matter
- `wiki/INDEX.md` — Auto-rebuilt table of all pages
- `wiki/CHANGELOG.md` — Prepended log of all ingest events
- `.wiki_store/processed/` — SHA-256 hashes for deduplication
- `.wiki_store/chroma/` — ChromaDB vector store
