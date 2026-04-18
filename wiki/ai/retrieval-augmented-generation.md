---
title: Retrieval-Augmented Generation (RAG)
tags: [RAG, retrieval, generation, knowledge, LLM]
source: "2312.10997v5 — Retrieval-Augmented Generation for Large Language Models: A Survey (Gao et al., 2023)"
---

## Summary

Retrieval-Augmented Generation (RAG) enhances [[large-language-models]] by supplying relevant external documents at inference time — retrieved from a knowledge base based on the user's query. This extends LLMs beyond their training cutoff, reduces [[hallucination]], and enables knowledge-intensive tasks without expensive retraining. RAG has become the dominant architecture for enterprise LLM deployments.

## Explanation

### The Core Idea

An LLM has a fixed training-time knowledge cutoff and is prone to hallucination when queried about facts not well represented in training data. RAG solves this by:

1. **Retrieve**: Given a query, fetch relevant documents/passages from an external corpus
2. **Augment**: Prepend retrieved content to the LLM's prompt
3. **Generate**: The LLM conditions its response on both the query and retrieved context

```
Query → Retriever → [doc₁, doc₂, doc₃] → LLM(query + docs) → Response
```

### RAG vs. Alternatives

| Approach | Knowledge Source | Update Cost | Hallucination Risk |
|----------|-----------------|-------------|-------------------|
| Parametric LLM | Training weights | Very high (retrain) | High |
| Fine-tuning | Updated weights | Medium | Medium |
| RAG | External corpus | Low (update index) | Low-Medium |
| Tool use / search | Live web/APIs | None | Low (ground truth) |

### Three RAG Paradigms

See [[rag-paradigms]] for detailed breakdown of:
- **Naive RAG**: Basic index → retrieve → generate
- **Advanced RAG**: Pre/post-retrieval optimisation
- **Modular RAG**: Flexible component-based assembly

### Key Components

**Indexing**
- Chunk documents into passages (fixed-size or semantic chunking)
- Encode chunks into dense vector embeddings
- Store in a [[vector-databases-and-embeddings|vector database]] (FAISS, Pinecone, Weaviate, Chroma)

**Retrieval**
- Encode query into same embedding space
- Nearest-neighbour search (cosine or dot-product similarity)
- Optional: hybrid BM25 (sparse) + dense retrieval, re-rankers

**Generation**
- Assemble prompt: query + retrieved passages + instructions
- LLM generates final answer

### RAG Evaluation Frameworks

| Framework | Focus |
|-----------|-------|
| RAGAS | Faithfulness, answer relevance, context precision/recall |
| ARES | LLM-as-judge for faithfulness and relevance |
| RGB | Noise robustness, negative rejection, information integration |
| RECALL | Knowledge conflict detection |
| CRUD-RAG | Decomposed: Create, Read, Update, Delete knowledge operations |

### RAG Efficiency Gains

The LLM survey (Naveed et al. 2023) quantifies RAG's impact on model efficiency:
- An **11B retrieval-augmented model** is competitive with **540B PaLM** on knowledge tasks
- A **7.5B RAG model** matches **280B Gopher** on several benchmarks
- RETRO pre-trains smaller models with RAG, outperforming models 25× larger

This demonstrates that RAG can substitute for parameter scale when the bottleneck is knowledge access rather than reasoning.

### Applications

- Open-domain question answering
- Enterprise knowledge base Q&A (documents, policies, code)
- Medical/legal research assistants
- Customer support over product documentation
- Code search and retrieval

## Related Pages

- [[rag-paradigms]] — Naive / Advanced / Modular RAG in detail
- [[vector-databases-and-embeddings]] — the retrieval infrastructure
- [[hallucination]] — RAG reduces but does not eliminate hallucination
- [[large-language-models]] — LLMs as the generation component
- [[model-context-protocol]] — MCP extends RAG to active tool invocation; overlapping but distinct
- [[long-term-memory-in-ai]] — RAG is an external memory mechanism; contrast with intrinsic LTM
- [[capability-contortions]] — AGI paper argues RAG masks the fundamental lack of intrinsic memory storage

## Contradictions

> **RAG as infrastructure vs RAG as contortion**: The RAG survey (Paper 3) treats RAG as essential, mature infrastructure for enterprise LLM deployment. The AGI paper (Paper 5) characterises RAG as a *capability contortion* — an engineering workaround that masks the model's fundamental inability to store and retrieve information intrinsically. Both are correct in their domains (RAG is useful for current applications; but it doesn't constitute genuine LTM storage), but the framing reveals a key gap between practical utility and AGI progress. See [[long-term-memory-in-ai]].

> **RAG vs MCP scope**: The RAG survey addresses passive retrieval only. MCP (Paper 4 / [[model-context-protocol]]) extends context management to active operations (tool execution, write operations, state management). MCP subsumes RAG's retrieval function while adding broader capability.
