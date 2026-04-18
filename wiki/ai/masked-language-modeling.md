---
title: Masked Language Modeling (MLM)
tags: [MLM, masked-language-model, pre-training, bert, bidirectional, self-supervised]
source: "1810.04805v2 — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (Devlin et al., 2018)"
---

## Summary

Masked Language Modeling (MLM) is the self-supervised pre-training objective introduced in [[bert]]. Rather than predicting the next token (as in causal language models), MLM randomly masks a fraction of input tokens and trains the model to reconstruct them using **full bidirectional context**. This enables richer contextual representations than left-to-right language modelling.

## Explanation

### The Core Idea

Standard autoregressive language modelling is **causal**: each token can only attend to prior tokens. This prevents the model from using right-side context when encoding a word. Consider:

```
"The bank can guarantee deposits will eventually ___."
```

To predict the blank, right context ("customers") is as useful as left context. MLM allows both directions.

### The 80/10/10 Masking Strategy

15% of WordPiece tokens in each sequence are selected for prediction. Of those 15%:

| Replacement | Probability | Reason |
|-------------|-------------|--------|
| `[MASK]` token | 80% | Force the model to use context |
| Random other token | 10% | Force representation to be correct even without `[MASK]` |
| Original token unchanged | 10% | Provide the correct token distribution; match fine-tuning distribution |

**Why not mask 100% of selected tokens?**

If all selected tokens were replaced with `[MASK]`, the model would only learn to predict `[MASK]` positions — creating a **pre-training / fine-tuning mismatch** because `[MASK]` never appears at fine-tuning time. The 10% random + 10% unchanged mitigate this.

**Why only 15%?**

Masking too many tokens makes the task trivial (predict from heavy context) or too hard (no signal). 15% was found empirically to work well. This means only 15% of positions generate a training signal per step — making MLM about 3× more expensive than CLM to reach the same number of token predictions.

### MLM vs Causal Language Modelling (CLM)

| Property | MLM (BERT) | CLM (GPT) |
|----------|-----------|-----------|
| Direction | Bidirectional | Left-to-right only |
| Training objective | Predict masked tokens | Predict next token |
| `[MASK]` at inference | No | No |
| Suited for | Understanding, classification | Generation |
| Tokens predicted per step | ~15% of input | 100% of input |
| Context richness | Full (both sides) | Left-only |

### Span Masking (SpanBERT)

SpanBERT (Joshi et al., 2020) extended MLM by masking contiguous spans of tokens (2-10 tokens) rather than random individual tokens. A "Span Boundary Objective" (SBO) predicts each masked token from the boundary tokens alone. This improves performance on span-level tasks (QA, coreference resolution).

### Whole-Word Masking (WWM)

Standard BERT masks WordPiece subword tokens independently — so "playing" might become "play##ing" with only "play" masked. Whole-Word Masking ensures all subwords of a word are masked together. Google released whole-word-masked BERT variants with better performance on many tasks.

### ELECTRA: Replace Token Detection

ELECTRA (Clark et al., 2020) replaced MLM with a discriminative task: a small generator replaces some tokens; the main model (discriminator) predicts whether each token was replaced. This is more efficient than MLM because every token position contributes a training signal (vs 15% for MLM), achieving better performance at equal compute.

## Related Pages

- [[bert]] — MLM was introduced as BERT's primary pre-training task
- [[pretraining-and-finetuning]] — MLM is the pre-training objective; fine-tuning follows
- [[transformer-architecture]] — the Transformer encoder MLM is applied to
- [[attention-mechanism]] — bidirectional self-attention enables MLM's full-context conditioning
- [[large-language-models]] — many modern encoder models still use MLM variants

## Contradictions

> **MLM efficiency vs CLM**: MLM only produces training signal from 15% of tokens per sequence, making it roughly 6-7× less sample-efficient than CLM on a per-token basis. ELECTRA and subsequent work showed that MLM's inefficiency was a significant bottleneck. However, BERT's authors argue the bidirectional representations justify the cost.

> **Pre-training / fine-tuning mismatch**: The 80/10/10 strategy is a workaround for the fundamental mismatch that `[MASK]` only appears during pre-training. The 20% "noise" (random tokens + unchanged) doesn't fully close this gap — fine-tuning distributions still differ from pre-training. XLNet (Yang et al., 2019) proposed Permutation Language Modeling to avoid this mismatch entirely.
