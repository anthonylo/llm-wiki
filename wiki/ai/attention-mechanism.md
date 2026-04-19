---
title: Attention Mechanism (Attention Is All You Need)
tags: [attention, transformer, self-attention, multi-head-attention, vaswani, positional-encoding]
source: "1706.03762v7 — Attention Is All You Need (Vaswani et al., 2017)"
---

## Summary

"Attention Is All You Need" (Vaswani et al., 2017) introduced the Transformer — an architecture relying entirely on attention mechanisms, discarding recurrence (RNNs/LSTMs) and convolutions entirely. The key insight is that **scaled dot-product attention** lets every token attend to every other token in parallel, enabling far more efficient training and better capture of long-range dependencies. This paper is the foundation of all modern [[large-language-models]].

## Explanation

### Scaled Dot-Product Attention

The core operation:

```
Attention(Q, K, V) = softmax( QKᵀ / √dₖ ) · V
```

- **Q** (Query), **K** (Key), **V** (Value): linear projections of input embeddings
- **√dₖ scaling**: prevents dot products from growing large in high dimensions, which would push softmax into saturation (near-zero gradients). With dₖ=64, the scale factor is 8.
- The output is a weighted sum of Value vectors, where weights represent how much each token should attend to every other token.

### Multi-Head Attention

Rather than applying one attention function, the Transformer runs h=8 parallel attention heads:

```
MultiHead(Q,K,V) = Concat(head₁, ..., headₕ)Wᴼ
where headᵢ = Attention(QWᵢQ, KWᵢK, VWᵢV)
```

**Hyperparameters in the base model**: h=8, dₖ=dᵥ=64, dmodel=512

Each head learns to attend to different relationship types. Attention visualisation in the paper shows individual heads specialize: one head tracks anaphora (pronoun–antecedent resolution), another tracks syntactic dependencies (verbs attending to their objects), another attends to sentence-final punctuation. The ablation confirms h=8 is optimal — single-head loses 0.9 BLEU; 32 heads also degrades (too small dₖ per head).

### Sinusoidal Positional Encoding

Attention has no inherent notion of order. The paper adds fixed (non-learned) positional encodings:

```
PE(pos, 2i)   = sin( pos / 10000^(2i/dmodel) )
PE(pos, 2i+1) = cos( pos / 10000^(2i/dmodel) )
```

Wavelengths form a geometric progression from 2π to 10000·2π. This design allows the model to compute relative positions as linear combinations of PE(pos+k) in terms of PE(pos) — any fixed offset k can be expressed as a linear transformation. The paper chose sinusoidal over learned embeddings for hypothesized length extrapolation, but the ablation (Table 3, row E) showed nearly identical results (25.8 vs 25.7 BLEU).

### Encoder-Decoder Architecture

The Transformer uses N=6 encoder layers and N=6 decoder layers:

**Encoder (each layer)**:
1. Multi-head self-attention (bidirectional — every token attends to all others)
2. Position-wise Feed-Forward Network (FFN)
3. Layer normalisation + residual connection around each sublayer

**Decoder (each layer)**:
1. **Masked** multi-head self-attention — causal masking prevents future positions from being attended to. Implemented by setting illegal (future) positions to −∞ before softmax, producing zero attention weight after the exp.
2. **Cross-attention** (encoder-decoder attention): Q comes from the previous decoder layer; K and V come from the encoder output. This is how the decoder reads the source sequence.
3. FFN
4. Layer norms + residuals

**FFN sublayer**:
```
FFN(x) = max(0, xW₁ + b₁)W₂ + b₂
```
dff=2048, expanding dmodel=512 by 4×.

**Embedding weight sharing**: The paper ties (shares) the weight matrix between the input embedding layer, the output embedding layer, and the pre-softmax linear transformation. During embedding lookup, weights are scaled by √dmodel to counteract the fact that shared weights are also used as a learned projection.

### Training Details

| Hyperparameter | Base Model | Large Model |
|----------------|-----------|-------------|
| dmodel | 512 | 1024 |
| Layers (N) | 6 | 6 |
| Heads (h) | 8 | 16 |
| dff | 2048 | 4096 |
| Parameters | 65M | 213M |

**Optimiser**: Adam with β₁=0.9, β₂=0.98, ε=10⁻⁹

**Learning rate schedule** (warmup):
```
lrate = dmodel^(-0.5) · min(step^(-0.5), step · warmup_steps^(-1.5))
```
warmup_steps=4000. Learning rate increases linearly for warmup then decays proportionally to inverse square root of step number.

**Dropout**: P=0.1 applied to three locations: (1) sublayer outputs before residual addition, (2) embedding sums, (3) positional encodings.

**Label smoothing**: ε_ls=0.1. Hurts perplexity (model less confident) but improves BLEU and accuracy — prevents the model from becoming overconfident on any single class.

**Checkpoint averaging**: Base model results average the last 5 checkpoints (written every 10 min); large models average the last 20.

**Inference**: Beam size=4, length penalty α=0.6, max output length = input + 50.

### Ablation Studies (Table 3)

| Variant | EN-DE BLEU | Notes |
|---------|------------|-------|
| Base (h=8, dₖ=64) | 25.8 | Baseline |
| h=1 | 24.9 | Single head loses 0.9 BLEU |
| h=32 | 25.4 | Too many heads, each dₖ too small |
| dₖ=16 | 25.1 | Key dimension too small |
| Learned PE | 25.7 | Nearly equivalent to sinusoidal |
| No dropout | 25.2 | −0.6 BLEU |
| Big model | 26.4 | +0.6 over base |

Key finding: reducing dₖ degrades quality substantially. The paper hypothesises "determining compatibility is not easy and a more sophisticated compatibility function than dot product may be beneficial" — this motivated later work on alternative attention score functions.

### Results

**Machine Translation (WMT 2014)**:

| Task | BLEU | Notes |
|------|------|-------|
| English→German | 28.4 | +2.0 over prior best ensemble |
| English→French | 41.8 | New state-of-the-art |

Training cost: 3.5 days on 8 P100 GPUs (base model). Prior RNN systems required weeks.

**English constituency parsing (WSJ)**:
- 4-layer Transformer achieved 91.3 F1 (WSJ only), 92.7 F1 (semi-supervised)
- Competitive with task-specific parsers, demonstrating Transformer generalises beyond seq2seq

### Computational Complexity vs RNNs and CNNs

| Layer Type | Complexity per layer | Sequential ops | Max path length |
|-----------|---------------------|----------------|-----------------|
| Self-attention | O(n²·d) | O(1) | O(1) |
| Recurrent | O(n·d²) | O(n) | O(n) |
| Convolutional | O(k·n·d²) | O(1) | O(logₖ n) |
| Restricted attention (r) | O(r·n·d) | O(1) | O(n/r) |

The O(n²) attention cost is the bottleneck at long sequences — motivating Flash Attention, sparse attention, and linear attention variants in later work.

### Why Transformers Replaced RNNs

| Property | RNN/LSTM | Transformer |
|----------|----------|------------|
| Parallelisation | Sequential; O(n) steps | Fully parallel; O(1) steps |
| Path length (long-range deps) | O(n) operations | O(1) attention |
| Training speed | Slow (gradient through time) | Fast |
| Context | Fixed hidden state | Full sequence in attention |

See [[transformer-architecture]] for modern variants (Flash Attention, GQA, MLA) that address the O(n²) bottleneck.

## Related Pages

- [[transformer-architecture]] — comprehensive overview of all Transformer variants and modern developments
- [[bert]] — encoder-only Transformer pre-trained with bidirectional masked language modeling
- [[gpt-3]] — decoder-only Transformer scaled to 175B parameters
- [[large-language-models]] — all modern LLMs are Transformer-based
- [[scaling-laws]] — how Transformer performance scales with parameters and data
- [[pretraining-and-finetuning]] — Transformer pre-training objectives (CLM, MLM)

## Contradictions

> **Encoder-decoder vs encoder-only vs decoder-only**: The original Transformer used a full encoder-decoder architecture for seq2seq translation. BERT ([[bert]]) later showed that encoder-only with bidirectional attention produces superior representations for understanding tasks. GPT-3 ([[gpt-3]]) showed that decoder-only with causal masking at massive scale achieves strong downstream performance without any fine-tuning. All three claimed to be the right architecture for their target use cases — the field converged on decoder-only for generative LLMs and encoder-only for embedding/understanding tasks.

> **Fixed vs learned positional encoding**: The paper chose sinusoidal encodings for hypothesized extrapolation benefits. The ablation (Table 3E) showed learned and sinusoidal produce nearly identical BLEU (25.7 vs 25.8). Later models (GPT-2, BERT) used learned absolute embeddings; even later work (RoPE, ALiBi) introduced relative encodings that genuinely improve long-context performance — confirming the original choice mattered less than assumed.

> **Dot-product attention at large dₖ**: The paper warns that dot products grow large at high dₖ, saturating softmax. The √dₖ scaling addresses this. However, the ablation also shows that reducing dₖ (and thus the scale factor) hurts quality — the paper notes the compatibility function may need to be more expressive. This tension is unresolved in the original paper; later work (cosine attention, L2 attention) explored alternatives.
