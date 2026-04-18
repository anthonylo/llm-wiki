---
title: RAG Paradigms (Naive, Advanced, Modular)
tags: [RAG, paradigms, modular-RAG, advanced-RAG, retrieval]
source: "2312.10997v5 — Retrieval-Augmented Generation for Large Language Models: A Survey (Gao et al., 2023)"
---

## Summary

Gao et al. (2023) organise the RAG landscape into three evolutionary paradigms: **Naive RAG** (the original simple pipeline), **Advanced RAG** (optimisations before and after retrieval), and **Modular RAG** (flexible, configurable component assembly). Each paradigm addresses the limitations of its predecessor.

## Explanation

### Paradigm 1: Naive RAG

The foundational pipeline: **Index → Retrieve → Generate**

**Steps**:
1. *Indexing*: Clean, chunk, embed documents → store in vector DB
2. *Retrieval*: Encode query → cosine similarity → top-k chunks
3. *Generation*: Concatenate query + chunks → LLM → answer

**Problems with Naive RAG**:
- Low retrieval precision: irrelevant chunks pollute the prompt
- Low retrieval recall: relevant chunks may be missed (keyword mismatch)
- Redundant information: duplicate content wastes context
- Context window saturation: too many chunks hit the token limit
- Hallucination: LLM may ignore retrieved context and confabulate
- Knowledge conflicts: retrieved documents may contradict each other

---

### Paradigm 2: Advanced RAG

Advanced RAG adds *pre-retrieval* and *post-retrieval* optimisation stages.

**Pre-Retrieval Optimisation**

| Technique | Description |
|-----------|-------------|
| Query Expansion | Expand query with synonyms / related terms (e.g., HyDE) |
| Query Rewriting | Reformulate query for better retrieval |
| Query Decomposition | Break complex queries into sub-queries |
| Query Routing | Route to appropriate retrieval source |
| Sliding Window Chunking | Overlapping chunks for boundary context |
| Sentence-Level Splitting | Split at sentence boundaries, not fixed tokens |
| Hierarchical Indexing | Multi-granularity: document → section → sentence |

**HyDE (Hypothetical Document Embedding)**: LLM generates a hypothetical answer to the query, embed that, retrieve similar real documents. Bridges vocabulary gap.

**Post-Retrieval Optimisation**

| Technique | Description |
|-----------|-------------|
| Re-ranking | Score retrieved chunks by relevance (cross-encoder or LLM-as-judge) |
| Compression | Summarise or filter retrieved content before injection |
| Context Selection | Select most relevant passages from candidates |
| Diversity Filtering | Remove redundant retrieved chunks |

---

### Paradigm 3: Modular RAG

Modular RAG treats each component as an interchangeable module, enabling custom pipelines beyond the fixed Retrieve → Generate flow.

**Key Modules**:

| Module | Function |
|--------|----------|
| Search | Web search, database query, API call |
| Memory | Short-term (conversation history) + long-term (vector store) |
| Fusion | Merge results from multiple retrievers |
| Routing | Decide which module to invoke for a query |
| Predict | LLM generation with different personas / formats |
| Task Adapter | Task-specific post-processing |

**Advanced Retrieval Strategies in Modular RAG**:

- **Iterative Retrieval**: Retrieve → read → retrieve again based on new information; multi-hop reasoning
- **Recursive Retrieval**: Start with abstract, progressively retrieve finer-grained chunks
- **Adaptive Retrieval**: Use the LLM itself to decide *when* to retrieve (FLARE, Self-RAG)

**Self-RAG** (Asai et al., 2023):
- Model generates "reflection tokens" (Retrieve?, ISREL, ISSUP, ISUSE) to decide whether retrieval is needed
- Enables selective, on-demand retrieval vs. always-retrieve

---

### Retrieval Source Types

| Source Type | Examples |
|-------------|----------|
| Unstructured | Web pages, PDFs, emails, documents |
| Semi-structured | Tables in PDFs, HTML tables |
| Structured | SQL databases, knowledge graphs |
| LLM-generated | Hypothetical documents, summaries |

---

### Choosing a Paradigm

| Use Case | Recommended Paradigm |
|----------|---------------------|
| Simple document Q&A | Naive RAG |
| High-precision enterprise search | Advanced RAG + re-ranking |
| Multi-source, multi-hop reasoning | Modular RAG (iterative/recursive) |
| Low latency required | Naive RAG or compressed Advanced RAG |
| Dynamic, tool-integrated agentic use | Modular RAG → or [[model-context-protocol]] |

## Related Pages

- [[retrieval-augmented-generation]] — RAG overview and motivation
- [[vector-databases-and-embeddings]] — the retrieval infrastructure
- [[hallucination]] — RAG paradigms are principally motivated by hallucination reduction
- [[model-context-protocol]] — MCP provides active, programmatic context management beyond passive retrieval
- [[long-term-memory-in-ai]] — Modular RAG's memory module is external LTM; not intrinsic

## Contradictions

> **Self-RAG selective retrieval vs always-retrieve**: Naive RAG always retrieves. Self-RAG retrieves only when needed. This reflects genuine disagreement about the right retrieval strategy — retrieving irrelevant context can hurt generation quality (distraction effect), while always retrieving guarantees grounding.
