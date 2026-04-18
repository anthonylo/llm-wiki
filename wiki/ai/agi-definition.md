---
title: AGI Definition (CHC Framework)
tags: [AGI, CHC-theory, cognitive-capabilities, benchmark]
source: "2510.18212v3 — A Definition of AGI (Hendrycks et al., 2025)"
---

## Summary

Hendrycks et al. (2025) propose a formal, measurable definition of Artificial General Intelligence (AGI) grounded in the Cattell-Horn-Carroll (CHC) theory of human cognitive abilities. Rather than a vague "human-level AI" threshold, they define AGI as a system scoring ≥100% across 10 CHC-derived cognitive domains. Current frontier models score 27% (GPT-4) to 57% (GPT-5), with Long-Term Memory Storage as the most critical bottleneck (0% for both).

## Explanation

### Why a New Definition?

Existing AGI definitions suffer from:
- **Vagueness**: "pass the Turing test," "match human performance" — operationally undefined
- **Task-centricity**: Benchmark-passing doesn't imply general intelligence
- **Moving goalposts**: As models pass benchmarks, benchmarks are dismissed
- **Anthropocentric bias**: Human-level is one threshold, not the only meaningful one

Hendrycks et al. ground their definition in CHC theory — the most validated and widely used framework in human cognitive psychology.

### The CHC Cognitive Framework

CHC theory identifies broad cognitive domains from psychometric research on human intelligence:

| Domain Code | Domain Name | Description |
|-------------|-------------|-------------|
| **K** | General Knowledge | Commonsense, science, social science, history, culture |
| **RW** | Reading/Writing | Language comprehension and text production |
| **M** | Mathematics | Arithmetic, algebra, geometry, probability, calculus |
| **R** | On-the-Spot Reasoning | Deduction, induction, theory of mind, planning, adaptation |
| **WM** | Working Memory | Hold and manipulate information across modalities |
| **MS** | Long-Term Memory Storage | Encode, consolidate, and store new information from experience |
| **MR** | Long-Term Memory Retrieval | Fluency and precision of accessing stored knowledge |
| **V** | Visual Processing | Perception, generation, reasoning, spatial scanning |
| **A** | Auditory Processing | Speech, phonetics, voice, rhythm, music |
| **S** | Speed | Perceptual speed, reaction time, processing fluency |

### Current Model Scores

| Model | K | RW | M | R | WM | **MS** | MR | V | A | S | **Total** |
|-------|---|----|---|---|----|--------|----|---|---|---|-----------|
| GPT-4 | 8% | 6% | 4% | 0% | 2% | **0%** | 4% | 0% | 0% | 3% | **27%** |
| GPT-5 | 9% | 10% | 10% | 7% | 4% | **0%** | 4% | 4% | 6% | 3% | **57%** |

Domain key: K=General Knowledge, RW=Reading/Writing, M=Mathematics, R=Reasoning, WM=Working Memory, MS=Long-Term Memory Storage, MR=Long-Term Memory **Retrieval**, V=Visual Processing, A=Auditory Processing, S=**Speed**

### The AGI Threshold

AGI is defined as **≥100% across all 10 domains simultaneously**. This is a conjunctive threshold — a system that excels at 9 domains but fails at MS cannot be AGI.

The authors deliberately use ≥100% rather than "human average" to capture superhuman performance in most domains that current AI already exhibits in some areas.

### Long-Term Memory Storage (MS) — The Critical Bottleneck

**MS is rated 0% for both GPT-4 and GPT-5.** This is the most significant finding.

An LLM has:
- Training knowledge (frozen at training cutoff) — not MS (cannot be updated post-training)
- Context window (temporary, session-scoped) — WM (working memory), not MS
- RAG (external vector store) — external scaffolding, not intrinsic MS

True MS requires:
- **Encoding**: Taking new information during deployment and storing it
- **Retention**: Persisting it across sessions without retraining
- **Retrieval**: Accurately retrieving stored information on demand

Current LLMs fail all three intrinsically.

### The Jagged AI Profile

Current AI has a highly uneven ("jagged") cognitive profile:
- Superhuman in K, RW, and some reasoning domains
- Near-human in working memory (WM)
- Completely absent in MS (0%)
- Weak in spatial/visual reasoning (MR, V)

This jaggedness is why AI seems simultaneously impressive (GPT-5 writes better than most humans) and failures (can't remember a conversation from yesterday). The profile is not uniformly "below human" but uneven in ways that matter.

### AGI Taxonomy

The paper also defines a spectrum beyond AGI:

| Level | Description |
|-------|-------------|
| **Pandemic AI** | AI that can independently cause a pandemic-scale catastrophe |
| **Cyberwarfare AI** | AI with nation-state level offensive cyber capabilities |
| **Self-Sustaining AI** | AI that can autonomously acquire resources to sustain itself |
| **AGI** | ≥100% across all 10 CHC cognitive domains |
| **Recursive AI** | AI that can meaningfully improve its own AI capabilities |
| **Superintelligence** | AI that vastly exceeds human performance across all domains |
| **Replacement AI** | AI capable of fully replacing human economic activity |

Notably, Pandemic AI and Cyberwarfare AI may be reached *before* AGI — dangerous capability precedes general capability.

## Related Pages

- [[cognitive-capabilities-framework]] — detailed breakdown of the 10 CHC domains
- [[long-term-memory-in-ai]] — MS=0% is the defining bottleneck
- [[capability-contortions]] — workarounds that mask the MS gap
- [[large-language-models]] — current LLMs scored in this framework
- [[emergent-abilities]] — emergence may drive sudden jumps in domain scores
- [[scaling-laws]] — whether scaling alone closes the remaining 43% gap (GPT-5 at 57%)
- [[hallucination]] — manifestation of low K and MS scores
- [[retrieval-augmented-generation]] — external memory that doesn't count as intrinsic MS

## Contradictions

> **RAG ≠ Memory Storage**: The RAG survey (Paper 3) presents RAG as solving knowledge retrieval. The AGI paper explicitly excludes RAG from MS scoring — external memory scaffolding doesn't constitute genuine cognitive memory storage. This is the central tension between practical AI engineering and theoretical AGI measurement.

> **Scaling to AGI**: The LLM survey (Paper 2) implies that continued scaling + RLHF + improved training will progressively improve all capabilities. The AGI paper shows that two generations of frontier models (GPT-4 → GPT-5) improved most domains but MS remained at 0%. This suggests that simple scaling may not close the MS gap without architectural innovation.
