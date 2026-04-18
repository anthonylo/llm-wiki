---
title: Hallucination in LLMs
tags: [hallucination, factuality, faithfulness, reliability]
sources:
  - "2307.06435v10 — A Comprehensive Overview of Large Language Models"
  - "2312.10997v5 — RAG Survey"
  - "2510.18212v3 — A Definition of AGI"
---

## Summary

Hallucination refers to the generation of text that is fluent and confident but factually incorrect, unsupported by source documents, or outright fabricated. It is one of the most critical limitations of [[large-language-models]] and a primary motivation for [[retrieval-augmented-generation]]. The AGI paper frames hallucination as evidence of deep architectural gaps — not merely a fixable bug.

## Explanation

### Types of Hallucination

**Intrinsic Hallucination**
The model's output contradicts the provided source document. Example: asked to summarise a passage, the model introduces facts not in the passage.

**Extrinsic Hallucination**
The model's output cannot be verified from any source — neither confirming nor denying. Example: inventing a citation that doesn't exist.

**Factual Hallucination**
The model states something that is factually false in the real world:
- Wrong dates, names, statistics
- Fabricated citations and papers
- Incorrect technical explanations

**Self-Contradiction**
The model contradicts itself within a single response (less studied but common in long-form generation).

### Root Causes

| Cause | Description |
|-------|-------------|
| Training data noise | False claims exist in the training corpus |
| Distributional gaps | Model extrapolates poorly to rare or out-of-distribution facts |
| Decoding dynamics | Temperature/nucleus sampling can steer away from factual tokens |
| Sycophancy | Model tells users what they want to hear |
| Knowledge cutoff | Post-training facts are absent from weights |
| Overconfidence | Model doesn't calibrate uncertainty well |

### Hallucination Detection

Approaches for automated detection:
- **Natural Language Inference (NLI)**: Check if model output is entailed by source
- **QA-based**: Generate questions from output; verify answers against source
- **LLM-as-judge**: Use a second LLM to rate factual consistency
- **Self-consistency**: Sample multiple outputs; flag disagreements
- RAGAS framework includes faithfulness and answer relevance metrics

### Mitigation Strategies

| Strategy | Mechanism | Limitation |
|----------|-----------|------------|
| [[retrieval-augmented-generation|RAG]] | Ground generation in retrieved documents | Retrieved docs may themselves be wrong |
| Fine-tuning on factual data | Encode more facts in weights | Doesn't help for unseen facts |
| [[rlhf-and-alignment|RLHF]] | Reward factual, refuse uncertain | Reward hacking; doesn't solve knowledge gaps |
| Chain-of-thought | Forces reasoning steps | Can hallucinate reasoning steps |
| Citations / grounding | Require references in output | Model may still fabricate citations |
| Temperature=0 | Greedy decoding | Reduces variety; doesn't eliminate hallucination |

### Hallucination in RAG Systems

Even with retrieved context, LLMs can:
- **Ignore context**: Generate from parametric memory despite contradicting retrieved text
- **Misinterpret context**: Misread the retrieved passage
- **Context-conditioned hallucination**: Invent plausible extensions beyond what the retrieved text says

The RECALL benchmark specifically tests knowledge conflict handling: what happens when retrieved context contradicts the model's parametric knowledge?

### The AGI Perspective

The AGI paper (Paper 5) frames hallucination as evidence that current models lack genuine **knowledge** as a cognitive domain. Models with poor intrinsic Long-Term Memory Storage (MS=0% for GPT-4 and GPT-5) resort to probabilistic pattern-matching over training distribution rather than retrieving stored facts reliably. This is why RAG helps but doesn't fundamentally solve the problem.

> "Using RAG to patch hallucination is like adding an external hard drive to compensate for having no memory — useful, but not intelligence." — paraphrased from [[capability-contortions]]

## Related Pages

- [[retrieval-augmented-generation]] — primary architectural mitigation for hallucination
- [[rag-paradigms]] — Advanced/Modular RAG's post-retrieval steps target hallucination
- [[large-language-models]] — hallucination is a core LLM limitation
- [[rlhf-and-alignment]] — alignment reduces sycophancy and some hallucination types
- [[long-term-memory-in-ai]] — lack of LTM storage is the root architectural cause
- [[capability-contortions]] — AGI paper argues RAG is a contortion masking fundamental hallucination causes
- [[agi-definition]] — Knowledge (K) is a separate cognitive domain; hallucination indicates failure here

## Contradictions

> **RAG as solution vs RAG as workaround**: The RAG survey (Paper 3) treats RAG as a sufficient and mature mitigation for hallucination in production systems. The AGI paper (Paper 5) argues that RAG does not address the root cause — the model's inability to genuinely store and retrieve facts from long-term memory. Both positions are valid at different levels of analysis: RAG is useful in practice, but doesn't constitute genuine memory.
