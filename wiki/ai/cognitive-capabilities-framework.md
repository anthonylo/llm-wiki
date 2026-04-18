---
title: Cognitive Capabilities Framework (CHC Theory for AI)
tags: [CHC, cognitive-domains, AGI, intelligence-measurement]
source: "2510.18212v3 — A Definition of AGI (Hendrycks et al., 2025)"
---

## Summary

The Cattell-Horn-Carroll (CHC) theory of cognitive abilities is the dominant psychometric framework for understanding human intelligence. Hendrycks et al. (2025) adapt it to measure AI systems, providing an operationalised scorecard for tracking progress toward [[agi-definition|AGI]]. Each of the 10 cognitive domains has specific AI benchmarks that can be used to estimate proficiency.

## Explanation

### CHC Theory Origins

CHC theory integrates:
- **Cattell's Fluid-Crystallised Intelligence (Gf-Gc)**: Fluid (novel problem-solving) vs crystallised (accumulated knowledge)
- **Horn's extended model**: Additional domains beyond Gf-Gc
- **Carroll's three-stratum theory**: Hierarchical factor structure from large meta-analysis

The theory identifies ~10 broad cognitive abilities and ~70 narrow abilities. It is the foundation of most modern IQ assessments (WAIS, WJ-IV, etc.).

### The 10 Domains Applied to AI

#### 1. Crystallised Knowledge (K) — Intelligence Quotient: ~60–80%

**What it measures**: Accumulated knowledge acquired through experience and learning.

In humans: general knowledge, vocabulary, cultural literacy, procedural knowledge.

In AI benchmarks:
- MMLU (Massive Multitask Language Understanding): 57 subjects from STEM to humanities
- TriviaQA, NaturalQuestions
- ARC (AI2 Reasoning Challenge)

**Status**: Strong. LLMs excel at knowledge recall. GPT-4 achieves human expert levels on many knowledge benchmarks.

---

#### 2. Reading/Writing (RW) — ~70–85%

**What it measures**: Comprehension, fluent reading, coherent writing, language processing.

In AI benchmarks:
- Reading comprehension: SQuAD, RACE, QuALITY
- Writing quality: WinoBias, WritingPrompts evaluations
- Summarisation: CNN/DailyMail, XSum

**Status**: Very strong. LLMs often exceed average human writing quality.

---

#### 3. Mathematics (M) — ~55–70%

**What it measures**: Quantitative reasoning, numerical operations, mathematical problem-solving.

In AI benchmarks:
- GSM8K: grade-school math word problems
- MATH: competition mathematics
- AIME / AMC benchmarks

**Status**: Improving rapidly. GPT-4 struggles with multi-step symbolic reasoning; GPT-5 shows significant improvement with chain-of-thought. See [[scaling-laws]].

---

#### 4. Reasoning (R) — ~60–75%

**What it measures**: Fluid intelligence — deductive, inductive, and abductive reasoning. Novel problem-solving without relying on prior knowledge.

In AI benchmarks:
- BIG-Bench Hard (BBH)
- LogiQA, ReClor
- ARC-Challenge
- LSAT, GRE logical reasoning

**Status**: Moderate to good. CoT prompting significantly improves fluid reasoning. See [[in-context-learning]].

---

#### 5. Working Memory (WM) — ~45–65%

**What it measures**: Short-term capacity to hold and manipulate information during active processing.

In AI benchmarks:
- Multi-hop reasoning requiring tracking of intermediate state
- Context tracking across long documents
- BabiQ tasks

**AI mechanism**: The context window serves as working memory. Performance degrades for "lost-in-the-middle" items in long contexts.

**Status**: Limited by context window length and positional degradation. See [[long-term-memory-in-ai]].

---

#### 6. Long-Term Memory Storage (MS) — **0%** ⚠️

**What it measures**: The ability to encode, consolidate, and reliably retrieve information over extended time periods — across days, weeks, years.

In AI benchmarks:
- Persistent memory across sessions
- Updating knowledge without full retraining
- Continual learning without catastrophic forgetting

**AI mechanism**: LLMs have none of this intrinsically. Training weights encode knowledge but cannot be updated in deployment. Context window is session-scoped. [[retrieval-augmented-generation|RAG]] is external scaffolding.

**Status**: **0% for both GPT-4 and GPT-5** — the single biggest AGI bottleneck.

See [[long-term-memory-in-ai]] for full analysis.

---

#### 7. Long-Term Memory Retrieval (MR) — GPT-4: 4%, GPT-5: 4%

**What it measures**: The fluency and precision with which stored knowledge can be accessed. Includes retrieval fluency (speed of generating ideas, associations, solutions) and retrieval precision (accuracy — specifically, avoiding hallucination/confabulation).

In AI benchmarks:
- Ideational and expressional fluency tasks
- Word and naming fluency
- Hallucination detection benchmarks
- TruthfulQA, FaithDial (confabulation avoidance)

**Status**: Both GPT-4 and GPT-5 score only 4%. Models can rapidly retrieve many concepts from parameters but **frequently hallucinate** — a critical failure of retrieval precision. RAG is flagged as a [[capability-contortions|capability contortion]] that masks this weakness rather than solving it.

---

#### 8. Visual Processing (V) — GPT-4: 0%, GPT-5: 4%

**What it measures**: Perceiving, analyzing, reasoning about, and generating visual information. Includes perception (image recognition, captioning, anomaly detection), visual generation (image/video synthesis), visual reasoning (mental rotation, folding, spatial logic, embodied reasoning, chart understanding), and spatial scanning.

In AI benchmarks:
- MMBench, MMMU (visual QA)
- Mental rotation and spatial folding tasks
- Image captioning (COCO)
- Chart and diagram understanding

**Status**: GPT-4 scores 0% (no visual processing). GPT-5 scores 4% (appreciable but incomplete). Visual reasoning (spatial logic, mental rotation) remains significantly below human performance.

---

#### 9. Auditory Processing (A) — GPT-4: 0%, GPT-5: 6%

**What it measures**: Capacity to discriminate, recognise, and work with auditory stimuli — phonetics, speech, rhythm, and music. Includes phonetic coding, speech recognition (audio→text), voice quality (natural synthesis), rhythmic ability, and musical judgment.

In AI benchmarks:
- LibriSpeech (ASR — speech recognition)
- Phoneme discrimination and blending tasks
- Voice naturalness / conversational fluidity
- Rhythm and musical pattern recognition

**Status**: GPT-4 scores 0% (no audio processing). GPT-5 scores 6% (speech recognition at ~4%, voice generation improving; rhythm and musical judgment remain weak).

---

#### 10. Speed (S) — GPT-4: 3%, GPT-5: 3%

**What it measures**: The ability to perform simple cognitive tasks quickly — perceptual speed, reaction times, and processing fluency.

In AI benchmarks:
- Reading speed (text processing rate with comprehension)
- Writing speed (text generation rate)
- Number facility (speed of basic arithmetic)
- Simple and choice reaction time
- Perceptual scanning and comparison speed
- Pointer fluency (accurate pointer movement — requires visual processing)

**Status**: Both GPT-4 and GPT-5 score 3%. Models can read, write, and compute simple expressions quickly, but several speed tasks require multimodal processing (visual + motor) where current models are slow. GPT-5 often enters extended "thinking" mode which further reduces speed scores.

**Note**: Social intelligence is not a separate domain in CHC theory. Theory of mind is measured under **Reasoning (R)** (theory of mind sub-domain). Cognitive empathy is part of **General Knowledge (K)** commonsense. Facial emotion recognition falls under **Visual Processing (V)**.

---

### Summary Scorecard (from paper)

| Domain | GPT-4 | GPT-5 | AGI Target |
|--------|-------|-------|------------|
| K (General Knowledge) | 8% | 9% | 100% |
| RW (Reading/Writing) | 6% | 10% | 100% |
| M (Mathematics) | 4% | 10% | 100% |
| R (Reasoning) | 0% | 7% | 100% |
| WM (Working Memory) | 2% | 4% | 100% |
| **MS (LT Memory Storage)** | **0%** | **0%** | **100%** |
| MR (LT Memory Retrieval) | 4% | 4% | 100% |
| V (Visual Processing) | 0% | 4% | 100% |
| A (Auditory Processing) | 0% | 6% | 100% |
| S (Speed) | 3% | 3% | 100% |
| **Composite** | **27%** | **57%** | **100%** |

## Related Pages

- [[agi-definition]] — how these domains combine into an AGI definition
- [[long-term-memory-in-ai]] — the MS=0% bottleneck
- [[capability-contortions]] — workarounds for the domains where AI scores poorly
- [[hallucination]] — manifestation of weak K and MS scores
- [[rlhf-and-alignment]] — improves perceived helpfulness and social behaviour, but not measured as a separate CHC domain
- [[large-language-models]] — the systems being scored

## Contradictions

> **RLHF improves social intelligence, not memory**: RLHF (Paper 2) significantly improves perceived helpfulness, safety, and social alignment — all components of S. But it has zero effect on MS. Models that appear more intelligent due to RLHF may not actually score higher on the CHC composite.
