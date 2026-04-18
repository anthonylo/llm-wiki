---
title: Transformer Architecture
tags: [transformer, attention, neural-networks, architecture]
source: "2307.06435v10 — A Comprehensive Overview of Large Language Models (Naveed et al., 2023)"
---

## Summary

The Transformer (Vaswani et al., 2017) replaced recurrent networks as the dominant architecture for sequence modelling. Its core innovation — scaled dot-product self-attention — enables tokens to attend to every other token in parallel, capturing long-range dependencies without sequential computation bottlenecks. All modern [[large-language-models]] are built on Transformer variants.

## Explanation

### Core Components

**Tokenisation**
Text is split into subword tokens using Byte-Pair Encoding (BPE), WordPiece, or SentencePiece. Token IDs are mapped to dense embedding vectors.

**Positional Encoding**
Transformers have no inherent notion of order. Positional encodings add sequence position information to embeddings:
- *Sinusoidal* (original paper): fixed, extrapolation-limited
- *Learned absolute* (GPT): position embeddings as parameters
- *Rotary (RoPE)* (LLaMA, GPT-NeoX): relative positions encoded via rotation; extrapolates better to longer sequences
- *ALiBi*: additive bias in attention scores; strong long-context performance

**Self-Attention (Scaled Dot-Product)**

```
Attention(Q, K, V) = softmax( QKᵀ / √dₖ ) · V
```

- Q (Query), K (Key), V (Value) are linear projections of the input
- Scores measure token relevance to each other
- √dₖ scaling prevents gradient saturation

**Multi-Head Attention (MHA)**
Run h parallel attention heads, concatenate outputs. Each head can attend to different relationship types.

**Feed-Forward Network (FFN)**
Two-layer MLP applied position-wise after attention. Typically expands to 4× model dimension and contracts back.

**Layer Normalisation + Residual Connections**
Pre-LN (LLaMA) or post-LN (original) normalise activations; residuals enable gradient flow in deep networks.

### Attention Variants

| Variant | Key Property | Models |
|---------|-------------|--------|
| Full Self-Attention | Every token attends to every token | BERT, GPT-2/3 |
| Causal (Masked) Attention | Each token only attends to past tokens | GPT series, LLaMA |
| Cross-Attention | Tokens attend to a separate sequence | Encoder-decoder (T5) |
| Sparse Attention | Attend to subset of positions | Longformer, BigBird |
| Flash Attention | IO-aware exact attention (fast) | LLaMA 2+, Mistral |
| Multi-Query Attention (MQA) | Single K/V head, multiple Q heads | Falcon, GPT-J |
| Grouped-Query Attention (GQA) | Grouped K/V sharing | LLaMA 3 |
| Multi-Head Latent Attention (MLA) | Compresses K/V cache into latent vector; 5.76× faster inference than GQA | DeepSeek-v2 |

### Architecture Variants

**Encoder-Decoder (T5, BART)**
- Encoder: bidirectional, full self-attention → rich representations
- Decoder: causal self-attention + cross-attention over encoder output
- Suited for seq2seq tasks (translation, summarisation)

**Causal Decoder (GPT, LLaMA)**
- Single decoder stack with causal masking
- Pre-trains on next-token prediction
- Dominant architecture for generative LLMs

**Prefix Decoder (GLM, UniLM)**
- Bidirectional attention over input prefix, causal over generated suffix
- Combines BERT expressiveness with GPT generation

**Mixture-of-Experts (MoE)**
- Replace dense FFN with N expert FFNs + a gating network
- Only top-k experts activated per token → same parameters, less compute
- Used in Mixtral, Switch Transformer, GPT-4 (rumoured)

### Computational Complexity

Full attention is O(n²d) in sequence length n and dimension d. This is the fundamental reason context windows have historically been limited:
- 2048 tokens: tractable
- 128K tokens: requires engineering tricks (Flash Attention, ring attention, etc.)

See [[scaling-laws]] for how model size interacts with performance.

## Related Pages

- [[large-language-models]] — how Transformers are scaled into LLMs
- [[in-context-learning]] — emerges from attention mechanics over prompt context
- [[scaling-laws]] — compute, data, and parameter scaling behaviour
- [[pretraining-and-finetuning]] — training objectives for Transformer models
- [[long-term-memory-in-ai]] — context windows are Transformers' working memory; not true long-term storage
- [[retrieval-augmented-generation]] — supplements Transformer context with retrieved passages
