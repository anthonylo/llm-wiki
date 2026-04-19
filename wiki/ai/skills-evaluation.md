---
title: Agentic Skills Evaluation
tags: [agentic-skills, evaluation, skillsbench, deterministic-evaluation, benchmarks, curated-skills]
source: "2602.20867v1 — SoK: Agentic Skills — Beyond Tool Use in LLM Agents (Jiang et al., 2025)"
---

## Summary

Evaluating agentic skills requires measuring five dimensions (correctness, robustness, efficiency, generalization, safety) through deterministic evaluation harnesses rather than human grading. The SkillsBench benchmark (86 tasks, 7,308 agent trajectories, 11 domains) provides the most direct evidence: curated skills raise agent pass rates by **+16.2 percentage points** while self-generated skills degrade performance by **−1.3pp**. Smaller models equipped with curated skills outperform larger models without them. Focused 2–3 module skills outperform comprehensive documentation. 16 of 84 tasks show performance degradation with skills, highlighting the importance of the applicability condition C.

## Explanation

### Five Evaluation Dimensions

**1. Correctness**: Whether the skill achieves its intended outcome. Code skills: unit tests provide direct verification. Web interaction skills: environment state comparison (was the form submitted correctly?).

**2. Robustness**: Reliability under input variations, environment perturbations, and edge cases. A robust skill maintains consistent performance when confronted with minor deviations from training distribution (e.g., handling both legacy and updated UI layouts). Web skills encoding high-level intent ("fill in the departure field") are more robust than those encoding low-level actions ("click the element with id=departure-input").

**3. Efficiency**: Resource cost of executing a skill. Metrics: token consumption (NL skills), wall-clock time, number of tool calls, API costs. Efficiency directly affects deployment cost and composability — inefficient sub-skills slow downstream workflows.

**4. Generalization**: Whether a skill transfers to unseen tasks or domains. Requires out-of-distribution evaluation. Partially addressed by cross-website generalization in Mind2Web and cross-application evaluation in OSWorld.

**5. Safety**: Whether a skill avoids harmful actions, respects permission boundaries, and handles failures gracefully. Commonly evaluated through adversarial testing, red-teaming, and runtime monitoring for unauthorized behaviors.

### Deterministic Evaluation Harnesses

Human evaluation of agent skills does not scale. The preferred approach is **deterministic evaluation harnesses**: benchmark environments where success is measured automatically by checking environment state against expected outcomes.

**Key design principle**: Outcome-based verification — rather than judging intermediate reasoning quality or approach elegance, the harness checks whether the intended outcome was achieved. This aligns with skills as procedural modules valued for their effects, not their form.

SkillsBench operationalizes this by pairing each of 86 tasks with a deterministic verifier that checks environment state against expected outcomes, enabling reproducible evaluation across 7,308 agent trajectories.

### Benchmark-to-Skill-Dimension Mapping

| Benchmark | Environment | Correctness | Robustness | Efficiency | Generalization | Safety |
|-----------|------------|------------|-----------|-----------|---------------|--------|
| **SkillsBench** | Multi | ✓ | ~ | ✓ | ✓ | — |
| WebArena | Web | ✓ | ~ | ~ | — | — |
| Mind2Web | Web | ✓ | — | — | ✓ | — |
| OSWorld | Desktop | ✓ | ~ | — | ✓ | — |
| SWE-bench | SWE | ✓ | ~ | ~ | — | — |
| GAIA | Multi | ✓ | — | — | ✓ | — |
| AgentBench | Multi | ✓ | ~ | ~ | — | ✓ |
| AndroidWorld | Mobile | ✓ | ~ | — | — | — |

No single benchmark covers all dimensions; comprehensive skill evaluation requires combining multiple benchmarks.

### SkillsBench Anchor Case Study

SkillsBench evaluates 86 tasks across 11 domains: healthcare, manufacturing, cybersecurity, natural science, energy, finance, office work, media, robotics, mathematics, and software engineering.

**Configurations tested**: 7 agent-model configurations over 7,308 trajectories.

**Three conditions per task**: no skills, curated skills, self-generated skills — with deterministic verifiers ensuring objective evaluation.

#### Core Findings

**Curated skills dramatically improve performance**:
- Average pass rate increase: **+16.2pp** (24.3% → 40.6%)
- Only one configuration (Claude Opus 4.6) showed improvement with self-generated skills (+1.4pp); Codex + GPT-5.2 degraded by **−5.6pp**
- Self-generated skills average: **−1.3pp** relative to no-skills baseline

**Domain variance in curated skill benefit**:

| Domain | Pass rate improvement |
|--------|----------------------|
| Healthcare | **+51.9pp** |
| Manufacturing | **+41.9pp** |
| Cybersecurity | **+23.2pp** |
| Mathematics | +6.0pp |
| Software engineering | +4.5pp |

**Interpretation**: Skills provide the most value in domains where the base model's pretraining data is sparse or insufficiently procedural. Domains with abundant code and math pretraining data benefit less from external procedural knowledge. (Domain variance may also reflect confounders including task construction, verifier strictness, and skill authoring quality differences.)

#### Skill Quantity and Structure

- **2–3 module focused skills**: +18.6pp improvement (optimal)
- **4+ skills**: +5.9pp (diminishing returns)
- **"Detailed" skills** (moderate length, focused guidance): +18.8pp
- **"Comprehensive" skills** (exhaustive documentation): **−2.9pp** (degradation)

This pattern is consistent with Pattern-1 (metadata-driven progressive disclosure): loading focused procedural instructions outperforms loading comprehensive reference material. The quality problem is not just accuracy but also **conciseness** — effective skills must distill procedural knowledge rather than dump reference material.

#### Skills as Compute Equalizers

Smaller models equipped with curated skills can match or exceed larger models without skills:

| Configuration | Pass rate |
|--------------|-----------|
| Claude Haiku 4.5 with curated skills | **27.7%** |
| Claude Opus 4.5 without skills | 22.0% |

Skills substitute partially for model scale — procedural memory serves as an efficiency multiplier. This has direct cost implications: skill libraries may enable deployment of cheaper models with equivalent performance.

#### Negative-Delta Tasks

16 of 84 tasks show performance **degradation** with skills, with the worst case at **−39.3pp** — occurring where the base model already performs well and skills introduce conflicting guidance.

This highlights the importance of the applicability condition C in the `S=(C,π,T,R)` formalization: a skill should activate only when its procedural knowledge is beneficial. An overbroad C that activates in contexts where the agent's baseline is already strong degrades performance by introducing unnecessary constraints and distracting context.

### Open Evaluation Challenges

**Self-generated skill quality in open-ended settings**: SkillsBench shows self-generation fails in multi-domain settings without execution-verified practice loops. Voyager and AgentBench provide partial corroboration from independent sources (constrained environments succeed), but independent replication of the curated-vs-self-generated comparison across additional benchmarks is needed.

**Benchmark reliance**: Published benchmark results may not reflect real-world skill utility. Production deployments involve longer time horizons, messier environments, and adversarial conditions not captured by existing benchmarks.

**Skill boundary detection**: Current benchmarks do not evaluate whether agents correctly identify which tasks require skills vs. which they can solve from pretraining alone.

## Related Pages

- [[agentic-skills]] — formal definition S=(C,π,T,R); applicability condition C is the key to preventing negative-delta tasks
- [[skill-lifecycle]] — evaluation is stage 7 of the lifecycle; feeds back to practice and discovery
- [[skill-design-patterns]] — pattern trade-off table includes context cost and determinism; SkillsBench confirms P1 (focused metadata) outperforms P6 (comprehensive meta-skill generation)
- [[skill-security-governance]] — deterministic evaluation harnesses are the defense layer for self-generated skill quality; safety is a distinct evaluation dimension
- [[anthropic-agent-skills]] — progressive disclosure is Anthropic's architectural response to the comprehensive-skills degradation finding

## Contradictions

> **Curated vs self-generated skills**: SkillsBench shows self-generated skills hurt performance (−1.3pp). Voyager succeeds with self-generated skills by constraining generation to a specific environment with deterministic feedback. The finding is not that self-generation always fails — it is that self-generation requires verified practice loops. The SkillsBench evidence indicates the viability of self-generation depends critically on domain specificity and automated verification. Anthropic's future roadmap (agents creating their own skills) depends on solving this verification problem first.

> **Skill quantity vs performance**: Intuitively, more relevant skills should help more. SkillsBench shows the opposite: 4+ skills underperform 2–3 skills by 12.7pp. Comprehensive skills underperform focused skills by 21.7pp. The mechanism is context overload — loading too many instructions crowds out the agent's reasoning about the actual task. This is an empirical finding specific to current LLM context window dynamics; future models with better attention over long contexts may shift this finding.

> **Domain performance vs pretraining data hypothesis**: The hypothesis that skills help most where pretraining data is sparse (healthcare, manufacturing) and help least where pretraining data is abundant (SWE, mathematics) is plausible but unconfirmed. Alternative explanations include task construction difficulty, verifier strictness, and skill authoring quality varying across domains. Disentangling these confounders requires controlled experiments beyond what SkillsBench currently provides.
