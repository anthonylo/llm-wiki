---
title: Agentic Skill Design Patterns
tags: [agentic-skills, design-patterns, progressive-disclosure, code-as-skill, marketplace, voyager, mcp, openclaw]
source: "2602.20867v1 — SoK: Agentic Skills — Beyond Tool Use in LLM Agents (Jiang et al., 2025)"
---

## Summary

Jiang et al. (2025) identify seven system-level design patterns that describe how agentic skills are packaged, loaded, and executed. These patterns range from metadata-driven progressive disclosure (low autonomy, high token efficiency) to self-evolving libraries and marketplace distribution (high autonomy, high supply-chain risk). A complementary representation × scope taxonomy describes what skills are (NL, code, policy, hybrid) and what environments they operate over (web, OS, SWE, robotics). Real systems combine a median of 2 patterns; Claude Code uses 4.

## Explanation

### The Seven Design Patterns

#### P1: Metadata-Driven Progressive Disclosure

Skills are discoverable through compact metadata summaries (name, description, trigger conditions) that occupy minimal context. Full instructions are loaded only when the skill is selected for execution. This two-phase loading strategy addresses the finite context window constraint.

**Exemplary systems**: Claude Code, Semantic Kernel, LangChain, HuggingGPT

Claude Code registers each skill with a short description and trigger phrases. When the agent determines a skill is relevant, it reads the full SKILL.md — which may include multi-page instructions, reference documents, and scripts. See [[anthropic-agent-skills]].

**Main benefit**: Scale — an agent can know about hundreds of skills while spending context tokens only on the few it activates.

**Main risk**: Metadata quality. Wrong or incomplete descriptions cause retrieval to pick the wrong skill or miss a relevant one.

#### P2: Code-as-Skill (Executable Scripts)

Skills are executable programs (Python functions, shell scripts, DSL programs) invoked through a runtime interface.

**Exemplary systems**: Voyager (JavaScript functions in Minecraft), CodeAct (Python code actions), SWE-agent (shell execution), Code as Policies (robotic control)

Voyager generates JS functions as skills, stores them in a library, and retrieves them by natural-language description. CodeAct demonstrates that framing agent actions as executable Python code (rather than JSON tool calls) enables more expressive and verifiable behavior.

**Advantages**: Determinism — given the same inputs, a code skill produces the same outputs, enabling traditional software testing and verification.

**Limitation**: Brittleness — code skills break when underlying APIs, UI elements, or environmental conditions change.

#### P3: Workflow Enforcement

Skills impose hard-gated processes on agent behavior, ensuring the agent follows a prescribed methodology rather than improvising. Examples: TDD skill mandates tests-before-implementation; systematic debugging skill enforces diagnose-before-fix.

**Exemplary systems**: LATS (Language Agent Tree Search), TDD agents, systematic debuggers

LATS enforces a tree-search workflow combining planning, acting, and reflection in a structured loop.

**Note**: Pattern-3 operates at the controller level — it prescribes how the agent executes rather than constituting a reusable skill artifact itself. LATS exemplifies a workflow controller that hosts skills from other patterns.

**Advantage**: Reduces hallucination-driven shortcuts; provides clear audit trail.

**Governance risk**: If an attacker modifies workflow rules (e.g., through prompt injection), the enforcement mechanism is compromised.

#### P4: Self-Evolving Skill Libraries

The system evaluates whether each task's agent behavior produces a successful trajectory worthy of distillation into a new skill or refinement of an existing one.

**Exemplary systems**: Voyager, DEPS, CRADLE, GenerativeAgents (boundary case)

Voyager generates code-based skills, validates through in-game execution, and incorporates verified skills into a persistent library.

**Central tension**: Quality control. SkillsBench reports self-generated skills average **−1.3pp** relative to skill-free baselines — only one of five tested configurations showed improvement. Zero-shot self-generation without iterative verification degrades performance in open-ended settings. In contrast, Voyager and Eureka succeed in constrained environments with deterministic execution verification.

**"Skill debt"**: Without human oversight or robust verification, self-evolving libraries risk accumulating skill debt analogous to technical debt — each low-quality skill contributes incorrect heuristics that compound over time.

#### P5: Hybrid NL+Code Macros

Skills combine natural-language specifications with executable components within a single package. NL describes purpose, applicability conditions, and high-level logic; code provides deterministic implementation for concrete steps.

**Exemplary systems**: Claude Code (SKILL.md with NL + code blocks), ReAct (interleaved NL reasoning + executable actions)

ReAct represents a lightweight version: the agent alternates between NL reasoning ("I need to search for X") and executable actions (search API call), with the interleaving serving as an implicit hybrid skill.

**Advantage**: Flexibility — NL handles edge cases through reasoning; code provides determinism for well-understood steps.

**Risk**: Boundary ambiguity — when instructions conflict with code, the agent must decide which to follow, creating potential for inconsistent behavior.

#### P6: Meta-Skills (Skills That Create Skills)

Meta-skills analyze agent task history, identify recurring patterns, and generate candidate skills from those patterns.

**Exemplary systems**: Self-Instruct (precursor), CREATOR, Eureka (robotic reward function generation)

CREATOR enables LLMs to create new tools (code functions) on demand, disentangling abstract reasoning from concrete tool implementation. Eureka generates reward functions that parameterize robotic skills — creating skill specifications through code.

**Risk**: Recursive error amplification — if the meta-skill produces a flawed skill used as input for further skill generation, errors compound. Quality gates at each generation step are essential.

**Distinction from Pattern-4**: Pattern-4 is a lifecycle stage (self-evolving); Pattern-6 is a runtime callable generator. A meta-skill automates what would otherwise be manual discovery.

#### P7: Plugin/Marketplace Distribution

Skills are versioned, distributable packages with explicit dependency, compatibility, and governance metadata.

**Exemplary systems**: OpenAI GPT Store, Anthropic MCP servers, ToolLLM (16,000+ APIs), OpenClaw/ClawHub

Anthropic's [[model-context-protocol]] defines a standardized interface for tool and skill servers, enabling third-party skill distribution with authentication and permission boundaries.

OpenClaw grew to 200,000+ GitHub stars and ClawHub to 10,700+ published skills within weeks — faster than any software repository in history. This created a dual-source library: human-authored community skills alongside agent-authored local skills, both with full system access.

**Benefit**: Ecosystem growth; community contribution at scale.

**Critical risk**: Supply-chain attacks — a malicious or compromised skill package can execute arbitrary actions within the agent's permission scope. ClawHavoc demonstrated this at scale. See [[skill-security-governance]].

### Pattern Trade-offs

| Pattern | Context cost | Determinism | Composability | Governance |
|---------|-------------|-------------|---------------|-----------|
| P1: Metadata | Low | Low | Medium | Medium |
| P2: Code-as-skill | Low | High | High | High |
| P3: Workflow | Medium | High | Medium | High |
| P4: Self-evolving | Medium | Medium | Medium | Low |
| P5: Hybrid macro | Medium | Medium | Medium | Medium |
| P6: Meta-skill | High | Low | Low | Low |
| P7: Marketplace | Low | Varies | High | Medium–High |

**No single pattern dominates**. Production systems combine patterns: a marketplace-distributed plugin (P7) might use metadata-driven loading (P1) with hybrid NL+code implementation (P5) and workflow enforcement for critical steps (P3). Systems in the corpus use a median of 2 patterns (range 1–4). The most common combination is P1+P7 (metadata + marketplace), appearing in 4 systems.

### Representation × Scope Taxonomy

Complementing the system-level design patterns, skills are characterized along two orthogonal intrinsic axes.

#### Representation Axis (How the Policy is Encoded)

| Representation | Description | Governance surface |
|---------------|-------------|-------------------|
| **Natural language** | Step-by-step instructions, SOPs, playbooks | Easy to author, hard to verify; subject to interpretation ambiguity |
| **Code** | Python functions, shell scripts, DSL programs | Deterministic, testable; brittle to environmental changes |
| **Tool macros** | Structured sequence of tool calls with parameterization | Middle ground — more constrained than code, more expressive than single calls |
| **Policy-based** | Learned neural network fine-tuned on trajectories | Opaque; captures subtle patterns resistant to explicit codification |
| **Hybrid** | Combination of two or more of the above | Flexible; introduces boundary ambiguity |

#### Scope Axis (What Environment the Skill Operates Over)

| Scope | Examples | Benchmark |
|-------|----------|-----------|
| Single-tool | Database query skill with schema variation handling | — |
| Multi-tool orchestration | Search → extract → summarize → store | — |
| Web interaction | Form filling, information extraction, web workflows | WebArena, Mind2Web |
| OS/desktop workflows | Multi-application, window/file/system management | OSWorld |
| Software engineering | Bug localization, patch generation, testing, deployment | SWE-bench |
| Robotics/physical | Physical actuator control, navigation, manipulation | — |

**Scope × skill value interaction**: SkillsBench finds skills help most in healthcare (+51.9pp) and manufacturing (+41.9pp) but only +4.5pp in software engineering. This is consistent with the hypothesis that skills provide most value where the base model's pretraining data provides insufficient procedural grounding — domains abundant in code/math pretraining data benefit less.

### Sparsity of the Design Space

Table 5 in the SoK paper reveals most systems cluster in a narrow region: code-as-skill representation (P2) with self-evolving library patterns (P4) in game or SWE environments. Large regions remain unexplored, particularly:
- Policy-based skills with marketplace distribution (P7)
- NL skills with formal workflow enforcement (P3)

These unexplored regions may be inherently difficult or simply underexplored.

## Related Pages

- [[agentic-skills]] — formal definition S=(C,π,T,R) and the core concept
- [[skill-lifecycle]] — 7-stage lifecycle that the patterns support
- [[skill-security-governance]] — pattern-specific risk matrix and the ClawHavoc supply-chain attack
- [[anthropic-agent-skills]] — concrete P1+P5 implementation (SKILL.md progressive disclosure + hybrid NL+code)
- [[model-context-protocol]] — MCP is the canonical P7 marketplace distribution mechanism
- [[in-context-learning]] — P1 (progressive disclosure) is an architectural response to context window limits
- [[large-language-models]] — LLMs are the policy executor (π) for NL and hybrid skill representations

## Contradictions

> **Self-evolving libraries (P4) vs curated skills**: The SkillsBench benchmark shows self-generated skills average −1.3pp vs no-skills baseline, while Voyager and Eureka succeed with self-generated skills in constrained game/robotics environments. The critical factor is verifiability: bounded environments with deterministic execution feedback can validate self-generated skills; open-ended multi-domain settings cannot. The pattern is not inherently flawed — it requires execution-verified practice loops to work.

> **Code skills (P2) determinism vs brittleness**: Code skills offer determinism and testability but break when underlying APIs, UI elements, or environmental conditions change. Web interaction skills are particularly fragile: skills encoding "click the element with id=departure-input" break on UI updates; skills encoding "fill in the departure field" are more resilient. The tension between determinism (requiring precise specification) and robustness (requiring high-level intent encoding) is unresolved.

> **Representation–governance coupling**: More formal skill representations (code) admit stronger governance (static analysis, sandboxing, unit testing). NL skills resist all three. Yet NL is the easiest representation to author. Hybrid skills (P5) attempt a compromise but introduce boundary ambiguity. No existing system fully resolves the trade-off between authoring ease and governance strength.
