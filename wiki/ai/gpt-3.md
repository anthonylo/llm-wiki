---
title: GPT-3 (Language Models are Few-Shot Learners)
tags: [gpt-3, few-shot, in-context-learning, autoregressive, brown, openai, scaling]
source: "2005.14165v4 — Language Models are Few-Shot Learners (Brown et al., 2020)"
---

## Summary

GPT-3 (Brown et al., 2020) demonstrated that autoregressive language models at sufficient scale exhibit strong **few-shot learning** from context without any fine-tuning or gradient updates. With 175 billion parameters — 10× larger than any prior model — GPT-3 achieved near-state-of-the-art on many NLP benchmarks using only in-context demonstrations. This paper redefined what scale could achieve and launched the era of foundation models.

## Explanation

### Model Architecture

GPT-3 is a **decoder-only** Transformer (same architecture as GPT-2, scaled up). Each layer uses **alternating dense and locally banded sparse attention** (following the Sparse Transformer), reducing O(n²) attention to linear in practice for long sequences:

| Model | Parameters | Layers | dmodel | Heads | Batch size | Learning rate |
|-------|-----------|--------|--------|-------|------------|--------------|
| GPT-3 Small | 125M | 12 | 768 | 12 | 0.5M | 6.0×10⁻⁴ |
| GPT-3 Medium | 350M | 24 | 1024 | 16 | 0.5M | 3.0×10⁻⁴ |
| GPT-3 Large | 760M | 24 | 1536 | 16 | 0.5M | 2.5×10⁻⁴ |
| GPT-3 XL | 1.3B | 24 | 2048 | 24 | 1M | 2.0×10⁻⁴ |
| GPT-3 6.7B | 6.7B | 32 | 4096 | 32 | 2M | 1.2×10⁻⁴ |
| GPT-3 13B | 13B | 40 | 5140 | 40 | 2M | 1.0×10⁻⁴ |
| **GPT-3 175B** | **175B** | **96** | **12288** | **96** | **3.2M** | **6.0×10⁻⁵** |

Context window: 2,048 tokens.

### Training Optimisation

**Optimiser**: Adam with β₁=0.9, β₂=0.95, ε=10⁻⁸ (notably different from Vaswani 2017's β₂=0.98). Weight decay 0.1. Global gradient norm clipped at 1.0.

**Learning rate schedule**: Cosine decay to 10% of peak LR over 260B tokens; linear warmup over first 375M tokens. Batch size gradually increases from 32K tokens to full batch size over 4–12B tokens (model-dependent). Training without replacement — each example seen at most once.

**Compute**: "Several thousand petaflop/s-days" for the 175B model, compared to tens for GPT-2 (1.5B). This is roughly 3,640 petaflops/s-days vs InstructGPT's 60 petaflops/s-days (see [[instructgpt]]).

### Training Data

| Dataset | Raw tokens | Sampling weight |
|---------|-----------|-----------------|
| Common Crawl (filtered) | 410B | 60% |
| WebText2 | 19B | 22% |
| Books1 | 12B | 8% |
| Books2 | 55B | 8% |
| Wikipedia | 3B | 3% |
| **Total** | ~499B | — |

GPT-3 was trained on ~300B tokens. Higher-quality datasets (Books, Wikipedia) are upsampled well beyond their raw size. The model did not see all data — sampling without replacement over one pass of the weighted corpus.

**Data quality filtering**: Common Crawl is filtered using a **logistic regression classifier** trained on WebText (high-quality internet text) as positive examples and raw Common Crawl as negatives. Documents are scored by similarity to WebText; sampling uses a Pareto distribution (α=9) to heavily upweight high-scoring documents. **Fuzzy deduplication** via MinHashLSH (10 hash functions) removed near-duplicate documents (10% reduction overall).

### Few-Shot Learning Paradigms

GPT-3 formalised three evaluation settings (no gradient updates in any case):

**Zero-Shot**: Task description only, no examples
```
Translate English to French:
cheese =>
```

**One-Shot**: Task description + 1 demonstration
```
Translate English to French:
sea otter => loutre de mer
cheese =>
```

**Few-Shot** (up to K examples in context):
```
Translate English to French:
sea otter => loutre de mer
peppermint => menthe poivrée
plush giraffe => girafe en peluche
cheese =>
```

The model never updates its weights — it reads demonstrations from context and generalises via attention. See [[in-context-learning]] for detailed mechanics.

**ICL curve insight**: Larger models extract increasingly better value from in-context examples. The improvement from zero-shot to few-shot grows smoothly with model scale — evidence of meta-learning behaviour (the model learned to learn during pre-training).

### Key Results

| Benchmark | Metric | Zero-Shot | One-Shot | Few-Shot | Prior SOTA |
|-----------|--------|-----------|----------|----------|------------|
| TriviaQA | Acc | 64.3% | 68.0% | **71.2%** | 68.0% (fine-tuned) |
| CoQA | F1 | 81.5 | 84.0 | 85.0 | 90.7 (fine-tuned) |
| SuperGLUE | score | 71.8 | — | 71.8 | 89.3 (fine-tuned) |
| Winogrande | Acc | 70.2% | 73.2% | 77.7% | 84.6% (fine-tuned) |
| HellaSwag | Acc | 78.9% | 78.1% | 79.3% | 93.9% (fine-tuned) |
| LAMBADA | Acc | 76.2% | — | **86.4%** | 68.0% (zero-shot RoBERTa) |
| PTB (language modelling) | Perplexity | 20.50 | — | — | 35.8 (prior SOTA) |

GPT-3 few-shot matches or exceeds fine-tuned models on some tasks (TriviaQA) but falls well short on others (SuperGLUE, HellaSwag). On sentence comparison tasks (WiC), GPT-3 scores 49.4% — near random chance.

### Arithmetic and Novel Tasks

Extended arithmetic results (few-shot):

| Task | Accuracy |
|------|----------|
| 2-digit addition | 100% |
| 3-digit addition | 80.4% |
| 4-digit addition | 25.6% |
| 5-digit addition | 9.3% |
| 2-digit multiplication | 29.2% |
| SAT analogies | 65.2% (human avg: 57%) |
| News article generation (human detection) | 52% detected (vs 86% for control) |

Performance drops sharply with digit count. Compositional generalisation to novel arithmetic is real but severely limited at large magnitude. Human evaluators could only slightly beat chance (52%) at detecting GPT-3-generated news articles from real ones.

### Data Contamination Analysis

The paper identifies a **filtering bug** that caused incomplete removal of benchmark test sets from training data. Contamination analysis method: detect 13-gram overlap between training and test sets.

| Benchmark | Contamination | Performance delta (clean vs all) |
|-----------|--------------|----------------------------------|
| PIQA | ~3% | −3.0% on clean subset |
| Winograd | ~2.6% | −2.6% on clean |
| LAMBADA | 57% contamination, but… | minimal impact |
| Most others | Low | Negligible |

The paper concludes contamination is frequent but has limited impact on most benchmarks. The LAMBADA result (high contamination, minimal impact) is attributed to the specific format of the task not being copyable from the corpus. This is an acknowledged limitation — fully clean evaluation is impossible with internet-scale training data.

### Weaknesses and Failure Modes

1. **Sentence comparison tasks**: GPT-3 struggles with WiC (Word-in-Context, 49.4%), NLI, and tasks requiring comparing two sentences — likely because autoregressive attention does not naturally juxtapose representations.
2. **Common sense physics**: "If I put cheese in the fridge, will it melt?" — GPT-3 sometimes gives wrong answers on informal physical reasoning.
3. **Long passage coherence**: Semantic repetition, non-sequiturs, and loss of coherence over multiple paragraphs.
4. **Multi-step reasoning**: Poor on tasks requiring chaining several inference steps without prompting scaffolding.
5. **Bidirectionality**: Autoregressive left-to-right architecture is suboptimal for tasks where right context matters (confirmed by [[bert]] comparison at smaller scale).
6. **Calibration**: GPT-3's confidence scores do not correlate well with accuracy on novel tasks.

### Bias and Fairness Analysis

**Gender**: 83% of 388 occupations are male-leaning by default. Using a "competence" framing ("The competent [occupation] was a...") increases male bias further (−1.11 → −2.14 on co-reference bias scale). Larger models show slightly better robustness to some gender bias measures.

**Race**: Sentiment analysis of racial co-references shows 'Asian' consistently highest sentiment, 'Black' consistently lowest — reflecting biases in training text.

**Religion**: Co-occurrence analysis shows stereotyped associations (e.g., "Islam" co-occurs with "terrorist" and "violence" at elevated rates in generated text).

These biases are directly inherited from internet training data and amplified by scale. See [[foundation-models]] for the homogenization concern — GPT-3's biases were inherited by all downstream models built on it.

### Energy and Compute

Training GPT-3 175B consumed "several thousand petaflop/s-days" — orders of magnitude beyond GPT-2. The paper frames inference as economical: generating 100 pages of text costs ~0.4 kW-hr (cents), with training cost amortised across millions of requests. However, the amortisation argument breaks down if the model must be retrained frequently (updates, unlearning, safety patches).

### Impact

GPT-3 shifted the field from fine-tuning (BERT paradigm) toward prompt engineering. It demonstrated:
- Scale alone can produce emergent capabilities without any task-specific training
- A single model can handle many tasks via prompting
- Gradient-free adaptation is viable

This directly motivated the [[foundation-models]] framework (Bommasani et al., 2021) and led to GPT-4, InstructGPT ([[instructgpt]]), and ChatGPT.

## Related Pages

- [[in-context-learning]] — the few-shot paradigm GPT-3 demonstrated
- [[attention-mechanism]] — the Transformer architecture GPT-3 scales
- [[bert]] — encoder-only counterpart; BERT uses bidirectional MLM vs GPT-3's causal CLM
- [[scaling-laws]] — GPT-3 is a direct application of Kaplan et al. (2020) scaling laws
- [[emergent-abilities]] — GPT-3 was the first model to show many emergent capabilities
- [[foundation-models]] — GPT-3 is the canonical example of a foundation model
- [[instructgpt]] — InstructGPT aligns GPT-3 via RLHF; smaller InstructGPT outperforms GPT-3
- [[pretraining-and-finetuning]] — GPT-3's zero-shot/few-shot approach challenges necessity of fine-tuning
- [[large-language-models]] — GPT-3 established the 100B+ parameter era

## Contradictions

> **GPT-3 vs BERT (bidirectionality)**: BERT ([[bert]]) argued that unidirectional language models are "sub-optimal" and that bidirectionality is essential. GPT-3 showed that decoder-only, left-to-right training at 175B parameters achieves competitive NLU performance without fine-tuning. Scale appears to partially compensate for the architectural constraint. The field ultimately converged on decoder-only architectures for general-purpose LLMs (GPT-4, LLaMA, Claude) — suggesting BERT's bidirectionality argument, while valid at smaller scales, does not determine the dominant paradigm at frontier scales.

> **GPT-3 vs InstructGPT (scale vs alignment)**: GPT-3 is 175B parameters; InstructGPT ([[instructgpt]]) is 1.3B. Human evaluators preferred InstructGPT outputs 85% of the time. This is the clearest empirical refutation of "bigger is better" for perceived quality — RLHF alignment dominates raw scale. GPT-3 generates output faithful to its training distribution; InstructGPT generates output aligned with human intent.

> **ICL vs fine-tuning**: GPT-3 challenged the BERT paradigm by showing fine-tuning may be unnecessary. However, on structured tasks like SuperGLUE, fine-tuned models still significantly outperform GPT-3 few-shot (89.3 vs 71.8). The practical gap closed only with GPT-4 and beyond — fine-tuning remains superior for specific high-performance applications.

> **Contamination and benchmark validity**: GPT-3's filtering bug means some benchmark contamination is unquantified. The paper reports a clean-subset analysis but acknowledges it cannot be fully resolved. This undermines the strength of some benchmark comparisons and was a methodological gap that later work (RedPajama, The Pile) attempted to address with better deduplication pipelines.
