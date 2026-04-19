# Changelog

## 2026-04-19 — MapReduce: Original OSDI 2004 Paper

### Added (Sources)
- `processed/data/mapreduce-osdi04.pdf` — MapReduce: Simplified Data Processing on Large Clusters (Dean & Ghemawat, Google, OSDI 2004)

### Added (Pages)
- `wiki/data/mapreduce.md` — Programming model: map/reduce functions, key/value types, canonical examples (word count, grep, sort, inverted index), Google production scale (29,423 jobs, 3,288 TB input in Aug 2004), large-scale indexing rewrite
- `wiki/data/mapreduce-execution.md` — 7-step execution flow, master data structures, M×R task granularity, partitioning function, ordering guarantees, cluster environment, performance benchmarks (grep 150s, sort 891s vs TeraSort record 1,057s)
- `wiki/data/mapreduce-fault-tolerance.md` — Worker/master failure detection and re-execution, completed map vs reduce task asymmetry, atomic commits via temp file rename, non-deterministic semantics, bad-record skipping via signal handler + UDP, counter facility
- `wiki/data/mapreduce-optimizations.md` — Data locality scheduling (GFS replica awareness), backup tasks (−44% sort time when disabled), combiner function (partial pre-aggregation on map workers), custom partitioning functions

### Updated
- `wiki/INDEX.md` — Added MapReduce source entry, Source→Pages Map row, MapReduce section under Pages

## 2026-04-18 — Apache Spark: Original Paper + Data Engineer's Guide

### Added (Sources)
- `processed/data/Spark-Cluster-Computing-with-Working-Sets.pdf` — Spark: Cluster Computing with Working Sets (Zaharia et al., 2010, UC Berkeley)
- `processed/data/The-Data-Engineers-Guide-to-Apache-Spark.pdf` — The Data Engineer's Guide to Apache Spark (Databricks, 2017)

### Added (Pages)
- `wiki/data/apache-spark.md` — Spark overview: MapReduce limitations, architecture (driver/executor/cluster manager), RDDs, shared variables, performance results (10× Hadoop on iterative ML, sub-second interactive queries)
- `wiki/data/resilient-distributed-datasets.md` — RDD formal properties (getPartitions/getIterator/getPreferredLocations), lineage-based fault tolerance vs checkpointing, caching semantics, broadcast variables (+2.8× for ALS), accumulators, Scala closure serialization implementation
- `wiki/data/spark-structured-apis.md` — Structured API hierarchy, DataFrames vs RDDs, transformations (narrow/wide/shuffle), lazy evaluation + DAG execution, predicate pushdown, Catalyst optimizer, SparkSession, Structured Streaming

### Updated
- `wiki/INDEX.md` — Added Spark section, source entries, Source→Pages Map rows

## 2026-04-18 — Agentic Skills: SoK Paper + Anthropic Engineering Blog

### Added (Sources)
- `processed/ai/2602.20867v1.pdf` — SoK: Agentic Skills — Beyond Tool Use in LLM Agents (Jiang et al., 2025)
- `processed/ai/www-anthropic-com-...agent-ski.pdf` — Equipping agents for the real world with Agent Skills (Anthropic Engineering, 2025)

### Added (Pages)
- `wiki/ai/agentic-skills.md` — Formal definition S=(C,π,T,R), skills vs tools/plans/memory/prompt templates, skills as procedural memory, SkillsBench compute equalizer evidence
- `wiki/ai/skill-lifecycle.md` — 7-stage lifecycle model (discovery, practice/refinement, distillation, storage, retrieval/composition, execution, evaluation/update), feedback loops, representative systems per stage
- `wiki/ai/skill-design-patterns.md` — 7 design patterns (P1 metadata-driven through P7 marketplace), representation×scope taxonomy, pattern trade-off table, ClaudeCode as P1+P3+P5+P7 exemplar
- `wiki/ai/skill-security-governance.md` — 6 threat categories, 4-tier trust model, sandboxing, skill supply-chain governance, ClawHavoc case study (1,200 malicious skills, 36.8% infection rate, AMOS credential stealer), skill-native auditing vs VirusTotal
- `wiki/ai/skills-evaluation.md` — 5 evaluation dimensions, deterministic harnesses, SkillsBench results (+16.2pp curated, −1.3pp self-generated), domain variance, skills as compute equalizers, negative-delta tasks
- `wiki/ai/anthropic-agent-skills.md` — SKILL.md format, 3-level progressive disclosure, code execution, development best practices, security guidance, MCP relationship, open standard (Dec 2025)

### Updated
- `wiki/INDEX.md` — Added Agentic Skills section, source entries, Source→Pages Map rows, three new cross-paper themes

## 2026-04-18 — Foundational AI Papers: Attention, BERT, GPT-3, Foundation Models, InstructGPT

### Added (Sources)
- `processed/1706.03762v7.pdf` — Attention Is All You Need (Vaswani et al., 2017)
- `processed/1810.04805v2.pdf` — BERT: Pre-training of Deep Bidirectional Transformers (Devlin et al., 2018)
- `processed/2005.14165v4.pdf` — Language Models are Few-Shot Learners / GPT-3 (Brown et al., 2020)
- `processed/2108.07258v3.pdf` — On the Opportunities and Risks of Foundation Models (Bommasani et al., 2021)
- `processed/2203.02155v1.pdf` — Training language models to follow instructions / InstructGPT (Ouyang et al., 2022)

### Added (Wiki Pages)
- `ai/attention-mechanism.md` — Scaled dot-product attention formula, multi-head attention (h=8), sinusoidal positional encoding, encoder-decoder architecture, training results (28.4 BLEU EN-DE)
- `ai/bert.md` — Bidirectional Transformer encoder, BERT_BASE (110M) / BERT_LARGE (340M), MLM+NSP pre-training, GLUE 80.5%, fine-tuning paradigm
- `ai/masked-language-modeling.md` — MLM objective detail: 80/10/10 masking strategy, pre-training/fine-tuning mismatch, CLM comparison, SpanBERT/ELECTRA variants
- `ai/gpt-3.md` — 175B autoregressive LM, training data (499B tokens), zero/one/few-shot paradigms, benchmark results, data contamination discussion
- `ai/foundation-models.md` — Definition of foundation models, emergence and homogenization properties, domain applications, systemic risk analysis
- `ai/instructgpt.md` — SFT→RM→PPO pipeline with exact dataset sizes, 1.3B > 175B GPT-3 on human preference, alignment tax, PPO-ptx fix, hallucination reduction

### Updated
- `INDEX.md` — Added 5 new source papers; added "Foundational AI Papers" section with 6 new pages; added cross-paper themes for architecture evolution, scale vs alignment, and foundation model risks

---

## 2026-04-18 — Wiki Maintenance Pass: Link Audit, New Pages, and BROKENLINK Log

### Added
- `beer/pale-malt.md` — Base pale malt overview: Pilsner, Golden Ale, pale malt variants
- `beer/pale-ale-malt.md` — Pale ale–specific base malt with biscuity character
- `beer/munich-malt.md` — Rich amber base malt defining Märzen and Bock
- `beer/vienna-malt.md` — Intermediate amber base malt; historical context (Anton Dreher)
- `beer/wheat-malt.md` — Malted wheat: haze, foam, protein, Hefeweizen and NEIPA applications
- `beer/caramel-malt.md` — Crystal/caramel malts: stewing process, EBC range, non-fermentable sweetness
- `beer/chocolate-malt.md` — ~800 EBC roasted malt: chocolate, coffee, bittersweet flavours
- `beer/dark-malts.md` — Dark malt overview: kilned vs roasted, husk tannin issue, usage guidelines
- `beer/roasted-malts.md` — Roasted barley and black malt: extreme colour, dry bitterness
- `beer/black-malt.md` — Black patent malt: maximum colour, harsh roast, usage as colour agent
- `beer/hefeweizen.md` — Hefeweizen in detail: POF+ yeast, banana/clove balance, ferulic acid rest
- `beer/oktoberfest.md` — Oktoberfest history, Märzen vs modern pale Oktoberfest distinction
- `beer/beer-yeast.md` — Redirect stub → [[yeast-and-fermentation-chemistry]]
- `beer/top-fermented-beers.md` — Redirect stub → [[fermentation-types]]
- `beer/bottom-fermented-beers.md` — Redirect stub → [[fermentation-types]]
- `BROKENLINK.md` — Log of 9 links that cannot be resolved from current source material

### Fixed
- `hallucination.md` — Corrected escaped-pipe `\|` in markdown table wikilinks
- `model-context-protocol.md` — Corrected escaped-pipe `\|` in MCP vs RAG table wikilink
- `beer-types.md` — Added "Style Deep-Dives" section to Related Pages, linking all 11 orphaned style pages

### Updated
- `INDEX.md` — Full refresh: all 50+ pages listed across AI and beer domains; added Broken Links Log reference

---

## 2026-04-18 — Initial Knowledge Base from 5 arXiv Papers

### Added
- `context.md` — Formal context theory from Wan (2009), 0912.1838v1
- `large-language-models.md` — LLM overview from Naveed et al. (2023), 2307.06435v10
- `transformer-architecture.md` — Transformer internals from 2307.06435v10
- `pretraining-and-finetuning.md` — Training pipeline from 2307.06435v10
- `rlhf-and-alignment.md` — RLHF and alignment from 2307.06435v10
- `in-context-learning.md` — ICL and prompting from 2307.06435v10
- `scaling-laws.md` — Chinchilla scaling laws from 2307.06435v10
- `emergent-abilities.md` — Emergent capabilities from 2307.06435v10
- `retrieval-augmented-generation.md` — RAG overview from Gao et al. (2023), 2312.10997v5
- `rag-paradigms.md` — Naive/Advanced/Modular RAG from 2312.10997v5
- `vector-databases-and-embeddings.md` — Vector store infrastructure from 2312.10997v5
- `hallucination.md` — Hallucination types, causes, mitigations (cross-paper)
- `model-context-protocol.md` — MCP architecture from Hou et al. (2025), 2503.23278v3
- `mcp-security-threats.md` — 16 MCP threat scenarios from 2503.23278v3
- `agi-definition.md` — CHC-based AGI definition from Hendrycks et al. (2025), 2510.18212v3
- `cognitive-capabilities-framework.md` — 10 CHC cognitive domains from 2510.18212v3
- `long-term-memory-in-ai.md` — LTM bottleneck analysis (cross-paper)
- `capability-contortions.md` — Engineering workarounds from 2510.18212v3
- `INDEX.md` — Master wiki index

## 2026-04-18 — Beer & Malt Knowledge Base (Viking Malt Handbook)

### Added
- `beer-types.md` — Classification of beer styles (top/bottom fermented, all major styles)
- `fermentation-types.md` — Top vs bottom fermentation, yeast biology, flavour consequences, schedules
- `malt-production.md` — Malting process: steeping, germination, kilning, roasting, caramel and dark malt production
- `malt-types.md` — Base malts, caramel malts, dark/roasted malts, wheat malts, specialty malts with style pairings
- `malt-characteristics.md` — Analytical parameters: extract yield, EBC colour, diastatic power, protein, FAN, pH, viscosity
- `beer-brewing-process.md` — Full brewing process: mashing temperatures/rests, lautering, boiling, fermentation, conditioning, filtration
- `malt-extracts.md` — Maltax extract range; extract brewing recipes; gluten-free and alcohol-free applications

## 2026-04-18 — Beer & Malt Detailed Topics (wiki/beer/)

### Added
- `beer/hops.md` — Hop chemistry, alpha acids, bitterness (IBU/BU), Viking hop varieties, dry hopping
- `beer/water-chemistry.md` — Mineral ions, sulphate:chloride ratio, mash pH, historical style geography
- `beer/yeast-and-fermentation-chemistry.md` — Esters, phenols, diacetyl, fusel alcohols, attenuation, Viking yeast strains
- `beer/beer-recipe-design.md` — Grain bill design, OG/FG/ABV calculations, mash programming, hop schedules
- `beer/malt-flavor-chemistry.md` — Maillard reaction, caramelisation, kilning temperature vs flavour spectrum

### Also corrected
- `mcp-security-threats.md` — Fixed lifecycle phase assignments: Rug Pull and Cross-Server Shadowing are Creation-phase threats (not Deployment/Operation); updated phase mapping diagram
