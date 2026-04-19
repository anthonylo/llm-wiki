---
title: Agentic Skill Security and Governance
tags: [agentic-skills, security, prompt-injection, supply-chain, clawhavoc, trust-tiers, sandboxing, governance]
source: "2602.20867v1 — SoK: Agentic Skills — Beyond Tool Use in LLM Agents (Jiang et al., 2025)"
---

## Summary

Agentic skills introduce a distinct attack surface: a compromised skill can steer an agent toward malicious outcomes while appearing benign at the metadata level. Jiang et al. (2025) systematize six primary threat categories and propose a four-tier trust model for skill governance. The ClawHavoc campaign — 1,200 malicious skills infiltrating the OpenClaw marketplace, harvesting API keys, cryptocurrency wallets, and browser credentials from 135,000+ exposed instances across 82 countries — provides a documented large-scale example of marketplace-pattern (P7) supply-chain failure. Traditional malware scanners fail because they cannot audit the full `(C, π, T, R)` tuple; skill-native auditing tools are required.

## Explanation

### Six Primary Threat Categories

**1. Poisoned skill retrieval**
An attacker crafts skill metadata to cause the retrieval mechanism to surface a malicious skill in response to benign queries (analogous to SEO poisoning in web search). Exploits Pattern-1 (metadata-driven disclosure): adversarial metadata manipulates embedding-based ranking.

**2. Malicious skill payloads**
The skill's policy π contains instructions or code that perform unauthorized actions when executed. In code skills (P2), this resembles software supply-chain attacks. In NL skills (P5), the payload is a form of prompt injection — instructions embedded within skill text that redirect agent behavior.

**3. Cross-tenant leakage**
In multi-user systems with shared skill repositories, a skill authored by one tenant may access data or resources belonging to another. Requires per-tenant sandboxing with permission boundaries enforced by the execution runtime, not by the skill itself.

**4. Skill drift exploitation**
Skills safe at authoring time may become unsafe as the environment evolves. An attacker controlling part of the environment (e.g., a web page a skill navigates) can manipulate environmental state to change the skill's behavior without modifying the skill itself.

**5. Confused deputy via environmental injection**
An agent processing untrusted observations (web pages, user documents) may encounter adversarial instructions that coerce it into misusing an otherwise benign privileged skill. The skill itself remains uncompromised — the attack exploits the data/control boundary between observation space O and skill invocation. **This bypasses skill-level trust verification entirely**, making it particularly dangerous.

**6. Applicability condition poisoning**
An attacker manipulates input to C such that a malicious skill returns `C(o,g) = 1` universally, activating in contexts where it should not. Can occur through metadata poisoning (P1) or adversarial environmental states triggering overbroad predicates.

### Pattern-Specific Risk Matrix

| Pattern | Primary Risks | Severity |
|---------|--------------|----------|
| P1: Metadata | Metadata poisoning; misleading descriptions | Medium |
| P2: Code-as-skill | Code injection; sandbox escape; dependency vulnerabilities | High |
| P3: Workflow enforcement | Rule bypass via prompt injection; overly rigid constraints | Medium |
| P4: Self-evolving libraries | Poisoned distillation; skill drift; quality degradation | High |
| P5: Hybrid NL+code | Boundary ambiguity exploitation; conflicting instructions | Medium |
| P6: Meta-skills | Recursive error amplification; adversarial skill generation | High |
| P7: Marketplace | Supply-chain attacks; malicious packages; version tampering | Critical |
| Cross-cutting: Confused deputy | Environmental injection coerces misuse of privileged skills | High |
| Cross-cutting: C-poisoning | Adversarial input causes inappropriate skill activation | Medium |

### Four-Tier Trust Model

The paper proposes four nested trust tiers forming concentric security boundaries:

**Tier 1 (Metadata only)**: Agent sees only the skill name and description. No instructions or code are loaded. Supports skill discovery without execution risk.

**Tier 2 (Instruction access)**: Agent loads the skill's NL instructions into context window. Instructions may influence reasoning.
- **Critical caveat**: Tier-2 provides meaningful isolation only when the runtime enforces read-only mode during instruction loading, with tool execution gated behind a separate approval channel. Without architectural separation between reasoning and action, Tier-2 instructions can indirectly induce tool invocations through the agent's standard decision loop, effectively degrading to Tier-3.
- Tier-2 is particularly vulnerable to prompt injection embedded within skill instructions.

**Tier 3 (Supervised execution)**: Skill can execute actions (tool calls, code execution) but each action requires user approval or runs within a constrained sandbox.

**Tier 4 (Autonomous execution)**: Skill executes without per-action approval, subject to pre-configured permission boundaries and monitoring.

**Governance rules**:
- Production systems should default to Tier-1 for untrusted skills and require explicit trust escalation
- Trust tier should be **sticky**: a skill demonstrating reliable behavior at Tier-3 over multiple invocations may be promoted to Tier-4
- A single safety violation should trigger **demotion**
- Tier transitions must be enforced by the runtime, not by skill-provided metadata (prevents privilege escalation)

### Sandboxing and Permission Boundaries

Code skills (P2) require sandboxed execution environments limiting filesystem, network, and system resource access. Three granularity options:
- **Per-skill**: Each skill runs in its own sandbox
- **Per-session**: All skills in a session share a sandbox
- **Per-tier**: Sandboxing varies by trust level

NL skills present a different challenge: the "execution environment" is the context window; the "sandbox" is the instruction-following boundary. Architectural mitigations include separating skill instructions from user data, using structured I/O schemas, and employing output filtering to detect unauthorized actions.

### Skill Supply-Chain Governance (Four Mechanisms)

For marketplace-distributed skills (P7):
1. **Provenance signing**: Cryptographic signing of skill packages to detect tampering
2. **Automated scanning**: Static analysis and behavioral analysis of published skills before distribution
3. **Behavioral anomaly detection**: Runtime monitoring for skills exhibiting unexpected execution patterns
4. **Version pinning**: Locking to verified versions rather than allowing automatic updates

### Case Study: ClawHavoc Campaign

The ClawHavoc campaign provides a documented large-scale supply-chain attack against the OpenClaw/ClawHub skill marketplace.

**Scale of compromise**:
- Nearly 1,200 malicious skills infiltrated ClawHub
- 36.8% of all published skills contained at least one security flaw
- 12 publisher accounts involved; a single account responsible for 677 packages (57% of malicious listings)
- ClawHub's most-downloaded skill ("What Would Elon Do") contained 9 vulnerabilities including 2 critical ones, with ranking artificially inflated through 4,000 faked downloads
- VirusTotal analysis of 3,016+ skills confirmed hundreds exhibited malicious characteristics
- A Snyk audit found 283 of 3,984 skills (7.1%) exposed sensitive credentials in plaintext through LLM context windows and output logs
- 135,000+ exposed OpenClaw instances detected across 82 countries

**What was harvested (primary payload: Atomic macOS Stealer, AMOS)**:
- LLM API keys from `.env` files and OpenClaw configuration → billing fraud and model abuse
- Cryptocurrency wallet keys across 60+ wallet types (Phantom, MetaMask, Exodus) → irreversible asset theft
- Browser-stored passwords, credit card numbers, and autofill data across Chrome, Safari, Firefox, Brave, Edge

**Attack vector analysis through the (C, π, T, R) tuple**:
- **R (interface)**: Name squatting, misleading descriptions, inflated download counts manipulated R to distort discovery
- **π_code (policy, code portion)**: Pattern-2 (code-as-skill) was the execution vector — OpenClaw skills run with the agent's full system permissions
- **π_NL (policy, NL portion)**: Pattern-5 (hybrid NL+code) exploited through documentation-as-attack-surface — skill README files contained the social-engineering payload
- **T (termination)**: Exfiltrate-then-exit-cleanly pattern evades logging; persistent background access through non-terminating policies
- **C (applicability)**: Overbroad applicability predicates activated in unintended contexts

**Why Pattern-3 (workflow enforcement) was less exposed**: Hard-gated execution sequences constrain the agent's action space; a mandated test-before-deploy workflow is harder to bypass through prompt injection alone.

**Why traditional scanners failed**:
- VirusTotal is designed for binary malware signatures — labels syntactically valid NL prompt-injection payloads and harmless-looking shell commands as "Benign"
- VirusTotal cannot audit whether C's activation scope is proportionate to the skill's stated purpose
- Malicious T (early termination to evade logging) does not trigger traditional antivirus heuristics

**Governance response**:
- OpenClaw partnered with VirusTotal for SHA-256 fingerprinting, Code Insight (LLM-based behavioral analysis), and daily re-scans
- This was reactive; proactive governance (pre-publication scanning, behavioral sandboxing) is necessary

### Skill-Native Auditing Tools

**Agent Skills Guard and SkillGuard** implement a three-layer detection architecture mapped to the (C, π, T, R) formalization:

1. **Rule engine / AST analysis** (auditing π_code and R): Pattern rules and Abstract Syntax Tree analysis flag risky constructs (shell execution, eval(), reverse shells, credential access, destructive operations). Runs locally with low overhead; covers broad attack patterns across languages.

2. **LLM semantic analysis** (auditing π_NL and C): LLM reviews NL policy for hidden intent (prompt injection, social-engineering directives, instructions conflicting with stated purpose) and checks whether C's activation scope is appropriate. Catches attacks that rule-based scanning misses.

3. **Reputation scoring** (aggregating across C, π, T, R): Combines signals from layers 1 and 2 into a 0–100 score with threshold bands (above 80 = "safe"; below 30 = "malicious"). In a controlled evaluation of 39 test cases including 4 adversarial samples VirusTotal marked as Benign, no false positives on legitimate skills were found.

**Defense-in-depth conclusion**: Binary scanning (VirusTotal) catches commodity malware targeting π_code. Skill-native auditing catches NL-level attacks on π_NL and C. Runtime behavioral monitoring is needed for attacks on T and context-dependent exploits that manifest only during execution. No single layer suffices.

## Related Pages

- [[agentic-skills]] — formal definition S=(C,π,T,R); the tuple structure maps directly to the attack surfaces above
- [[skill-design-patterns]] — pattern-specific risk matrix; P7 (marketplace) is the highest-severity pattern
- [[skill-lifecycle]] — skill drift exploitation targets the evaluation/update stage; poisoned distillation targets the distillation stage
- [[skills-evaluation]] — deterministic evaluation harnesses as the defense against self-generated skill quality degradation
- [[anthropic-agent-skills]] — Anthropic's trust-tiered design (read-only skill discovery, explicit activation)
- [[model-context-protocol]] — MCP servers as P7 marketplace distribution; subject to the same supply-chain risks
- [[mcp-security-threats]] — related security analysis for MCP as a protocol
- [[hallucination]] — confused deputy attacks exploit the same data/reasoning boundary as hallucination in the observation space

## Contradictions

> **VirusTotal partnership as "not a silver bullet"**: OpenClaw acknowledged this after the ClawHavoc campaign. The tuple-level analysis reveals why: VirusTotal scans π_code but cannot audit π_NL, C, or T. This is a fundamental mismatch between binary malware tooling and the heterogeneous nature of agentic skills. The field needs skill-native auditing infrastructure, not repurposed binary analysis.

> **Pattern-3 governance vs flexibility trade-off**: Workflow enforcement (P3) is the most resilient pattern against supply-chain compromise because hard-gated sequences constrain execution before skills run. However, it is also the most rigid — it may over-constrain the agent for tasks requiring adaptive strategies. The patterns that are most governable (P2, P3) are the least flexible; the most flexible (P4, P6) are the least governable. No pattern offers both simultaneously.

> **Tier-2 isolation claim vs reality**: The four-tier trust model claims Tier-2 (instruction access) provides meaningful isolation from Tier-3 (supervised execution). This is true only with architectural separation between reasoning and action — a constraint that most current LLM agent frameworks do not enforce. In practice, NL instructions loaded into context can indirectly induce tool invocations through the agent's standard decision loop, making Tier-2 and Tier-3 effectively equivalent in many deployments. The trust model is aspirational for most current systems.
