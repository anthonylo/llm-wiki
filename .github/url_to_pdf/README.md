# url-to-pdf

Download any web URL as a PDF into the `inbox/` directory.

## Quick start

```bash
# Via the wiki CLI (recommended)
uv run wiki url-to-pdf https://arxiv.org/pdf/2305.10601

# Via the standalone script
uv run python .github/url_to_pdf/main.py https://arxiv.org/pdf/2305.10601

# Specify a custom inbox directory
uv run wiki url-to-pdf https://example.com/docs --inbox-dir /tmp/inbox
```

## How it works

1. Issues a HEAD request to detect `Content-Type`.
2. If the server returns `application/pdf`, the file is downloaded directly (fast, no browser needed).
3. Otherwise, playwright launches headless Chromium, navigates to the URL, waits for the network to settle, and prints to A4 PDF.

## First-time setup

```bash
uv add playwright requests
uv run playwright install chromium
```

## Output

The PDF is saved to `inbox/<derived-filename>.pdf`. The filename is taken from the URL path when it ends in `.pdf`; otherwise it is slugified from the domain + path.
