
# FieldTwin — Scientific Validation

**Version:** 1.0
**Execution Plan:** FieldTwin v6.2
**Status:** Exploratory baseline tested; ML-B V1/V2 NO-GO; independent analog suitability unvalidated.

## 1. Purpose

This document records the scientific validation of FieldTwin's Earth–Mars terrain comparisons, candidate rankings, and optional AI/ML methods.

Only actual measured and reproducible results may be reported.

## 2. Validation Objectives

FieldTwin must demonstrate that:

1. NASA datasets are authentic and traceable.
2. Earth and Mars terrain data are scientifically comparable.
3. Terrain descriptors are calculated correctly.
4. The physical-feature baseline is reproducible.
5. Known analog and negative control comparisons are evaluated.
6. Candidate rankings are robust to reasonable methodological changes.
7. Scientific uncertainty and limitations are documented.
8. Optional AI/ML provides measurable value if retained.

## 3. Data Validation

### Mars Dataset

- Dataset: Pending
- Product identifier: Pending
- Spatial resolution: Pending
- Coordinate reference system: Pending
- Elevation units: Pending
- Quality assessment: Not performed

### Earth Dataset

- Dataset: NASADEM_HGT.001 (planned)
- Granule identifiers: Pending
- Spatial resolution: Pending
- Coordinate reference system: Pending
- Elevation units: Pending
- Quality assessment: Not performed

**Status:** No datasets have been validated.

## 4. Terrain Feature Validation

Required descriptors:

- Slope distributions.
- Local terrain relief.
- Terrain roughness.

For each descriptor, document:

- Mathematical definition.
- Input dataset.
- Spatial analysis scale.
- Units.
- Missing-data handling.
- Reference calculation or test.
- Observed result.
- Validation status.

Automated tests must include synthetic terrain cases with independently calculable expected results.

**Status:** Feature tests not yet implemented.

## 5. Baseline Validation

The interpretable physical-feature baseline must be evaluated before introducing ML.

Record:

- Candidate universe.
- Feature normalization.
- Feature weights.
- Ranking methodology.
- Missing-data treatment.
- Evaluation references.
- Actual ranking results.
- Scientific limitations.

**Status:** Baseline not implemented.

## 6. Known Analog and Negative Control

### Known Analog

- Site: Not selected
- Independent supporting reference: Pending
- Expected relevance: Pending
- Measured features: Pending
- Baseline ranking: Pending

### Negative Control

- Site: Not selected
- Selection justification: Pending
- Expected dissimilarity: Pending
- Measured features: Pending
- Baseline ranking: Pending

The known analog and negative control must be chosen using documented evidence.

They must not be selected after seeing results merely to make the method appear successful.

## 7. Robustness and Sensitivity

Evaluate:

1. Spatial resolution sensitivity.
2. Terrain analysis-window sensitivity.
3. Feature-selection sensitivity.
4. Feature-weight sensitivity.
5. Missing-data effects.
6. Candidate ranking stability.
7. Geographic sampling limitations.

Record actual measurements, sample sizes, and observed changes.

**Status:** Not evaluated.

## 8. Optional AI/ML Benchmark

AI/ML is not mandatory.

Before model evaluation, establish:

`docs/MODEL_BENCHMARK.md`

The benchmark must specify:

- Baseline and ML methods.
- Same eligible candidate universe.
- Independent reference evidence.
- Geographic holdout strategy.
- Primary performance metric.
- Secondary performance metrics.
- Predeclared improvement threshold.
- Uncertainty and failure criteria.

An illustrative primary metric is expert-rated nDCG@5.

An illustrative absolute improvement threshold is 0.05, subject to pre-registration by the team.

These are proposed evaluation choices, not NASA requirements.

Save actual results to:

`outputs/validated/model_comparison.json`

Implement the evaluation test:

`tests/test_model_comparison.py`

If ML does not demonstrate sufficient scientific or operational value, retain the interpretable baseline.

**Status:** ML benchmark not performed.

## 9. Scientific Uncertainty

Document uncertainty arising from:

- Measurement accuracy.
- Dataset processing.
- Spatial resolution.
- Missing observations.
- Sampling strategy.
- Feature weighting.
- Reference evidence.
- Environmental differences between Earth and Mars.

Do not present unsupported numerical precision.

## 10. Blue Team / Red Team Review

### Blue Team

Determine whether the evidence supports the proposed Earth analog recommendation and rover-testing objective.

### Red Team

Challenge:

- Data validity.
- Coordinate systems.
- Spatial scale mismatch.
- Feature calculations.
- Reference-site selection.
- Model evaluation design.
- Data leakage.
- Uncertainty.
- Scientific interpretation.
- Reproducibility.

### Review Outcomes

- PASS — Sufficient evidence and tests.
- REVISE — Correctable weaknesses.
- BLOCK — Critical validation failure.

**Current review outcome:** Pending.

## 11. Validation Results

| Validation area | Status |
|---|---|
| NASA source eligibility | Pending |
| Mars data verification | Pending |
| Earth data verification | Pending |
| Spatial scale comparability | Pending |
| Terrain feature tests | Pending |
| Baseline evaluation | Pending |
| Known analog comparison | Pending |
| Negative control comparison | Pending |
| Robustness analysis | Pending |
| Optional ML benchmark | Not performed |
| Scientific uncertainty | Pending |
| Red Team review | Pending |

No validation results are claimed.

## 12. Reproducibility Requirements

Validation is complete only when:

- [ ] Actual dataset identifiers are recorded.
- [ ] Processing parameters are documented.
- [ ] Scientific tests pass.
- [ ] Baseline results are reproducible.
- [ ] Controls are evaluated.
- [ ] Uncertainty is reported.
- [ ] Relevant robustness checks are completed.
- [ ] Optional ML passes its predeclared evaluation gate.
- [ ] Independent review is completed.
- [ ] Results and relevant evidence are version-controlled.

## 13. References

NASA Planetary Data System:
https://pds.nasa.gov/

NASA Earthdata:
https://search.earthdata.nasa.gov/

NASA Space Apps Challenge:
https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=details

---

**Validation principle:** No scientific result is accepted without traceable evidence, reproducible methods, and documented limitations.

## Phase 3 — Initial Dataset Validation
### NASA MOLA
- Global raster: 5760 × 2880, signed 16-bit.
- Resolution: approximately 3.704 km map-plane posting.
- Elevation extrema: -8177 to 21171 m.
- Observation-count raster spatially aligned.
- Positive-count cells: 15,685,242.
- Zero-count cells: 903,558.
- Zero elevation must not automatically be treated as missing.
- Intended use: regional Mars context only.

### USGS CTX DTM
- Product: T01_000893_1847_XN_04N191W__N09_065929_1853_XN_05N191W.
- GeoTIFF: 1203 × 1568, float32, 20 m posting.
- Valid coverage: 80.00%.
- Central 50% coverage: 99.99%.
- All valid cells form one eight-connected region.
- Elevation range: -2976.107 to -2895.599 m.
- CTX-MOLA QA mean difference: -0.423 m.
- CTX-MOLA QA standard deviation: 6.564 m.
- Hillshade aligned successfully.
- Visual artifact inspection remains pending.
- Orthorectified image URL returned HTTP 404.
- Twenty-meter posting does not establish effective terrain resolution.
- CTX-MOLA agreement is not independent validation.

### NASADEM Earth
- Granule: NASADEM_HGT_s25w070.
- CMR ID: G2816781179-LPCLOUD.
- Raster: 3601 × 3601, EPSG:4326.
- Sampling: one arc-second.
- Valid numerical coverage: 100%.
- Elevation range: 902 to 4340 m.
- Mean elevation: 2207.07 m.
- HGT, NUM and SWB layers extracted successfully.

### Scientific limitations
- Earth and Mars vertical references differ.
- Horizontal sampling differs from effective terrain resolution.
- Numerical validity does not guarantee elevation accuracy.
- No matched-scale terrain descriptors have been calculated.
- No analog suitability or similarity score has been established.

## Phase 5 final validation disposition
Date: 2026-11-15

The verified physical baseline is exploratory,
not an independent analog suitability validation.

ML-B V1 and ML-B V2 are scientifically NO-GO.
The V2 prospective metrics were independently
recomputed from saved site-level results.

Synthetic missing-block integrity testing
passed 12/12 examples in V2.

No independently rated analog-relevance
ground truth, validated unique analog, or
physical rover field performance is claimed.

See `docs/PHASE5_SCIENTIFIC_CLOSEOUT.md`,
`docs/ML_B_V2_FINAL_RESULTS.md`, and
`docs/PROJECT_GATE_P1.md`.

Earlier planning placeholders in this document
must not be interpreted as the latest status.
