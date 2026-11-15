# FieldTwin — ML-B Failure Analysis

Date: 2026-11-15
Status: DEVELOPMENT-ONLY DIAGNOSTIC COMPLETED

## 1. Purpose

Investigate why the original Isolation Forest
missed seven synthetic missing-data artifacts.

This analysis does not change the original
benchmark or numerical NO-GO decision.

Original benchmark checkpoint: 5f4247e.

## 2. Development-only evidence

Dataset: NASADEM s25w070.
Development patches: 81.
Model: original 300-estimator Isolation Forest.

Missing-data fraction across training:
- Unique value: 0.0.
- StandardScaler variance: 0.0.
- StandardScaler scale: 1.0.
- Robust baseline scale: 0.01.

Isolation Forest tree-split counts:

| Feature | Tree splits |
|---|---:|
| Missing-data fraction | 0 |
| Adjacent difference P50 | 1424 |
| Adjacent difference P95 | 1506 |
| Adjacent difference maximum | 1409 |
| Plane residual RMS | 1409 |
| Local median residual maximum | 1389 |

The trained forest makes no decisions directly
on missing-data fraction.

## 3. Development synthetic diagnostics

Each condition was evaluated on 81
development-region DEM patches.

| Condition | Forest flags | Robust flags |
|---|---:|---:|
| Clean | 4/81 | 4/81 |
| Missing 2x2 | 4/81 | 81/81 |
| Missing 3x3 | 5/81 | 81/81 |

Mean forest anomaly scores:
- Clean: 0.470559.
- Missing 2x2: 0.470379.
- Missing 3x3: 0.472066.

Mean robust anomaly scores:
- Clean: 1.404289.
- Missing 2x2: 4.076790.
- Missing 3x3: 9.000000.

Mean score differences relative to clean:
- Forest 2x2: -0.000180.
- Forest 3x3: +0.001507.
- Robust 2x2: +2.672501.
- Robust 3x3: +7.595711.

Values are transcribed from the user-reported
development-only diagnostic execution.

## 4. Technical interpretation

Missing-data fraction was constant during
development-only Isolation Forest fitting.

The trained trees contain zero splits using
this feature.

Therefore changes to missing-data fraction
cannot directly influence those trained trees.

Small changes to forest scores after injecting
missing blocks may arise through changes to
the five other DEM descriptors.

The robust comparator explicitly normalizes
missing fraction using a 0.01 minimum scale,
which strongly increases its anomaly score.

This supports the feature-insensitivity diagnosis.

It does not prove that the missing feature
alone explains every benchmark difference.

## 5. Proposed second-generation architecture

Separate DEM integrity screening from
learned terrain-pattern anomaly screening.

Layer A: Deterministic integrity checks.
- Missing elevation cells.
- Invalid numerical values.
- Insufficient valid-data coverage.
- Explicit, auditable reason codes.

Layer B: Learned anomaly screening.
- Physical elevation-gradient descriptors.
- Local residual and roughness descriptors.
- Development-fitted Isolation Forest or
  other independently justified ML method.
- Explicit uncertainty and detection limits.

Produce distinct outputs for the two layers.

Do not describe deterministic missing-data
checks as a learned ML discovery.

The architecture is a proposal only.
No V2 performance claim has been established.

## 6. Future evaluation safeguards

The original ML-B benchmark remains NO-GO.

The previously inspected tiles s25w071 and
s24w068 cannot serve as fresh independent
acceptance holdouts for a revised design.

Obtain new geographic evaluation data not
previously used for performance assessment.

Before V2 fitting or new holdout evaluation:
- Define eligible new patches and provenance.
- Define detector and comparator scoring.
- Predeclare injection types and prevalence.
- Freeze evaluation metrics and acceptance gates.
- Define how both integrity and ML layers are
  credited in a fair comparator.
- Retain separate missing-data and terrain
  anomaly performance metrics.

A new model must be labeled exploratory until
prospective evaluation is completed.

## 7. Scientific limitations

Synthetic injections do not validate genuine
NASADEM or CTX processing-error detection.

Untouched patches are not independently
verified to be free of real artifacts.

The original robust comparator has substantial
false alarms on untouched geographic patches.

No rover safety or Mars-analog suitability
claim follows from this diagnostic.

Original ML-A and ML-B results are preserved.

Phase 6 remains frozen.

## 8. References

Original experiment:
docs/ML_DISCOVERY_PROTOCOL.md

Original ML-B results:
docs/ML_B_RESULTS.md

https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html

https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html
