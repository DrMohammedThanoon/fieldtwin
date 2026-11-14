# FieldTwin — Terrain Benchmark Protocol

Status: Pilot-informed prospective evaluation plan.
Date: 2026-11-14.

## Mission
Evaluate Earth terrain for Mars rover terrain-informed
route planning and traversability algorithm testing.

## Mars target
USGS CTX stereo DTM currently used in the Phase 4 pilot.
Target selection remains provisional.

## Primary analysis
- Window: 1000 m square
- Processing grid: 100 m
- Coverage threshold: at least 95%
- Features: global slope, relief P95-P05,
  plane-detrended RMS roughness,
  local slope P50 and P90
- No finalized feature weights or similarity thresholds

## Sensitivity analysis
- Additional windows: 600 m and 2000 m
- Secondary processing grid: 200 m
- Report local-stencil sample counts
- Do not assume grid posting equals effective resolution
- Evaluate CTX artifact and elevation uncertainty

## Exploratory candidate
- Latitude: -24.4
- Longitude: -69.9
- Selected from a previously examined 81-point pilot
- NOT an independently validated candidate

## Historical field-test reference
- NASA ARADS Playa, Chile
- Latitude: -24.101642
- Longitude: -70.138175
- Reference: https://pmc.ncbi.nlm.nih.gov/articles/PMC10750310/
- Historical rover-testing reference, NOT a guaranteed
  positive topographic-similarity control
- Earlier analyses used approximate coordinates

## Proposed independent negative control
- Lascar volcano, Chile
- Latitude: -23.37
- Longitude: -67.73
- Smithsonian GVP volcano number: 355100
- Reference: https://volcano.si.edu/volcano.cfm?vn=355100
- Selected independently based on volcanic landform
  and contrasting summit terrain
- Expected to differ from the selected smooth Mars target
- This expectation has NOT been tested against its DEM
- Preserve and report results even if expectation fails

## Required evaluation safeguards
- Keep exploratory and confirmatory results separate
- Compare identical physical windows and grid spacings
- Do not tune weights to force a desired site ordering
- Do not use ARADS as the terrain-positive control
- Report all measured features and scale sensitivity
- Quantify uncertainty before claiming reliable ranking
- Separate topography from soil, traction, rock hazards,
  atmosphere, and other rover-transfer limitations
- Do not claim rover readiness from DEM similarity alone
