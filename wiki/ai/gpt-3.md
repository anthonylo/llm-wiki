---
title: GPT-3 (Language Models are Few-Shot Learners)
tags: [gpt-3, few-shot, in-context-learning, autoregressive, brown, openai, scaling]
source: "2005.14165v4 — Language Models are Few-Shot Learners (Brown et al., 2020)"
---

## Summary

GPT-3 (Brown et al., 2020) demonstrated that autoregressive language models at sufficient scale exhibit strong **few-shot learning** from context without any fine-tuning or gradient updates. With 175 billion parameters — 10× larger than any prior model — GPT-3 achieved near-state-of-the-art on many NLP benchmarks using only in-context demonstrations. This paper redefined what scale could achieve and launched the era of foundation models.

## Explanation

### Model Architecture

GPT-3 is a **decoder-only** Transformer (same architecture as GPT-2, scaled up):

| Model | Parameters | Layers | dmodel | Heads | Batch size | Learning rate |
|-------|-----------|--------|--------|-------|------------|--------------|
| GPT-3 Small | 125M | 12 | 768 | 12 | 0.5M | 6.0×10⁻⁴ |
| GPT-3 Medium | 350M | 24 | 1024 | 16 | 0.5M | 3.0×10⁻⁴ |
| GPT-3 Large | 760M | 24 | 1536 | 16 | 0.5M | 2.5×10⁻⁴ |
| GPT-3 XL | 1.3B | 24 | 2048 | 24 | 1M | 2.0×10⁻⁴ |
| GPT-3 6.7B | 6.7B | 32 | 4096 | 32 | 2M | 1.2×10⁻⁴ |
| GPT-3 13B | 13B | 40 | 5140 | 40 | 2M | 1.0×10⁻⁴ |
| **GPT-3 175B** | **175B** | **96** | **12288** | **96** | **3.2M** | **6.0×10⁻⁵** |

All use **alternating dense and locally banded sparse attention** in each layer (following Sparse Transformer). Context window: 2,048 tokens.

### Training Data

| Dataset | Tokens | Weight |
|---------|--------|--------|
| Common Crawl (filtered) | 410B | 60% |
| WebText2 | 19B | 22% |
| Books1 | 12B | 8% |
| Books2 | 55B | 8% |
| Wikipedia | 3B | 3% |
| **Total** | ~499B tokens | — |

GPT-3 was trained on ~300B tokens. Higher-quality datasets (Books, Wikipedia) are upsampled relative to their raw size.

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

**Few-Shot** (up to K=10 or K=100 examples in context):
```
Translate English to French:
sea otter => loutre de mer
peppermint => menthe poivrée
plush giraffe => girafe en peluche
cheese =>
```

The model never updates its weights — it reads the demonstrations from context and generalises via attention. See [[in-context-learning]] for detailed mechanics.

### Key Results

| Benchmark | Metric | Zero-Shot | One-Shot | Few-Shot | Prior SOTA |
|-----------|--------|-----------|----------|----------|------------|
| TriviaQA | Acc | 64.3% | 68.0% | 71.2% | 68.0% (fine-tuned) |
| CoQA | F1 | 81.5 | 84.0 | 85.0 | 90.7 (fine-tuned) |
| SuperGLUE | score | 71.8 | — | 71.8 | 89.3 (fine-tuned) |
| Winogrande | Acc | 70.2% | 73.2% | 77.7% | 84.6% (fine-tuned) |
| HellaSwag | Acc | 78.9% | 78.1% | 79.3% | 93.9% (fine-tuned) |
| LAMBADA (language modeling) | Acc | 76.2% | — | 86.4% | 68.0% (zero-shot RoBERTa) |

GPT-3 few-shot matches or exceeds fine-tuned models on some tasks (TriviaQA) but falls short on others (SuperGLUE). The key finding: **scale enables emergent few-shot ability without any task-specific training**.

### Arithmetic and Novel Tasks

GPT-3 performs surprisingly well on tasks not in training data:
- **2-digit addition**: 100% accuracy (zero-shot)
- **3-digit addition**: 80.2% (few-shot)
- **4-digit addition**: 25.3% (few-shot)
- **SAT analogies**: 53.7% (few-shot) vs human 57%

These tasks require compositional generalisation — evidence that scale produces qualitatively new capabilities. See [[emergent-abilities]].

### Data Contamination

A significant concern in the paper: because GPT-3 was trained on large internet datasets, some test sets may have appeared in training data (contamination). The paper reports a careful analysis, removing suspected contaminated benchmarks, but acknowledges this cannot be fully eliminated. Contamination may inflate performance on some benchmarks.

### Limitations

1. **Sample efficiency**: Requires massive compute ($4.6M+ estimated for the 175B run)
2. **Context window**: 2,048 tokens limits few-shot examples
3. **No weight updates**: In-context learning is transient — the model forgets after the session
4. **Bias**: Generates text reflecting biases in training data (racial, gender, religion)
5. **Text only**: Cannot process images, code, or other modalities (base GPT-3)
6. **Calibration**: Confidence scores poorly calibrated

### Impact

GPT-3 shifted the field from fine-tuning (BERT paradigm) toward prompt engineering. It demonstrated that:
- Scale alone can produce emergent capabilities
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

> **GPT-3 vs InstructGPT (scale vs alignment)**: GPT-3 is 175B parameters; InstructGPT ([[instructgpt]]) is 1.3B. Human evaluators preferred InstructGPT outputs 85% of the time. This is the clearest empirical refutation of "bigger is better" — RLHF alignment dominates raw scale for the metric of human preference. GPT-3 generates output faithful to its training distribution; InstructGPT generates output aligned with human intent.

> **ICL vs fine-tuning**: GPT-3 challenged the BERT paradigm by showing fine-tuning may be unnecessary. However, on structured tasks like SuperGLUE, fine-tuned models still significantly outperform GPT-3 few-shot. The practical gap closed only with GPT-4 and beyond — fine-tuning remains superior for specific high-performance applications.
