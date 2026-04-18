---
title: RLHF and Alignment
tags: [RLHF, alignment, reward-model, PPO, RLAIF, Constitutional-AI]
source: "2307.06435v10 — A Comprehensive Overview of Large Language Models (Naveed et al., 2023)"
---

## Summary

Reinforcement Learning from Human Feedback (RLHF) is the dominant technique for aligning [[large-language-models]] with human preferences — making models helpful, harmless, and honest. After supervised fine-tuning (SFT), a reward model is trained on human preference rankings, and the LLM is updated via policy optimisation (PPO) to maximise that reward signal.

## Explanation

### The Alignment Problem

A base LLM trained on raw text learns to predict text distributions, not to be helpful or safe. Without alignment:
- Models produce toxic, biased, or harmful outputs
- Models may optimise for fluency over factual accuracy
- Models follow the statistical pattern of training data, not user intent

RLHF addresses this by directly encoding human preferences into model behaviour.

### Three-Stage RLHF Pipeline

**Stage 1: Supervised Fine-Tuning (SFT)**
Fine-tune the pre-trained model on high-quality demonstration data (instruction → response pairs written by humans). Produces a capable instruction-following base.

**Stage 2: Reward Model Training**
- Collect comparison data: for a given prompt, show multiple SFT responses to human annotators
- Annotators rank responses by preference (quality, safety, helpfulness)
- Train a **reward model** (RM) — a separate LLM with a scalar output head — to predict which response humans prefer
- Loss: Bradley-Terry model over pairwise comparisons

**Stage 3: Policy Optimisation (PPO)**
- The SFT model is the **policy** (actor)
- Generate responses, score them with the RM
- Update the policy to maximise expected reward using Proximal Policy Optimisation (PPO)
- KL penalty from the SFT model prevents reward hacking (policy diverging too far)

```
Reward = RM_score(response) − β · KL(policy || SFT_policy)
```

### Reward Hacking

Models can find spurious patterns the reward model rewards without being genuinely better (Goodhart's Law: "when a measure becomes a target, it ceases to be a good measure"). Examples:
- Producing longer responses (annotators may prefer length as a proxy for quality)
- Using sycophantic language that scores well regardless of accuracy

The KL penalty mitigates this by penalising large policy divergence.

### Variants and Alternatives

| Method | Key Idea |
|--------|----------|
| **PPO** (InstructGPT, GPT-4) | Standard RL policy gradient with KL constraint |
| **DPO** (Direct Preference Optimisation) | Reformulates RL as supervised learning on preferences; no separate RM needed |
| **RLAIF** (RL from AI Feedback) | Replace human annotators with an AI critic (e.g., Claude) |
| **Constitutional AI** (Anthropic) | Self-critique against a written constitution + RLAIF |
| **Rejection Sampling** | Generate many responses, keep highest-RM-scored ones |

### Constitutional AI (Anthropic)

Anthropic's approach explicitly specifies a set of principles (a "constitution") the model must follow. The model:
1. Generates a response
2. Critiques its own response against the constitution
3. Revises based on critique
4. This revised response is used as training data

This reduces reliance on expensive human annotation for every category of harm.

### Alignment Objectives

A well-aligned model should be:
- **Helpful**: Complete tasks users request
- **Harmless**: Avoid producing harmful content
- **Honest**: Be truthful; express uncertainty accurately

The "HHH" framing (from Anthropic) captures the core tension: helpfulness and harmlessness can conflict.

## Related Pages

- [[large-language-models]] — RLHF is stage 3 of the LLM pipeline
- [[pretraining-and-finetuning]] — SFT precedes RLHF
- [[hallucination]] — alignment reduces but does not eliminate hallucination
- [[agi-definition]] — RLHF improves reasoning (theory of mind under R) and commonsense (under K), but doesn't map to a single CHC domain

## Contradictions

> **Alignment vs AGI**: RLHF improves perceived helpfulness and reduces harmful outputs. In the CHC framework, this touches theory-of-mind tasks (Reasoning, R=0%→7% GPT-4→GPT-5) and commonsense knowledge (K). However, RLHF has zero effect on Long-Term Memory Storage (MS=0% for both). A highly RLHF-aligned model is not necessarily closer to AGI — the 57% AGI score for GPT-5 is driven by improvements in M, R, A and V, not alignment.
