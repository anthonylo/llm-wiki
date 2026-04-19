---
name: url-to-pdf
description: "Download a web URL as a PDF and save it to the inbox directory."
---

This local skill downloads a URL and saves it as a PDF to the `inbox/` directory, ready for wiki ingestion.

## Usage

- `python .github/url_to_pdf/main.py https://example.com/paper`
- `python .github/url_to_pdf/main.py https://arxiv.org/pdf/2305.10601 --inbox-dir inbox/`

## Notes

- If the URL serves a PDF directly (`Content-Type: application/pdf`), it is streamed and saved without any rendering step.
- For HTML pages, a headless Chromium browser (playwright) renders the page to PDF.
- If `--inbox-dir` is omitted, the skill uses `INBOX_DIR` from `.env` or the default `inbox/` directory.
- Run from the repository root so Python can import `wiki_engine`.
- Requires `playwright` and `requests` installed (`uv sync`) and Chromium downloaded (`uv run playwright install chromium`).
