---
title: Foundation Models
tags: [foundation-models, emergence, homogenization, stanford, bommasani, ai-safety, transfer-learning]
source: "2108.07258v3 — On the Opportunities and Risks of Foundation Models (Bommasani et al., 2021)"
---

## Summary

"Foundation Models" is the term coined by Bommasani et al. (2021) at Stanford CRFM to describe models trained on broad data at scale that can be adapted to a wide range of downstream tasks. Examples include [[gpt-3]], BERT ([[bert]]), CLIP, DALL-E, and Codex. The paper argues these models represent a paradigm shift — not just a new technique — and introduces two defining properties: **emergence** and **homogenization**. The paper is a 214-page survey covering capabilities, applications, and risks across AI safety, law, healthcare, education, and more.

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

The paper notes this is analogous to critical infrastructure: if a core library (like OpenSSL) has a bug, everything depending on it is vulnerable simultaneously. The risk is a single point of failure at societal scale.

### Capabilities Covered (Selected)

The paper surveys foundation model capabilities across many dimensions:

| Capability | Example | Notes |
|-----------|---------|-------|
| Language understanding | BERT, GPT-3 | GLUE/SuperGLUE benchmarks |
| Language generation | GPT-3, T5 | Summarisation, translation |
| In-context learning | GPT-3 | Zero/few-shot without fine-tuning |
| Code generation | Codex | GitHub Copilot |
| Formal reasoning | GPT-3+verifier | Theorem proving, program synthesis |
| Image understanding | CLIP | Zero-shot classification |
| Image generation | DALL-E | Text-to-image |
| Robotics | RT-1 | Language-conditioned manipulation |
| Drug discovery | AlphaFold | Protein structure prediction |
| Healthcare | BioMedLM | Clinical note processing |

**Reasoning and search** (§2.4): Foundation models can contribute to unbounded search spaces (theorem proving, retrosynthesis) through three properties: *generativity* (unconstrained generation of candidate solutions), *universality* (transfer across problem types), and *grounding* (multimodal understanding of problem conditions).

### The Three-Paradigm Shift

The paper argues ML has gone through three paradigms:
1. **Feature engineering**: Hand-crafted features + simple models
2. **Architecture engineering**: Learned features, hand-designed architectures (ResNet, LSTM)
3. **Foundation models**: Pre-train on broad data, adapt downstream — architectural choices matter less than pre-training breadth and scale

In paradigm 3, a single architecture (Transformer) dominates all modalities. This creates both efficiency (reuse) and fragility (homogenization).

### Adaptation Methods

The paper covers a spectrum of adaptation techniques, ranging from expensive to cheap:

| Method | Description | Parameters updated |
|--------|-------------|-------------------|
| Full fine-tuning | Update all weights | All |
| Adapter modules | Add small bottleneck layers; freeze rest | ~1–5% |
| LoRA | Low-rank weight delta matrices | ~0.1–1% |
| Prefix/prompt tuning | Prepend learnable tokens | Prefix tokens only |
| Bias tuning | Update only bias parameters | ~0.1% |
| Zero-shot / ICL | No update; use prompt | 0% |

**Temporal adaptation**: As the world changes, foundation models go stale. Retraining is expensive; efficient update methods (continual learning, selective retraining) are an open challenge. Naive fine-tuning causes **catastrophic forgetting** — updates for new data destroy old knowledge.

**Machine unlearning**: Removing specific training data post-hoc (e.g., for GDPR compliance or copyright claims) without full retraining. Currently an open research problem — no efficient, reliable method exists.

### Evaluation Framework

A key distinction the paper draws:

| Type | What it measures | Examples |
|------|-----------------|---------|
| **Intrinsic** | The foundation model itself | Perplexity, embedding quality, probe accuracy |
| **Extrinsic** | Downstream task performance | GLUE, SQuAD, clinical trial matching |

Intrinsic metrics (e.g., perplexity) often do not predict extrinsic downstream performance well — a lower perplexity model is not necessarily better for summarisation. This **proxy relationship problem** means standard training metrics provide limited signal for real-world quality.

Evaluation design principles beyond accuracy: robustness to distribution shift, fairness across demographics, compute efficiency, environmental impact, and interpretability.

### Applications and Domain Risks

**Healthcare**: Clinical decision support, drug discovery, patient communication. Multiple data modalities: images, EHR tables, lab time series, genetics, clinical text. Key risks: hallucination of medical facts, lack of explainability (GDPR), training data representativeness (historical bias in clinical datasets).

**Law**: Contract review, discovery automation, case research, judge outcome prediction. Key risks: factuality guarantees absent (hallucination), risk scoring raises ethical and fairness concerns, access to justice gap (models may increase inequality if only available to well-resourced parties).

**Education**: Personalised tutoring, content generation, student feedback. Key risks: attribution problem (learner vs. FM contribution), unintended removal of teacher from the loop, privacy laws (FERPA, COPPA), student misconception detection ("noticing" errors requires pedagogical understanding).

**General AI research**: Foundation models as research tools — automatic theorem proving, drug discovery, combinatorial optimisation.

### Risks and Failure Modes

**Bias amplification**: Foundation models learn from internet-scale text, which reflects societal biases. Because many applications share one model, biases are amplified uniformly across all downstream uses. The paper distinguishes *intrinsic biases* (in representations) from *extrinsic harms* (in deployed behaviour) — they require different measurement approaches.

**Misuse**: The same model that writes helpful emails can generate personalised disinformation, deepfakes, phishing attacks, or harassment at scale. Higher-quality synthetic content is harder for humans to detect. Notably, foundation models could also *detect* misuse — a dual-use dynamic.

**Concentration of power**: Building frontier foundation models requires massive compute ($10M–$100M+ training runs). This restricts model development to a handful of organisations — concentrating decision-making about AI development globally.

**Environmental cost**: Training a single 175B parameter model produces ~552 tonnes of CO₂ equivalent. The paper argues for amortisation but acknowledges this assumes stable models — frequent retraining or many model families negates the argument. Environmental cost should be an explicit evaluation criterion.

**Single point of failure**: With homogenization, a flaw in one model becomes a flaw in thousands of products simultaneously.

**Security threats**: Adversarial triggers can cause foundation models to generate undesirable outputs. Memorization enables training data extraction attacks. "Function creep" — using a model for purposes beyond its original scope — introduces unforeseen failure modes.

**Multilingual gaps**: ~6,000 world languages exist; multilingual foundation models cover ~100. English dominates training data in quality and quantity. Parameter competition across languages means adding more languages may hurt high-resource language performance. Low-resource languages remain severely underserved.

### Relationship to Scaling Laws

The foundation model paradigm depends critically on [[scaling-laws]] (Kaplan et al., 2020): if performance scales predictably with data and parameters, then investing in large pre-trained models is economically rational. Foundation models are the operational manifestation of betting that scaling laws continue to hold — including across modalities, domains, and task types.

### Alignment and AI Safety

The paper treats alignment as a first-class concern:
- **Emergent harmful capabilities**: The same unpredictability that produces emergent beneficial capabilities produces emergent harmful ones — deception, strategic planning, misspecified goal pursuit
- **Misspecified objectives**: Foundation models optimised for next-token prediction (or human preference) may develop proxy objectives that diverge from intended goals
- **Interpretability gap**: The paper identifies interpretability as essential for safety analysis, but foundation models' emergent properties are by definition not anticipated — making post-hoc explanation validity uncertain
- **Longer-term hazards**: As capabilities advance, alignment becomes harder; the paper argues safety investment must scale with capability

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

> **Amortisation argument vs environmental cost**: The paper argues that training cost amortises over millions of API requests. However, this assumes the model is stable — any retraining, safety patching, or capability update incurs new environmental cost. If the field trains dozens of competing foundation models (GPT-4, Gemini, LLaMA, Claude, etc.), the amortisation argument breaks down. The homogenization that reduces per-application cost is in tension with the competitive diversity that drives progress.

> **Human acquisition vs foundation model data efficiency**: Foundation models see orders of magnitude more text than humans do in a lifetime. Yet humans generalise with far fewer examples and handle novel situations more robustly. The paper notes this sample efficiency gap — foundation models may not be learning the same representations as humans, raising questions about whether they will generalise in the same ways at the tail of the distribution.
