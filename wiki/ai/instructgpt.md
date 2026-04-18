---
title: InstructGPT (RLHF for Instruction Following)
tags: [instructgpt, RLHF, PPO, alignment, SFT, reward-model, openai, ouyang, alignment-tax]
source: "2203.02155v1 — Training language models to follow instructions with human feedback (Ouyang et al., 2022)"
---

## Summary

InstructGPT (Ouyang et al., 2022) demonstrated that **Reinforcement Learning from Human Feedback (RLHF)** can make a 1.3B parameter model preferred by human evaluators over a 175B GPT-3 model. The paper formalised the three-stage alignment pipeline — Supervised Fine-Tuning (SFT) → Reward Model (RM) → PPO — and introduced the concept of the **alignment tax**: RLHF improves instruction following but can degrade performance on standard NLP benchmarks.

## Explanation

### The Core Problem with GPT-3

GPT-3 ([[gpt-3]]) trained on internet text predicts statistically likely continuations — not necessarily helpful, truthful, or safe responses. Given a prompt like "Write a poem about Elon Musk," GPT-3 optimises for text that *looks* like what follows such prompts on the internet. It does not optimise for what the user actually wants.

InstructGPT's goal: **align model behaviour with user intent** ("helpful, honest, harmless").

### Three-Stage RLHF Pipeline

**Stage 1: Supervised Fine-Tuning (SFT)**

- **Dataset**: 13,000 prompts from the OpenAI API (real user prompts) + labeller-written prompts
- **Labels**: 40 contracted human labellers wrote high-quality responses to each prompt
- **Training**: Fine-tune GPT-3 on these (prompt, response) pairs via standard supervised learning
- **Result**: A well-behaved instruction follower but not optimised for preference

**Stage 2: Reward Model Training**

- **Dataset**: 33,000 comparisons — for each prompt, labellers ranked 4–9 SFT responses by preference
- **Architecture**: SFT model with a linear head producing a scalar reward
- **Training objective**: Bradley-Terry model over pairwise comparisons
  ```
  Loss = -E[ log σ(r(x,yw) - r(x,yl)) ]
  ```
  where yw = preferred response, yl = rejected response
- **Result**: A model that predicts which responses humans prefer

**Stage 3: PPO (Proximal Policy Optimisation)**

- **Policy**: The SFT model
- **Reward signal**: RM score minus a KL penalty
  ```
  Reward = RM(response) − β · KL(policy_θ || SFT)
  ```
  β typically 0.02–0.2. KL prevents the model from optimising for RM quirks (reward hacking).
- The policy (language model) generates responses; PPO updates weights to maximise expected reward
- **Sampling**: ~31,000 prompts used for PPO training

This is the same structure described in [[rlhf-and-alignment]], but InstructGPT provides the specific numbers and ablations.

### The Key Result: 1.3B > 175B

Human labellers preferred InstructGPT (1.3B) outputs over GPT-3 (175B) **85% of the time**.

This result established that:
- **Alignment technique matters more than parameter count** for human-perceived quality
- Raw scale is necessary but not sufficient; direction (alignment) matters
- The 175B GPT-3 is "more capable" on many NLP benchmarks, yet less preferred by humans

This directly contradicts the naive extrapolation of [[scaling-laws]]: beyond a threshold, adding parameters without alignment does not improve real-world utility.

### The Alignment Tax

RLHF improves instruction following but **degrades performance on some standard NLP benchmarks** — the "alignment tax":

| Benchmark | GPT-3 | PPO | Change |
|-----------|-------|-----|--------|
| SQuAD v2 F1 | 76.3 | 71.8 | -4.5 pp |
| DROP F1 | 38.4 | 34.6 | -3.8 pp |
| HellaSwag | 80.3 | 78.4 | -1.9 pp |
| WinogradNLI | 88.3 | 89.5 | +1.2 pp |

The model becomes better at following instructions and worse at some knowledge-intensive NLP tasks. This is because RLHF fine-tuning moves the model's distribution toward "what annotators prefer" — a distribution with different coverage than the NLP benchmark tasks.

### PPO-ptx: Reducing the Alignment Tax

To mitigate benchmark regression, the paper introduces **PPO-ptx**: mix the PPO reward with the original language modelling pre-training objective:

```
Reward = RM(response) − β · KL(policy || SFT) + γ · log P_pretrain(x)
```

γ=0.0 is standard PPO; γ>0 is PPO-ptx. The pretraining term anchors the model to its original distribution, reducing forgetting of NLP capabilities.

PPO-ptx largely closes the alignment tax gap while preserving instruction-following improvements.

### Hallucination Reduction

| Condition | Hallucination rate (closed-domain QA) |
|-----------|--------------------------------------|
| GPT-3 175B | 41% |
| InstructGPT 1.3B (PPO) | 21% |

RLHF halved the hallucination rate on this task. This is because the reward model was trained to prefer factually accurate, hedged responses over confident but incorrect ones. See [[hallucination]].

### Human Labeller Setup

- **40 contractors** recruited from Upwork and Scale AI
- Screened for agreement with researchers on sensitive content handling
- Labellers are predominantly English-speaking; limited diversity
- Each comparison takes ~3–7 minutes; 33,000 comparisons collected for RM

The labeller population is a key constraint: InstructGPT is aligned to the preferences of this specific group. Different demographics might produce different alignment.

### The Helpful/Honest/Harmless Framework

InstructGPT operationalised three alignment properties, in priority order:

1. **Helpful**: Complete the user's intended task
2. **Honest**: Not assert false things; express appropriate uncertainty; not create false impressions
3. **Harmless**: Not produce harmful, dangerous, or offensive content

When in conflict (e.g. a user requests harmful content), honesty and harmlessness take precedence over helpfulness. Labellers were given detailed rubrics.

This HHH framework (from Anthropic) became the standard framing for LLM alignment.

## Related Pages

- [[rlhf-and-alignment]] — the general RLHF framework; InstructGPT is the canonical implementation
- [[gpt-3]] — InstructGPT fine-tunes GPT-3; 1.3B aligned model outperforms 175B base model
- [[foundation-models]] — InstructGPT addresses the homogenization risk of raw GPT-3 deployment
- [[hallucination]] — RLHF reduces but doesn't eliminate hallucination
- [[pretraining-and-finetuning]] — SFT is the first stage of InstructGPT's pipeline
- [[emergent-abilities]] — alignment doesn't eliminate emergent capabilities, both beneficial and harmful
- [[scaling-laws]] — InstructGPT challenges "bigger = better" by showing alignment matters more

## Contradictions

> **Alignment tax vs NLP benchmarks**: InstructGPT is better by human evaluation but worse on SQuAD, DROP, and HellaSwag. This exposes a fundamental tension: human preferences and benchmark performance are not the same metric. If benchmark performance is used as the proxy for capability (as in most research), RLHF looks like a regression. If human preference is the metric, it's strictly better. The field has not fully resolved which metric matters more.

> **1.3B > 175B on human preference**: This result seems to refute scaling laws. However, the comparison is not strictly fair — InstructGPT 1.3B was fine-tuned on 13K demonstration prompts from GPT-3's API users (real-world distribution), which GPT-3 never saw in supervised form. The 1.3B model is better on the *specific task humans care about*; GPT-3 175B is still better on breadth. It is more accurate to say: RLHF is a highly effective technique for closing the preference gap between small and large models on the specific tasks it is trained for.

> **Labeller diversity**: InstructGPT's "alignment" reflects 40 specific labellers' values. The paper acknowledges this: "Our labellers' instructions represent one approach to alignment." Scaling this to global deployment means encoding one cultural perspective as "aligned." This contradicts the Foundation Models paper's ([[foundation-models]]) concern about homogenization — here the homogenization is of *values*, not just capabilities.
