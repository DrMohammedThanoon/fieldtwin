# FieldTwin — Analog Transfer Matrix

Status: Exploratory scientific framework
Date: 2026-11-14

## 1. Mission Objective

Identify Earth terrain suitable for testing
DEM-informed Mars rover route-selection algorithms.

The central question is:

Which aspects of rover navigation can reasonably be
evaluated at an Earth site selected for similarity to
a particular Mars terrain target?

FieldTwin does not claim that matching topography
reproduces the entire Martian environment.

## 2. Evidence Classifications

- DEM-supported: measurable terrain-scale proxy,
  subject to resolution and uncertainty.
- Additional evidence required: DEM-based similarity
  alone does not establish the needed property.
- Not directly transferable: requires specialized
  simulation, environmental controls, or modeling.

These are evidence categories, not suitability scores.

## 3. Analog Transfer Matrix

| Characteristic | Classification | Earth testing application | Evidence or limitation |
|---|---|---|---|
| Regional slope | DEM-supported | Test grade-aware regional route selection | Matched physical windows; uncertainty review pending |
| Local relief | DEM-supported | Compare regional terrain elevation variation | P95-P05 metric; window dependent |
| DEM-scale roughness | DEM-supported | Assess terrain-scale route cost sensitivity | Plane-detrended RMS; stereo artifacts may affect result |
| Local slope P50/P90 | Additional evidence required | Diagnose steeper terrain sections | Strong scale sensitivity; excluded from baseline ranking |
| Route corridor continuity | Additional evidence required | Test whether planned paths avoid difficult regions | Requires route-level maps and an actual path-planning test |
| Rocks, steps and wheel-scale obstacles | Additional evidence required | Test close-range hazard avoidance | Current DEM resolution is insufficient; require imagery or local surveys |
| Soil strength and wheel traction | Additional evidence required | Test slippage, sinkage and mobility | Require terrain mechanics and rover measurements |
| Surface composition | Additional evidence required | Compare engineering effects of terrain materials | Require imagery, spectroscopy or field sampling |
| Gravity | Not directly transferable | Evaluate effects on normal force and mobility | Earth gravity differs substantially from Mars |
| Atmosphere and temperature | Not directly transferable | Evaluate environmental performance | Require chamber testing or physically justified simulation |
| Dust, lighting and visibility | Additional evidence required | Evaluate perception and sensor robustness | Require observations and controlled scenarios |
| Communications and operational delays | Not directly transferable | Evaluate autonomy under mission-like constraints | Require software simulation of communications and operations |
| Field access and test safety | Additional evidence required | Decide whether Earth field trials are practical | Require permits, access and safety assessment |

## 4. Existing FieldTwin Evidence

Mars reference:
- USGS CTX stereo-derived DEM.
- Provisional reference due to unresolved stereo artifacts
  and elevation uncertainty.

Earth study sites:
- Four exploratory NASADEM candidates.
- ARADS Playa historical rover-testing reference.
- Láscar independently selected negative control.

Initial baseline:
- Analysis windows: 1000 m and 2000 m.
- Grid spacing: 100 m.
- Ranking features: global slope, local relief
  and plane-detrended RMS roughness.
- Method: unweighted Pareto non-dominated sorting.

Observed fronts at both window sizes:
- Front 1: Pilots A, B, C and D.
- Front 2: ARADS Playa.
- Front 3: Láscar control.

These are relative positions among six sites, not
validated analog suitability classifications.

## 5. Uncertainty and Transfer Restrictions

- CTX visual review remains provisional.
- Numerical coverage is not elevation accuracy.
- Processing grid spacing is not effective DEM resolution.
- Elevation datums differ between Earth and Mars.
- Do not compare absolute elevations as interchangeable.
- Local slope estimates are scale sensitive.
- Independent Gaussian perturbations are only hypothetical
  stress tests, not calibrated error probabilities.
- No physical rover trials have yet been conducted.
- No independently validated positive topographic control.
- No final winning Earth analog has been selected.

## 6. Proposed Rover-Test Protocol

Stage A — DEM-Based Desktop Evaluation
- Define a start point, destination and route corridor.
- Compare planned routes using terrain-aware and
  terrain-unaware route-selection baselines.
- Measure route length and DEM-derived exposure to
  slope, relief and roughness.
- Repeat under multiple analysis scales and
  uncertainty scenarios.

Stage B — Earth Field Evaluation (Future)
- Confirm site access and survey fine-scale obstacles.
- Measure soil and traction-related properties.
- Run a suitable rover on surveyed test routes.
- Record slip, traversal time, path deviation,
  intervention events and actual hazards.

Stage C — Mars Transfer Assessment (Future)
- Identify which observed Earth performance metrics
  depend on gravity, soil mechanics or environment.
- Use validated models or controlled testing to
  assess non-transferable operating conditions.
- Record limitations and unresolved uncertainties.
- Do not infer Mars rover success solely from
  performance on Earth.

## 7. Scientific Acceptance Gates

A candidate must not be described as validated until:

1. The rover task and relevant route-scale objectives
   are defined.
2. DEM resolution and uncertainty are addressed.
3. The geographic search and candidate selection
   are documented without cherry-picking.
4. Controls and independent evaluation are reported.
5. Fine-scale hazards and material limitations are
   assessed for the intended rover test.
6. Earth-to-Mars transfer limitations are explicit.

## 8. Official References

NASA JPL — Rover navigation:
https://robotics.jpl.nasa.gov/what-we-do/flight-projects/mars-science-laboratory/surface-system-software-and-rover-navigation/

NASA JPL — Multi-sensor terrain classification:
https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/multi-sensor-terrain-classification-and-terrain-adaptive-navigation-for-rovers-in-very-rough-terrain/

USGS — Mars CTX stereo terrain models:
https://stac.astrogeology.usgs.gov/docs/data/mars/ctxdtms/

NASA Earthdata — NASADEM:
https://www.earthdata.nasa.gov/data/catalog/lpcloud-nasadem-hgt-001

NASA — Mars environment:
https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/mars/
