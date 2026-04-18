"""Tests for ingest adapters."""
from pathlib import Path

import pytest

from wiki_engine.ingest import get_adapter
from wiki_engine.ingest.base import SourceSection
from wiki_engine.ingest.csv_adapter import CSVAdapter
from wiki_engine.ingest.excel_adapter import ExcelAdapter
from wiki_engine.ingest.json_adapter import JSONAdapter


class TestCSVAdapter:
    def test_parse_returns_one_section(self, sample_csv):
        adapter = CSVAdapter(sample_csv)
        sections = adapter.parse()
        assert len(sections) == 1

    def test_csv_section_has_correct_columns(self, sample_csv):
        sections = CSVAdapter(sample_csv).parse()
        assert sections[0].column_names == ["id", "name", "department", "salary", "start_date"]

    def test_csv_row_count(self, sample_csv):
        sections = CSVAdapter(sample_csv).parse()
        assert sections[0].row_count == 5

    def test_tsv_auto_detected(self, sample_tsv):
        sections = CSVAdapter(sample_tsv).parse()
        assert sections[0].content_type == "tsv"
        assert sections[0].row_count == 4

    def test_slug_is_stem(self, sample_csv):
        sections = CSVAdapter(sample_csv).parse()
        assert sections[0].slug == "sample"

    def test_raw_text_contains_header(self, sample_csv):
        sections = CSVAdapter(sample_csv).parse()
        assert "name" in sections[0].raw_text
        assert "department" in sections[0].raw_text


class TestExcelAdapter:
    def test_parse_returns_sections_plus_index(self, sample_xlsx):
        adapter = ExcelAdapter(sample_xlsx)
        sections = adapter.parse()
        # 2 non-empty sheets + 1 workbook index
        assert len(sections) == 3

    def test_empty_sheet_skipped(self, sample_xlsx):
        sections = ExcelAdapter(sample_xlsx).parse()
        sheet_names = [s.section_name for s in sections]
        assert "Empty" not in sheet_names

    def test_workbook_index_last(self, sample_xlsx):
        sections = ExcelAdapter(sample_xlsx).parse()
        assert sections[-1].metadata.get("is_index") is True

    def test_sheet_slugs_in_index_metadata(self, sample_xlsx):
        sections = ExcelAdapter(sample_xlsx).parse()
        index_sec = sections[-1]
        assert "sheet_slugs" in index_sec.metadata
        assert len(index_sec.metadata["sheet_slugs"]) == 2

    def test_employees_sheet_columns(self, sample_xlsx):
        sections = ExcelAdapter(sample_xlsx).parse()
        employees = next(s for s in sections if s.section_name == "Employees")
        assert "name" in employees.column_names


class TestJSONAdapter:
    def test_dict_creates_one_section_per_key(self, sample_json):
        sections = JSONAdapter(sample_json).parse()
        # sample.json has 2 top-level keys: "team" and "project"
        assert len(sections) == 2
        slugs = {s.section_name for s in sections}
        assert "team" in slugs
        assert "project" in slugs

    def test_list_value_has_row_count(self, sample_json):
        sections = JSONAdapter(sample_json).parse()
        team_sec = next(s for s in sections if s.section_name == "team")
        assert team_sec.row_count == 3

    def test_raw_text_not_empty(self, sample_json):
        sections = JSONAdapter(sample_json).parse()
        for s in sections:
            assert len(s.raw_text) > 0


class TestGetAdapter:
    def test_csv_returns_csv_adapter(self, sample_csv):
        adapter = get_adapter(sample_csv)
        assert isinstance(adapter, CSVAdapter)

    def test_xlsx_returns_excel_adapter(self, sample_xlsx):
        adapter = get_adapter(sample_xlsx)
        assert isinstance(adapter, ExcelAdapter)

    def test_json_returns_json_adapter(self, sample_json):
        adapter = get_adapter(sample_json)
        assert isinstance(adapter, JSONAdapter)

    def test_unsupported_raises(self, tmp_path):
        bad_file = tmp_path / "test.parquet"
        bad_file.touch()
        with pytest.raises(ValueError, match="Unsupported"):
            get_adapter(bad_file)


class TestSourceSectionSlug:
    def test_slug_simple(self, sample_csv):
        sections = CSVAdapter(sample_csv).parse()
        assert sections[0].slug == "sample"

    def test_slug_with_spaces(self, tmp_path):
        # Create a CSV with spaces in name
        f = tmp_path / "my data file.csv"
        f.write_text("a,b\n1,2\n")
        sections = CSVAdapter(f).parse()
        assert " " not in sections[0].slug

    def test_excel_sheet_slug(self, sample_xlsx):
        sections = ExcelAdapter(sample_xlsx).parse()
        employees = next(s for s in sections if s.section_name == "Employees")
        assert employees.slug == "sample-employees"
