# FieldTwin — Phase 4 Baseline Results

Date: 2026-11-14

## Purpose

Exploratory Earth–Mars terrain comparison for
terrain-informed rover route planning.

## Method

- Mars reference: USGS CTX stereo-derived DTM.
- Earth DEM: NASADEM_HGT.001.
- Primary window: 1000 m square.
- Sensitivity window: 2000 m square.
- Processing grid: 100 m.
- Objectives: minimize absolute differences in
  global slope, relief P95-P05, and plane-detrended
  RMS roughness.
- Method: unweighted Pareto non-dominated sorting.
- Local slope P50/P90 are diagnostic, not ranking inputs.
- No similarity score or suitability threshold assigned.

## Reproducible results

Generated using:

`python -m science.benchmark_baseline`

```text
WINDOW: 1000 m | GRID: 100 m
Front | Site | dSlope_deg | dRelief_m | dRoughness_m
1 | PILOT_A | 0.3466 | 1.2989 | 0.8763
1 | PILOT_B | 0.4169 | 4.2665 | 0.1416
1 | PILOT_C | 0.5306 | 5.2783 | 0.0507
1 | PILOT_D | 0.3002 | 15.3001 | 4.6438
2 | ARADS_PLAYA | 1.1069 | 25.6388 | 10.9648
3 | LASCAR_CONTROL | 15.5691 | 311.4918 | 50.3790

WINDOW: 2000 m | GRID: 100 m
Front | Site | dSlope_deg | dRelief_m | dRoughness_m
1 | PILOT_A | 0.3553 | 13.6412 | 2.5780
1 | PILOT_B | 0.3963 | 8.4537 | 0.3032
1 | PILOT_C | 0.1393 | 26.2381 | 9.7089
1 | PILOT_D | 0.1535 | 24.2295 | 6.7832
2 | ARADS_PLAYA | 1.1698 | 91.9557 | 28.3047
3 | LASCAR_CONTROL | 10.5081 | 511.5400 | 112.3766

No similarity weights or suitability scores.
FIELDTWIN_BASELINE_PARETO_OK
```

## Interpretation

- Four exploratory candidates belong to Front 1
  at both tested window sizes.
- ARADS Playa is Front 2 in this six-site comparison.
- Láscar is Front 3 and behaves as the hypothesized
  contrasting volcanic terrain control.
- Front numbers are relative to these six sites.
- No unique winning analog has been established.

## Scientific limitations and remaining work

- Exploratory candidates were selected using related
  DEM-derived features; evaluation is not independent.
- A verified positive topographic control is still needed.
- The Earth search does not cover all relevant regions.
- Effective spatial resolution and CTX stereo artifacts
  require quantitative treatment.
- NASADEM NUM and SWB quality information has not
  yet been incorporated into candidate eligibility.
- Elevation uncertainty and ranking stability must be
  assessed before claims of reliable similarity.
- DEM similarity alone cannot assess soil traction,
  individual rocks, environmental conditions, or
  overall rover-testing suitability.
- The historical ARADS reference is not automatically
  a positive topographic-similarity control.

## Source documentation

See `data/SOURCES.md` and
`docs/BENCHMARK_PROTOCOL.md`.
