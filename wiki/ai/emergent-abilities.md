---
title: Emergent Abilities
tags: [emergence, scaling, capabilities, phase-transition]
source: "2307.06435v10 — A Comprehensive Overview of Large Language Models (Naveed et al., 2023)"
---

## Summary

Emergent abilities are capabilities that appear unpredictably in [[large-language-models]] above certain scale thresholds, absent in smaller models but suddenly present in larger ones. Unlike smoothly scaling metrics (loss, perplexity), emergent abilities exhibit phase-transition behaviour — near-zero performance below a threshold, then rapid capability gain beyond it. This phenomenon makes LLM capability forecasting difficult and has significant implications for AI safety.

## Explanation

### Definition

Wei et al. (2022) formally defined emergent abilities as:

> "Abilities that are not present in smaller-scale models and are not linearly predictable from performance on smaller scales."

A capability is emergent if its accuracy curve versus model scale shows a sharp inflection point rather than a smooth power-law improvement.

### Canonical Examples

| Ability | Approximate Emergence Threshold | Description |
|---------|--------------------------------|-------------|
| Few-shot prompting | ~10B parameters | Using in-context examples effectively |
| Arithmetic (multi-digit) | ~50B parameters | Correctly solving 3-digit multiplication |
| Chain-of-thought reasoning | ~60B–100B parameters | Step-by-step reasoning chains work |
| BIG-Bench Hard tasks | ~100B–200B parameters | Complex logical, symbolic tasks |
| Calibrated uncertainty | ~100B+ parameters | Models know when they don't know |

### Mechanism Hypotheses

1. **Multi-component skills**: Some capabilities require multiple sub-skills that all must reach sufficient competence. Each scales smoothly, but the composed capability appears emergent.

2. **Metric granularity**: Coarse-grained binary metrics (right/wrong) hide smooth sub-task improvement. If measured with partial credit metrics, emergence may disappear.

3. **Representation phase transitions**: Analogous to physics phase transitions — qualitative state change when a critical density of interconnected representations is reached.

### The Debate: Are Emergent Abilities Real?

Schaeffer et al. (2023) argued that many "emergent" abilities are artefacts of discontinuous metrics. Measuring the same underlying capability with a continuous metric (e.g., token-level accuracy vs. string match) often reveals smooth scaling.

Counterargument: even if the underlying latent capability scales smoothly, the *practical* ability threshold (where a capability becomes useful) is real and matters for deployment.

### Implications for AI Safety

Emergent abilities create *predictability gaps*: researchers cannot enumerate all capabilities that will emerge from a model of a given scale before training. This is relevant to:
- Dangerous capability discovery (biosecurity, cyberoffence)
- Safety evaluations (red-teaming may miss emergent attack vectors)
- Governance (scale thresholds for reporting/oversight)

The AGI paper (Paper 5) implicitly references emergence when noting that GPT-5 jumps from 27% to 57% AGI score — a significant qualitative capability shift across a single generation.

### Emergent Abilities and AGI

The AGI definition paper ([[agi-definition]]) identifies 10 cognitive domains and scores current models. If domains exhibit emergent thresholds, AGI might arrive suddenly when the last critical domains cross their thresholds — rather than as a gradual linear progression.

## Related Pages

- [[large-language-models]] — the systems exhibiting emergent abilities
- [[scaling-laws]] — smooth scaling backdrop against which emergence appears discontinuous
- [[in-context-learning]] — ICL is a primary emergent ability
- [[agi-definition]] — AGI involves a threshold of cognitive domains; emergence is relevant
- [[capability-contortions]] — contortions may mimic emergent capabilities without genuine underlying ability

## Contradictions

> **Smooth vs discontinuous**: Scaling laws ([[scaling-laws]]) predict smooth loss improvement. Emergent abilities suggest discontinuous jumps. Schaeffer et al. (2023) argue these are compatible (metric choice artefact). Whether capabilities are truly discontinuous has deep implications for safety forecasting and AGI timelines.
