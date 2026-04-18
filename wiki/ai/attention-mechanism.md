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

Each head learns to attend to different relationship types (syntactic, semantic, positional). Outputs are concatenated and projected back to dmodel.

### Sinusoidal Positional Encoding

Attention has no inherent notion of order. The paper adds fixed (non-learned) positional encodings:

```
PE(pos, 2i)   = sin( pos / 10000^(2i/dmodel) )
PE(pos, 2i+1) = cos( pos / 10000^(2i/dmodel) )
```

Sine and cosine at different frequencies allow the model to learn relative positions via linear combinations. This generalises to sequence lengths not seen in training — a limitation of learned positional encodings.

### Encoder-Decoder Architecture

The Transformer uses 6 encoder layers and 6 decoder layers (N=6 for both):

**Encoder (each layer)**:
1. Multi-head self-attention (bidirectional — every token attends to all others)
2. Position-wise Feed-Forward Network (FFN)
3. Layer normalisation + residual connection around each sublayer

**Decoder (each layer)**:
1. Masked multi-head self-attention (causal — each token only attends to past tokens)
2. Cross-attention over encoder output
3. FFN
4. Layer norms + residuals

**FFN sublayer**:
```
FFN(x) = max(0, xW₁ + b₁)W₂ + b₂
```
dff=2048, expanding dmodel=512 by 4×.

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

**Dropout**: 0.1 applied to sublayer outputs and embeddings.

### Results (Machine Translation)

| Task | BLEU | Notes |
|------|------|-------|
| English→German (WMT 2014) | 28.4 | +2.0 over prior best ensemble |
| English→French (WMT 2014) | 41.8 | New state-of-the-art |

Training cost: 3.5 days on 8 P100 GPUs (base model). Prior RNN systems required weeks.

### Why Transformers Replaced RNNs

| Property | RNN/LSTM | Transformer |
|----------|----------|------------|
| Parallelisation | Sequential; O(n) steps | Fully parallel; O(1) steps |
| Path length (long-range deps) | O(n) operations | O(1) attention |
| Training speed | Slow (gradient through time) | Fast |
| Context | Fixed hidden state | Full sequence in attention |
| Complexity per layer | O(n·d²) | O(n²·d) |

The O(n²) attention cost becomes the bottleneck only at very long sequences — this is why context window engineering later became important. See [[transformer-architecture]] for variants (Flash Attention, GQA, MLA) that address this.

## Related Pages

- [[transformer-architecture]] — comprehensive overview of all Transformer variants and modern developments
- [[bert]] — encoder-only Transformer pre-trained with bidirectional masked language modeling
- [[gpt-3]] — decoder-only Transformer scaled to 175B parameters
- [[large-language-models]] — all modern LLMs are Transformer-based
- [[scaling-laws]] — how Transformer performance scales with parameters and data
- [[pretraining-and-finetuning]] — Transformer pre-training objectives (CLM, MLM)


## Contradictions

> **Encoder-decoder vs encoder-only vs decoder-only**: The original Transformer used a full encoder-decoder architecture for seq2seq translation. BERT ([[bert]]) later showed that encoder-only with bidirectional attention produces superior representations for understanding tasks. GPT-3 ([[gpt-3]]) showed that decoder-only with causal masking at massive scale achieves strong downstream performance without any fine-tuning. All three claimed to be the right architecture for their target use cases — the field converged on decoder-only for generative LLMs and encoder-only for embedding/understanding tasks.

> **Fixed vs learned positional encoding**: The paper chose sinusoidal encodings ("we chose the sinusoidal version because it may allow the model to extrapolate to sequence lengths longer than those encountered during training"). Later models (GPT-2, BERT) used learned absolute positional embeddings with no measurable performance difference on standard benchmarks, suggesting the choice matters less than the architectural frame.
