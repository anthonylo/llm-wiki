---
title: In-Context Learning (ICL)
tags: [ICL, prompting, few-shot, zero-shot, chain-of-thought]
source: "2307.06435v10 — A Comprehensive Overview of Large Language Models (Naveed et al., 2023)"
---

## Summary

In-Context Learning (ICL) is the ability of [[large-language-models]] to perform new tasks from examples or instructions provided directly in the prompt — without any gradient updates to model weights. This emergent capability appears at sufficient scale and is the foundation of modern prompting techniques including zero-shot, few-shot, and chain-of-thought prompting.

## Explanation

### What is ICL?

At test time, the model receives a prompt containing:
- A task description (optional)
- Input-output *demonstrations* (few-shot) or none (zero-shot)
- The new query to answer

The model predicts the correct continuation by recognising the pattern from demonstrations. No backpropagation occurs; the "learning" is implicit in the forward pass via attention over the prompt.

### Prompting Paradigms

**Zero-Shot Prompting**
Only a task description; no examples:
```
Classify the sentiment of the following text as positive or negative.
Text: "The movie was unexpectedly moving."
Sentiment:
```

**Few-Shot Prompting**
Include k demonstrations:
```
Text: "I loved every minute." → Positive
Text: "Total waste of time." → Negative
Text: "The cinematography was stunning." →
```

**Chain-of-Thought (CoT) Prompting** (Wei et al., 2022)
Add reasoning steps in demonstrations:
```
Q: A bag has 3 red and 5 blue marbles. You pick 2. How many ways to pick 1 red and 1 blue?
A: Red choices: 3. Blue choices: 5. Total: 3×5 = 15.
Q: [new problem]
A:
```
CoT dramatically improves multi-step arithmetic and logical reasoning.

**Zero-Shot CoT**
Simply append "Let's think step by step." — the model generates its own reasoning chain.

**Tree-of-Thought (ToT)** (Yao et al., 2023)
Explore multiple reasoning branches, evaluate intermediate steps, backtrack. Useful for search-like problems.

**Self-Consistency**
Sample multiple CoT outputs, take majority vote over final answers. Increases reliability.

### Why Does ICL Work?

Several hypotheses:
1. **Pattern completion**: ICL is gradient descent compressed into attention weights during pre-training; the forward pass mimics optimisation
2. **Task recognition**: The model identifies the task from demonstrations and retrieves relevant pre-trained "skills"
3. **Meta-learning**: Pre-training on diverse tasks induces learning-to-learn behaviour

### Sensitivity Issues

ICL is sensitive to:
- **Example ordering**: Shuffling few-shot examples can change accuracy by up to 30%
- **Template format**: Minor phrasing changes affect outputs
- **Label space**: Using wrong labels in demonstrations can still produce correct answers (model ignores demonstration labels sometimes)

### ICL vs. Fine-tuning

| Property | ICL | Fine-tuning |
|----------|-----|-------------|
| Weight updates | None | Yes |
| Data requirement | 0–few examples | Hundreds to thousands |
| Inference cost | Higher (long prompt) | Standard |
| Generalisation | Broad | Task-specific |
| Persistence | Lost after session | Encoded in weights |

ICL is preferred when labelled data is scarce or when task flexibility matters. Fine-tuning wins for production deployments with stable tasks.

### Context Window as Working Memory

ICL relies on the context window to hold all demonstrations, reasoning, and history. This is a finite resource:
- Long contexts degrade "lost-in-the-middle" performance
- ICL cannot retain learning across sessions (stateless)

See [[long-term-memory-in-ai]] for why this is an architectural limitation.

## Related Pages

- [[large-language-models]] — ICL is an emergent property of LLMs at scale
- [[transformer-architecture]] — attention mechanism enables attending over demonstrations
- [[scaling-laws]] — ICL emerges as a capability only above certain parameter thresholds
- [[emergent-abilities]] — ICL is a canonical example of an emergent ability
- [[pretraining-and-finetuning]] — fine-tuning is the alternative to ICL
- [[long-term-memory-in-ai]] — ICL's limitation: context window is not persistent memory
- [[context]] — formal context theory provides a richer framework than token windows
- [[capability-contortions]] — relying on context window for memory is a capability contortion per the AGI paper

## Contradictions

> **ICL vs formal context**: In-context learning treats context as a flat token sequence. Formal context theory (Paper 1 / [[context]]) requires typed dimensions and formal operators. LLM context conflates task description, examples, history, and instructions into a single unstructured window.
