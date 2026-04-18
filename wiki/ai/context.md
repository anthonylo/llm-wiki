---
title: Context (Formal Theory)
tags: [context, logic, AI, formal-systems]
source: "0912.1838v1 — A Brief History of Context (Kaiyu Wan, 2009)"
---

## Summary

Context is the information surrounding an entity or event that gives it meaning. Formal context theory attempts to make this intuitive notion mathematically precise — enabling context-aware reasoning systems, programming languages, and AI agents to handle context as a first-class citizen rather than an implicit background assumption.

## Explanation

### The Problem of Context

Context pervades all of computing and reasoning: the meaning of a variable depends on its scope, the truth of a statement depends on the world it describes, and the relevance of information depends on the task at hand. Despite its ubiquity, context remained informally treated in most systems until researchers began formalising it in the 1980s–2000s.

### McCarthy's AI Formalization

John McCarthy (1993) proposed that context should be a formal object in AI. His key contribution was the *ist* predicate:

> `ist(c, p)` — "proposition p is true in context c"

This allows lifting and entering contexts:

- **Outer** → `ist(c, p)` elevates a proposition into context c
- **Enter** → inside context c, p holds directly

McCarthy's framework enabled *context inheritance*: a child context inherits propositions from its parent unless overridden.

### Formal Definition (Wan, 2009)

A context `c` is defined as a typed set of dimension-value pairs:

```
c = { (d, x) | d ∈ DIM  ∧  x : T_d }
```

Where:
- `DIM` is the set of context dimensions (e.g., time, location, user, task)
- `T_d` is the type of values for dimension `d`
- Each dimension has at most one value per context (functional constraint)

### Context Operators

| Operator | Symbol | Meaning |
|----------|--------|---------|
| Override | `c₁ ⊕ c₂` | c₂ values take precedence over c₁ |
| Choice | `c₁ \| c₂` | non-deterministic choice between contexts |
| Projection | `c ↓ D` | restrict context to dimension set D |
| Hiding | `c ↑ D` | remove dimensions D from context |

### The Lucx Language

Wan proposes *Lucx* — a context-aware extension of the logic programming language Luc. Lucx adds context as a first-class computation parameter:

- Programs can query, construct, and modify their own context
- Enables clean separation of "what to compute" from "in what context"
- Context polymorphism: same function, different contexts, different behaviour

### Context in Distributed Systems

Context becomes especially important in multi-agent and distributed systems:

- **Location context**: where is the agent?
- **Time context**: what is the temporal frame?
- **Capability context**: what resources are available?
- **Epistemic context**: what does this agent know?

Formal context operators enable composing and transforming contexts safely as information flows between components.

## Related Pages

- [[model-context-protocol]] — MCP treats context as a data structure passed between hosts, clients, and servers; informal compared to Wan's typed relation
- [[in-context-learning]] — LLMs use "context" as a token window; a fundamentally different (informal) notion from formal context theory
- [[large-language-models]] — LLM context windows are positional sequences, not typed dimension-value pairs
- [[agi-definition]] — AGI systems must reason across multiple contextual frames; Wan's framework provides formal machinery for this
- [[capability-contortions]] — treating long context windows as a substitute for long-term memory is an informal use of "context" that formal theory would distinguish

## Contradictions

> **Informal vs formal context**: The term "context" is overloaded across all five papers. Wan (2009) defines context as a typed mathematical relation with formal operators. LLM papers (2307.06435) and MCP (2503.23278) use "context" informally to mean "token sequence in the prompt window." These are fundamentally different concepts — conflating them risks architectural confusion.

> **MCP naming**: The "Model Context Protocol" (Paper 4) uses "context" to refer to tool invocations and data passed to/from servers — closer to McCarthy's ist-predicate idea of passing propositions into a context, but without the formal typing that Wan requires.
