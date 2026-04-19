---
title: Agentic Skill Lifecycle
tags: [agentic-skills, skill-lifecycle, voyager, reflexion, skill-distillation, llm-agents]
source: "2602.20867v1 — SoK: Agentic Skills — Beyond Tool Use in LLM Agents (Jiang et al., 2025)"
---

## Summary

The agentic skill lifecycle is a seven-stage model tracing a skill from initial formation to eventual retirement: **Discovery → Practice/Refinement → Distillation → Storage → Retrieval/Composition → Execution → Evaluation/Update**. The model is not strictly linear — feedback loops connect evaluation back to practice, retrieval back to storage, and execution back to discovery. This lifecycle view treats skills as evolving system components shaped by interaction, feedback, and deployment constraints, rather than static artifacts.

## Explanation

### Stage 1: Discovery

Skill discovery identifies recurring task patterns or workflow bottlenecks that justify encapsulating behavior into a reusable module.

| System | Discovery Mechanism |
|--------|---------------------|
| Voyager | Curriculum proposes increasingly complex tasks in Minecraft; successful novel task trajectories become skill candidates |
| DEPS | Plan decomposition identifies sub-goals; repeated sub-goal patterns are promoted to skills |
| AppAgent | User demonstrations on mobile interfaces identify reusable interaction patterns |
| SayCan | Language instructions grounded in robot affordances — candidate skills scored by language relevance AND physical feasibility |
| DECKARD | Language-guided world models: agent imagines plans before executing them in game environments |

**Key open problem**: Most systems rely on pre-defined curricula, human demonstrations, or explicit reward signals to seed discovery. Fully **unsupervised discovery** — identifying skill boundaries without human-provided task definitions — remains unsolved. See [[skills-evaluation]] §10.2.

### Stage 2: Practice and Refinement

Once a candidate skill is identified, it must be refined into a reliable procedure through iteration.

**Reflexion** demonstrates a *verbal reinforcement learning* loop: after a failed attempt, the agent generates textual analysis of what went wrong and uses it to guide the next attempt. This operates within an episode without persistent skill storage — transient skill refinement.

**Eureka** uses LLMs to autonomously design reward functions for robotic skill acquisition through evolutionary search, automating the practice-and-refine loop for physical skills.

**Inner Monologue** extends verbal feedback to embodied agents using language-based scene descriptions and success signals to iteratively refine robotic action sequences.

### Stage 3: Distillation

Distillation extracts a stable, generalizable procedure from trajectories or demonstrations and packages it into the `(C, π, T, R)` tuple with descriptive metadata.

| System | Distillation Method |
|--------|---------------------|
| AgentTuning | Collects trajectories from GPT-4 across diverse agent tasks → fine-tunes LLaMA models (distills procedural knowledge into model weights) |
| FireAct | Fine-tunes on ReAct-style traces → distills reasoning-acting patterns into internalized skill |

**Critical distinction**: Practice improves a skill's reliability through iteration; distillation changes its *representation* (e.g., from verbose trajectory to compact code function, or from prompt-based instructions to model weights).

### Stage 4: Storage and Retrieval

Skills must be persisted in a library with indexing mechanisms that support efficient retrieval.

- **Voyager**: skill library indexed by natural-language descriptions; embedding similarity retrieves relevant skills for new tasks
- **CRADLE**: multi-level memory stores skills alongside episodic context; retrieval based on both task similarity and environmental state
- **MemGPT**: hierarchical memory with main memory (context window) and archival storage (external database) — an infrastructure model for skill libraries

**The retrieval design challenge**: balancing precision (returning the most applicable skill) with recall (not missing relevant skills in novel contexts).

### Stage 5: Retrieval/Composition

At runtime, the agent selects relevant skills and composes them into higher-level workflows.

**Embedding-based retrieval**: Task description is embedded and compared against skill description embeddings; top-k matches loaded into context window. Used by Voyager, AppAgent.

**LLM-mediated routing**: Agent reasons about which skill to invoke based on skill metadata (Pattern-1 progressive disclosure). More flexible but consumes additional inference tokens.

**Hybrid strategy**: Embedding retrieval narrows the candidate set; agent reasoning selects the final skill. Balances recall (embedding) with precision (reasoning).

**Skill conflict resolution**: When C₁(o,g) = 1 and C₂(o,g) = 1 simultaneously, systems rely on embedding similarity ranking or ad hoc LLM judgment. A principled conflict-resolution policy (analogous to method specificity in HTNs or rule priority in production systems) remains an open research problem.

### Stage 6: Execution

Execution runs the skill policy π within the agent's action loop. Execution model varies by representation:
- **NL skills**: injected into context window
- **Code skills**: executed in sandboxed environments
- **Policy skills**: run through learned parameters

CodeAct demonstrates that representing agent actions as executable Python code (rather than structured JSON tool calls) improves both expressiveness and verifiability.

**Failure recovery**: When termination condition T signals failure, a recovery skill is invoked to diagnose the cause and decide whether to retry, backtrack, or escalate. LATS implements recovery through tree search; Reflexion uses verbal reflection. Treating recovery as a first-class skill has governance implications — the recovery skill must be at least as trusted as the skill it recovers.

**Multi-agent skill sharing**: MetaGPT assigns specialized roles (product manager, architect, engineer) each with role-specific skills composing into a software development workflow. AutoGen enables multi-agent conversations where agents with different skill profiles collaborate. Shared repositories introduce cross-agent security concerns — a compromised shared skill affects all agents consuming it.

### Stage 7: Evaluation and Update

After deployment, the system monitors performance, detects drift, and revises, replaces, or retires skills.

**Deterministic evaluation harnesses** are preferred: the environment itself provides ground-truth verification by checking environment state against expected outcomes. SkillsBench operationalizes this across 7,308 agent trajectories with deterministic verifiers. See [[skills-evaluation]].

**Skill drift exploitation**: Skills safe at authoring time may become unsafe as the environment evolves. An attacker controlling part of the environment (e.g., a web page a skill navigates) can manipulate it to change skill behavior without modifying the skill itself. See [[skill-security-governance]].

### Feedback Loops

The lifecycle is not linear. Three primary feedback loops:
1. **Evaluation → Practice**: When a deployed skill underperforms, it re-enters the practice loop
2. **Retrieval → Storage**: When indexing fails to surface relevant skills, the storage representation is revised
3. **Execution → Discovery**: When runtime failures reveal new recurring failure modes, they trigger new skill discovery

## Related Pages

- [[agentic-skills]] — formal definition S=(C,π,T,R) and core concept
- [[skill-design-patterns]] — how skills are packaged and executed (system-level patterns)
- [[skill-security-governance]] — threat model, trust tiers, and governance for skills at each lifecycle stage
- [[skills-evaluation]] — evaluation dimensions and SkillsBench benchmark results
- [[anthropic-agent-skills]] — Anthropic's concrete lifecycle: human authoring → SKILL.md → progressive disclosure → agent execution
- [[in-context-learning]] — related retrieval mechanism; skills extend ICL with persistent storage
- [[rlhf-and-alignment]] — feedback signals for skill refinement (human feedback, AI judges, reward models)

## Contradictions

> **Practice vs distillation in Reflexion**: Reflexion generates textual analysis after failures but does not produce persistent skills. The SoK paper classifies it under Pattern-3 (workflow enforcement) rather than Pattern-4 (self-evolving). This is an edge case: in-context refinement is procedurally similar to skill practice but differs in persistence. The absence of cross-session skill storage means Reflexion's "procedural knowledge" disappears at episode end — exactly the problem skills are meant to solve.

> **Distillation into model weights vs callable artifacts**: AgentTuning and FireAct distill skills into model weights through fine-tuning. This produces internally encoded procedural knowledge that requires no explicit skill retrieval at runtime. However, it sacrifices the explicit governance surface of callable skills (no C, T, or R to audit) and cannot be updated without retraining. The trade-off between implicit (weight-based) and explicit (callable) procedural knowledge is unresolved in the field.
