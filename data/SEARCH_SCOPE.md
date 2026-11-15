
# FieldTwin — Earth Analog Search Scope

**Version:** 1.0
**Execution Plan:** FieldTwin v6.2
**Status:** Phase 4 exploratory search completed; confirmatory geographic validation pending. See Section 12.

## 1. Purpose

This document defines and records the geographical scope, candidate-selection procedure, controls, and exclusions used by FieldTwin.

It ensures that all Earth analog recommendations are traceable to a documented and reproducible search.

A six-site exploratory Pareto comparison has been completed. No unique analog winner or novel geographic discovery is claimed.

## 2. Mars Reference

- Mars reference region: Provisional CTX study area documented in Phase 3 source records
- Mission or rover-testing objective: DEM-informed rover route selection
- Terrain dataset: USGS CTX stereo-derived DTM; provisional quality
- Spatial coverage: Selected valid reference windows; see Phase 4 benchmark
- Effective analysis scale: 1000 m and 2000 m comparison windows on a 100 m computational grid; source effective resolution not established as identical
- Terrain characteristics: Global slope, P95-P05 relief, and plane-detrended RMS roughness

The Mars reference must be supported by actual verified observations.

## 3. Earth Search Region

- Search region name: Bounded Atacama exploratory sampling study
- Country or geographical area: Northern Chile
- Search boundary coordinates: Original 9 x 9 pilot sampling region documented in later sections; no continuous search-polygon claim
- Boundary GeoJSON or polygon: Not independently verified as an exported artifact
- Search area: 81 sampled pilot locations; not an exhaustive regional search
- Elevation dataset: NASADEM_HGT.001, acquired and analyzed
- Dataset coverage: Verified at the selected terrain-analysis locations; not a claim about all Atacama terrain
- Effective analysis scale: 1000 m and 2000 m windows, 100 m computational grid

Only areas actually analyzed may be reported as searched.

## 4. Candidate Selection Method

The intended selection workflow is:

1. Define a bounded Earth search area.
2. Verify NASA elevation-data coverage.
3. Identify valid terrain-analysis locations.
4. Apply documented inclusion and exclusion criteria.
5. Calculate comparable terrain features.
6. Compare candidate features against the Mars reference.
7. Rank candidates using an interpretable baseline.
8. Evaluate controls and scientific uncertainty.

The final sampling procedure, feature thresholds, and weighting must be documented before scientific conclusions are reported.

## 5. Inclusion Criteria

Final criteria will be determined from the mission-testing objective and dataset characteristics.

Possible criteria include:

- Valid elevation data.
- Sufficient terrain coverage.
- Compatible effective spatial resolution.
- Appropriate terrain characteristics.
- Potential relevance to rover mobility or navigation.

These are proposed screening considerations, not finalized thresholds.

## 6. Exclusion Criteria

Possible exclusions include:

- Missing or unreliable elevation observations.
- Insufficient valid terrain coverage.
- Incompatible spatial analysis scale.
- Terrain outside the documented search boundary.
- Locations that cannot support the defined mission-testing objective.

All actual exclusions must be recorded with their reasons.

## 7. Reference and Control Sites

### Known Analog

- Site name: ARADS Playa (historical regional analog context)
- Coordinates: -24.101642, -70.138175 (FieldTwin sample point)
- Scientific reference: NASA ARADS field operations; exact campaign footprint correspondence not independently established
- Selection justification: Established Atacama rover-testing precedent, not an independent positive terrain-suitability label
- Dataset coverage: NASADEM terrain evaluated at this sample point

The known analog must be independently documented.

### Negative Control

- Site name: Láscar control
- Coordinates: -23.37, -67.73 (FieldTwin sample point)
- Selection justification: Rugged volcanic comparison terrain documented by Smithsonian; dissimilarity evaluated only within the selected benchmark
- Dataset coverage: NASADEM terrain evaluated at this sample point

The negative control must provide a scientifically justified dissimilar comparison.

## 8. Candidate Inventory

| Candidate ID | Location | Coordinates | Data status | Evaluation status |
|---|---|---|---|---|
| PILOT_A | Atacama pilot | -24.5, -69.6 | NASADEM acquired | Exploratory Pareto Front 1 |
| PILOT_B | Atacama pilot | -24.4, -69.9 | NASADEM acquired | Exploratory Pareto Front 1; numerical routing case |
| PILOT_C | Atacama pilot | -24.3, -69.9 | NASADEM acquired | Exploratory Pareto Front 1 |
| PILOT_D | Atacama pilot | -24.2, -69.9 | NASADEM acquired | Exploratory Pareto Front 1 |
| ARADS_PLAYA | Historical analog context | -24.101642, -70.138175 | NASADEM acquired | Exploratory Pareto Front 2 |
| LASCAR_CONTROL | Rugged volcanic comparison | -23.37, -67.73 | NASADEM acquired | Exploratory Pareto Front 3 |

Six selected locations have been numerically evaluated using physical terrain descriptors. Their real-world analog suitability remains unvalidated.

## 9. Search Limitations

The final report must explicitly describe:

- Areas searched.
- Areas not searched.
- Dataset coverage limitations.
- Spatial-resolution limitations.
- Candidate-sampling limitations.
- Missing observations.
- Potential selection bias.
- Uncertainty affecting rankings.

FieldTwin must never describe a bounded regional search as an exhaustive global survey.

## 10. Novelty and Discovery Claims

A high-ranked candidate is not automatically a new discovery.

Potential novelty requires a separate literature and existing-analog audit documented in:

`docs/NOVELTY_AUDIT.md`

Possible classifications:

- Known analog.
- Under-recognized candidate.
- New proposed mission-specific use.
- Insufficient evidence.

## 11. Verification Gate

Search-scope validation requires:

- [ ] Mars reference documented.
- [ ] Rover-testing objective defined.
- [ ] Earth search boundary recorded.
- [ ] Actual NASA data coverage verified.
- [ ] Inclusion criteria documented.
- [ ] Exclusion criteria documented.
- [ ] Candidate-selection procedure reproducible.
- [ ] Known analog independently supported.
- [ ] Negative control justified.
- [ ] Geographic limitations disclosed.

**Current status:** Not yet validated.

---

**Scientific principle:** FieldTwin can claim only what its documented geographical search and measurements support.

## Phase 3 — Initial Geographic Scope
### Mars reference candidate
- USGS CTX DTM product:
  T01_000893_1847_XN_04N191W__N09_065929_1853_XN_05N191W.
- STAC bounding box:
  168.06222 to 168.49260 degrees E;
  4.43947 to 4.99562 degrees N.
- Candidate only; scientific acceptance remains provisional.

### Earth acquisition pilot
- Region: Atacama Desert, Chile.
- NASADEM tile: s25w070.
- Nominal tile: 25 to 24 degrees S,
  70 to 69 degrees W.
- This is an acquisition pilot, not a completed
  bounded analog search.

### Unresolved study-design requirements
- Define the precise rover mobility/navigation task.
- Predefine the bounded Earth candidate universe.
- Document inclusion and exclusion criteria.
- Identify a literature-supported known analog.
- Select a defensible negative control.
- Verify actual locations used in prior rover tests.
- Record searched and unsearched geographic areas.
- Compare Earth and Mars at matched physical scales.
- Assess uncertainties and rank stability.
- Do not claim discovery before these requirements pass.

## 12. Phase 5 — Verified Search-Scope Update

Date: 2026-11-15
Status: Exploratory analysis documented; independent
geographic validation not established.

This section supersedes earlier pending-status statements
where Phase 3 or Phase 4 subsequently completed the work.

### Mars reference

- Provisional USGS CTX stereo-derived DTM.
- Real elevation data processed in Phase 4.
- Fine-scale DTM quality remains provisional.
- No physical rover safety or traversability validation.

### Earth exploratory search

- Region: Atacama Desert, Chile.
- NASADEM acquisition tile: s25w070.
- Defined sampling grid: 9 x 9 = 81 locations.
- Latitude: -24.9 through -24.1.
- Longitude: -69.9 through -69.1.
- Search window: 2000 m.
- Processing grids: 100 m and 200 m.
- Initial screening: slope and relief differences.
- Defined sample count is not independently validated
  candidate count or confirmed usable-location count.

### Phase 4 comparison inventory

- PILOT_A: -24.5, -69.6
- PILOT_B: -24.4, -69.9
- PILOT_C: -24.3, -69.9
- PILOT_D: -24.2, -69.9
- ARADS_PLAYA: -24.101642, -70.138175
- LASCAR_CONTROL: -23.37, -67.73

The later six-site baseline uses slope, relief, and
roughness, with unweighted Pareto dominance.

The four pilot candidates were non-dominated at both
reported 1000 m and 2000 m comparison scales.
No unique analog winner was established.

ARADS is a historical rover-testing reference, not
independently validated positive terrain ground truth.

Lascar is the contrasting negative control.
ARADS and Lascar required separate NASADEM tiles
and must not be represented as part of the original
81-location s25w070 sampling grid.

### Geographic validation limitations

- The exploratory pilot has already informed selection.
- No independent geographic holdout set is established.
- No independently rated terrain-relevance labels exist.
- The pilot is not a global or exhaustive Earth survey.
- Geographic separation and spatial-dependence buffers
  must be justified before confirmatory ML evaluation.
- Phase 5 ML evaluation remains NOT ACTIVATED.

### Evidence and source of truth

- science/earth_candidate_pilot.py
- science/baseline.py
- docs/BENCHMARK_PROTOCOL.md
- docs/PHASE4_BASELINE_RESULTS.md
- docs/MODEL_BENCHMARK.md
- outputs/validated/terrain_baseline.json

Earlier pending fields are historical planning records.
The files above document the later implemented work.
Unverified details must remain explicitly unresolved.
