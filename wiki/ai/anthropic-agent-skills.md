---
title: Anthropic Agent Skills
tags: [anthropic, agent-skills, claude-code, skill-md, progressive-disclosure, mcp, claude]
source: "www-anthropic-com-engineering-equipping-agents-for-the-real-world-with-agent-ski.pdf — Equipping agents for the real world with Agent Skills (Anthropic Engineering, 2025)"
---

## Summary

Anthropic's Agent Skills are organized folders of instructions, scripts, and resources that agents can discover and load dynamically to perform better at specific tasks. A skill is a directory containing a `SKILL.md` file with YAML front-matter (`name`, `description`) plus any additional linked files and code. At startup, skill metadata is loaded into the system prompt for all installed skills. When Claude determines a skill is relevant, it reads the full skill into context. This progressive disclosure model makes the effective skill context "effectively unbounded" while staying within the context window at runtime. Skills are supported across Claude.ai, Claude Code, the Claude Agent SDK, and the Claude Developer Platform. The format was published as an open standard in December 2025.

## Explanation

### The Core Concept

> "Building a skill for an agent is like putting together an onboarding guide for a new hire."
> — Anthropic Engineering, 2025

Instead of building fragmented custom agents for each use case, anyone can specialize agents with composable capabilities by capturing and sharing procedural knowledge. This transforms general-purpose agents into specialized ones.

The design maps directly to the [[agentic-skills]] formalization S=(C,π,T,R):
- **C (applicability condition)**: The `name` and `description` in SKILL.md front-matter — Claude uses these to decide when to trigger the skill
- **π (executable policy)**: The body of SKILL.md plus linked files and executable scripts
- **T (termination condition)**: Implicit — Claude determines when skill-guided execution is complete
- **R (interface)**: The SKILL.md file path and directory structure as the callable API

### Anatomy of a Skill: Progressive Disclosure

Progressive disclosure is the core design principle — skills let Claude load information only as needed, like a well-organized manual with a table of contents, then chapters, then appendix.

**Level 1: Skill metadata (always loaded)**
```yaml
---
name: pdf
description: "Enables PDF form filling and manipulation"
---
```
At startup, the `name` and `description` of every installed skill are pre-loaded into the system prompt. This provides just enough information for Claude to know when each skill should be used without loading all content into context. Claude Code exemplifies Pattern-1 (metadata-driven progressive disclosure) in the [[agentic-skills]] taxonomy.

**Level 2: SKILL.md body (loaded on activation)**
When Claude determines the skill is relevant, it reads the full `SKILL.md` into context. The body contains step-by-step instructions, usage constraints, and references to linked files.

**Level 3+: Linked files (loaded as needed)**
Skills can bundle additional files referenced by name from SKILL.md. For the PDF skill example, `SKILL.md` references `reference.md` and `forms.md`. Claude reads `forms.md` only when filling out a form — if the task doesn't involve forms, `forms.md` is never loaded.

**Practical implication**: The amount of context that can be bundled into a skill is effectively unbounded, because agents with filesystem access and code execution tools don't need to read the entirety of a skill into their context window. Only what is needed is loaded.

### Context Window Sequence (PDF Skill Example)

1. Context window begins: core system prompt + metadata for all installed skills + user's initial message
2. Claude triggers the PDF skill: invokes Bash tool to read `pdf/SKILL.md` into context
3. Claude determines forms are involved: reads `pdf/forms.md` into context
4. Claude proceeds with the user's task equipped with the relevant skill instructions

### Skills with Code Execution

Skills can include pre-written code that Claude executes at its discretion.

**Why code alongside instructions?** LLMs excel at reasoning but certain operations are better suited for traditional code execution — sorting, parsing, deterministic transformations. Beyond efficiency, many applications require the deterministic reliability that only code can provide.

**Example**: The PDF skill includes a pre-written Python script that reads a PDF and extracts all form fields. Claude can run this script without loading either the script or the PDF into context. Because the code is deterministic, this workflow is consistent and repeatable across invocations.

This maps to Pattern-5 (Hybrid NL+Code Macros) and Pattern-2 (Code-as-Skill) in the [[skill-design-patterns]] taxonomy.

### Development Best Practices

**Start with evaluation**: Identify specific gaps by running agents on representative tasks and observing where they struggle or require additional context. Build skills incrementally to address these shortcomings.

**Structure for scale**:
- When SKILL.md becomes unwieldy, split content into separate files and reference them
- If contexts are mutually exclusive or rarely used together, keep paths separate to reduce token usage
- Code can serve as both executable tools and as documentation — clarify which Claude should run vs read as reference

**Think from Claude's perspective**: Monitor how Claude uses your skill in real scenarios. Pay special attention to the `name` and `description` — Claude uses these when deciding whether to trigger the skill. Poor metadata → wrong skill activation (or no activation).

**Iterate with Claude**: Ask Claude to capture its successful approaches and common mistakes into reusable context and code within a skill. If it goes off track, ask it to self-reflect on what went wrong. This process helps discover what context Claude actually needs rather than trying to anticipate it upfront.

### Security Considerations

> "Skills provide Claude with new capabilities through instructions and code. While this makes them powerful, it also means that malicious skills may introduce vulnerabilities."
> — Anthropic Engineering, 2025

Key guidance from Anthropic:
- **Install skills only from trusted sources**
- For less-trusted sources: thoroughly audit before use by reading all bundled files, paying particular attention to code dependencies, bundled resources (images, scripts), and instructions directing Claude to connect to external network sources
- Prompt injection via skill payloads is the primary NL-level threat

For detailed threat analysis, see [[skill-security-governance]] which covers the ClawHavoc case study of 1,200 malicious skills in the OpenClaw marketplace.

### Relationship to MCP

The Anthropic blog post explicitly connects Skills to the [[model-context-protocol]]:

> "We'll also explore how Skills can complement Model Context Protocol (MCP) servers by teaching agents more complex workflows that involve external tools and software."

Skills handle procedural knowledge (how to use tools in multi-step workflows); MCP handles tool integration (what tools are available). They are complementary: a skill might describe a complex workflow that invokes several MCP-provided tools.

### Future Direction

Anthropic states its intent to:
1. Continue adding features for the full lifecycle: creating, editing, discovering, sharing, and using Skills
2. Enable organizations and individuals to share their context and workflows with Claude
3. Explore Skills complementing MCP servers
4. **"Enable agents to create, edit, and evaluate Skills on their own, letting them codify their own patterns of behavior into reusable capabilities"**

This last goal — autonomous skill self-generation — is directly in tension with SkillsBench evidence showing self-generated skills degrade agent performance by −1.3pp in open-ended multi-domain settings. See [[skills-evaluation]] for the contradiction.

### Open Standard

In December 2025 (2 months after the original blog post), Anthropic published Agent Skills as an open standard for cross-platform portability — enabling skills to be used across different agent frameworks, not just Anthropic's own products.

## Related Pages

- [[agentic-skills]] — formal definition of the concept Anthropic implemented; Skills exemplify P1+P5 design patterns
- [[skill-design-patterns]] — Pattern-1 (metadata-driven progressive disclosure) and Pattern-5 (hybrid NL+code macros) describe Claude Code's skill architecture
- [[skill-security-governance]] — security analysis including the ClawHavoc marketplace attack
- [[skills-evaluation]] — SkillsBench findings; curated skills like Anthropic's approach yield +16.2pp; self-generation (future goal) yields −1.3pp
- [[skill-lifecycle]] — Anthropic's approach maps to the lifecycle: human authoring (discovery+distillation) → SKILL.md storage → Claude activation (retrieval) → execution
- [[model-context-protocol]] — MCP complements Skills for tool integration vs. workflow knowledge
- [[in-context-learning]] — progressive disclosure is an architectural extension of in-context learning with persistent storage and selective loading

## Contradictions

> **Anthropic's autonomous skill creation roadmap vs SkillsBench evidence**: Anthropic expresses excitement about agents creating their own skills, saying this would let agents "codify their own patterns of behavior into reusable capabilities." The SkillsBench benchmark (86 tasks, 7,308 trajectories) shows self-generated skills degrade performance by −1.3pp on average, compared to +16.2pp for curated skills. Only Claude Opus 4.6 showed marginal improvement (+1.4pp) with self-generated skills. Anthropic's goal is achievable in principle — Voyager demonstrates self-generated skills working in constrained environments — but requires solving the verification problem for open-ended multi-domain settings first.

> **"Effectively unbounded" skill context vs focused-skill evidence**: Anthropic's progressive disclosure design makes bundled skill context "effectively unbounded." SkillsBench shows that comprehensive skills (exhaustive documentation) degrade performance by −2.9pp, while focused 2–3 module skills improve performance by +18.8pp. Progressive disclosure is the correct architectural mechanism (it prevents loading everything at once), but it does not prevent skill authors from creating individually comprehensive skill files. The design principle is sound; the authoring guidance must emphasize conciseness to realize its benefits.

> **Skills as complement vs replacement for model capability**: Anthropic frames skills as filling gaps in Claude's capabilities ("Claude already knows a lot about understanding PDFs, but is limited in its ability to manipulate them directly"). SkillsBench shows skills help most in healthcare and manufacturing — domains where pretraining data is sparse — and least in software engineering — a domain where Claude has abundant pretraining. This confirms the Anthropic framing: skills are most valuable as procedural supplements to model knowledge gaps, not as replacements for model capability in areas the model already handles well.
