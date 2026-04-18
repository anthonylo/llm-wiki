"""Tests for the pipeline (mocked LLM calls)."""
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from wiki_engine.wiki.page import WikiPage, ProcessingResult
from wiki_engine.ingest.base import SourceSection


SAMPLE_MARKDOWN = """\
---
title: Sample Data
source: sample.csv
section: sample
generated: 2026-04-17
---

## Summary

This dataset contains employee records.

## Data

| id | name | department | salary |
|----|------|------------|--------|
| 1 | Alice | Engineering | 95000 |

## Notes

Data quality looks good.
"""


def _make_section(tmp_path: Path) -> SourceSection:
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("id,name\n1,Alice\n")
    return SourceSection(
        source_file=csv_file,
        section_name="sample",
        content_type="csv",
        raw_text="id,name\n1,Alice",
        row_count=1,
        column_names=["id", "name"],
    )


class TestPipelineDedup:
    def test_skip_if_already_processed(self, tmp_path):
        from wiki_engine import pipeline

        csv_file = tmp_path / "data.csv"
        csv_file.write_text("a,b\n1,2\n")
        processed_dir = tmp_path / ".wiki_store" / "processed"
        processed_dir.mkdir(parents=True)

        # Pre-write hash
        import hashlib
        h = hashlib.sha256(csv_file.read_bytes()).hexdigest()
        (processed_dir / "data.csv.hash").write_text(h)

        with patch("wiki_engine.pipeline.get_settings") as mock_settings:
            settings = MagicMock()
            settings.wiki_dir = tmp_path / "wiki"
            settings.store_dir = tmp_path / ".wiki_store"
            settings.processed_dir = processed_dir
            settings.wiki_dir.mkdir(parents=True, exist_ok=True)
            mock_settings.return_value = settings

            results = pipeline.run(csv_file, force=False)

        assert len(results) == 1
        assert results[0].status == "skipped"

    def test_force_bypasses_dedup(self, tmp_path):
        from wiki_engine import pipeline

        csv_file = tmp_path / "data.csv"
        csv_file.write_text("a,b\n1,2\n")
        processed_dir = tmp_path / ".wiki_store" / "processed"
        processed_dir.mkdir(parents=True)
        (processed_dir / "data.csv.hash").write_text("old_hash")

        mock_page = WikiPage(
            slug="data",
            title="Data",
            source_section=_make_section(tmp_path),
            content=SAMPLE_MARKDOWN,
        )

        with patch("wiki_engine.pipeline.get_settings") as mock_settings, \
             patch("wiki_engine.pipeline.get_adapter") as mock_adapter, \
             patch("wiki_engine.pipeline.generator.generate", return_value=mock_page), \
             patch("wiki_engine.pipeline.validator.check_fidelity", return_value={"passed": True, "score": 0.95, "issues": []}), \
             patch("wiki_engine.pipeline.validator.check_consistency", return_value={"passed": True, "contradictions": []}), \
             patch("wiki_engine.pipeline.linker.find_links", return_value=[]), \
             patch("wiki_engine.pipeline.emb_store.query_similar", return_value=[]), \
             patch("wiki_engine.pipeline.emb_store.upsert"), \
             patch("wiki_engine.pipeline.index.update"), \
             patch("wiki_engine.pipeline.changelog.append"):

            settings = MagicMock()
            settings.wiki_dir = tmp_path / "wiki"
            settings.store_dir = tmp_path / ".wiki_store"
            settings.processed_dir = processed_dir
            settings.wiki_dir.mkdir(parents=True, exist_ok=True)
            mock_settings.return_value = settings

            mock_section = _make_section(tmp_path)
            mock_adapter_instance = MagicMock()
            mock_adapter_instance.parse.return_value = [mock_section]
            mock_adapter.return_value = mock_adapter_instance

            results = pipeline.run(csv_file, force=True)

        assert results[0].status != "skipped"


class TestPipelineValidation:
    def test_fidelity_fail_triggers_regeneration(self, tmp_path):
        from wiki_engine import pipeline

        csv_file = tmp_path / "data.csv"
        csv_file.write_text("a,b\n1,2\n")

        mock_section = _make_section(tmp_path)
        mock_page = WikiPage(
            slug="sample",
            title="Sample",
            source_section=mock_section,
            content=SAMPLE_MARKDOWN,
        )

        fidelity_fail = {"passed": False, "score": 0.5, "issues": ["Missing column"]}
        fidelity_pass = {"passed": True, "score": 0.95, "issues": []}

        with patch("wiki_engine.pipeline.get_settings") as mock_settings, \
             patch("wiki_engine.pipeline.get_adapter") as mock_adapter, \
             patch("wiki_engine.pipeline.generator.generate", return_value=mock_page), \
             patch("wiki_engine.pipeline.validator.check_fidelity", side_effect=[fidelity_fail, fidelity_pass]), \
             patch("wiki_engine.pipeline.validator.check_consistency", return_value={"passed": True, "contradictions": []}), \
             patch("wiki_engine.pipeline.linker.find_links", return_value=[]), \
             patch("wiki_engine.pipeline.emb_store.query_similar", return_value=[]), \
             patch("wiki_engine.pipeline.emb_store.upsert"), \
             patch("wiki_engine.pipeline.index.update"), \
             patch("wiki_engine.pipeline.changelog.append"):

            settings = MagicMock()
            settings.wiki_dir = tmp_path / "wiki"
            settings.store_dir = tmp_path / ".wiki_store"
            settings.processed_dir = tmp_path / ".wiki_store" / "processed"
            settings.processed_dir.mkdir(parents=True, exist_ok=True)
            settings.wiki_dir.mkdir(parents=True, exist_ok=True)
            mock_settings.return_value = settings

            mock_adapter_instance = MagicMock()
            mock_adapter_instance.parse.return_value = [mock_section]
            mock_adapter.return_value = mock_adapter_instance

            results = pipeline.run(csv_file, force=True)

        assert results[0].status == "ok"

    def test_double_fidelity_fail_rejects(self, tmp_path):
        from wiki_engine import pipeline

        csv_file = tmp_path / "data.csv"
        csv_file.write_text("a,b\n1,2\n")

        mock_section = _make_section(tmp_path)
        mock_page = WikiPage(
            slug="sample",
            title="Sample",
            source_section=mock_section,
            content=SAMPLE_MARKDOWN,
        )

        fidelity_fail = {"passed": False, "score": 0.4, "issues": ["Wrong data"]}

        with patch("wiki_engine.pipeline.get_settings") as mock_settings, \
             patch("wiki_engine.pipeline.get_adapter") as mock_adapter, \
             patch("wiki_engine.pipeline.generator.generate", return_value=mock_page), \
             patch("wiki_engine.pipeline.validator.check_fidelity", return_value=fidelity_fail), \
             patch("wiki_engine.pipeline.index.update"), \
             patch("wiki_engine.pipeline.changelog.append"):

            settings = MagicMock()
            settings.wiki_dir = tmp_path / "wiki"
            settings.store_dir = tmp_path / ".wiki_store"
            settings.processed_dir = tmp_path / ".wiki_store" / "processed"
            settings.processed_dir.mkdir(parents=True, exist_ok=True)
            settings.wiki_dir.mkdir(parents=True, exist_ok=True)
            mock_settings.return_value = settings

            mock_adapter_instance = MagicMock()
            mock_adapter_instance.parse.return_value = [mock_section]
            mock_adapter.return_value = mock_adapter_instance

            results = pipeline.run(csv_file, force=True)

        assert results[0].status == "rejected"

    def test_consistency_fail_blocks(self, tmp_path):
        from wiki_engine import pipeline

        csv_file = tmp_path / "data.csv"
        csv_file.write_text("a,b\n1,2\n")

        mock_section = _make_section(tmp_path)
        mock_page = WikiPage(
            slug="sample",
            title="Sample",
            source_section=mock_section,
            content=SAMPLE_MARKDOWN,
        )

        contradictions = [{"draft_claim": "X", "existing_page": "old", "existing_claim": "Y", "explanation": "conflict"}]

        with patch("wiki_engine.pipeline.get_settings") as mock_settings, \
             patch("wiki_engine.pipeline.get_adapter") as mock_adapter, \
             patch("wiki_engine.pipeline.generator.generate", return_value=mock_page), \
             patch("wiki_engine.pipeline.validator.check_fidelity", return_value={"passed": True, "score": 0.95, "issues": []}), \
             patch("wiki_engine.pipeline.validator.check_consistency", return_value={"passed": False, "contradictions": contradictions}), \
             patch("wiki_engine.pipeline.emb_store.query_similar", return_value=[]), \
             patch("wiki_engine.pipeline.index.update"), \
             patch("wiki_engine.pipeline.changelog.append"):

            settings = MagicMock()
            settings.wiki_dir = tmp_path / "wiki"
            settings.store_dir = tmp_path / ".wiki_store"
            settings.processed_dir = tmp_path / ".wiki_store" / "processed"
            settings.processed_dir.mkdir(parents=True, exist_ok=True)
            settings.wiki_dir.mkdir(parents=True, exist_ok=True)
            mock_settings.return_value = settings

            mock_adapter_instance = MagicMock()
            mock_adapter_instance.parse.return_value = [mock_section]
            mock_adapter.return_value = mock_adapter_instance

            results = pipeline.run(csv_file, force=True)

        assert results[0].status == "blocked"
