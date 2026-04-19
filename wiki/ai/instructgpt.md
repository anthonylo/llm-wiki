---
title: InstructGPT (RLHF for Instruction Following)
tags: [instructgpt, RLHF, PPO, alignment, SFT, reward-model, openai, ouyang, alignment-tax]
source: "2203.02155v1 — Training language models to follow instructions with human feedback (Ouyang et al., 2022)"
---

## Summary

InstructGPT (Ouyang et al., 2022) demonstrated that **Reinforcement Learning from Human Feedback (RLHF)** can make a 1.3B parameter model preferred by human evaluators over a 175B GPT-3 model. The paper formalised the three-stage alignment pipeline — Supervised Fine-Tuning (SFT) → Reward Model (RM) → PPO — and introduced the concept of the **alignment tax**: RLHF improves instruction following but can degrade performance on standard NLP benchmarks. Training InstructGPT costs 60 petaflops/s-days vs 3,640 for GPT-3 pre-training — alignment is more compute-efficient than scale for improving human preference.

## Explanation

### The Core Problem with GPT-3

GPT-3 ([[gpt-3]]) trained on internet text predicts statistically likely continuations — not necessarily helpful, truthful, or safe responses. Without alignment:
- GPT-3 generates text that *looks like* what follows a prompt, not what the user wants
- It produces toxic, biased, or harmful content at rates matching training data
- It often ignores explicit instructions in favour of statistical completion patterns

InstructGPT's goal: **align model behaviour with user intent** ("helpful, honest, harmless").

### Three-Stage RLHF Pipeline

**Stage 1: Supervised Fine-Tuning (SFT)**

- **Dataset**: 12,725 prompts (11,295 labeller-written + 1,430 API customer prompts)
- **Labels**: 40 contracted human labellers wrote high-quality responses
- **Training**: Fine-tune GPT-3 on (prompt, response) pairs — 16 epochs, cosine LR decay, residual dropout 0.2
- **LR**: 9.65×10⁻⁶ (1.3B/6B models), 5.03×10⁻⁶ (175B); batch sizes 32 and 8 respectively
- **Note**: Model selection uses RM score on validation set, not validation loss. SFT overfits validation loss after 1 epoch, but training longer improves both RM score and human preference ratings

**Stage 2: Reward Model Training**

- **Dataset**: 33,207 comparisons (6,623 labeller + 26,584 customer prompts); labellers ranked K=4–9 SFT responses per prompt
- **Architecture**: 6B parameter RM (not 175B — 175B RMs were unstable; 6B was stable across a wide range of LRs)
- **Training objective**: Bradley-Terry model over pairwise comparisons
  ```
  Loss = -E[ log σ(r(x,yw) - r(x,yl)) ]
  ```
  where yw = preferred response, yl = rejected response
- **Training**: Single epoch over full dataset; LR=9×10⁻⁶ with cosine schedule (10% of initial by end); batch=64 distinct prompts (4–9 completions each)
- **Sensitivity**: Insensitive to ±50% LR changes; very sensitive to epochs (multiple epochs overfit quickly)
- **RM accuracy**: 72.4 ± 0.4% on training labellers; 69.6 ± 0.9% on held-out labellers (5-fold cross-validation)

**Stage 3: PPO (Proximal Policy Optimisation)**

- **Policy**: The SFT model
- **Reward signal**: RM score minus a KL penalty
  ```
  Reward = RM(response) − β · KL(policy_θ || SFT)
  ```
  β=0.02 (typical 0.02–0.2). KL prevents reward hacking (diverging too far from SFT).
- **Dataset**: 31,144 customer prompts for PPO (no labels)
- **Training**: 256k episodes; batch=512, minibatch=64 (8 minibatches/batch); single inner epoch/minibatch; warmup over first 10 iterations at 1/10 peak LR; PPO clip ratio=0.2; sampling temperature=1.0

This is the same structure described in [[rlhf-and-alignment]], but InstructGPT provides the specific numbers and ablations.

### PPO-ptx: Reducing the Alignment Tax

**PPO-ptx** mixes PPO reward with the pre-training objective:

```
Reward = RM(response) − β · KL(policy || SFT) + γ · log P_pretrain(x)
```

γ=27.8 (pretraining loss coefficient); 8× more pretraining examples than RL episodes. Pretraining data randomly drawn from GPT-3's original pre-training set.

PPO-ptx largely closes the alignment tax gap while preserving instruction-following improvements.

### Dataset Composition

| Split | Labeller prompts | Customer prompts | Total | Purpose |
|-------|-----------------|-----------------|-------|---------|
| SFT | 11,295 | 1,430 | 12,725 | Demonstrations |
| RM | 6,623 | 26,584 | 33,207 | Comparisons |
| PPO | — | 31,144 | 31,144 | RL training (no labels) |

**Use case distribution** (Table 1): Generation 45.6%, Open QA 12.4%, Brainstorming 11.2%, Chat 8.4%, Rewrite 6.6%, Summarisation 4.2%, Classification 3.5%, Closed QA 2.6%, Extract 1.9%, Other 3.5%

**Language**: ~96% English; 4%+ in 20+ other languages. Model sometimes generates English when prompted in other languages.

**Deduplication**: Common prefix checking; 200 prompt limit per user ID.

### The Key Result: 1.3B > 175B

Human labellers preferred InstructGPT (1.3B) outputs over GPT-3 (175B) **85% of the time**.

**Head-to-head win rates** (InstructGPT 175B PPO-ptx vs.):

| Comparison | Win rate |
|-----------|----------|
| GPT-3 175B (few-shot prompted) | 71 ± 4% |
| SFT baseline (175B) | 73.4 ± 2% |
| FLAN (fine-tuned on 1M NLP examples) | 78 ± 4% |
| T0++ (fine-tuned on 1M NLP examples) | 79 ± 4% |

InstructGPT outperforms FLAN and T0 by large margins despite those models being trained on vastly more NLP task data — confirming that real-world instruction distributions matter more than NLP task breadth.

Held-out labellers (not in training data) prefer InstructGPT at roughly the same rate as training labellers — suggesting the model generalises to new annotators, not just the training cohort.

### The Alignment Tax

RLHF improves instruction following but **degrades performance on some standard NLP benchmarks**:

| Benchmark | GPT-3 | PPO | Change |
|-----------|-------|-----|--------|
| SQuAD v2 F1 | 76.3 | 71.8 | **−4.5 pp** |
| DROP F1 | 38.4 | 34.6 | **−3.8 pp** |
| HellaSwag | 80.3 | 78.4 | **−1.9 pp** |
| WMT En-Fr BLEU | baseline | regresses | negative |
| WinogradNLI | 88.3 | 89.5 | +1.2 pp |

The model becomes better at following instructions and worse at some knowledge-intensive NLP tasks. PPO-ptx (γ=27.8) largely closes these gaps.

### Safety Evaluations

**Hallucination**: InstructGPT halved the hallucination rate on closed-domain QA:

| Condition | Hallucination rate |
|-----------|-------------------|
| GPT-3 175B | 41% |
| InstructGPT 1.3B (PPO) | 21% |

On TruthfulQA: InstructGPT generates truthful and informative answers approximately **twice as often** as GPT-3.

**Toxicity**:
- When prompted to be respectful: InstructGPT produces 25% fewer toxic outputs than GPT-3
- Without any prompt: toxicity improvement largely disappears (no prompt condition)
- When explicitly instructed to be toxic: InstructGPT produces **more** toxic outputs than GPT-3 — RLHF amplifies compliance, including to harmful instructions

**Bias**: No significant improvement over GPT-3 on Winogender or CrowS-Pairs benchmarks. RLHF training with English-speaking labellers did not measurably reduce social biases.

### Failure Modes

Three specific failure modes documented:
1. **False premise acceptance**: If the prompt contains a false assumption, InstructGPT treats it as true ("The Eiffel Tower is in London — describe what you can see from its top")
2. **Excessive hedging**: Overly qualified responses to simple factual questions, giving multiple possible answers when one is clearly correct
3. **Multi-constraint degradation**: Performance degrades with multiple simultaneous constraints ("List 10 movies made in the 1930s set in France with a female lead") — each additional constraint reduces accuracy

### Human Labeller Setup

- **40 contractors** recruited from Upwork and Scale AI
- Screened via four criteria: sensitive speech flagging agreement (≥75%), model output ranking agreement with researchers (≥75%), demonstration quality score (≥6/7 Likert), self-assessed sensitivity to diverse groups
- Predominantly English-speaking, United States or Southeast Asia — limited demographic diversity
- ~1 labeller per comparison (cost constraint); inter-annotator agreement: 72.6 ± 1.5% among training labellers, 77.3 ± 1.3% among held-out labellers
- Each comparison: ~3–7 minutes

The labeller population is a key constraint: InstructGPT is aligned to the preferences of this specific group. Different demographics might produce different alignment.

### The Helpful/Honest/Harmless Framework

InstructGPT operationalised three alignment properties, in priority order:

1. **Helpful**: Complete the user's intended task
2. **Honest**: Not assert false things; express appropriate uncertainty; not create false impressions
3. **Harmless**: Not produce harmful, dangerous, or offensive content

The paper distinguishes between what models are aligned *to*:
- **Operator instructions**: What the API customer asks for
- **User intentions**: What end users actually want (may differ from literal prompt)
- **Labeller values**: What the 40 contractors judged as good
- **Human values broadly**: Much harder to specify and measure

InstructGPT is explicitly aligned to (3) and partially to (1–2). Alignment to broad human values remains an open research problem.

### Compute Efficiency of Alignment

| Training | Compute |
|---------|---------|
| GPT-3 pre-training | 3,640 petaflops/s-days |
| InstructGPT 175B SFT | 4.9 petaflops/s-days |
| InstructGPT 175B PPO-ptx | 60 petaflops/s-days |

RLHF alignment costs ~1.6% of the pre-training compute yet produces a model preferred by humans 71% of the time over the base model. This cost efficiency is a major argument for post-training alignment pipelines.

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

> **Toxicity amplification**: InstructGPT reduces toxicity by default but produces *more* toxic content than GPT-3 when explicitly instructed to. RLHF aligned the model to follow instructions — including harmful ones — more reliably. This is the "instruction-following alignment tax": better alignment to user intent means more faithful compliance with bad intent. This directly contradicts the expectation that alignment makes models unconditionally safer.

> **Labeller diversity**: InstructGPT's "alignment" reflects 40 specific labellers' values. The paper acknowledges: "Our labellers' instructions represent one approach to alignment." Scaling this to global deployment means encoding one cultural perspective as "aligned." This contradicts the Foundation Models paper's ([[foundation-models]]) concern about homogenization — here the homogenization is of *values*, not just capabilities.

> **Bias: alignment doesn't help**: RLHF significantly improves instruction following and truthfulness but shows no improvement on Winogender or CrowS-Pairs social bias benchmarks. Alignment optimises for what labellers prefer; if labellers don't systematically penalise biased outputs, bias is not reduced. This suggests alignment and debiasing require separate interventions.
