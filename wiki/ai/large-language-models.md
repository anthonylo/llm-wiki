---
title: Large Language Models (LLMs)
tags: [LLM, NLP, deep-learning, transformers]
source: "2307.06435v10 — A Comprehensive Overview of Large Language Models (Naveed et al., 2023)"
---

## Summary

Large Language Models (LLMs) are deep neural networks trained on massive text corpora to model the probability distribution over sequences of tokens. Through scale alone, they acquire generalised reasoning, in-context learning, and emergent capabilities not present in smaller models. Modern LLMs follow the Transformer architecture and are deployed via a pre-train → fine-tune → align pipeline.

## Explanation

### What Makes a Model "Large"

Scale operates across three axes:
- **Parameters**: billions to trillions of weights
- **Training data**: hundreds of billions to trillions of tokens
- **Compute**: thousands of GPU-days (typically A100/H100 clusters)

The boundary is fuzzy, but models ≥7B parameters trained on ≥100B tokens are generally considered "large." Scale unlocks [[emergent-abilities]] not visible in smaller models.

### Architecture Families

| Family | Examples | Training Objective | Use Case |
|--------|----------|--------------------|----------|
| Encoder-Decoder | T5, BART | Span masking + seq2seq | Translation, summarisation |
| Causal Decoder | GPT series, LLaMA, Falcon | Next-token prediction | Generation, chat |
| Prefix Decoder | GLM, UniLM | Mixed MLM + AR | Flexible input/output |
| Mixture-of-Experts (MoE) | Mixtral, Switch | Sparse gating | Efficiency at scale |

See [[transformer-architecture]] for internal mechanics.

### Training Pipeline

1. **Pre-training** on large text corpus → base language model
2. **Supervised Fine-Tuning (SFT)** on instruction-following data → instruction model
3. **RLHF / Alignment** → helpful, harmless, honest model

See [[pretraining-and-finetuning]] and [[rlhf-and-alignment]].

### Key Capabilities

- **In-Context Learning (ICL)**: Adapt to new tasks via examples in the prompt; no gradient updates. See [[in-context-learning]].
- **Chain-of-Thought (CoT)**: Step-by-step reasoning elicited by prompting.
- **Instruction Following**: Execute natural language instructions after SFT.
- **Code Generation**: Write and debug code across multiple languages.
- **Tool Use**: Call external APIs and tools when given tool descriptions.

### Limitations

| Limitation | Description |
|------------|-------------|
| [[hallucination]] | Generate plausible but false statements |
| Knowledge cutoff | No information after training data cutoff |
| Context window | Limited working memory (tokens, not true memory) |
| Reasoning gaps | Fail on multi-step symbolic and mathematical problems |
| Bias | Inherit social biases from training data |

### Notable Models

- **GPT-4** (OpenAI): 27% AGI score per CHC evaluation; strong across most domains
- **GPT-5** (OpenAI): 57% AGI score per CHC evaluation; significant improvement
- **LLaMA 2/3** (Meta): Open-weight causal decoders
- **Claude series** (Anthropic): RLHF-aligned, constitutional AI
- **Gemini** (Google DeepMind): Multimodal

## Related Pages

- [[transformer-architecture]] — the architectural foundation of all modern LLMs
- [[scaling-laws]] — how performance improves predictably with scale
- [[pretraining-and-finetuning]] — training pipeline in detail
- [[rlhf-and-alignment]] — alignment after pre-training
- [[in-context-learning]] — zero/few-shot prompting mechanics
- [[emergent-abilities]] — capabilities that appear only at sufficient scale
- [[hallucination]] — a core failure mode
- [[retrieval-augmented-generation]] — external memory extension for LLMs
- [[model-context-protocol]] — tool-use infrastructure for LLMs
- [[agi-definition]] — where current LLMs sit on the path to AGI

## Contradictions

> **Context window as memory**: The LLM survey (Paper 2) presents longer context windows as progress in LLM capability. The AGI paper (Paper 5) argues that using context windows to compensate for the absence of Long-Term Memory Storage is a *capability contortion* — it masks a fundamental architectural gap rather than solving it. See [[capability-contortions]] and [[long-term-memory-in-ai]].
