---
title: Capability Contortions
tags: [capability-contortions, jagged-AI, workarounds, AGI, engineering]
source: "2510.18212v3 — A Definition of AGI (Hendrycks et al., 2025)"
---

## Summary

"Capability contortions" is the term used in Hendrycks et al. (2025) to describe the engineering workarounds that allow AI systems to appear capable in domains where they have fundamental architectural deficits. Contortions produce useful products but mask genuine cognitive gaps — making the path to [[agi-definition|AGI]] harder to see clearly. The most prominent examples are using context windows as a substitute for [[long-term-memory-in-ai|Long-Term Memory Storage]] and using [[retrieval-augmented-generation|RAG]] to mask [[hallucination|hallucination]] from lack of genuine knowledge retrieval.

## Explanation

### The Core Idea

A capability contortion is an engineering technique that:
1. Addresses a *symptom* of a cognitive deficit
2. Produces useful behaviour in practice
3. Does **not** address the underlying architectural gap
4. May give a misleading signal about AI progress toward AGI

Contortions are not inherently wrong — they are often the right engineering choice for production systems. The problem arises when they are mistaken for genuine cognitive capability.

### Primary Contortions

#### Contortion 1: Context Window as Long-Term Memory

**The deficit**: LLMs have no intrinsic Long-Term Memory Storage (MS=0%).

**The workaround**: Use a very long context window (32K, 128K, even 1M tokens) to hold conversation history, relevant documents, and user preferences within a single session.

**Why it's a contortion**:
- Context window is Working Memory (WM), not LTM — session-scoped, not persistent
- Each new session starts blank
- The model doesn't "remember" — it re-reads information placed in context
- Performance degrades on content in the middle of very long contexts ("lost in the middle")

**The illusion**: A 128K-token context window makes the model *appear* to have memory because it can reference earlier parts of a long conversation. It cannot reference any prior session.

---

#### Contortion 2: RAG as Knowledge/Memory

**The deficit**: LLMs have knowledge cutoffs and unreliable fact retrieval (hallucination).

**The workaround**: [[retrieval-augmented-generation|RAG]] — retrieve relevant documents from an external corpus at query time and inject them into the context window.

**Why it's a contortion**:
- Retrieval is external; the model doesn't store or own the knowledge
- The model reads retrieved text from WM (context), not from intrinsic MS
- If RAG fails to retrieve the right document, the model still hallucinates
- RAG cannot update the model's beliefs or resolve internal contradictions

**The illusion**: RAG makes the model *appear* knowledgeable about recent events or proprietary documents. It doesn't change the model's intrinsic memory score.

---

#### Contortion 3: Tool Use as Reasoning/Calculation

**The deficit**: LLMs are poor at precise multi-step arithmetic and formal symbol manipulation.

**The workaround**: Give the model a calculator, code interpreter, or formal solver tool. The model calls the tool for computation rather than doing it internally.

**Why it's a contortion**:
- The model itself still cannot reliably do the computation
- The illusion of mathematical ability depends on the external tool
- In domains without tool access, the deficit reappears

---

#### Contortion 4: Prompting as Reasoning Enhancement

**The deficit**: LLMs fail at many reasoning tasks without explicit guidance.

**The workaround**: Chain-of-thought prompting, Tree-of-Thought, self-consistency — engineering prompt patterns that elicit better reasoning.

**Why this is partially (not fully) a contortion**:
- Some CoT improvement reflects genuine latent reasoning capacity being unlocked
- But structured prompting is doing cognitive work the model should do autonomously
- A truly reasoning system shouldn't need to be told "let's think step by step"

---

### The Jagged AI Profile

The combination of genuine strengths and contortion-masked weaknesses produces what the paper calls the **jagged AI profile**:

```
  100% ┤     ████████
       │     ████████  ████████
   75% ┤     ████████  ████████          ████████ ████████
       │     ████████  ████████          ████████ ████████ ████████
   50% ┤     ████████  ████████ ████████ ████████ ████████ ████████
       │     ████████  ████████ ████████ ████████ ████████ ████████ ████████
   25% ┤ ... ████████  ████████ ████████ ████████ ████████ ████████ ████████ ████████
       │     ████████  ████████ ████████ ████████ ████████ ████████ ████████ ████████
    0% ┤     K         RW       M        R        WM       MS       MR       V    A  S
                                                           ↑
                                                    MISSING ENTIRELY
```

GPT-5 scores ~57% overall but 0% on MS — the profile is not uniformly "below human" but missing a critical domain entirely.

### Implications for AGI Measurement

1. **Benchmark contamination**: Contortions can inflate benchmark scores without genuine capability improvement
2. **Progress misreading**: Improving a contortion (better RAG) looks like AGI progress but doesn't change the underlying CHC score
3. **Safety blind spots**: A system that appears capable due to contortions may fail in ways that reveal the underlying deficit in unexpected contexts
4. **Research misdirection**: Optimising contortions rather than addressing root architectural gaps

### What Genuine Progress Looks Like

Instead of better RAG → genuine LTM Storage (MS)
Instead of longer context → genuine WM expansion with reliable retrieval
Instead of CoT prompting → intrinsic fluid reasoning (R)

## Related Pages

- [[agi-definition]] — contortions affect composite AGI score measurement
- [[long-term-memory-in-ai]] — the primary contortion target
- [[retrieval-augmented-generation]] — RAG is both useful and a contortion
- [[in-context-learning]] — context window usage as WM substitute
- [[hallucination]] — what RAG contortion is masking
- [[cognitive-capabilities-framework]] — the domains where contortions are applied
- [[large-language-models]] — the systems using these contortions
- [[scaling-laws]] — scaling alone doesn't fix the contorted domains

## Contradictions

> **RAG survey vs AGI paper**: The RAG survey (Paper 3) presents RAG as a solution to knowledge limitations and hallucination — a mature, production-ready approach. The AGI paper (Paper 5) frames the same RAG as an engineering contortion that masks fundamental architectural deficits. These aren't strictly contradictory (RAG is useful AND a contortion) but represent fundamentally different evaluation frameworks: engineering utility vs cognitive architecture.

> **Context window progress**: The LLM survey (Paper 2) describes longer context windows as a major capability improvement. The AGI paper recognises this as WM improvement only — not MS improvement. In the AGI framework, a million-token context window improves the WM score, not the MS score (which stays at 0%).
