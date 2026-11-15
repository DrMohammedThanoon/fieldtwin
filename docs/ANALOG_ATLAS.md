# Analog Atlas — context view

**Status:** context only. Literature-coded, not validated, not a FieldTwin search result.

## Purpose
Gives judges geographic and geological context for Mars reference sites and Earth analog sites reported in the literature. FieldTwin's measured search remains the bounded Atacama study (`data/SEARCH_SCOPE.md`); the Atlas never feeds the Comparison or Transfer views or `outputs/validated/`.

## Method
`science/analog_atlas.py` loads `data/context/analog_atlas/`, re-requests NASA POWER climatology for the 16 Earth sites, verifies against `power.csv` (tolerance 0.05), recomputes the four climate criteria and writes `app/src/data/analog_atlas.json`. Earth ↔ Mars only (24 Mars sites). No ranking is stored.

## Criteria (13, each 0–1)
| Kind | Criteria |
|---|---|
| Measured (NASA POWER) | aridity, dry air, cold, temperature extremes |
| Literature-coded | basalt, impact, caves, ice, salts, ancient water, wind erosion, biosignature value, bare surface |

Formulas (P in mm/yr = PRECTOTCORR_ANN × 365.25):
- arid = 1 − min(log10(P+1)/log10(1001), 1)
- dry_air = 1 − RH2M_ANN/100
- cold = clamp((25 − T2M_ANN)/60, 0, 1)
- swing = clamp((T2M_MAX_ANN − T2M_MIN_ANN)/80, 0, 1)
- Mars climate criteria are fixed at 1.0 for all Mars sites.

## Context index
Computed in the browser: weighted mean of (1 − |earth − mars|) over 13 criteria; weight ×2 where the Mars value ≥ 0.8; user weights 0–3 multiply on top. It is shown as "Context index (0–1, literature-coded)" with a per-criterion breakdown.

It is **not a similarity percentage**: the nine coded values are subjective literature codings, Mars climate is fixed rather than measured, the ×2 rule is a heuristic, and nothing validates the result against terrain or rover performance (DESIGN.md §6, §8).

## Limitations
- Only 4/13 criteria measured; NASA POWER cells are ~0.5°, coarser than any site.
- Earth cannot reproduce Mars gravity (0.38 g), thin CO₂ atmosphere or radiation.
- Slope, ruggedness and relief are not measured for atlas sites (see the Comparison view for measured Atacama values).
- Mars coordinates are planetocentric, east-positive, and are shown only on the Mars image.
- Per-value provenance of the coded traits is not recorded; they inherit the site-level source links.

## Editorial overrides
One handoff sentence was reworded in `science/analog_atlas.py` (`TEXT_OVERRIDES`): Dry Valleys "the closest climate match to Mars" → "a commonly cited Mars climate analog", because the superlative has no recorded evidence and the UI must not use similarity-style claims.
