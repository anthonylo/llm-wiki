# Changelog

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
