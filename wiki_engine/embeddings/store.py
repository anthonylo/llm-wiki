from __future__ import annotations

from pathlib import Path

import chromadb
from chromadb.config import Settings

from .encoder import encode

COLLECTION_NAME = "wiki_pages"

_client: chromadb.ClientAPI | None = None
_collection: chromadb.Collection | None = None


def _get_collection(store_dir: Path) -> chromadb.Collection:
    global _client, _collection
    if _collection is None:
        chroma_path = store_dir / "chroma"
        chroma_path.mkdir(parents=True, exist_ok=True)
        _client = chromadb.PersistentClient(
            path=str(chroma_path),
            settings=Settings(anonymized_telemetry=False),
        )
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def upsert(slug: str, title: str, content: str, store_dir: Path) -> None:
    """Add or update a page in the vector store."""
    col = _get_collection(store_dir)
    text = f"{title}\n\n{content}"
    embedding = encode([text])[0]
    col.upsert(
        ids=[slug],
        embeddings=[embedding],
        documents=[content],
        metadatas=[{"slug": slug, "title": title}],
    )


def query_similar(content: str, top_k: int, store_dir: Path, exclude_slug: str | None = None) -> list[dict]:
    """Return up to top_k similar pages as list of {slug, title, content} dicts."""
    col = _get_collection(store_dir)
    count = col.count()
    if count == 0:
        return []

    embedding = encode([content])[0]
    effective_k = min(top_k + (1 if exclude_slug else 0), count)
    results = col.query(
        query_embeddings=[embedding],
        n_results=effective_k,
        include=["documents", "metadatas"],
    )

    pages = []
    for i, doc_id in enumerate(results["ids"][0]):
        if doc_id == exclude_slug:
            continue
        meta = results["metadatas"][0][i]
        doc = results["documents"][0][i]
        pages.append({"slug": doc_id, "title": meta.get("title", doc_id), "content": doc})
        if len(pages) >= top_k:
            break
    return pages
