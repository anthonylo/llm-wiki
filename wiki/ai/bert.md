---
title: BERT (Bidirectional Encoder Representations from Transformers)
tags: [bert, bidirectional, pre-training, masked-language-modeling, nlp, devlin, fine-tuning]
source: "1810.04805v2 — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (Devlin et al., 2018)"
---

## Summary

BERT (Devlin et al., 2018) introduced **bidirectional pre-training** for language representations — a critical advance over GPT's left-to-right pre-training. By masking random tokens and predicting them using full left-and-right context, BERT learns richer contextual embeddings. A single pre-trained BERT model can be fine-tuned with one additional output layer to achieve state-of-the-art on 11 NLP tasks simultaneously.

## Explanation

### The Bidirectionality Innovation

Previous language models were unidirectional: GPT processed tokens left-to-right (each token only sees prior context). This limits the representation quality, especially for tasks where right context matters (e.g., fill-in-the-blank, named entity recognition).

BERT uses a **Masked Language Model** (MLM) objective that randomly masks 15% of tokens and asks the model to predict them using both left and right context. See [[masked-language-modeling]] for full detail.

**The BERT paper explicitly positions this against GPT**: "GPT uses a left-to-right architecture, where every token can only attend to previous tokens in the self-attention layers of the Transformer. Such restrictions are sub-optimal for sentence-level tasks."

### Model Architecture

BERT is a stack of Transformer **encoder** layers only (no decoder). Two sizes:

| Model | Layers (L) | Hidden size (H) | Attention heads (A) | Parameters |
|-------|-----------|-----------------|--------------------|-----------:|
| BERT_BASE | 12 | 768 | 12 | 110M |
| BERT_LARGE | 24 | 1024 | 16 | 340M |

BERT_BASE was designed to be comparable to GPT (same size) for fair comparison.

**Tokenisation**: WordPiece with a 30,000-token vocabulary. Rare words are split into subwords (e.g. "playing" → "play", "##ing").

**Special tokens**:
- `[CLS]`: prepended to every sequence; its final hidden state is used as the sequence representation for classification tasks
- `[SEP]`: separates sentence pairs (sentence A from sentence B)
- `[MASK]`: replaces masked tokens during MLM pre-training

### Pre-Training Tasks

**Task 1: Masked Language Model (MLM)**
- Randomly mask 15% of input tokens
- Of those: 80% → `[MASK]`, 10% → random token, 10% → unchanged
- Predict the original token at masked positions
- Enables bidirectional conditioning without "seeing the answer"

**Task 2: Next Sentence Prediction (NSP)**
- Given sentence pair (A, B), predict whether B follows A in the original document
- 50% positive (real consecutive sentences), 50% negative (random sentence)
- Trains cross-sentence understanding, important for QA and NLI

See [[masked-language-modeling]] for detailed analysis of the 80/10/10 masking strategy and its motivations.

### Pre-Training Data

| Dataset | Size |
|---------|------|
| BooksCorpus | 800M words |
| English Wikipedia (text only) | 2,500M words |
| **Total** | ~3,300M words |

Wikipedia tables and lists are excluded; only passage text is used. BERT_LARGE was trained for 1M steps on 256 TPU chips (Cloud TPU v3) for ~4 days.

### Fine-Tuning Paradigm

BERT established the **pre-train → fine-tune** paradigm: the same base model, minimally adapted, achieves state-of-the-art across wildly different NLP tasks:

```
Pre-trained BERT → add task-specific output layer → fine-tune all weights on task data
```

Task output layers:
- **Classification** (GLUE, sentiment): linear layer over `[CLS]` token
- **Span extraction** (SQuAD QA): two linear layers (start, end position)
- **Sequence tagging** (NER): linear layer over each token
- **Sentence pair** (NLI, paraphrase): linear layer over `[CLS]` with both sentences as input

Fine-tuning is cheap: typically 2–4 epochs on task data. The pre-training does the heavy lifting.

### Results

| Benchmark | Prior Best | BERT_LARGE | Improvement |
|-----------|-----------|------------|-------------|
| GLUE score | 72.8 | 80.5 | +7.7 pp |
| SQuAD v1.1 F1 | 91.7 | 93.2 | +1.5 pp |
| SQuAD v2.0 F1 | 66.3 | 83.1 | +16.8 pp |
| NER (CoNLL-2003) | 92.8 | 93.5 | +0.7 pp |

BERT surpassed human performance on SQuAD v1.1 (91.2 human, 93.2 BERT).

### Ablation Studies

The BERT paper tested removing each component:

| Variant | GLUE Dev Avg |
|---------|-------------|
| BERT_BASE (full) | 82.2 |
| No NSP | 81.6 (-0.6) |
| Left-to-right LTR (no MLM) | 77.9 (-4.3) |
| LTR + BiLSTM on top | 79.5 (-2.7) |

This confirmed that bidirectionality (MLM) is far more important than NSP.

## Related Pages

- [[attention-mechanism]] — the Transformer architecture BERT is built on
- [[masked-language-modeling]] — the core MLM pre-training objective
- [[pretraining-and-finetuning]] — pre-train/fine-tune paradigm introduced by BERT
- [[transformer-architecture]] — encoder/decoder variants and modern developments
- [[gpt-3]] — decoder-only counterpart; different training objective, same Transformer backbone
- [[large-language-models]] — BERT's descendants (RoBERTa, DeBERTa, ELECTRA)
- [[scaling-laws]] — BERT at 110M/340M; scaling later pushed to billions

## Contradictions

> **NSP task later disputed**: BERT introduced NSP as essential for sentence-pair tasks. However, RoBERTa (Liu et al., 2019) trained BERT without NSP and achieved *better* performance across the board. They attributed BERT's NSP gains to confounding factors (NSP training used shorter sequences; removing NSP allowed longer full-document sequences). This directly contradicts BERT's own ablation, which showed a +0.6 GLUE improvement from NSP.

> **Bidirectionality vs scale**: BERT argued that left-to-right architectures are "sub-optimal" for language understanding. GPT-3 ([[gpt-3]]) later showed that decoder-only models at 175B parameters achieve competitive or superior performance on many NLU tasks — suggesting scale can partially compensate for architectural restrictions. The two papers represent different bets on what matters most: architecture quality vs parameter count.

> **Fine-tuning paradigm vs in-context learning**: BERT established fine-tuning as the dominant adaptation method. GPT-3 ([[gpt-3]]) then showed that fine-tuning may be unnecessary for large enough models — in-context learning without weight updates can match or exceed fine-tuned smaller models. This tension (fine-tuning vs [[in-context-learning]]) remains unresolved and task-dependent.
