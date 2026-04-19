---
title: Agentic Skills
tags: [agentic-skills, llm-agents, procedural-memory, tool-use, jiang, anthropic, sok]
source: "2602.20867v1 — SoK: Agentic Skills — Beyond Tool Use in LLM Agents (Jiang et al., 2025)"
---

## Summary

"Agentic skills" are reusable, callable modules that encapsulate procedural knowledge for LLM agents — analogous to procedural memory in cognitive science. Unlike one-shot plans or atomic tool calls, skills persist across tasks and carry their own applicability conditions, execution policies, termination criteria, and callable interfaces. Jiang et al. (2025) provide the first systematization of the concept, formalising it as a four-tuple S = (C, π, T, R), and mapping the full lifecycle, design patterns, security threats, and evaluation landscape. Anthropic independently developed the same abstraction concretely as [[anthropic-agent-skills]].

## Explanation

### Formal Definition

> "An agentic skill is a tuple S = (C, π, T, R)"
> — Jiang et al., 2025

- **C** (Applicability Condition): `C : O × G → {0,1}` — a predicate over observations and goals that determines whether the skill is appropriate for the current context
- **π** (Executable Policy): `π : O × H → A ∪ Σ` — maps observations and interaction history to actions or sub-skill invocations; may be NL instructions, code, a learned controller, or hybrid
- **T** (Termination Condition): `T : O × H × G → {0,1}` — specifies when the skill has completed (successfully or not)
- **R** (Reusable Interface): `R = (name, params, returns)` — callable signature for programmatic invocation by the agent, other skills, or external orchestrators

This parallels the **options framework** `(I, π, β)` in reinforcement learning (Sutton et al.), where C corresponds to the initiation set I and T to the termination condition β. The interface R adds explicit invocability, which the options framework lacks.

### Skills vs Related Abstractions

| Abstraction | Unit of Reuse | Execution Semantics | Composability | Governance |
|------------|--------------|---------------------|---------------|-----------|
| **Tool** | Single API call | Stateless, single invocation | Sequential chaining | Permission per tool |
| **Plan** | Task decomposition | One-time reasoning scaffold | Hierarchical decomposition | None (ephemeral) |
| **Episodic memory** | Stored observation | Retrieval, no execution | Indirect (informs reasoning) | Access control on store |
| **Prompt template** | Text fragment | Injected into context window | String concatenation | Template authorship |
| **Agentic skill** | Callable workflow | Hierarchical, with termination | DAG, recursive | Trust tier, sandboxing, provenance |

The key distinctions:
- Tools lack internal decision-making and termination logic
- Plans are one-time and not directly executable
- Memory encodes *what happened*, not *how to act*
- Prompt templates have no applicability conditions or callable interface
- Skills encode *how to act* across recurring task classes — this is **procedural memory**

### Skills as Procedural Memory

Anderson's ACT-R cognitive architecture distinguishes *declarative memory* (facts) from *procedural memory* (condition–action pairs). Experts differ from novices in the richness of their procedural repertoire — patterns that trigger automatically when conditions are met, freeing working memory for higher-level reasoning.

LLM agents face the same problem: without a skill layer, every task requires re-deriving an execution strategy from scratch within a finite context window. Skills serve as the agent's procedural memory, compressing learned procedures into reusable modules that reduce context window load — analogous to how *chunking* in human expertise compresses multi-step procedures into single retrievable units.

**Practical implication**: A curated skill verified across many contexts is more reliable than an ad-hoc plan, for the same reason a tested library function is more reliable than inline code.

### Evidence for Skills as Compute Equalizers

The SkillsBench benchmark (86 tasks, 7,308 trajectories) provides direct evidence:
- Curated skills raise agent pass rates by **+16.2 percentage points** (24.3% → 40.6%)
- Self-generated skills **degrade** performance by **−1.3pp** on average
- **Claude Haiku 4.5 with skills (27.7%) outperforms Claude Opus 4.5 without skills (22.0%)** — skills substitute for model scale
- Focused skills (2–3 modules) yield +18.6pp; 4+ modules show diminishing returns (+5.9pp)
- "Comprehensive" skills with exhaustive documentation degrade performance by −2.9pp

Domain variance: healthcare (+51.9pp), manufacturing (+41.9pp), cybersecurity (+23.2pp), software engineering (+4.5pp), mathematics (+6.0pp). Skills help most where pretraining data provides insufficient procedural grounding.

See [[skills-evaluation]] for full benchmark details.

### Lifecycle Overview

Skills are not static — they move through seven stages: **Discovery → Practice/Refinement → Distillation → Storage → Retrieval/Composition → Execution → Evaluation/Update**. Feedback loops connect evaluation back to practice and discovery. See [[skill-lifecycle]] for the full model.

### Design Patterns

Seven system-level design patterns describe how skills are packaged and executed, from metadata-driven progressive disclosure (P1) through marketplace distribution (P7). Anthropic's Claude Code uses P1 + P3 + P5 + P7 (four patterns simultaneously). See [[skill-design-patterns]] for the full taxonomy.

### Security

Skills create a new attack surface: a compromised skill can steer an agent toward malicious outcomes while appearing benign at the metadata level. Six primary threat categories exist, including poisoned retrieval, malicious payloads, and supply-chain attacks. The ClawHavoc campaign (1,200 malicious skills, 36.8% infection rate) demonstrated this at scale. See [[skill-security-governance]] for full analysis.

## Related Pages

- [[skill-lifecycle]] — 7-stage lifecycle from discovery to retirement
- [[skill-design-patterns]] — 7 design patterns and representation×scope taxonomy
- [[skill-security-governance]] — threat model, trust tiers, ClawHavoc case study
- [[skills-evaluation]] — SkillsBench findings, evaluation dimensions
- [[anthropic-agent-skills]] — Anthropic's concrete implementation (SKILL.md format, progressive disclosure)
- [[model-context-protocol]] — MCP as a marketplace-style skill distribution mechanism (Pattern-7)
- [[in-context-learning]] — related to how skills are injected into the context window
- [[foundation-models]] — foundation models are the enabling layer; skills are the procedural layer on top
- [[rlhf-and-alignment]] — alignment governs what skills an agent is willing to execute
- [[large-language-models]] — underlying model that interprets and executes skill policies

## Contradictions

> **Curated vs self-generated skills**: SkillsBench shows self-generated skills degrade performance (−1.3pp average). Yet Voyager and Eureka succeed with self-generated skills in constrained game environments. The resolution appears to be domain specificity: self-generation succeeds with deterministic execution verification in bounded environments; open-ended multi-domain settings without execution-verified practice loops cannot yet self-generate reliably. Anthropic's blog post expresses ambition for agents to "create, edit, and evaluate Skills on their own" — but the empirical evidence suggests this remains an open problem, not a solved one.

> **Skill quantity vs comprehensiveness**: SkillsBench empirically shows 2–3 focused skill modules outperform comprehensive documentation by 21.5pp (+18.6pp vs −2.9pp). The intuition is that comprehensive reference material overloads the agent's context; focused procedural knowledge is more actionable. This runs against the instinct to pack more information into a skill ("more context = better outcomes"). The Anthropic blog's progressive disclosure pattern is the architectural response to this finding — but it does not guarantee that skill authors will keep individual skill bodies concise.

> **Skills vs tool calling as the correct abstraction**: The SoK paper draws a sharp boundary: tools are atomic primitives, skills are multi-step procedural modules with applicability conditions and termination logic. In practice, the boundary is fuzzy — CodeAct shows that framing agent actions as Python code (a form of code-as-skill) outperforms structured JSON tool calls, blurring the tool/skill distinction. The field has not settled on a unified abstraction.
