# FieldTwin — ML-B Benchmark Results

Date: 2026-11-15
Pre-evaluation commit: a9d2e63
Numerical decision: NO-GO

## 1. Provenance

Results transcribed from the successful user-reported
STEP 5-ML.B.15 Terminal evaluation.
No benchmark rerun or model modification was made
when creating this report.

Training: 81 development NASADEM patches, s25w070.
Evaluation: 122 land-eligible patches in two other tiles.
Synthetic positives: 31.
Untouched comparisons: 91.
Synthetic prevalence: 31/122 (25.41%).
Features: six numerical DEM descriptors.

Isolation Forest: 300 estimators.
Forest threshold: 0.58051443.
Robust threshold: 3.49108558.
Both thresholds development-calibrated.

## 2. Geographic holdout results

| Metric | s25w071 | s24w068 |
|---|---:|---:|
| Total patches | 44 | 78 |
| Synthetic positives | 11 | 20 |
| Untouched patches | 33 | 58 |
| Forest AP | 0.380413 | 0.419628 |
| Robust AP | 0.687546 | 0.869571 |
| Forest true positives | 9 | 15 |
| Robust true positives | 11 | 20 |
| Forest false positives | 15 | 17 |
| Robust false positives | 14 | 17 |

## 3. Pooled performance

- Isolation Forest AP: 0.389040.
- Robust baseline AP: 0.792177.
- Absolute AP difference: -0.403137.
- Isolation Forest detection: 24/31 (77.42%).
- Robust baseline detection: 31/31 (100.00%).
- Isolation Forest false alarms: 32/91 (35.16%).
- Robust baseline false alarms: 31/91 (34.07%).

Pooled AP was computed from individual patch scores
during the benchmark, not by averaging tile APs.

## 4. Frozen numerical acceptance

- Required pooled AP gain >= +0.05: FAIL.
- No per-tile Forest AP degradation: FAIL on both.
- Per-tile excess FPR <= 0.05: PASS on both.

Overall ML-B numerical decision: NO-GO.
No acceptance threshold was changed.

## 5. Defect category observations

Across the 31 injected defects:
- 7 were missing-data blocks.
- 24 were spikes, depressions, or strips.

Isolation Forest detected:
- Missing-data blocks: 0/7.
- Other injected categories: 24/24.

Robust comparator detected:
- Missing-data blocks: 7/7.
- Other injected categories: 24/24.

These are thresholded results for synthetic defects.
They do not establish real-world defect sensitivity.

## 6. Red Team interpretation

The clean development set has zero missing-data
fraction. StandardScaler cannot learn unit variance
for a constant feature. The robust comparator uses
a fixed 0.01 minimum scale for missing fraction.

This is a plausible explanation for the missing-block
detection difference, not a proven causal diagnosis.

High false-alarm rates on untouched comparison
patches remain a substantial operational limitation.

Untouched patches are not verified artifact-free.
Geographic transfer and real artifact detection
have not been independently validated.

## 7. Scientific decision and future work

The tested robust-statistical method outperformed
Isolation Forest on synthetic-defect AP.

Retain ML-B as a completed experimental comparison.
Do not promote Isolation Forest as superior.

Investigate zero-variance missing-data features
using development-only diagnostic experiments.

Any revised model is a new exploratory version.
Its improvement must be tested prospectively
on new, previously unused geographic holdouts.

Preserve the existing Pareto baseline and
previously documented ML-A outcomes.

Real DEM defect validation: NOT ESTABLISHED.
Mars analog suitability: NOT ESTABLISHED.
Phase 6: FROZEN.

References:
- docs/ML_DISCOVERY_PROTOCOL.md
- https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html
- https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
