---
title: Vector Databases and Embeddings
tags: [vector-database, embeddings, semantic-search, FAISS, ChromaDB]
source: "2312.10997v5 — Retrieval-Augmented Generation for Large Language Models: A Survey (Gao et al., 2023)"
---

## Summary

Vector databases store dense numerical representations (embeddings) of text, images, and other data, enabling semantic similarity search at scale. They are the retrieval backbone of [[retrieval-augmented-generation]] systems, allowing LLMs to query external knowledge using meaning rather than keyword matching.

## Explanation

### Embeddings

An **embedding** is a fixed-size dense vector (e.g., 384, 768, or 1536 dimensions) that encodes the semantic meaning of an input. Inputs with similar meaning have vectors that are close in high-dimensional space (measured by cosine similarity or dot product).

**Embedding Models**:

| Model | Dimensions | Notes |
|-------|------------|-------|
| `all-MiniLM-L6-v2` | 384 | Fast, CPU-friendly, used in this wiki system |
| `text-embedding-ada-002` | 1536 | OpenAI; strong general-purpose |
| `text-embedding-3-large` | 3072 | OpenAI; SOTA |
| `BGE-large-en` | 1024 | Strong open-source retrieval model |
| `E5-mistral-7b-instruct` | 4096 | LLM-based; top MTEB scores |

### Sparse vs Dense Retrieval

| Type | Method | Strengths | Weaknesses |
|------|--------|-----------|------------|
| **Sparse** | BM25, TF-IDF | Exact term matching, fast, interpretable | Vocabulary mismatch, no semantic understanding |
| **Dense** | Embedding similarity | Semantic matching, handles synonyms | Slower, requires embedding model, less interpretable |
| **Hybrid** | Sparse + dense fusion | Best of both | More complex setup |

**Hybrid retrieval** (e.g., BM25 + FAISS with RRF fusion) is the recommended production approach.

### Vector Database Landscape

| Database | Key Properties |
|----------|----------------|
| **FAISS** (Meta) | In-memory, extremely fast, no persistence by default |
| **ChromaDB** | Embedded, persistent, Python-native, used in this wiki system |
| **Pinecone** | Managed cloud service; production-scale |
| **Weaviate** | Graph + vector hybrid; schema-based |
| **Qdrant** | Rust-based; filtering + vector search |
| **Milvus** | Distributed; enterprise-scale |
| **pgvector** | PostgreSQL extension; simple for existing Postgres users |

### Approximate Nearest Neighbour (ANN)

Exact nearest-neighbour search over millions of vectors is too slow (O(n)). ANN algorithms trade a small accuracy loss for much faster search:

- **HNSW** (Hierarchical Navigable Small World): graph-based, very fast, high recall — default in ChromaDB and Qdrant
- **IVF** (Inverted File Index): clusters vectors; search only nearby clusters — used in FAISS
- **PQ** (Product Quantisation): compress vectors for memory efficiency

### Chunking Strategy

How documents are split into indexable units significantly impacts retrieval quality:

| Strategy | Description | Best For |
|----------|-------------|----------|
| Fixed-size | Split at N tokens with overlap | Simple baseline |
| Sentence | Split at sentence boundaries | Prose text |
| Paragraph | Split at paragraph breaks | Structured docs |
| Semantic | Cluster by topic similarity | Long heterogeneous docs |
| Hierarchical | Index at multiple granularities | Large document corpora |

This wiki system's [[model-context-protocol|MCP paper section]] recommends semantic chunking for technical papers.

### Re-ranking

Retrieved chunks are ranked by embedding similarity, but this is imprecise. A **cross-encoder re-ranker** takes (query, document) pairs and outputs a relevance score — much more accurate than bi-encoder similarity but slower. Common re-rankers: BGE-reranker, Cohere Rerank, FlashRank.

## Related Pages

- [[retrieval-augmented-generation]] — vector DBs are the retrieval backbone of RAG
- [[rag-paradigms]] — chunking, indexing, and re-ranking are Advanced/Modular RAG components
- [[hallucination]] — grounding via retrieval reduces hallucination
- [[long-term-memory-in-ai]] — vector stores are external long-term memory; not intrinsic to the LLM
- [[capability-contortions]] — using external vector stores is one of the "contortions" the AGI paper critiques
