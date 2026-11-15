# FieldTwin — ML-B V2 Development Fit

Date: 2026-11-15
Status: DEVELOPMENT-ONLY FIT; HOLDOUT UNTOUCHED
Git checkpoint: cc5cf82

## Scientific purpose

Record the frozen V2 fitting and calibration results
before prospective evaluation.

The original ML-A and ML-B benchmarks remain unchanged.

## Development population

Source tile: s25w070
Training geographic sites: 63
Calibration geographic sites: 18
Training examples: 819
Clean training examples: 63
Synthetic physical anomalies: 756
Calibration examples: 18 clean, untouched patches
Physical descriptors: 5
Training/calibration geographic overlap: NONE

Training matrix SHA256:
fedd6e439e531f8d7a7a062d80a7dccd094c42d72cd9742817d143beeea49af1

Calibration matrix SHA256:
60bd6dfaa192cdfa9316ee839875f6fda78ac43761bbd11e7c5089ace344ad2c

## Input provenance

- data/raw/earth/nasadem/s25w070.hgt: 23c81aeedf2bdb8e537a28a002722ddbe377da698bad1f372e61d1b12b81ff27
- data/raw/earth/nasadem/s25w070.swb: a5566df5920e147ae1f50a45ceca1f0b86333b4cc9c62dcfedd65b7a13a9036f

Frozen protocol SHA256:
c6390983fd073c6474ec8b1e1cd07c28f764f9f859b2291dcb4ed3cdf915150b

Holdout inventory SHA256:
5434bc8c69181f7d6c8d1efeafe05d66201a020a5749fad199d590ec0cda6623

## Fitted methods

- RandomForestClassifier: 300 trees, frozen seed 20261116.
- StandardScaler + LogisticRegression, frozen settings.
- Clean-training-fitted robust median/MAD comparator.

No model specification or training partition was changed.

## Clean-development score diagnostics

| Method | Training median | Calibration median | 95th-percentile calibration threshold | Calibration flags |
|---|---:|---:|---:|---:|
| random_forest | 0.00000000 | 0.00746048 | 0.50608020 | 1/18 |
| logistic_regression | 0.00393578 | 0.00735980 | 0.03346996 | 1/18 |
| robust | 0.92335930 | 2.56007813 | 12.46553271 | 1/18 |

Each threshold uses NumPy's linear-interpolated
95th percentile on 18 clean calibration scores.

Flags require score strictly greater than threshold.

## Interpretation

All three scoring methods were successfully fitted.

Calibration score medians exceed clean-training
score medians for all three methods.

This is a descriptive observation, not proof of
generalization failure or success.

Each method flags 1/18 calibration observations.

This 5.56% calibration flag rate is largely imposed
by the percentile threshold construction. It must
not be reported as an independently measured FPR.

The 18 calibration sites share one development
region and are not a separate geographic holdout.

Random Forest and Logistic Regression outputs are
synthetic-label discrimination scores, not calibrated
probabilities of real DEM defects.

The 819 training examples are correlated observations
derived from 63 geographic patches.

## Prospective evaluation safeguards

The following regions have not been loaded or scored:

- s21w069: 81 eligible evaluation windows.
- s28w069: 80 eligible evaluation windows.

Do not adjust the frozen models, thresholds, injection
scheme, or acceptance gates after inspecting holdout
results.

No verified real-world DEM anomaly performance
has been established.

Original ML-B NO-GO result remains unchanged.

## Current state

Development fitting: COMPLETED.
Development threshold calculation: COMPLETED.
Fitted model files persisted: NO.
New geographic holdout scoring: NOT PERFORMED.
Prospective acceptance: NOT EVALUATED.
Phase 6: FROZEN.

## References

docs/ML_B_V2_PROTOCOL.md

docs/ML_B_V2_HOLDOUT_INVENTORY.md

docs/ML_B_RESULTS.md

https://numpy.org/doc/stable/reference/generated/numpy.percentile.html

https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
