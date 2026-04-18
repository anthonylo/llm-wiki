---
title: Foundation Models
tags: [foundation-models, emergence, homogenization, stanford, bommasani, ai-safety, transfer-learning]
source: "2108.07258v3 — On the Opportunities and Risks of Foundation Models (Bommasani et al., 2021)"
---

## Summary

"Foundation Models" is the term coined by Bommasani et al. (2021) at Stanford CRFM to describe models trained on broad data at scale that can be adapted to a wide range of downstream tasks. Examples include [[gpt-3]], BERT ([[bert]]), CLIP, DALL-E, and Codex. The paper argues these models represent a paradigm shift — not just a new technique — and introduces two defining properties: **emergence** and **homogenization**. The paper is a 214-page survey covering capabilities, applications, and risks.

## Explanation

### Definition

> "A foundation model is any model that is trained on broad data (generally using self-supervision at scale) that can be adapted (e.g. fine-tuned) to a wide range of downstream tasks."
> — Bommasani et al., 2021

The term "foundation" conveys two things:
1. **The model is the base** on which many downstream applications are built (structural metaphor)
2. **The foundation is unfinished** — the model is incomplete without adaptation (cautionary metaphor)

Prior terms: "pre-trained model," "large language model," "general-purpose AI system." The paper argues these don't capture the cross-modal and multi-task generality of systems like GPT-3.

### Two Defining Properties

**1. Emergence**

Foundation models exhibit capabilities that were not explicitly trained for and that emerged from scale and self-supervised training on diverse data:
- Language translation (GPT-3 was not trained to translate)
- In-context learning (see [[in-context-learning]])
- Code generation
- Commonsense reasoning
- Multimodal understanding (CLIP)

Emergence is related to but distinct from the concept in [[emergent-abilities]] — here it refers specifically to capabilities that arise from the breadth and scale of pre-training data rather than purely parameter count.

**2. Homogenization**

As more applications are built on fewer foundation models, the AI ecosystem **homogenizes**:
- A single GPT-3 model underlies dozens of products (text summarisers, code assistants, chatbots)
- Any bias, failure, or security vulnerability in that model propagates to all downstream applications
- This is a systemic, correlated risk: unlike previous ML, failures are no longer independent

The paper notes this is analogous to critical infrastructure: if a core library (like OpenSSL) has a bug, everything depending on it is vulnerable simultaneously.

### Capabilities Covered (Selected)

The paper surveys foundation model capabilities across many dimensions:

| Capability | Example | Notes |
|-----------|---------|-------|
| Language understanding | BERT, GPT-3 | GLUE/SuperGLUE benchmarks |
| Language generation | GPT-3, T5 | Summarisation, translation |
| In-context learning | GPT-3 | Zero/few-shot without fine-tuning |
| Code generation | Codex | GitHub Copilot |
| Image understanding | CLIP | Zero-shot classification |
| Image generation | DALL-E | Text-to-image |
| Robotics | RT-1 | Language-conditioned manipulation |
| Drug discovery | AlphaFold | Protein structure prediction |
| Healthcare | BioMedLM | Clinical note processing |

### Applications and Domains

The paper enumerates 5 major application domains:

1. **Healthcare**: Clinical decision support, drug discovery, patient communication; risks include hallucination of medical facts
2. **Law**: Contract review, case research, legal reasoning; risk of confident errors
3. **Education**: Personalised tutoring, content generation; risks around plagiarism, accuracy
4. **Finance**: Earnings analysis, risk assessment; hallucination risk in financial advice
5. **General AI research**: Foundation models as research tools for other AI work

### Risks and Failure Modes

**Bias amplification**: Foundation models learn from internet-scale text, which reflects societal biases. Because many applications share one model, biases are amplified uniformly across all downstream uses.

**Misuse**: The same model that writes helpful emails can generate phishing attacks, propaganda, or disinformation at scale.

**Concentration of power**: Building frontier foundation models requires massive compute ($10M–$100M+ training runs). This restricts model development to a handful of organisations — concentrating decision-making about AI development globally.

**Environmental cost**: Training a single 175B parameter model produces ~552 tonnes of CO₂ equivalent (comparable to 5 average US cars over their lifetime). Widespread deployment multiplies this.

**Single point of failure**: With homogenization, a flaw in one model becomes a flaw in thousands of products simultaneously — analogous to a critical dependency vulnerability.

### Relationship to Scaling Laws

The foundation model paradigm depends critically on [[scaling-laws]] (Kaplan et al., 2020): if performance scales predictably with data and parameters, then investing in large pre-trained models is economically rational. Foundation models are the operational manifestation of betting that scaling laws continue to hold.

### The Paradigm Shift Argument

The paper argues three prior paradigms in ML:
1. **Feature engineering** (hand-crafted features + simple models)
2. **Architecture engineering** (learned features, hand-designed architectures — ResNet, LSTM)
3. **Foundation models** (pre-train on broad data, adapt downstream)

In paradigm 3, the architectural choices matter less than the breadth and scale of pre-training. A single model architecture (Transformer) dominates all modalities. This creates both efficiency (reuse) and fragility (homogenization).

## Related Pages

- [[gpt-3]] — the canonical text foundation model; directly motivated this paper
- [[bert]] — earlier encoder-only foundation model; established pre-train/fine-tune paradigm
- [[emergent-abilities]] — capabilities that emerge from scale; directly relevant to "emergence" property
- [[scaling-laws]] — the mathematical basis for why investing in foundation models is rational
- [[in-context-learning]] — key emergent capability of foundation models
- [[rlhf-and-alignment]] — alignment techniques applied to foundation models
- [[instructgpt]] — RLHF alignment of a foundation model (GPT-3)
- [[large-language-models]] — foundation models for language specifically
- [[hallucination]] — a core risk of deploying foundation models

## Contradictions

> **Homogenization risk vs individual paper contributions**: Each paper in this cluster (Attention Is All You Need, BERT, GPT-3, InstructGPT) celebrates the power of a specific model. The Foundation Models paper warns that the downstream consequence of everyone building on the same models is **systemic correlated failure**. These perspectives are complementary but in tension: maximising capability by concentrating on one model family conflicts with resilience.

> **Emergence vs interpretability**: The paper celebrates emergence as evidence of foundation model power. However, emergent capabilities are, by definition, not understood ahead of time — they cannot be predicted, tested for, or reliably switched off. This makes safety analysis extremely difficult. The same scale that produces emergent helpfulness produces emergent harmful capabilities.

> **Broad pre-training vs task-specific fine-tuning**: Foundation models are meant to be adapted to downstream tasks. But the paper acknowledges that fine-tuning a foundation model on a narrow task can degrade its broader capabilities (catastrophic forgetting, alignment tax — see [[instructgpt]]). The "adapt to everything" promise is qualified by the practical difficulty of adaptation without degradation.
