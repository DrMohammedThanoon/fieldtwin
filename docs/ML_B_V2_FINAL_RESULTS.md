# FieldTwin — ML-B V2 Final Scientific Results

**Experimental status:** Completed first prospective geographic benchmark

**Preregistered decision:** **NO-GO**

**Evaluation source commit:** `b4d51aa`

**Prospective results SHA-256:** `24d7ef7c78c5b1af7ebb6bd300e4b3752a0b805142379316dd974f281f93d2b4`

**Independent audit SHA-256:** `089ff742c9b588fb2f6f92d81d7dffc89bc197776866c30508b1a0dca78992f9`

## 1. Research objective

Assess whether the frozen supervised Random Forest
detects synthetically injected physical anomalies in
NASADEM elevation patches better than both a supervised
Logistic Regression comparator and an unsupervised
robust-statistical comparator.

A separate deterministic integrity layer screens
missing elevation blocks.

The frozen experimental protocol and acceptance
criteria are in `docs/ML_B_V2_PROTOCOL.md`.

## 2. Experimental design and population

The fitted models use 63 development geographic
locations for training and 18 separate clean
development locations for threshold calibration.

Evaluation uses two independent geographic tiles:

- `s21w069`: 81 eligible locations
- `s28w069`: 80 eligible locations

The mixed-land location `(5, 2)` in `s28w069`
was excluded under the frozen eligibility rule.

The final evaluation population contains:

- 161 geographic locations
- 36 synthetically injected physical anomalies
- 12 synthetically injected missing-elevation blocks
- 113 untouched negative comparisons

The physical scoring layer evaluates 149 observations
(36 physical positives and 113 clean negatives).
Missing-data cases are evaluated separately.

This is a geographic holdout experiment using
synthetic anomaly labels, not a real-world defect
ground-truth benchmark.

## 3. Pooled results

| Method | Average precision | Physical TP | False positives | Clean false-positive rate |
|---|---:|---:|---:|---:|
| random_forest | 0.974571 | 36/36 | 20/113 | 17.70% |
| logistic_regression | 0.975984 | 36/36 | 28/113 | 24.78% |
| robust | 0.610942 | 20/36 | 16/113 | 14.16% |

Random Forest pooled AP advantage over its best
comparator: **-0.001413**.

The required improvement was at least **+0.050000**.

The best pooled AP comparator was Logistic Regression.

## 4. Geographic tile results

AP = average precision.
FPR = false-positive rate among untouched negatives.
TPR = physical-anomaly true-positive rate.

| Tile | Method | AP | FPR | TPR | TP | FP | TN | FN |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| s21w069 | random_forest | 1.000000 | 0.122807 | 1.000000 | 18 | 7 | 50 | 0 |
| s21w069 | logistic_regression | 1.000000 | 0.210526 | 1.000000 | 18 | 12 | 45 | 0 |
| s21w069 | robust | 0.675020 | 0.105263 | 0.500000 | 9 | 6 | 51 | 9 |
| s28w069 | random_forest | 0.934752 | 0.232143 | 1.000000 | 18 | 13 | 43 | 0 |
| s28w069 | logistic_regression | 0.958655 | 0.285714 | 1.000000 | 18 | 16 | 40 | 0 |
| s28w069 | robust | 0.579315 | 0.178571 | 0.611111 | 11 | 10 | 46 | 7 |

The reported confusion counts use the preregistered
clean-development calibration thresholds.

## 5. Frozen scientific acceptance criteria

| Preregistered acceptance criterion | Result |
|---|---|
| Pooled RF AP exceeds the best comparator by at least 0.05 | FAIL |
| RF AP is no worse than either comparator on each tile | FAIL |
| RF clean FPR exceeds neither comparator by more than 0.05 on either tile | FAIL |
| Deterministic integrity screen detects all 12 missing blocks | PASS |

**Passed: 1 of 4. Failed: 3 of 4.**

On `s28w069`, Random Forest has three more false
positives than the robust comparator among 56
untouched negative locations. Its FPR excess is
0.053571,
above the allowed maximum of 0.050000.

On the same tile, Random Forest AP is lower than
Logistic Regression AP.

The deterministic integrity screen detected
**12 of 12** injected missing-elevation blocks.

## 6. Blue Team interpretation

Random Forest detected all 36 synthetically
injected physical anomalies at its frozen threshold.

Its pooled ranking performance was substantially
better than the unsupervised robust comparator.

The separate deterministic missing-data
screen detected all 12 synthetic missing blocks.

These observations support the feasibility of
the individual physical-detection and integrity
components under the specified synthetic scenarios.

They do not establish superiority of Random
Forest over the strongest supervised comparator.

## 7. Red Team interpretation and limitations

The model failed the preregistered GO/NO-GO criteria.

Logistic Regression achieved slightly higher pooled
AP and higher AP on `s28w069`.

Random Forest produced 20 false positives among
113 untouched negative locations.

Both supervised methods were trained to recognize
the experiment's synthetic defect patterns.
Success on those patterns does not establish
reliable detection of naturally occurring
NASADEM defects.

Synthetic samples derived from a geographic
location are not independent real-world defect
observations. Geographic separation improves
evaluation design but does not remove all
distribution-shift concerns.

The 18 clean development calibration locations
are not an independent deployment population.
Observed holdout FPR is higher than the
development calibration flag rate.

No independent expert-labeled natural DEM defect
dataset was evaluated.

This report does not establish operational
reliability, real-world error sensitivity, or
general-purpose transfer to other terrain or
planetary datasets.

## 8. Scientific decision and next actions

**ML-B V2: NO-GO.**

The frozen V2 Random Forest cannot be presented
as a validated improvement over both comparators.

The deterministic missing-data screen has a
successful synthetic integrity result, which
may be reported separately with that qualification.

Preserve the original ML-B V1 NO-GO outcome,
the V2 experiment, the exact fitted artifact,
the first-attempt record, and all site-level
prospective outputs.

Any future revised model or altered threshold
must be labeled a new exploratory experiment,
with a newly preregistered protocol and genuinely
unseen confirmatory evaluation data.

Do not reuse these two evaluated tiles as
untouched confirmatory geographic holdouts.

The original physical Pareto baseline remains
separate from these failed ML acceptance gates.

**Phase 6 remains FROZEN** pending a separate
project-level decision about appropriate scope
and evidence-supported presentation.

## 9. Integrity and reproducibility

- First evaluation attempt: `docs/ML_B_V2_EVALUATION_ATTEMPT.json`
- Original site-level results: `docs/ML_B_V2_PROSPECTIVE_RESULTS.json`
- Independent metric audit: `docs/ML_B_V2_INDEPENDENT_AUDIT.json`
- Holdout extraction manifest: `docs/ML_B_V2_HOLDOUT_EXTRACTION.json`
- Fitted-model provenance: `docs/ML_B_V2_FITTED_ARTIFACT.json`
- Frozen protocol: `docs/ML_B_V2_PROTOCOL.md`

The independent audit recalculated pooled AP, tile-level
metrics, confusion counts, and acceptance decisions
from the saved results.

It did not reopen the real rasters, reload fitted
models, or regenerate anomaly predictions.

## 10. Technical references

- NASA LP DAAC, NASADEM HGT V001:
  https://lpdaac.usgs.gov/products/nasadem_hgtv001/
- scikit-learn, average precision:
  https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html
- scikit-learn, precision-recall evaluation:
  https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics
