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

## CTX Visual Quality Review

Status: PROVISIONAL — 2026-11-14

- Source: USGS MRO CTX stereo-derived DEM.
- Reviewed the full hillshade and central 2 km DEM,
  detrended elevation residual, and hillshade.
- Central valid raster coverage: 99.99%.
- Central detrended elevation RMS: 3.218 m.
- No obvious major discontinuity in the selected window.
- Directional fine-scale texture is visible.
- A localized bright feature / possible isolated gap
  appears near the upper-right portion of the window.
- Fine-scale textures may be actual terrain,
  stereo-processing artifacts, or both.
- Residual RMS is NOT an elevation-accuracy estimate.
- CTX-to-MOLA alignment is not independent validation.
- Corresponding orthorectified imagery has not yet
  been independently inspected.

Decision:
- Retain the CTX window for exploratory development.
- Do not claim final analog suitability from this DEM.
- Treat fine-scale slopes and roughness cautiously.
- Require uncertainty assessment and independent imagery
  review before final scientific acceptance.

Reference:
https://stac.astrogeology.usgs.gov/docs/data/mars/ctxdtms/

## Elevation Perturbation Sensitivity

Status: EXPLORATORY — 2026-11-14

### Experimental setup
- Mars reference: USGS CTX DEM.
- Analysis window: 1000 m square.
- Processing grid: 100 m.
- Trials: 100 per scenario.
- Random seed: 20261114.
- Simulated independent Gaussian Mars elevation errors.
- Perturbation standard deviations: 1 m, 3 m, 5 m.
- Earth terrain features held fixed.
- These perturbations are not calibrated CTX errors.

### Pareto Front 1 membership

| Site | 1 m | 3 m | 5 m |
|---|---:|---:|---:|
| Pilot A | 100/100 | 100/100 | 30/100 |
| Pilot B | 100/100 | 100/100 | 60/100 |
| Pilot C | 21/100 | 27/100 | 72/100 |
| Pilot D | 100/100 | 100/100 | 100/100 |
| ARADS Playa | 0/100 | 0/100 | 0/100 |
| Láscar control | 0/100 | 0/100 | 0/100 |

Identical full Pareto ordering:
- 1 m: 21/100
- 3 m: 27/100
- 5 m: 30/100

### Interpretation
- Candidate membership is sensitive to perturbations.
- Pilot D retained Front 1 membership in every trial.
- ARADS and Láscar never reached Front 1.
- Front 1 membership is not a suitability score.
- Perturbation frequencies are not calibrated
  probabilities of analog suitability.
- Full-front stability is not monotonic with
  perturbation size in this finite experiment.
- Actual DEM uncertainty remains unquantified.

### Scientific restrictions
- No validated analog winner.
- No confidence scores derived from these frequencies.
- Do not infer centimeter-level accuracy from
  small terrain-feature differences.
- Real stereo errors may be spatially correlated.
- Earth DEM uncertainty was not simulated.
- Robustness under alternative error models remains open.

### Next stage
Develop the Analog Transfer Matrix to distinguish:
1. Supported DEM-based terrain characteristics.
2. Features requiring additional observations.
3. Environmental and engineering properties that
   cannot be transferred from DEM similarity alone.

Reference:
https://stac.astrogeology.usgs.gov/docs/data/mars/ctxdtms/

## DEM-Scale Multi-Route Benchmark

Status: Exploratory experiment — 2026-11-14.

### Experimental design

- Four terrain locations: Mars CTX, FieldTwin Pilot B,
  ARADS Playa, and Láscar volcano.
- Analysis window: 1000 m square.
- Processing grid: 100 m.
- Five predefined start–destination pairs per location.
- Routing: eight-connected Dijkstra shortest path.
- Baseline: distance-only shortest path.
- Experimental slope limits: 3° and 10°.
- Total searches: 20 unconstrained and 40 constrained.

### Reproducible results

Command: `python -m science.multi_route_benchmark`

```text
FIELDTWIN REPRODUCIBLE MULTI-ROUTE BENCHMARK
Window: 1000 m | Grid: 100 m
Detour averages include feasible routes only.

MARS
  Limit 3 deg | feasible=5/5 | infeasible=0/5 | longer=1 | feasible_mean_detour=2.37%
  Limit 10 deg | feasible=5/5 | infeasible=0/5 | longer=0 | feasible_mean_detour=0.00%

PILOT_B
  Limit 3 deg | feasible=5/5 | infeasible=0/5 | longer=3 | feasible_mean_detour=5.92%
  Limit 10 deg | feasible=5/5 | infeasible=0/5 | longer=0 | feasible_mean_detour=0.00%

ARADS
  Limit 3 deg | feasible=3/5 | infeasible=2/5 | longer=3 | feasible_mean_detour=30.07%
  Limit 10 deg | feasible=5/5 | infeasible=0/5 | longer=2 | feasible_mean_detour=8.08%

LASCAR
  Limit 3 deg | feasible=0/5 | infeasible=5/5 | longer=0
  Limit 10 deg | feasible=0/5 | infeasible=5/5 | longer=0

Route searches: 60
FIELDTWIN_MULTI_ROUTE_BENCHMARK_OK
```

### Scientific interpretation

- Mars and Pilot B: all five routes were feasible
  under both experimental slope limits.
- ARADS: three of five routes were feasible at 3°,
  increasing to five of five at 10°.
- Láscar: no constrained routes were feasible
  under either tested slope limit.
- Constrained routes can require additional distance
  to satisfy the selected grade limit.
- Reported mean detours include feasible routes only.
- Infeasible routes must be reported separately.
- These results demonstrate software behavior,
  not validated physical rover performance.

### Limitations

- Only five predefined route pairs were evaluated.
- Slope limits are hypothetical, not certified.
- Eight-connected center-to-center routing is simplified.
- Grid-edge slope cannot establish clearance or safety
  across the physical area between cell centers.
- No soil, slip, traction, rock or sensor data included.
- Uncertainty in DEM-derived path constraints remains.
- No field validation or operational superiority claimed.

### Next scientific requirements

- Test route sensitivity to DEM uncertainty.
- Evaluate alternative start and destination locations.
- Define task-specific engineering acceptance criteria.
- Link routing outcomes to the Analog Transfer Matrix.

Reference:
https://robotics.jpl.nasa.gov/what-we-do/flight-projects/mars-science-laboratory/surface-system-software-and-rover-navigation/

## Route-Feasibility Elevation Stress Test

Status: Exploratory — 2026-11-14.

### Design
- Four locations; five endpoint pairs.
- Experimental slope constraints: 3 and 10 degrees.
- Independent and spatially correlated Gaussian perturbations.
- Correlated noise smoothed with Gaussian sigma=2 grid cells.
- Simulated elevation SD: 1 and 3 m.
- 30 trials per model and magnitude.
- Reproducible random seed: 20261114.
- Original searches: 40; simulated searches: 4800.
- These are assumed perturbations, not measured DEM errors.

### Reproducible output

Command: `python -m science.route_uncertainty`

```text
FIELDTWIN ROUTE UNCERTAINTY EXPERIMENT
Window: 1000 m | Grid: 100 m
Seed: 20261114 | Trials per scenario: 30
Assumed SD: 1 m and 3 m (not calibrated errors)

MARS
independent | SD=1.0 m | limit=3 deg | original=5/5 | feasible=150/150 | changed=0/150
independent | SD=1.0 m | limit=10 deg | original=5/5 | feasible=150/150 | changed=0/150
independent | SD=3.0 m | limit=3 deg | original=5/5 | feasible=150/150 | changed=0/150
independent | SD=3.0 m | limit=10 deg | original=5/5 | feasible=150/150 | changed=0/150
correlated | SD=1.0 m | limit=3 deg | original=5/5 | feasible=150/150 | changed=0/150
correlated | SD=1.0 m | limit=10 deg | original=5/5 | feasible=150/150 | changed=0/150
correlated | SD=3.0 m | limit=3 deg | original=5/5 | feasible=150/150 | changed=0/150
correlated | SD=3.0 m | limit=10 deg | original=5/5 | feasible=150/150 | changed=0/150

PILOT_B
independent | SD=1.0 m | limit=3 deg | original=5/5 | feasible=150/150 | changed=0/150
independent | SD=1.0 m | limit=10 deg | original=5/5 | feasible=150/150 | changed=0/150
independent | SD=3.0 m | limit=3 deg | original=5/5 | feasible=143/150 | changed=7/150
independent | SD=3.0 m | limit=10 deg | original=5/5 | feasible=150/150 | changed=0/150
correlated | SD=1.0 m | limit=3 deg | original=5/5 | feasible=150/150 | changed=0/150
correlated | SD=1.0 m | limit=10 deg | original=5/5 | feasible=150/150 | changed=0/150
correlated | SD=3.0 m | limit=3 deg | original=5/5 | feasible=150/150 | changed=0/150
correlated | SD=3.0 m | limit=10 deg | original=5/5 | feasible=150/150 | changed=0/150

ARADS
independent | SD=1.0 m | limit=3 deg | original=3/5 | feasible=88/150 | changed=2/150
independent | SD=1.0 m | limit=10 deg | original=5/5 | feasible=150/150 | changed=0/150
independent | SD=3.0 m | limit=3 deg | original=3/5 | feasible=78/150 | changed=12/150
independent | SD=3.0 m | limit=10 deg | original=5/5 | feasible=150/150 | changed=0/150
correlated | SD=1.0 m | limit=3 deg | original=3/5 | feasible=90/150 | changed=0/150
correlated | SD=1.0 m | limit=10 deg | original=5/5 | feasible=150/150 | changed=0/150
correlated | SD=3.0 m | limit=3 deg | original=3/5 | feasible=84/150 | changed=6/150
correlated | SD=3.0 m | limit=10 deg | original=5/5 | feasible=150/150 | changed=0/150

LASCAR
independent | SD=1.0 m | limit=3 deg | original=0/5 | feasible=0/150 | changed=0/150
independent | SD=1.0 m | limit=10 deg | original=0/5 | feasible=6/150 | changed=6/150
independent | SD=3.0 m | limit=3 deg | original=0/5 | feasible=0/150 | changed=0/150
independent | SD=3.0 m | limit=10 deg | original=0/5 | feasible=16/150 | changed=16/150
correlated | SD=1.0 m | limit=3 deg | original=0/5 | feasible=0/150 | changed=0/150
correlated | SD=1.0 m | limit=10 deg | original=0/5 | feasible=0/150 | changed=0/150
correlated | SD=3.0 m | limit=3 deg | original=0/5 | feasible=0/150 | changed=0/150
correlated | SD=3.0 m | limit=10 deg | original=0/5 | feasible=4/150 | changed=4/150

Route searches: 4840
Results are not calibrated safety probabilities.
FIELDTWIN_ROUTE_UNCERTAINTY_OK
```

### Interpretation
- Mars feasibility did not change in the tested scenarios.
- Pilot B changed in some independent-noise 3 m trials.
- ARADS feasibility changes were concentrated at 3 degrees.
- Láscar occasionally became feasible at 10 degrees.
- Independent versus correlated noise produced different outcomes.
- Results are conditional on these sites, paths, grids,
  perturbation models, and experimental constraints.
- No calibrated probability, physical rover safety claim,
  or validated Earth-Mars transfer claim is supported.

Reference:
https://stac.astrogeology.usgs.gov/docs/data/mars/ctxdtms/
