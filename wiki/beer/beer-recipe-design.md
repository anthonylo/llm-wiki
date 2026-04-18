---
title: Beer Recipe Design
tags: [recipe, grain-bill, OG, FG, ABV, IBU, EBC, brewing-calculations]
source: "VikingMalt_BeerMaltHandbook_Online-1.pdf — Viking Malt Beer & Malt Handbook"
---

## Summary

Beer recipe design is the process of selecting and quantifying ingredients — malt, hops, yeast, and water — to hit target specifications: gravity (OG/FG), alcohol content (ABV), colour (EBC), and bitterness (BU/IBU). The Viking Malt handbook provides a library of worked recipes demonstrating how different malt combinations, hop additions, fermentation schedules, and yeast choices produce radically different beers from the same fundamental process.

## Explanation

### Key Parameters

Every beer recipe specifies these target values:

| Parameter | Definition | Calculation |
|-----------|------------|-------------|
| **OG** (Original Gravity) | Wort density before fermentation; indicates total dissolved sugars | Measured with hydrometer or refractometer |
| **FG** (Final Gravity) | Wort density after fermentation; residual unfermented sugars | Measured post-fermentation |
| **ABV** (Alcohol by Volume) | Alcoholic strength | `ABV ≈ (OG − FG) × 131` (simplified formula) |
| **Attenuation** | % of sugars fermented | `(OG − FG) / (OG − 1.000) × 100` |
| **Colour (EBC)** | European Brewing Convention units | `Σ(kg_malt × EBC_malt) / volume_litres` |
| **Bitterness (BU/IBU)** | Iso-alpha acids in mg/L | Depends on hop AA%, weight, boil time, volume |

### Gravity Scales

OG and FG can be expressed in two scales:
- **Specific Gravity (SG)**: water = 1.000; typical OG 1.040–1.080
- **Degrees Plato (°P)**: dissolved solids as % by weight; typical OG 10–20°P
- Approximate conversion: `SG = 1 + (°P / 250)`

### The Grain Bill (Grist)

The grain bill is the recipe's malt composition expressed as percentages of total grain weight. Design principles:

**1. Establish the base malt (typically 60–90%)**
- Sets fermentable extract, diastatic power, and base flavour
- Pilsner Malt → lightest colour, neutral flavour
- Pale Ale Malt → slightly more malt character
- Vienna/Munich → amber colour, malt-forward

**2. Add specialty malts for colour, flavour, body (up to 30–40%)**
- Caramel malts: colour, sweetness, body
- Dark/roasted malts: colour, bitterness, roasted flavour
- Dextrin/CaraBody: body and head retention without colour
- Wheat/Oat: head foam, haze, mouthfeel

**3. Check diastatic power**
- Total mash must average >100–150 WK
- Pure base malt (350 WK): can support up to ~50% zero-diastatic specialty malts

### Example Grain Bills from Viking Recipes

**Viking Premium Lager** (clean, golden)
- 66% Viking Pilsner Malt
- 17% Viking Dextrin Malt (body)
- 12% Viking Golden Ale Malt
- 5% Viking Cookie Malt
→ OG/FG: 10.7°P / 2.4°P → ABV ~4.4%

**4Malt Ale** (red, malty)
- Viking Ale Malt family (base)
- Viking Caramel Malt 50 (colour + sweetness)
- Multiple specialty malts
→ Pressurised with 70% N₂ / 30% CO₂ (nitrogenated, creamy mouthfeel)

**Viking Active Stout** (dark, easy-drinking)
- 60.6% Viking Red Active Malt
- 30.3% Viking Pilsner Zero Malt
- Remaining: roasted products
→ OG/FG: 9.8°P / 2.2°P → ABV ~3.9%

**Malt Mandala (Russian Imperial Stout)** (extreme)
- Multiple dark malts + caramel malts
- Oats
→ ABV: "dominant, black as a moonless night"

### Mash Design

Once the grain bill is set, the mash programme is designed:

| Variable | Typical Value | Effect |
|----------|---------------|--------|
| **Malt:Water ratio** | 1:3 to 1:5 (kg:L) | Thicker = more enzyme activity, less fermentable |
| **Strike water temp** | OG temp + ~3°C (heat loss) | Hits target mash temp |
| **Beta-amylase rest** | 62–65°C | Fermentable maltose production (drier beer) |
| **Alpha-amylase rest** | 68–72°C | Dextrin production (fuller body) |
| **Mash-out** | 78°C | Denatures enzymes, sets fermentability |
| **pH** | 5.2–5.4 | Optimal enzyme activity |

**Viking Low Lager** uses malt:water ratio of 1:7.5 — unusually thin, designed for the specific yeast and low-gravity target.

### Hop Schedule Design

Three decisions:
1. **Total bitterness target (IBU/BU)** — style-dependent (see [[hops]])
2. **Bittering additions** — typically high-alpha hop added at 60 min
3. **Aroma additions** — added late boil, whirlpool, or dry hop

**Viking handbook examples**:
- Dark Red Lager: Saaz bitter at start; Saaz aroma at end (classic Pilsner-style dual addition)
- Alcohol-Free Lager: Magnum (13% AA) at start; Cascade aroma → maximum efficiency from low-gravity wort

### Fermentation Schedule Design

Key decisions:
1. **Yeast strain** — defines ester/phenol profile (see [[yeast-and-fermentation-chemistry]])
2. **Pitch temperature** — ale (18–22°C), lager (9–12°C)
3. **Fermentation duration** — determined by FG stability
4. **Diacetyl rest** — raise temp ~2–3°C near end before crash
5. **Cold crash / conditioning** — temperature and duration

### ABV Calculation (Examples from Viking Recipes)

| Beer | OG | FG | ABV calc |
|------|----|----|----------|
| Viking Active Stout | 9.8°P | 2.2°P | (9.8-2.2)×0.131/10 ≈ ~3.9% |
| Viking CaraBody Pils | 11.2°P | 2.1°P | ~4.5% |
| Viking Premium Lager | 10.7°P | 2.4°P | ~4.3% |
| Alcohol-Free Lager | Very low OG | — | 0.03% |

*Note: °Plato requires adjusted formula: `ABV ≈ (OG_P − FG_P) × 0.131 / 10` ×10 factor corrects for Plato scale.*

### Scaling a Recipe

All ingredient quantities scale linearly with batch volume:
- Double the batch → double all grain and hop quantities
- Adjust water volumes proportionally
- Yeast pitch rate scales with volume × gravity (cells/mL/°P)

### Filtration Decisions

- **Filtered, clear**: sheet filtration to 0.5 μm (standard Viking extract recipes use BECO SD 30)
- **Unfiltered, hazy**: deliberate — NEIPA, Hefeweizen, Viking APA
- Filtration removes yeast, reducing refermentation potential; important for packaged shelf stability

## Related Pages

- [[malt-types]] — the ingredient options for the grain bill
- [[malt-characteristics]] — extract yield, EBC, and diastatic power guide grain bill calculations
- [[hops]] — hop schedule design and bitterness calculations
- [[yeast-and-fermentation-chemistry]] — yeast selection and fermentation profile
- [[beer-brewing-process]] — the process executing the recipe
- [[fermentation-types]] — ale vs lager determines fermentation schedule
- [[malt-extracts]] — recipes using extract instead of grain bill + mashing
- [[water-chemistry]] — water mineral profile is an implicit recipe ingredient

## Contradictions

> **°Plato vs Specific Gravity**: Viking recipes uniformly use Degrees Plato (OG/FG in °P). Homebrewing and much Anglo-American craft brewing literature uses Specific Gravity (1.040, 1.010, etc.). Both measure the same thing (wort density / dissolved sugars) but the numeric scales differ. Converting without adjustment gives incorrect ABV calculations.

> **Recipe as art vs science**: The handbook presents recipes as inspiration ("a brewer can create variety by varying recipes, mashing programmes, types of yeast and fermentation conditions"), not rigid specifications. The same grain bill can produce different beers depending on mash temperature, water chemistry, yeast strain, and fermentation temperature. Recipe design sets boundaries; execution determines the result.
