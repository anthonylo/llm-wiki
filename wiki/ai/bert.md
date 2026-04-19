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

| Model | Layers (L) | Hidden size (H) | FFN size | Attention heads (A) | Parameters |
|-------|-----------|-----------------|----------|--------------------|-----------:|
| BERT_BASE | 12 | 768 | 3072 | 12 | 110M |
| BERT_LARGE | 24 | 1024 | 4096 | 16 | 340M |

BERT_BASE was designed to match GPT's size for fair comparison (same parameter count, only attention direction differs).

**Activation function**: GELU (Gaussian Error Linear Unit), following OpenAI GPT — not the ReLU used in the original Transformer.

**Tokenisation**: WordPiece with a 30,000-token vocabulary. Rare words are split into subwords (e.g. "playing" → "play", "##ing").

**Input representation** — every input is the sum of three learned embeddings:
1. **Token embedding**: maps each WordPiece token to a dense vector
2. **Segment embedding**: differentiates sentence A from sentence B in sentence-pair inputs
3. **Position embedding**: learned absolute position (not sinusoidal)

**Special tokens**:
- `[CLS]`: prepended to every sequence; its final hidden state is used as the aggregate sequence representation for classification tasks
- `[SEP]`: separates sentence pairs (sentence A from sentence B) and marks end of single-sentence input
- `[MASK]`: replaces masked tokens during MLM pre-training

### Pre-Training Tasks

**Task 1: Masked Language Model (MLM)**
- Randomly mask 15% of input tokens
- Of those: 80% → `[MASK]`, 10% → random token, 10% → unchanged
- Predict the original token at masked positions
- Enables bidirectional conditioning without "seeing the answer"
- BERT achieves 97-98% accuracy on NSP (suggests task is somewhat easy)

**Task 2: Next Sentence Prediction (NSP)**
- Given sentence pair (A, B), predict whether B follows A in the original document
- 50% positive (real consecutive sentences), 50% negative (random sentence from corpus)
- Trains cross-sentence understanding, important for QA and NLI
- The corpus is document-level (not shuffled sentences) to preserve long-range context needed for real next-sentence pairs

See [[masked-language-modeling]] for detailed analysis of the 80/10/10 masking strategy and its motivations.

### Pre-Training Data

| Dataset | Size |
|---------|------|
| BooksCorpus | 800M words |
| English Wikipedia (text only) | 2,500M words |
| **Total** | ~3,300M words |

Wikipedia tables and lists are excluded; only passage text is used. Document-level corpus (not sentence-shuffled) is essential for NSP to have meaningful positive examples.

### Training Procedure

**Optimiser**: Adam with β₁=0.9, β₂=0.999, L2 weight decay=0.01, learning rate warmup over first 10,000 steps, linear decay thereafter.

**Staged sequence length**: Pre-trained with sequences of length 128 for 90% of steps (computationally efficient), then length 512 for the remaining 10% (learns long-range dependencies). This is because attention is O(n²) — doubling sequence length quadruples compute.

**Batch composition**: 256 sequences × ≤512 tokens = up to 128,000 tokens per batch. 1,000,000 total steps ≈ 40 epochs over the 3.3B word corpus.

**Hardware**:
- BERT_BASE: 4 Cloud TPU v3 Pods (16 TPU chips total), 4 days
- BERT_LARGE: 16 Cloud TPU v3 Pods (64 TPU chips), 4 days

**Dropout**: P=0.1 on all layers.

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

Fine-tuning typically takes 2–4 epochs on task data. The pre-training does the heavy lifting.

**Fine-tuning instability**: BERT_LARGE showed instability on small GLUE datasets (e.g. MRPC, 3.6k examples), requiring multiple random restarts and checkpoint selection. The authors attributed this to small dataset size and high initial learning rate interaction.

### Feature-Based Approach

Instead of fine-tuning, BERT representations can be used as frozen features (e.g. for NER):

| Feature strategy | NER F1 |
|-----------------|--------|
| Fine-tuning (all layers) | 96.4 |
| Last 4 layers concatenated | 96.1 |
| Last 4 layers summed | 95.9 |
| Last layer only | 94.9 |

The feature-based approach (last 4 layers) achieves within 0.3 F1 of fine-tuning — useful in deployment scenarios where BERT weights cannot be modified.

### Results

| Benchmark | Prior Best | BERT_LARGE | Improvement |
|-----------|-----------|------------|-------------|
| GLUE score | 72.8 (GPT) | 80.5 | +7.7 pp |
| ELMo (BiLSTM, feature-based) | 71.0 | 79.6 (BASE) | +8.6 pp |
| SQuAD v1.1 F1 | 91.7 | 93.2 | +1.5 pp |
| SQuAD v2.0 F1 | 66.3 | 83.1 | +16.8 pp |
| NER (CoNLL-2003) | 92.8 | 93.5 | +0.7 pp |

BERT surpassed human performance on SQuAD v1.1 (91.2 human, 93.2 BERT). The ELMo comparison directly shows why fine-tuning (BERT) outperforms feature-based (ELMo): +8.6 pp on GLUE.

**BERT vs GPT (matched size)**: BERT_BASE and OpenAI GPT are the same size. On MNLI, BERT_BASE achieves 86.7% vs GPT's 82.1% (+4.6 pp). The difference is entirely attributable to bidirectionality.

### Ablation Studies

The BERT paper tested removing each component:

| Variant | MNLI | QNLI | MRPC | SQuAD | GLUE avg |
|---------|------|------|------|-------|----------|
| BERT_BASE (full) | 84.6 | 88.6 | 86.7 | 88.5 | 82.2 |
| No NSP | 83.9 | 84.9 | 86.5 | 87.9 | 81.6 |
| No NSP + Left-to-Right | 82.1 | 84.3 | 77.5 | 77.8 | 77.9 |
| No NSP + LTR + BiLSTM | 82.1 | 84.1 | 79.3 | 84.9 | 79.5 |

Key findings:
- Removing NSP hurts QNLI severely (-3.5) but has small effect overall: NSP matters most for cross-sentence tasks
- Removing bidirectionality (LTR) causes −4.3 GLUE avg drop — the largest single contributor
- Adding a BiLSTM on top of LTR model partially recovers SQuAD (84.9) but cannot match bidirectional MLM

### Model Size Scaling

BERT tested monotonic scaling (smaller variants):

| Layers | Hidden | Heads | MNLI | MRPC | LM ppl |
|--------|--------|-------|------|------|--------|
| 3 | 768 | 12 | 77.9 | 79.8 | 5.84 |
| 6 | 768 | 3 | 80.6 | 82.3 | 4.53 |
| 6 | 768 | 12 | 81.9 | 84.8 | 4.53 |
| 12 | 768 | 12 | 84.4 | 86.7 | 3.45 |
| 24 | 1024 | 16 | 86.6 | 88.3 | 3.23 |

Strictly monotonic improvement with depth and width, even on small datasets (MRPC = 3.6k examples). This result, combined with scaling laws, motivated the billion-parameter era.

## Related Pages

- [[attention-mechanism]] — the Transformer architecture BERT is built on
- [[masked-language-modeling]] — the core MLM pre-training objective
- [[pretraining-and-finetuning]] — pre-train/fine-tune paradigm introduced by BERT
- [[transformer-architecture]] — encoder/decoder variants and modern developments
- [[gpt-3]] — decoder-only counterpart; different training objective, same Transformer backbone
- [[large-language-models]] — BERT's descendants (RoBERTa, DeBERTa, ELECTRA)
- [[scaling-laws]] — BERT at 110M/340M; scaling later pushed to billions

## Contradictions

> **NSP task later disputed**: BERT introduced NSP as essential for sentence-pair tasks. BERT achieves 97-98% accuracy on NSP itself, suggesting it may be too easy to be informative. RoBERTa (Liu et al., 2019) trained BERT without NSP and achieved *better* performance across the board — they attributed BERT's NSP gains to a confounding variable: NSP training used shorter sequences (128 tokens) while removing NSP allowed full 512-token document sequences. This directly contradicts BERT's own ablation showing +0.6 GLUE improvement from NSP.

> **Bidirectionality vs scale**: BERT argued that left-to-right architectures are "sub-optimal" for language understanding. GPT-3 ([[gpt-3]]) later showed that decoder-only models at 175B parameters achieve competitive or superior performance on many NLU tasks — suggesting scale can partially compensate for architectural restrictions. BERT vs GPT (matched size): BERT wins by 4.6 pp MNLI. GPT-3 (100× larger): matches or exceeds fine-tuned BERT on many tasks without fine-tuning.

> **Fine-tuning paradigm vs in-context learning**: BERT established fine-tuning as the dominant adaptation method. GPT-3 ([[gpt-3]]) then showed that fine-tuning may be unnecessary for large enough models — in-context learning without weight updates can match or exceed fine-tuned smaller models. This tension (fine-tuning vs [[in-context-learning]]) remains unresolved and task-dependent.

> **GELU vs ReLU**: BERT adopted GELU following GPT, while the original Transformer used ReLU. No ablation comparing these in the BERT paper is presented — the choice follows convention rather than evidence. Later models (GPT-2, GPT-3, LLaMA) all use GELU or SiLU variants, empirically confirming the preference for smooth activations.
