"""Tests for the PDF ingest adapter."""
from pathlib import Path

import pytest

from wiki_engine.ingest import get_adapter
from wiki_engine.ingest.pdf_adapter import PDFAdapter, _split_by_headings, _split_by_pages, _table_to_markdown


class TestPDFAdapter:
    def test_parse_returns_sections(self, sample_pdf):
        adapter = PDFAdapter(sample_pdf)
        sections = adapter.parse()
        assert len(sections) >= 1

    def test_all_sections_have_content(self, sample_pdf):
        sections = PDFAdapter(sample_pdf).parse()
        for s in sections:
            assert len(s.raw_text.strip()) > 0

    def test_content_type_is_pdf(self, sample_pdf):
        sections = PDFAdapter(sample_pdf).parse()
        for s in sections:
            assert s.content_type == "pdf"

    def test_section_names_are_non_empty(self, sample_pdf):
        sections = PDFAdapter(sample_pdf).parse()
        for s in sections:
            assert s.section_name.strip() != ""

    def test_source_file_preserved(self, sample_pdf):
        sections = PDFAdapter(sample_pdf).parse()
        for s in sections:
            assert s.source_file == sample_pdf

    def test_metadata_has_total_pages(self, sample_pdf):
        sections = PDFAdapter(sample_pdf).parse()
        for s in sections:
            assert "total_pages" in s.metadata
            assert s.metadata["total_pages"] >= 1

    def test_heading_sections_detected(self, sample_pdf):
        # sample.pdf has "ABSTRACT", "1. INTRODUCTION", etc. — should split on headings
        sections = PDFAdapter(sample_pdf).parse()
        # The fixture has 5 headed sections; expect at least 2
        assert len(sections) >= 2

    def test_slug_includes_file_stem(self, sample_pdf):
        sections = PDFAdapter(sample_pdf).parse()
        for s in sections:
            assert "sample" in s.slug

    def test_text_cap_applied(self, tmp_path):
        """A PDF whose extracted text exceeds MAX_CHARS_PER_SECTION should be capped."""
        from fpdf import FPDF
        from wiki_engine.ingest.pdf_adapter import MAX_CHARS_PER_SECTION

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "", 10)
        # Write a block of text well over the cap
        big_text = ("word " * 100 + "\n") * 200  # ~100K chars
        pdf.multi_cell(0, 5, big_text)
        pdf_path = tmp_path / "big.pdf"
        pdf.output(str(pdf_path))

        sections = PDFAdapter(pdf_path).parse()
        for s in sections:
            assert len(s.raw_text) <= MAX_CHARS_PER_SECTION + 200  # allow note suffix


class TestGetAdapterPDF:
    def test_pdf_returns_pdf_adapter(self, sample_pdf):
        adapter = get_adapter(sample_pdf)
        assert isinstance(adapter, PDFAdapter)


class TestSplitByHeadings:
    def test_detects_numbered_sections(self):
        text = "1. Introduction\n\nThis is the intro.\n\n2. Methods\n\nThis is methods."
        result = _split_by_headings(text)
        assert result is not None
        assert len(result) == 2

    def test_detects_allcaps_headings(self):
        text = "ABSTRACT\n\nSome abstract text here.\n\nCONCLUSION\n\nFinal thoughts."
        result = _split_by_headings(text)
        assert result is not None
        assert len(result) == 2

    def test_returns_none_for_no_headings(self):
        text = "Just some plain text\nwith no headings at all\njust flowing words."
        result = _split_by_headings(text)
        assert result is None

    def test_returns_none_for_single_heading(self):
        text = "ABSTRACT\n\nOnly one section here, no second heading."
        result = _split_by_headings(text)
        assert result is None


class TestSplitByPages:
    def test_single_chunk_for_short_doc(self):
        pages = ["Page one text.", "Page two text."]
        result = _split_by_pages(pages, pages_per_chunk=15)
        assert len(result) == 1
        assert result[0][0] == "full"

    def test_multiple_chunks_for_long_doc(self):
        pages = [f"Page {i} content." for i in range(30)]
        result = _split_by_pages(pages, pages_per_chunk=10)
        assert len(result) == 3

    def test_chunk_names_are_part_n(self):
        pages = [f"Page {i}." for i in range(20)]
        result = _split_by_pages(pages, pages_per_chunk=10)
        names = [r[0] for r in result]
        assert "part-1" in names
        assert "part-2" in names

    def test_empty_pages_skipped(self):
        pages = ["Real content.", "", "   ", "More content."]
        result = _split_by_pages(pages, pages_per_chunk=10)
        assert len(result) == 1


class TestTableToMarkdown:
    def test_basic_table(self):
        table = [["Name", "Score"], ["Alice", "95"], ["Bob", "87"]]
        md = _table_to_markdown(table)
        assert "| Name | Score |" in md
        assert "| Alice | 95 |" in md
        assert "---" in md

    def test_empty_table_returns_empty(self):
        assert _table_to_markdown([]) == ""
        assert _table_to_markdown([[]]) == ""

    def test_none_cells_become_empty_string(self):
        table = [["A", "B"], [None, "val"]]
        md = _table_to_markdown(table)
        assert "|  | val |" in md
