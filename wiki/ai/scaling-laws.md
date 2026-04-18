---
title: Scaling Laws
tags: [scaling, compute, Chinchilla, training, efficiency]
source: "2307.06435v10 — A Comprehensive Overview of Large Language Models (Naveed et al., 2023)"
---

## Summary

Scaling laws describe predictable power-law relationships between model size (parameters), training data size (tokens), compute budget, and model performance (loss). They allow researchers to forecast capability before training, allocate compute optimally, and plan roadmaps. The Chinchilla result (2022) overturned previous assumptions by showing that most large models were significantly undertrained relative to their parameter count.

## Explanation

### Kaplan et al. (2020) — OpenAI Scaling Laws

The original scaling law paper found:

> Test loss scales as a power law with N (parameters), D (tokens), and C (compute):
> `L(N) ∝ N^{-α_N}`, `L(D) ∝ D^{-α_D}`, `L(C) ∝ C^{-α_C}`

Key findings:
- Performance improves smoothly with scale — no plateau visible at that time
- **Given a fixed compute budget**, it was more efficient to scale parameters than data
- The recommended ratio was roughly N ∝ C^{0.73} (scale parameters faster than data)

This led to the era of very large, undertrained models (GPT-3: 175B params on 300B tokens).

### Chinchilla Scaling Laws (Hoffmann et al., 2022)

DeepMind's Chinchilla paper re-examined the compute-optimal frontier with more training runs. Key finding:

> **Compute-optimal training** requires scaling parameters and data *equally*:
> `N_opt ∝ C^{0.5}`,  `D_opt ∝ C^{0.5}`
> → ~20 tokens per parameter for compute-optimal training

Chinchilla (70B params, 1.4T tokens) outperformed Gopher (280B params, 300B tokens) despite 4× fewer parameters — demonstrating that token starvation was the dominant issue.

### Implications

| Model | Params | Training Tokens | Tokens/Param | Assessment |
|-------|--------|----------------|--------------|------------|
| GPT-3 | 175B | 300B | ~1.7 | Severely undertrained |
| Chinchilla | 70B | 1.4T | ~20 | Compute-optimal |
| LLaMA-2 | 70B | 2T | ~29 | Slightly over-trained (good for inference) |
| GPT-4 | ~1T (est.) | ~13T (est.) | ~13 | Unknown |

"Overtrained" models (more tokens per parameter than Chinchilla-optimal) are actually desirable for deployment because inference cost per query matters more than training cost at scale.

### Scaling and Emergent Abilities

Scaling laws predict *smooth* loss improvement, but many capabilities exhibit *discontinuous emergence* above certain scale thresholds. See [[emergent-abilities]].

### The Data Wall

A looming constraint: high-quality human-generated text on the internet is finite. Estimates suggest this "data wall" is approaching:
- Total estimated high-quality web text: 10T–100T tokens
- Already used by frontier models: 10T+ tokens
- Mitigation: synthetic data generation, multi-epoch training, code data, multimodal data

### Inference Scaling (Test-Time Compute)

Recent work (OpenAI o1, o3) shows that scaling *inference* compute via longer chain-of-thought also improves performance — especially on mathematical and reasoning tasks. This shifts the scaling paradigm from training-time to test-time compute.

## Related Pages

- [[large-language-models]] — scaling is how LLMs are built
- [[transformer-architecture]] — the architecture being scaled
- [[pretraining-and-finetuning]] — scaling governs pre-training efficiency
- [[emergent-abilities]] — capabilities that scale laws don't predict (discontinuous jumps)
- [[agi-definition]] — current models at 27–57% AGI score; scaling alone may not reach 100%

## Contradictions

> **Smooth scaling vs emergent jumps**: Scaling laws predict monotonically smooth loss improvement. Emergent abilities ([[emergent-abilities]]) appear discontinuously. This tension — whether capability is truly smooth or has phase transitions — is unresolved. The AGI paper (Paper 5) implicitly assumes qualitative capability thresholds, not just smooth scaling.
