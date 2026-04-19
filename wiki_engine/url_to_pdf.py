from __future__ import annotations

import re
import urllib.parse
from pathlib import Path


def _url_to_filename(url: str) -> str:
    """Derive a .pdf filename from a URL."""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.rstrip("/")

    if path.endswith(".pdf"):
        name = Path(path).name
    else:
        # Slug from host + path
        combined = (parsed.netloc + path).lower()
        combined = re.sub(r"[^a-z0-9]+", "-", combined).strip("-")
        name = combined[:80] + ".pdf"

    return name


def download_url_as_pdf(url: str, inbox_dir: Path) -> Path:
    """Download *url* as a PDF and save it under *inbox_dir*.

    If the URL already serves a PDF (Content-Type: application/pdf), the file
    is streamed directly.  Otherwise a headless Chromium instance (playwright)
    renders the page and prints it to PDF.

    Returns the Path of the written file.
    """
    import requests

    inbox_dir.mkdir(parents=True, exist_ok=True)
    filename = _url_to_filename(url)
    dest = inbox_dir / filename

    # --- Try direct download first (handles arXiv /pdf/ links, etc.) ---
    head = requests.head(url, allow_redirects=True, timeout=15)
    content_type = head.headers.get("Content-Type", "")

    if "application/pdf" in content_type:
        resp = requests.get(url, allow_redirects=True, timeout=60, stream=True)
        resp.raise_for_status()
        with dest.open("wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return dest

    # --- Render HTML page with playwright ---
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise RuntimeError(
            "playwright is required to convert HTML pages to PDF. "
            "Install it with: uv add playwright && uv run playwright install chromium"
        ) from e

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=60_000)
        page.pdf(path=str(dest), format="A4", print_background=True)
        browser.close()

    return dest
