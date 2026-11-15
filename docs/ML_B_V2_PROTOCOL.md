# FieldTwin — ML-B Version 2 Experimental Protocol

Date: 2026-11-15
Status: PROSPECTIVE DESIGN FROZEN BEFORE V2 FITTING

## 1. Objective

Evaluate a hybrid DEM quality-screening architecture
combining deterministic integrity checks with a
supervised machine-learning anomaly detector.

The ML contribution is restricted to detecting
synthetic elevation irregularities on otherwise
finite DEM patches.

Missing-data detection is deterministic and
must not be credited as learned ML performance.

Original ML-B Isolation Forest decision: NO-GO.
Original ML-A decision: NOT FULLY ACCEPTED.

All previous benchmarks remain unchanged.

## 2. Data separation

Original NASADEM development tile: s25w070.

Use fixed development-grid positions:

- Training: columns 0 through 6, rows 0 through 8.
- Calibration: columns 7 and 8, rows 0 through 8.

Training patches: 63.
Calibration patches: 18.

These populations are geographically separated
within the development tile but are not
independent terrain populations.

Calibration patches must not be used for
supervised model fitting or robust-statistic fitting.

New evaluation regions:

s21w069:
- 81 eligible patches.
- All grid locations row 0..8, col 0..8.

s28w069:
- 80 eligible patches.
- Exclude row 5, col 2.

Total prospective evaluation patches: 161.

Preserve the exact locations in
docs/ML_B_V2_HOLDOUT_INVENTORY.md.

The new geographic evaluation data must not enter
training, calibration, feature selection, or tuning.

## 3. Hybrid model architecture

Layer A: deterministic integrity screening.

Check each 10 x 10 DEM patch for:
- Nonfinite elevation values.
- Missing elevation fraction.
- Insufficient valid-data coverage.

An injected missing block produces a distinct
integrity-alert reason code.

Use the same integrity layer for every
machine-learning and comparator method.

The integrity layer is not trained.

Layer B: learned numerical anomaly screening.

Operate only on fully finite elevation patches.

Use five physical descriptors from the original
six-descriptor ML-B feature implementation:

1. Median adjacent absolute elevation difference.
2. P95 adjacent absolute elevation difference.
3. Maximum adjacent absolute elevation difference.
4. Plane-detrended RMS roughness.
5. Maximum local-median elevation residual.

Missing-data fraction is handled by Layer A,
not by the learned Layer B.

No holdout-driven feature selection is permitted.

## 4. Synthetic development training

Source: 63 clean NASADEM development patches.

For each development patch, create:
- One untouched clean example.
- Two reproducible injections for each of
  six physical defect/type-severity combinations.

Physical defect combinations:
- Spike: +60 m and +120 m.
- Depression: -40 m and -80 m.
- Strip offset: +30 m and +60 m.

Training examples per development location:
- One clean.
- Twelve synthetic physical anomalies.

Total examples:
- 63 clean negatives.
- 756 synthetic positives.
- 819 total training examples.

Synthetic labels are derived solely from
the controlled modifications.

Use a deterministic NumPy SeedSequence
with base seed 20261116 and explicit
row, column, defect class and replicate IDs.

Injection positions must use interior locations
and remain independent of model scores.

The generator must preserve original DEM arrays.

All examples from one development location
remain inside the same training partition.

Do not treat the 819 correlated examples
as 819 independent geographic observations.

## 5. Learned detector

Primary V2 model: RandomForestClassifier.

Frozen parameters:
- n_estimators: 300.
- max_depth: 8.
- min_samples_leaf: 3.
- max_features: sqrt.
- class_weight: balanced_subsample.
- bootstrap: True.
- random_state: 20261116.
- n_jobs: 1.

Output:
Probability assigned to synthetic physical anomaly.

This is a model discrimination score, not
a calibrated probability of a real sensor error.

No holdout-based hyperparameter tuning.

## 6. Fair comparators

Comparator A: supervised Logistic Regression.

Train using the same 819 examples and labels.

Use the same five physical descriptors.

Development-training-only StandardScaler.

Frozen parameters:
- class_weight: balanced.
- solver: lbfgs.
- max_iter: 5000.
- random_state: 20261116.

Output:
Synthetic-anomaly class probability.

Comparator B: robust statistical anomaly scoring.

Fit using the 63 clean training patches only.

Use the same five physical descriptors.

For each descriptor:
- Median center from clean training examples.
- Positive MAD scaled by 1.4826.
- For zero MAD use max(IQR / 1.349, 1.0).

Score:
Maximum absolute normalized median deviation.

The robust comparator receives no synthetic
positive labels; this supervision difference
must be disclosed.

The primary superiority benchmark compares
Random Forest against BOTH comparators,
including the supervised Logistic Regression.

All methods share Layer A integrity screening.

## 7. Development-only score thresholds

Use only the 18 clean calibration patches.

For each Layer B method independently:
- Calculate anomaly scores on calibration patches.
- Set the flagging threshold at the 95th percentile.
- Use NumPy linear interpolation.
- Flag only when score is strictly greater
  than its own frozen threshold.

Do not recompute thresholds from evaluation scores.

All three methods use their continuous scores
for average-precision evaluation.

## 8. Prospective holdout injections

Use seed 20261116 with a distinct stream per tile.

Create exactly 24 synthetic positives per tile.

s21w069:
- 24 modified patches.
- 57 untouched comparison patches.
- Positive prevalence: 24 / 81.

s28w069:
- 24 modified patches.
- 56 untouched comparison patches.
- Positive prevalence: 24 / 80.

Combined:
- 48 modified patches.
- 113 untouched comparison patches.
- Positive prevalence: 48 / 161.

Eight artifact/type-severity combinations:
- Spike low and high.
- Depression low and high.
- Strip low and high.
- Missing block low and high.

Allocate exactly 3 examples per combination
in each evaluation tile.

Physical synthetic positives per tile: 18.
Missing-data positives per tile: 6.

Use deterministic selection without replacement
from the frozen eligible geographic identities.

Use an independent random stream per tile.

Assignment must not inspect elevation descriptors,
anomaly scores, or observed model performance.

Physical and missing-artifact geometries and
magnitudes follow original protocol section 12.3.

Only one synthetic modification per positive patch.

All modifications occur in memory.

## 9. Primary ML evaluation

Evaluate Layer B on:
- 18 physical synthetic positives per tile.
- 57 or 56 untouched comparisons per tile.

Exclude the six missing-block examples per tile
from the primary Layer B average precision.

This isolates genuinely learned physical-anomaly
discrimination from deterministic integrity checks.

Compute:
- Average precision per tile and pooled.
- Positive prevalence and exact sample counts.
- Precision-recall curves.
- False-positive rates on untouched patches.
- Thresholded recall by physical defect type.
- Separate low/high severity performance.

Use continuous anomaly scores for AP.

Pooled AP is calculated from concatenated
individual patch scores, not averaged tile AP.

## 10. Prospective acceptance gates

All following requirements must pass:

Gate A:
Pooled Random Forest AP must exceed the larger
of pooled Logistic Regression AP and pooled
robust-statistical AP by at least 0.05 absolute.

Gate B:
Random Forest AP must not be lower than either
comparator's AP on either evaluation tile.

Gate C:
On each tile, Random Forest false-positive rate
on untouched patches must not exceed either
comparator's false-positive rate by more than
0.05 absolute.

Gate D:
The shared deterministic integrity layer must
flag all injected missing-data blocks.

Report any failures without changing thresholds.

No acceptance gate can be relaxed after
inspection of prospective holdout results.

## 11. Secondary analyses

Report separately:
- Missing-data detection: 12 injected cases.
- Integrity-layer false alarms on clean patches.
- Full hybrid binary detection counts.
- Per-defect-type and severity recall.
- Development-only calibration flag counts.
- Individual evaluation-region performance.
- Comparison with original ML-B methodology.

Do not merge deterministic integrity success
into the primary ML average-precision score.

Do not pool incomparable continuous scoring
scales without a separately frozen definition.

## 12. Scientific safeguards

The original holdouts s25w071 and s24w068
were previously inspected and cannot serve as
fresh V2 acceptance regions.

The new regions were inspected only for source
identity, geographic eligibility and DEM coverage.

No new-region anomaly scores have been examined.

Synthetic-defect classification is not validated
real-world DEM artifact detection.

Do not claim:
- Verified real NASADEM defects.
- Verified CTX processing errors.
- Physical rover safety.
- Mars-to-Earth ML transfer.
- Independently validated Mars analog suitability.

Document all training sample correlations,
finite geographic scope, and class prevalence.

Preserve the original physical Pareto baseline.

Any V2 optimization after the benchmark requires
a new experiment and additional untouched data.

Phase 6 remains frozen.

## 13. References

V2 geographic inventory:
docs/ML_B_V2_HOLDOUT_INVENTORY.md

Original ML-B protocol:
docs/ML_DISCOVERY_PROTOCOL.md

Original ML-B results:
docs/ML_B_RESULTS.md

Failure diagnostic:
docs/ML_B_FAILURE_ANALYSIS.md

https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html

https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html
