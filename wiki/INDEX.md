# Wiki Index

Knowledge base from ingested papers and handbooks. Last updated: 2026-04-18.

## Sources

| File | Title | Year |
|------|-------|------|
| `0912.1838v1.pdf` | A Brief History of Context | 2009 |
| `2307.06435v10.pdf` | A Comprehensive Overview of Large Language Models | 2023 |
| `2312.10997v5.pdf` | Retrieval-Augmented Generation for Large Language Models: A Survey | 2023 |
| `2503.23278v3.pdf` | Model Context Protocol: Landscape, Security Threats, and Future Research Directions | 2025 |
| `2510.18212v3.pdf` | A Definition of AGI | 2025 |
| `VikingMalt_BeerMaltHandbook_Online-1.pdf` | Viking Malt Beer & Malt Handbook | 2024 |

---

## Pages

### Context & Foundations (`wiki/ai/`)
- [[context]] — Formal context theory (Wan 2009): typed dimension-value pairs, Lucx language, McCarthy's ist-predicate

### Large Language Models (`wiki/ai/`)
- [[large-language-models]] — LLM overview: architecture families, capabilities, limitations
- [[transformer-architecture]] — Attention mechanisms (MHA/GQA/MLA), architecture variants, positional encodings
- [[pretraining-and-finetuning]] — Training pipeline: objectives, instruction tuning, PEFT
- [[rlhf-and-alignment]] — RLHF, reward modelling, PPO, Constitutional AI
- [[in-context-learning]] — Zero/few-shot prompting, CoT, ToT, ICL mechanics
- [[scaling-laws]] — Chinchilla laws, compute-optimal training, data wall
- [[emergent-abilities]] — Phase-transition capabilities at scale

### Retrieval-Augmented Generation (`wiki/ai/`)
- [[retrieval-augmented-generation]] — RAG overview: retrieve-augment-generate pipeline
- [[rag-paradigms]] — Naive / Advanced / Modular RAG paradigms
- [[vector-databases-and-embeddings]] — Embedding models, vector stores, ANN search

### Reliability & Limitations (`wiki/ai/`)
- [[hallucination]] — Types, causes, detection, mitigation

### Model Context Protocol (`wiki/ai/`)
- [[model-context-protocol]] — MCP architecture: Host/Client/Server, tool primitives
- [[mcp-security-threats]] — 16 threat scenarios across 4 attacker types and 4 lifecycle phases

### AGI & Cognitive Capabilities (`wiki/ai/`)
- [[agi-definition]] — CHC-based AGI definition; GPT-4=27%, GPT-5=57%
- [[cognitive-capabilities-framework]] — 10 CHC domains with AI benchmarks and scores
- [[long-term-memory-in-ai]] — MS=0% bottleneck; why LLMs lack genuine LTM
- [[capability-contortions]] — Engineering workarounds masking architectural deficits

---

### Beer & Brewing — Core Concepts (`wiki/beer/`)

- [[beer-types]] — Classification of beer styles: top/bottom fermented, all major styles
- [[fermentation-types]] — Top vs bottom fermentation: yeast biology, flavour consequences, schedules
- [[beer-brewing-process]] — Full brewing process: mashing, lautering, boiling, fermentation, conditioning, filtration
- [[malt-production]] — Malting process: steeping, germination, kilning, roasting, caramel malt production
- [[malt-types]] — Base malts, caramel malts, dark/roasted malts, wheat malts, specialty malts
- [[malt-characteristics]] — Analytical parameters: extract yield, EBC colour, diastatic power, protein, FAN, pH, viscosity
- [[malt-extracts]] — Maltax extract range; extract brewing recipes; gluten-free and alcohol-free applications

### Beer & Brewing — Ingredients (`wiki/beer/`)

- [[hops]] — Alpha acids, bitterness (IBU/BU), isomerisation, Viking varieties, dry hopping
- [[water-chemistry]] — Mineral ions, sulphate:chloride ratio, mash pH, historical style geography
- [[yeast-and-fermentation-chemistry]] — Esters, phenols, diacetyl, attenuation, strain selection, Viking yeast strains

### Beer & Brewing — Malt Types (`wiki/beer/`)

- [[pale-malt]] — Base pale malts: Pilsner, Golden Ale, and pale malt variants overview
- [[pale-ale-malt]] — Pale ale–specific base malt with biscuity character
- [[munich-malt]] — Rich amber base malt defining Märzen and Bock
- [[vienna-malt]] — Intermediate amber base malt defining Vienna Lager
- [[wheat-malt]] — Malted wheat: haze, foam, Hefeweizen, NEIPA
- [[caramel-malt]] — Crystal/caramel malts: non-fermentable sweetness, colour, body
- [[chocolate-malt]] — Roasted malt at ~800 EBC: chocolate and coffee flavours
- [[dark-malts]] — Dark malt overview: the full roasted/kilned specialty spectrum
- [[roasted-malts]] — Roasted barley and black malt: extreme colour and dry bitterness
- [[black-malt]] — Black patent malt: maximum colour, harsh roast

### Beer & Brewing — Recipe & Flavour (`wiki/beer/`)

- [[beer-recipe-design]] — Grain bill design, OG/FG/ABV calculations, mash programming, hop schedules
- [[malt-flavor-chemistry]] — Maillard reaction, caramelisation, kilning temperature vs flavour spectrum

### Beer & Brewing — Beer Styles (`wiki/beer/`)

- [[pilsner]] — Bohemian and German Pilsner
- [[lager]] — Lager styles overview
- [[marzen]] — Märzen / Oktoberfest amber lager
- [[oktoberfest]] — Oktoberfest history, Märzen vs modern pale Oktoberfest
- [[bock]] — Bock, Doppelbock, Maibock
- [[dark-lager]] — Dunkel, Schwarzbier, dark bottom-fermented styles
- [[ale]] — Ale styles: Pale Ale, IPA, Bitter, Barleywine
- [[stout]] — Dry Stout, Sweet Stout, Imperial Stout
- [[porter]] — Porter history and substyles
- [[wheat-beer]] — Wheat beer styles overview
- [[hefeweizen]] — Hefeweizen in detail: yeast chemistry, POF+ gene, banana/clove balance

### Redirect Stubs (`wiki/beer/`)
- [[beer-yeast]] → [[yeast-and-fermentation-chemistry]]
- [[top-fermented-beers]] → [[fermentation-types]]
- [[bottom-fermented-beers]] → [[fermentation-types]]

---

## Broken Links Log

See `BROKENLINK.md` for links that appeared in pages but could not be resolved to existing content.

---

## Key Cross-Paper Themes

### The Memory Gap
[[long-term-memory-in-ai]] is rated 0% (MS=0) for frontier models. [[retrieval-augmented-generation]] and context windows are [[capability-contortions]] that mask but don't solve this.

### Context — Formal vs Informal
[[context]] (Paper 1) defines context mathematically as typed dimension-value pairs. All other papers use "context" informally. [[model-context-protocol]] uses context as structured primitives; [[in-context-learning]] uses context as a token window.

### RAG: Infrastructure vs Workaround
[[retrieval-augmented-generation]] is simultaneously: essential production infrastructure (Paper 3) and a capability contortion masking the absence of genuine memory (Paper 5).

### MCP Extends RAG
[[model-context-protocol]] subsumes RAG's retrieval function while adding active tool execution, write operations, and state management. RAG is a subset of what MCP enables.

### Scaling and AGI
[[scaling-laws]] predict smooth loss improvement. [[emergent-abilities]] suggest discontinuous jumps. The [[agi-definition]] shows MS=0% even after GPT-4→GPT-5 scaling — suggesting architectural innovation, not just scaling, is needed for AGI.
