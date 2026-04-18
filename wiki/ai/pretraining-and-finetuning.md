---
title: Pre-training and Fine-tuning
tags: [pre-training, fine-tuning, transfer-learning, instruction-tuning]
source: "2307.06435v10 — A Comprehensive Overview of Large Language Models (Naveed et al., 2023)"
---

## Summary

Modern [[large-language-models]] are developed in stages: a general base model is first pre-trained on vast unlabelled corpora (learning language structure and world knowledge), then fine-tuned on curated task-specific or instruction-following data. This two-stage approach allows reusing expensive pre-training while adapting efficiently to downstream applications.

## Explanation

### Pre-training Objectives

Pre-training defines what the model learns to predict from unlabelled data:

| Objective | Description | Example Models |
|-----------|-------------|----------------|
| Causal / Full LM | Predict next token given all previous | GPT, LLaMA, Falcon |
| Prefix LM | Bidirectional over prefix, causal over suffix | GLM, PaLM |
| Masked LM (MLM) | Predict masked tokens bidirectionally | BERT, RoBERTa |
| Span Corruption | Predict masked spans (T5-style) | T5, UL2 |
| Unified LM | Combines multiple objectives in one model | UniLM |

Causal LM dominates for generative LLMs because it naturally supports both pre-training and open-ended generation at inference.

### Pre-training Data

High-quality, diverse corpora are essential:
- Web crawls (Common Crawl, C4, The Pile)
- Books (BookCorpus, Project Gutenberg)
- Code (GitHub, The Stack)
- Academic papers (arXiv, PubMed)
- Curated Wikipedia / encyclopaedic content

Data quality filtering (deduplication, language filtering, quality scoring) has outsized impact on final model quality.

### Transfer Learning and Fine-tuning

After pre-training, the model's weights serve as a starting point. Fine-tuning updates weights on a smaller, labelled dataset:

**Full Fine-tuning**: Update all parameters. Expensive but thorough.

**Parameter-Efficient Fine-tuning (PEFT)**:
- *LoRA*: Add low-rank weight matrices; train only these (<<1% of parameters)
- *Prefix Tuning*: Prepend trainable "soft prompt" tokens to each layer
- *Adapter Layers*: Insert small bottleneck modules between Transformer blocks

### Instruction Tuning

Instruction tuning (also: SFT — Supervised Fine-Tuning) trains the model to follow natural language instructions:

- Dataset: (instruction, response) pairs across diverse tasks
- Examples: FLAN, Alpaca, ShareGPT, OpenHermes
- Result: model generalises to *unseen* instruction types (cross-task generalisation)
- This is what turns a raw base model into a "chat" or "instruct" model

Key insight: diversity of tasks in the fine-tuning dataset matters more than dataset size alone.

### Multi-task Fine-tuning

Training simultaneously on many labelled tasks (NLU, NLG, translation, QA, etc.) produces more robust instruction-following. FLAN-T5 and FLAN-PaLM demonstrated that multi-task instruction tuning dramatically improves zero-shot generalisation.

### Fine-tuning vs. Prompting

| Approach | Updates Weights | Data Required | Cost |
|----------|----------------|---------------|------|
| Fine-tuning | Yes | Labelled examples | High |
| Prompting / ICL | No | In-context examples | Zero |
| LoRA / PEFT | Partial | Few examples | Low |

See [[in-context-learning]] for the prompting alternative.

### Catastrophic Forgetting

Fine-tuning on a narrow task can degrade performance on others (catastrophic forgetting). Mitigations:
- Replay buffers (mix in pre-training data)
- Regularisation (EWC — Elastic Weight Consolidation)
- Low learning rates

## Related Pages

- [[large-language-models]] — the full LLM development pipeline
- [[transformer-architecture]] — the architecture being trained
- [[rlhf-and-alignment]] — next stage after SFT: aligning model behaviour
- [[scaling-laws]] — how pre-training scale determines capability ceiling
- [[in-context-learning]] — an alternative to fine-tuning at inference time
- [[retrieval-augmented-generation]] — augments knowledge at inference rather than training time
