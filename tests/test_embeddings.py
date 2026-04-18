"""Tests for embedding store."""
import pytest
from pathlib import Path


@pytest.fixture
def store_dir(tmp_path):
    return tmp_path / ".wiki_store"


class TestEmbeddingStore:
    def test_upsert_and_query(self, store_dir):
        from wiki_engine.embeddings import store

        store._client = None
        store._collection = None

        store.upsert("page-a", "Page A", "This is about apples and fruit.", store_dir)
        store.upsert("page-b", "Page B", "This is about oranges and citrus.", store_dir)

        results = store.query_similar("fruit and apples", top_k=2, store_dir=store_dir)
        assert len(results) >= 1
        slugs = [r["slug"] for r in results]
        assert "page-a" in slugs

        store._client = None
        store._collection = None

    def test_exclude_slug(self, store_dir):
        from wiki_engine.embeddings import store

        store._client = None
        store._collection = None

        store.upsert("page-x", "Page X", "Machine learning and neural networks.", store_dir)
        store.upsert("page-y", "Page Y", "Deep learning with transformers.", store_dir)

        results = store.query_similar(
            "neural networks", top_k=5, store_dir=store_dir, exclude_slug="page-x"
        )
        slugs = [r["slug"] for r in results]
        assert "page-x" not in slugs

        store._client = None
        store._collection = None

    def test_empty_store_returns_empty(self, tmp_path):
        from wiki_engine.embeddings import store
        empty_dir = tmp_path / "empty_store"

        store._client = None
        store._collection = None

        results = store.query_similar("anything", top_k=5, store_dir=empty_dir)
        assert results == []

        store._client = None
        store._collection = None
