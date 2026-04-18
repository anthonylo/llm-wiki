---
title: Long-Term Memory in AI
tags: [long-term-memory, memory-storage, MS, bottleneck, AGI]
sources:
  - "2312.10997v5 — RAG Survey"
  - "2510.18212v3 — A Definition of AGI"
---

## Summary

Long-Term Memory Storage (MS) is the ability to encode, retain, and reliably retrieve information over extended periods — across sessions, without retraining. It is rated **0%** for both GPT-4 and GPT-5 in the [[agi-definition|AGI CHC framework]], making it the single largest bottleneck on the path to AGI. Current systems compensate with external workarounds ([[retrieval-augmented-generation|RAG]], [[model-context-protocol|MCP]]) that provide the *appearance* of memory without genuine cognitive storage.

## Explanation

### What Long-Term Memory Requires

True MS involves three processes:
1. **Encoding**: Taking new information encountered during operation and storing it in a persistent form
2. **Consolidation**: Integrating new information with existing knowledge; updating beliefs based on new evidence
3. **Retrieval**: Accurately recalling specific stored information on demand, even after long intervals

Human long-term memory consolidates during sleep, degrades gracefully, and supports episodic (what happened), semantic (facts), and procedural (skills) memory.

### Why Current LLMs Have 0% MS

| Mechanism | What It Looks Like | Why It's Not MS |
|-----------|-------------------|----------------|
| **Training weights** | Vast world knowledge | Frozen at training cutoff; cannot be updated in deployment |
| **Context window** | Holds conversation history | Session-scoped; cleared after each session. This is Working Memory (WM), not LTM |
| **RAG** | External vector store | External scaffolding; not intrinsic to the model; model doesn't "know" what's in it |
| **Fine-tuning** | Adapts weights to new domain | Batch process; not real-time encoding; causes catastrophic forgetting |

The key criterion: **can the model, during normal operation, encode a new fact and reliably retrieve it in a future session without any external intervention?** Answer: No.

### The Working Memory Confusion

A common misconception: long context windows (200K tokens in some models) are "memory." They are not:

- Context window = Working Memory (WM): temporary, active, session-scoped
- Long-Term Memory Storage (MS): persistent, passive, survives across sessions

Using longer context windows to compensate for lack of LTM is a [[capability-contortions|capability contortion]] — it patches the symptom (can't remember across turns) without addressing the root cause (no storage mechanism).

### External Memory Workarounds

The industry has developed workarounds that approximate LTM:

**Retrieval-Augmented Generation (RAG)**
- Store facts as embeddings in a [[vector-databases-and-embeddings|vector database]]
- Retrieve relevant facts at query time
- The LLM reads retrieved facts from context (WM) rather than retrieving from intrinsic MS
- Limitation: RAG is passive; can't update beliefs or resolve contradictions autonomously

**[[model-context-protocol|MCP]] Memory Servers**
- Persist conversation history and facts to a database
- Retrieve at session start via MCP resource primitives
- Same fundamental issue: LLM reads from context; storage is external

**Episodic Memory Systems** (e.g., MemGPT, A-MEM)
- Explicitly manage memory tiers (working, episodic, archival)
- LLM itself calls "memory write" and "memory read" tools
- Closer to true MS behaviour but still architectural scaffolding

**Continual Learning Research**
- Active research area: train models that can learn new facts without catastrophic forgetting
- Elastic Weight Consolidation (EWC), Progressive Neural Networks, Hypernetworks
- Not yet production-viable for frontier LLMs

### Consequences of MS=0%

1. **Hallucination**: Without reliable memory storage, models resort to distributional pattern matching → [[hallucination]]
2. **Personalisation ceiling**: Models cannot remember users across sessions without explicit re-injection of history
3. **Knowledge drift**: Models' knowledge becomes increasingly stale without periodic retraining
4. **Compound reasoning failures**: Multi-session reasoning tasks (e.g., "remember our plan from last week") fail
5. **AGI gap**: MS=0% prevents reaching AGI definition threshold regardless of improvements elsewhere

### What Architectural MS Would Look Like

A system with genuine MS would:
- During a conversation, encounter a new fact → write it to a persistent key-value or vector store linked to the model's "identity"
- In the next session (days later), without any re-injection of history, naturally recall: "Oh, you told me last week that X"
- Update its beliefs when given contradicting new information: "I thought X, but now I know Y"
- Not require a human to manage memory explicitly

No current production LLM does this.

## Related Pages

- [[agi-definition]] — MS=0% is the biggest AGI bottleneck; AGI requires 100%
- [[cognitive-capabilities-framework]] — MS is domain #6 of 10
- [[capability-contortions]] — the workarounds used to mask MS=0%
- [[retrieval-augmented-generation]] — the primary external memory workaround
- [[model-context-protocol]] — MCP memory servers provide external persistence
- [[hallucination]] — a direct consequence of MS=0%
- [[in-context-learning]] — uses context window (WM) not long-term memory (MS)
- [[large-language-models]] — the systems lacking MS

## Contradictions

> **RAG as memory vs RAG as workaround**: The RAG survey (Paper 3) positions RAG as solving knowledge retrieval — implying memory. The AGI paper (Paper 5) explicitly scores RAG as non-MS, noting it's external scaffolding. This is not a factual contradiction — both papers can be correct — but the framing has practical consequences: teams that believe RAG provides "memory" may underestimate architectural gaps.

> **Context window progress**: The LLM survey (Paper 2) highlights increasing context window sizes (4K → 128K → 1M tokens) as a significant capability improvement. The AGI paper scores long context windows as WM progress, not MS progress. The absolute size of the context window does not affect the MS score at all — even a 1M-token context window is still Working Memory, not Long-Term Memory Storage.
