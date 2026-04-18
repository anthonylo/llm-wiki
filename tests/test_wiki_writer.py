"""Tests for wiki writer, index, and changelog."""
from pathlib import Path
import pytest

from wiki_engine.wiki.page import WikiPage
from wiki_engine.wiki import writer, index, changelog
from wiki_engine.ingest.base import SourceSection


def make_page(slug: str, title: str, content: str, links=None) -> WikiPage:
    section = SourceSection(
        source_file=Path(f"{slug}.csv"),
        section_name=slug,
        content_type="csv",
        raw_text="a,b\n1,2",
    )
    return WikiPage(slug=slug, title=title, source_section=section, content=content, links=links or [])


class TestWikiWriter:
    def test_write_creates_file(self, tmp_path):
        page = make_page("test-page", "Test Page", "# Test\nHello world.")
        out = writer.write(page, tmp_path)
        assert out.exists()
        assert out.name == "test-page.md"

    def test_write_content_preserved(self, tmp_path):
        page = make_page("test-page", "Test Page", "# Test\nHello world.")
        out = writer.write(page, tmp_path)
        assert "Hello world." in out.read_text()

    def test_related_pages_injected(self, tmp_path):
        links = [{"slug": "other-page", "reason": "related topic"}]
        page = make_page("main-page", "Main", "# Main\nContent.", links=links)
        out = writer.write(page, tmp_path)
        text = out.read_text()
        assert "## Related Pages" in text
        assert "other-page" in text

    def test_no_related_pages_when_no_links(self, tmp_path):
        page = make_page("solo-page", "Solo", "# Solo\nContent.")
        out = writer.write(page, tmp_path)
        assert "## Related Pages" not in out.read_text()


class TestIndexManager:
    def test_index_created(self, tmp_path):
        make_page("p1", "Page 1", "---\ntitle: Page 1\n---\n# P1")
        page = make_page("p1", "Page 1", "---\ntitle: Page 1\n---\n# P1")
        writer.write(page, tmp_path)
        index.update(tmp_path)
        idx = tmp_path / "INDEX.md"
        assert idx.exists()

    def test_index_contains_page(self, tmp_path):
        page = make_page("mypage", "My Page", "---\ntitle: My Page\n---\n# My Page")
        writer.write(page, tmp_path)
        index.update(tmp_path)
        text = (tmp_path / "INDEX.md").read_text()
        assert "mypage.md" in text

    def test_index_excluded_from_listing(self, tmp_path):
        page = make_page("page1", "Page1", "# Page1")
        writer.write(page, tmp_path)
        index.update(tmp_path)
        # Running update again shouldn't double-count INDEX.md
        index.update(tmp_path)
        text = (tmp_path / "INDEX.md").read_text()
        assert text.count("INDEX.md") == 0


class TestChangelog:
    def test_changelog_created(self, tmp_path):
        changelog.append(tmp_path, "test-slug", "ok", "test.csv", "fidelity=0.95")
        assert (tmp_path / "CHANGELOG.md").exists()

    def test_changelog_contains_entry(self, tmp_path):
        changelog.append(tmp_path, "my-page", "ok", "data.csv", "fidelity=0.98")
        text = (tmp_path / "CHANGELOG.md").read_text()
        assert "my-page" in text
        assert "OK" in text

    def test_changelog_blocked_entry(self, tmp_path):
        changelog.append(tmp_path, "bad-page", "blocked", "data.csv", "contradicts existing")
        text = (tmp_path / "CHANGELOG.md").read_text()
        assert "BLOCKED" in text

    def test_entries_are_prepended(self, tmp_path):
        changelog.append(tmp_path, "first", "ok", "a.csv")
        changelog.append(tmp_path, "second", "ok", "b.csv")
        text = (tmp_path / "CHANGELOG.md").read_text()
        # second entry should appear before first
        assert text.index("second") < text.index("first")
