"""PDF ingest adapter — extracts text from PDFs and splits into logical sections.

Splitting strategy:
  1. Try to detect major section headings (numbered like "1. Intro" or ALL-CAPS like "ABSTRACT").
  2. If ≥2 headings found, each heading + its body becomes one SourceSection.
  3. If no headings detected, fall back to page-chunked sections (MAX_PAGES_PER_CHUNK pages each).

Tables found by pdfplumber are rendered as Markdown tables and stitched into the text
at the position of the page they appear on.
"""

from __future__ import annotations

import re
from pathlib import Path

import pdfplumber

from .base import IngestAdapter, SourceSection

MAX_PAGES_PER_CHUNK = 15  # fallback chunk size
MAX_CHARS_PER_SECTION = 16_000  # hard cap before sending to LLM (~4K tokens)
MAX_PAGES = 500  # reject PDFs larger than this to prevent CPU/memory exhaustion
MAX_FILE_BYTES = 100 * 1024 * 1024  # 100 MB

# Match lines that look like section headings:
#   "1.  Introduction", "2.3 Related Work", "ABSTRACT", "CONCLUSION"
_HEADING_RE = re.compile(
    r"^(?:(\d+(?:\.\d+)*\.?\s+)\S.{0,70})$"   # numbered:  "1. Foo" / "2.3.1 Bar"
    r"|^([A-Z][A-Z\d\s,:\-]{3,69})$",          # ALL-CAPS:  "ABSTRACT", "RELATED WORK"
    re.MULTILINE,
)


def _table_to_markdown(table: list[list]) -> str:
    """Convert a pdfplumber table (list of rows) to a Markdown table string."""
    if not table or not table[0]:
        return ""
    rows = [[str(cell or "").strip() for cell in row] for row in table]
    header, *body = rows
    sep = ["---"] * len(header)
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
    ]
    for row in body:
        # Pad short rows
        while len(row) < len(header):
            row.append("")
        lines.append("| " + " | ".join(row[: len(header)]) + " |")
    return "\n".join(lines)


def _extract_pages(pdf_path: Path) -> tuple[list[str], int]:
    """Return (list_of_page_texts, total_pages). Tables are rendered as MD inline."""
    size = pdf_path.stat().st_size
    if size > MAX_FILE_BYTES:
        raise ValueError(
            f"{pdf_path.name} is {size / 1_048_576:.1f} MB, "
            f"exceeding the {MAX_FILE_BYTES // 1_048_576} MB limit."
        )
    page_texts: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        if total > MAX_PAGES:
            raise ValueError(
                f"{pdf_path.name} has {total} pages, exceeding the {MAX_PAGES}-page limit."
            )
        for page in pdf.pages:
            # Extract tables first so we can replace them inline
            tables = page.extract_tables()
            text = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
            if tables:
                md_tables = "\n\n".join(_table_to_markdown(t) for t in tables if t)
                text = text + "\n\n" + md_tables if md_tables else text
            page_texts.append(text.strip())
    return page_texts, total


def _split_by_headings(full_text: str) -> list[tuple[str, str]] | None:
    """Try to split full_text into (heading, body) pairs. Returns None if < 2 headings."""
    matches = list(_HEADING_RE.finditer(full_text))
    if len(matches) < 2:
        return None

    sections: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        heading = m.group().strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        body = full_text[start:end].strip()
        if body:  # skip empty sections
            sections.append((heading, f"{heading}\n\n{body}"))

    return sections if len(sections) >= 2 else None


def _split_by_pages(page_texts: list[str], pages_per_chunk: int) -> list[tuple[str, str]]:
    """Chunk pages into groups of pages_per_chunk."""
    chunks: list[tuple[str, str]] = []
    for i in range(0, len(page_texts), pages_per_chunk):
        group = page_texts[i : i + pages_per_chunk]
        text = "\n\n".join(t for t in group if t)
        if text.strip():
            part = i // pages_per_chunk + 1
            total_parts = (len(page_texts) + pages_per_chunk - 1) // pages_per_chunk
            name = f"part-{part}" if total_parts > 1 else "full"
            chunks.append((name, text))
    return chunks


def _cap_text(text: str) -> str:
    """Hard-cap text at MAX_CHARS_PER_SECTION, appending a note if truncated."""
    if len(text) <= MAX_CHARS_PER_SECTION:
        return text
    return text[:MAX_CHARS_PER_SECTION] + f"\n\n[Note: text truncated at {MAX_CHARS_PER_SECTION} chars]"


class PDFAdapter(IngestAdapter):
    """Adapter for PDF files — one SourceSection per detected section or page-chunk."""

    def parse(self) -> list[SourceSection]:
        page_texts, total_pages = _extract_pages(self.file_path)
        full_text = "\n\n".join(t for t in page_texts if t)

        if not full_text.strip():
            raise ValueError(
                f"{self.file_path.name} appears to be a scanned/image-only PDF "
                "with no extractable text. OCR is not yet supported."
            )

        # Try heading-based split first
        named_sections = _split_by_headings(full_text)

        # Fall back to page chunking
        if named_sections is None:
            named_sections = _split_by_pages(page_texts, MAX_PAGES_PER_CHUNK)

        result: list[SourceSection] = []
        for name, text in named_sections:
            result.append(
                SourceSection(
                    source_file=self.file_path,
                    section_name=name,
                    content_type="pdf",
                    raw_text=_cap_text(text),
                    row_count=text.count("\n"),
                    metadata={
                        "total_pages": total_pages,
                        "total_sections": len(named_sections),
                    },
                )
            )
        return result
