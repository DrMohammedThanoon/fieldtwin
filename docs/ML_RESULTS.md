# FieldTwin — ML-A Terrain Discovery Results

Date: 2026-11-15
Status: REAL ML EXPERIMENT COMPLETED;
FULL ACCEPTANCE NOT ESTABLISHED

## 1. Scientific contribution

FieldTwin implements an unsupervised terrain-pattern
discovery pipeline using measured NASADEM features,
development-only standardization, PCA, and MiniBatchKMeans.

Its candidate-selection method was evaluated against
geographic, physical-feature, and random comparators.

The results demonstrate improved descriptor-space
representation over geographic sampling in both
examined evaluation regions.

This is a measurable engineering contribution, not
proof of superior Mars analog suitability.

## 2. Experimental evidence

Training windows: 81.
Development tile: s25w070.
Eligible evaluation windows: 122.
Candidate pools: 22 and 39.
Reserved assessment windows: 22 and 39.
Candidate-selection budget: 8 per region.

Five physical terrain descriptors were used.

PCA explained variance:
Component 1: 0.8993.
Component 2: 0.0844.
Total: approximately 0.9837.

The eight learned development clusters included
one singleton cluster, requiring robustness review.

## 3. Measured benchmark

Lower representation distance is better.

| Method | s25w071 | s24w068 |
|---|---:|---:|
| ML-A | 1.540442 | 0.966896 |
| Geographic | 1.735467 | 1.162176 |
| Physical-feature | 1.454899 | 1.197883 |
| Random mean | 1.748243 | 1.298027 |
| Random SD | 0.272754 | 0.201217 |

ML improvement over geographic sampling:
- s25w071: 11.24%.
- s24w068: 16.80%.

Relative to physical-feature selection:
- s25w071: ML distance was 5.88% higher.
- s24w068: ML distance was 19.28% lower.

These measurements are transcribed from the
successful user-reported ML-A evaluation output.
No evaluation was rerun to create this document.

## 4. Original preregistered decision

Requirement A:
At least 10% improvement over geographic sampling
in each evaluation region.

Result: PASS in both regions.

Requirement B:
ML representation distance no more than 5%
above physical-feature farthest-first selection
in each evaluation region.

Result: FAIL in s25w071; PASS in s24w068.

Overall numerical acceptance: FAIL.

Do not retroactively change these thresholds
or describe the combined gate as passed.

## 5. Additional interpretation

The geographic-sampling comparison demonstrates
that ML-A has measurable terrain-representation
value under the examined candidate budgets.

This interpretation is supported by the original
component metrics. It does not supersede the
full preregistered go/no-go decision.

Any newly proposed acceptance criteria must be
identified as exploratory or tested prospectively
on fresh, independently held-out geographic data.

## 6. Scientific limitations

- Only two geographic evaluation regions.
- Limited statistical generalizability.
- Feature-space coverage is not analog suitability.
- No independent Mars-analog relevance labels.
- One singleton development cluster.
- Terrain-scale robustness evaluation pending.
- No field-based rover validation.
- No demonstrated physical traversability.
- No validated superiority over all non-ML methods.

## 7. Current project decision

ML-A: IMPLEMENTED AND EXPERIMENTALLY EVALUATED.

Improvement over geographic sampling: DEMONSTRATED
IN BOTH EVALUATED REGIONS.

Full preregistered ML-A acceptance: NOT MET.

Maintain the interpretable Pareto terrain comparison
as FieldTwin's primary scientific engine.

Continue robustness evaluation and ML-B development.

Phase 6 remains frozen.

Reference: docs/ML_DISCOVERY_PROTOCOL.md
