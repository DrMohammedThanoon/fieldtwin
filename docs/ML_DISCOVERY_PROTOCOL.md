# FieldTwin — ML Discovery and DEM Quality Protocol

Date: 2026-11-15
Status: PRE-REGISTERED DESIGN — NO MODELS TRAINED
Branch: feat/ml-terrain-discovery

## 1. Objective

Evaluate two distinct machine-learning contributions:

ML-A: Unsupervised Earth terrain-pattern discovery.
ML-B: DEM anomaly screening for scientific quality review.

Neither method is intended to replace the existing
three-feature physical Pareto baseline.

The original docs/MODEL_BENCHMARK.md retains its
separate independently rated analog-ranking criterion.

## 2. Available evidence

Existing local datasets:
- NASADEM: s25w070, s25w071, s24w068.
- Mars: one provisional USGS CTX elevation DTM.
- CTX hillshade is not an independent elevation DTM.

Previously evaluated locations are exploratory.
No independent analog-suitability labels are available.

## 3. ML-A: Terrain-pattern discovery

Task:
Identify distinguishable DEM-scale Earth terrain patterns
and select representative candidate windows for further
physical comparison with the Mars reference.

Candidate method:
- Physical terrain descriptor extraction.
- StandardScaler fitted on development observations.
- PCA with two components.
- MiniBatchKMeans with eight clusters.
- Fixed random seed: 20261115.
- No Mars-reference similarity labels used in fitting.

Primary descriptors:
- Global slope.
- Relief P95-P05.
- Plane-detrended RMS roughness.
- Local slope P50.
- Local slope P90.

Use 1000 m analysis windows and a 100 m processing grid.
Require at least 95 percent valid elevation coverage.
Spatial sampling, candidate budgets, and exact footprints
must be locked before model fitting.

Use the existing physical baseline after candidate discovery.
A cluster is not a suitability class.

## 4. ML-A: Evaluation

Development region:
- NASADEM s25w070.

Proposed geographically separated evaluation:
- NASADEM s25w071.
- NASADEM s24w068.

These are tile identifiers, not proof of independent
statistical populations. Their geographic separation,
overlapping-window buffers, usable candidate counts,
and actual evaluation footprints require verification.

No overlapping analysis windows may cross partitions.
Exclude evaluation windows within a documented
spatial-dependence buffer of development windows.

Compare identical candidate-selection budgets against:
1. Spatially systematic sampling.
2. Seeded random eligible-window sampling.
3. Deterministic physical-feature farthest-first selection.

Primary engineering metric:
Mean nearest-selected-candidate distance across eligible
evaluation windows in standardized physical-feature space,
with lower values indicating better descriptor coverage.

Use scaling learned on development data, not held-out data.

This metric measures physical-feature representation,
not independently validated Mars analog quality.

Provisional ML-A go/no-go:
- At least 10 percent lower mean representation distance
  than systematic sampling on each usable holdout region.
- Report the comparison against random and farthest-first.
- No worse than 5 percent above the farthest-first distance
  on either usable holdout region.
- No unexplained data leakage or missingness bias.
- Stable interpretation under geographic and scale checks.

Thresholds are project decisions, not NASA standards.
If holdouts are inadequate, report descriptive outcomes
only and classify ML-A as not independently validated.

Secondary metrics:
- Cluster occupancy and geographic distribution.
- Stability of terrain groups under resampling.
- Representation of terrain extremes.
- Candidate geographic diversity.
- Processing time and memory.
- Sensitivity to additional terrain descriptors.
- Stability across window sizes and grid spacing.

Do not claim analog suitability from cluster stability
or physical-feature coverage alone.

## 5. ML-B: DEM anomaly detection

Task:
Identify unusual local elevation patterns that merit
independent DEM quality inspection.

Candidate:
IsolationForest using local numerical DEM descriptors.

Comparison:
A deterministic robust-statistical anomaly baseline
using median-based deviations and local gradients.

Training:
Use only a defined development region.
No held-out evaluation data may fit preprocessing,
anomaly thresholds, or model parameters.

Evaluation:
- Spatially separated DEM patches.
- Synthetic artifact injection with fixed random seeds.
- Multiple defined artifact types and magnitudes.
- Untouched clean patches retained as negative cases.
- Independent imagery review when genuinely available.

Synthetic artifacts provide experimental labels only.
They are NOT verified real CTX stereo-processing defects.

Primary metric:
Average precision for patch-level synthetic defect
detection, including prevalence and sample counts.

Provisional ML-B go/no-go:
- At least +0.05 absolute average precision over
  the deterministic baseline on held-out patches.
- Report false-positive rate on clean patches.
- No material increase in false alarms without
  an independently justified operational benefit.
- No claims of real-artifact validation from synthetic
  injection results alone.

The exact synthetic defect generator, prevalence,
false-alarm limit, geographic split, and eligible sample
count must be frozen before any ML-B model is fitted.

If independent artifact ground truth is absent,
report the model as an experimental QA aid only.

## 6. Shared scientific safeguards

- No random adjacent-pixel train/test splitting.
- No model fitting on evaluation observations.
- No tuning based on held-out performance.
- No fabricated expert labels or rover test results.
- Preserve original DEM values and masks.
- Never use CTX hillshade as independent DEM truth.
- Record effective resolution and sensor differences.
- Report actual sample sizes and exclusion reasons.
- Preserve source IDs, CRS, units, and provenance.
- Report uncertainty and failures, not only successes.
- Use reproducible seeds and saved model settings.

A model that fails its criterion is not promoted.

## 7. Expected implementation artifacts

Proposed:
- science/ml_terrain.py
- science/ml_quality.py
- science/evaluate_ml.py
- tests/test_ml_terrain.py
- tests/test_ml_quality.py
- docs/ML_RESULTS.md
- outputs/validated/ml_discovery.json

These are planned files, not completed results.

## 8. Scientific acceptance

ML-A may be presented as measured terrain-discovery
assistance only if its evaluation gates pass.

ML-B may be presented as a measured synthetic-defect
screening experiment only if its evaluation gates pass.

Neither establishes:
- Unique or newly discovered Earth analogs.
- Physical rover safety.
- Validated Mars-to-Earth transfer.
- Independently rated ML superiority in analog ranking.

The Pareto baseline remains authoritative unless
separate evidence supports changing that decision.

Phase 6 remains frozen until at least one actual
ML implementation is tested and its limitations
are documented.

## 9. References

https://scikit-learn.org/stable/modules/decomposition.html
https://scikit-learn.org/stable/modules/clustering.html
https://scikit-learn.org/stable/modules/outlier_detection.html
https://scikit-learn.org/stable/modules/cross_validation.html
https://stac.astrogeology.usgs.gov/docs/data/mars/ctxdtms/

Internal references:
- science/terrain.py
- science/baseline.py
- docs/MODEL_BENCHMARK.md
- docs/PHASE4_BASELINE_RESULTS.md
- docs/ANALOG_TRANSFER_MATRIX.md


## 10. Frozen ML-A Geographic Sampling Design

Date: 2026-11-15
Status: FROZEN BEFORE MODEL FITTING

### 10.1 Verified sampling

Three NASADEM tiles, 81 predefined locations each:

Development:
s25w070: lon -69.9 to -69.1,
latitude -24.9 to -24.1.

Evaluation 1:
s25w071: lon -70.9 to -70.1,
latitude -24.9 to -24.1.

Evaluation 2:
s24w068: lon -67.9 to -67.1,
latitude -23.9 to -23.1.

Each tile uses a 9 x 9 regular geographic grid
including the stated endpoints.

Window: 1000 m square.
Processing grid: 100 m.
Target CRS: EPSG:32719.
Minimum valid elevation coverage: 0.95.
Minimum local-slope stencil coverage: 0.95.

The eligibility preflight returned 81/81 valid
locations per tile, 243 in total.

Nearest development-to-evaluation center distances:
s25w071: 20.21 km.
s24w068: 124.09 km.

These distances do not establish statistical
independence or absence of regional bias.

### 10.2 Evaluation partition

All 81 development locations may be used for
fitting the ML-A feature scaler, PCA and clustering.

For each evaluation tile:
- Even (row + column) parity: 41 candidate locations.
- Odd (row + column) parity: 40 assessment locations.
- Row and column indices start at zero.
- Selection budget: exactly 8 candidate locations.
- No model fitting on either evaluation tile.
- Assessment features cannot influence selection.

Existing diagnostic inspection of one central window
per evaluation tile must be disclosed; the evaluation
data are not entirely previously unseen.

### 10.3 Model specification

Five physical descriptors, in fixed order:
1. slope_deg
2. relief_p95_p05_m
3. roughness_rms_m
4. local_slope_p50_deg
5. local_slope_p90_deg

Fit StandardScaler on development samples only.
Fit PCA(n_components=2) on scaled development data.
Fit MiniBatchKMeans with:
- n_clusters=8
- batch_size=32
- n_init=10
- random_state=20261115

All evaluation data use these fitted transformations.

For ML candidate selection, transform the 41
candidate-pool observations into PCA space.

Process the eight learned centroids in cluster-ID
order. For each centroid, select the nearest
remaining candidate in PCA Euclidean distance.
Break equal-distance ties by row, then column.
Each candidate may be selected only once.

### 10.4 Comparator specifications

Every method selects 8 locations from the same
41-location candidate pool.

Geographic systematic comparator:
Start at the lowest (row, column) grid position,
then repeatedly select the point maximizing
minimum projected geographic distance to the
already selected points. Tie-break by row, column.

Random comparator:
Uniform sampling without replacement, using
30 predefined seeds from 20261115 through
20261144. Report the distribution, not only
the most favorable random result.

Physical-feature farthest-first comparator:
Use the development-fitted StandardScaler.
Start with the candidate closest to the
development standardized-feature mean.
Then repeatedly maximize minimum Euclidean
distance to selected candidates.
Tie-break by row, column.

Do not use assessment features for selection
or comparator fitting.

### 10.5 Evaluation

Compute the primary representation-distance metric
on the 40 reserved assessment locations per tile.

For each assessment location, measure its
Euclidean distance in development-standardized
five-feature space to its nearest selected candidate.

Report the mean across the 40 locations,
separately for each evaluation tile.

Apply the existing preregistered improvement
thresholds without adjusting them after results.

Report all comparator outcomes, cluster occupancy,
candidate identifiers, missingness, and runtime.

Two evaluation tiles are insufficient for strong
population-level statistical generalization.
Do not treat individual windows as independent
replicates for geographic confidence intervals.

Even successful representation coverage does not
demonstrate independently validated Mars analog
suitability or physical rover safety.

### 10.6 Model activation

This section freezes experimental choices.
No model has yet been fitted or evaluated.

Implementation may proceed only after this
design is verified and reviewed.


## 11. Pre-Fit Land Eligibility Correction

Date: 2026-11-15
Status: PRE-FIT CORRECTION — NO ML TRAINING PERFORMED

### 11.1 Reason

The initial 243-window extraction verified numeric
elevation coverage, but did not exclude water surfaces.

A subsequent NASADEM SWB audit identified 36 fully
water-classified windows in s25w071.

These windows yielded zero-valued terrain descriptors
and are not eligible terrestrial rover-testing sites.

### 11.2 Corrected eligibility rule

Retain the original 1000 m analysis window and
100 m processing grid.

Require:
- Elevation valid fraction >= 0.95.
- Local-slope stencil fraction >= 0.95.
- SWB land fraction == 1.0 on the 100 m screening grid.
- SWB code 0 represents land.
- SWB code 255 represents water.
- Unknown mask values are not eligible.

Water-mask reprojection uses nearest-neighbor sampling.
This is a DEM-scale land-screening rule, not proof of
site accessibility, environmental safety, or absence
of smaller water features.

The land rule is established before any ML-A fitting.

### 11.3 Verified revised sample inventory

Development tile s25w070:
- Defined windows: 81.
- Full-land windows: 81.
- Development samples retained: 81.

Evaluation tile s25w071:
- Defined windows: 81.
- Full-land windows: 44.
- Fully water windows: 36.
- Mixed window: 1.
- Eligible candidate pool: 22.
- Eligible reserved assessment: 22.

Evaluation tile s24w068:
- Defined windows: 81.
- Full-land windows: 78.
- Mixed windows: 3.
- Eligible candidate pool: 39.
- Eligible reserved assessment: 39.

Total:
- Defined windows: 243.
- Full-land eligible windows: 203.
- Excluded water or mixed windows: 40.

These corrected eligible counts supersede the
41/40 evaluation counts in Section 10.

### 11.4 Preserved experimental decisions

The following remain unchanged:
- Development tile and geographic holdout tiles.
- Original 9 x 9 sampling-center coordinates.
- Even/odd geographic partition assignment.
- Five terrain descriptors.
- Development-only scaler, PCA and clustering.
- Eight selected candidates per evaluation tile.
- Primary representation-distance metric.
- Non-ML comparator specifications.
- Previously declared go/no-go thresholds.
- Geographic and scientific limitations.

Evaluation measures only land-eligible assessment
windows: 22 for s25w071 and 39 for s24w068.

No excluded samples may silently enter model fitting,
candidate selection, or reported assessment metrics.

### 11.5 Red Team qualification

The correction was triggered by pre-training data QA,
not observed ML benchmark performance.

The geographic evaluation populations have changed
from the initial planned counts.

This reduction and its potential effect on statistical
representativeness must be disclosed in final results.

No scientific or ML superiority claim is established
by this correction.


## 12. Frozen ML-B Experimental Design

Frozen before any ML-B model fitting or evaluation.

### 12.1 Scope and data

Objective: Detect synthetic local DEM irregularities
that warrant independent scientific quality review.

Source: NASADEM elevation tiles and accompanying
NASADEM SWB land/water masks.

Patch: 1000 m x 1000 m, 100 m grid, EPSG:32719.

Each screened patch contains 10 x 10 elevation cells.

Development:
- s25w070: 81 fully land-eligible clean patches.

Geographic evaluation:
- s25w071: 44 fully land-eligible patches.
- s24w068: 78 fully land-eligible patches.

Total evaluation: 122 patches.

The eligible sample inventories derive from the
previously audited SWB screening procedure.

Development and evaluation are geographically
separated, but independent terrain populations
are not established merely by this separation.

No evaluation data may fit preprocessing,
Isolation Forest, baseline parameters, or cutoffs.

### 12.2 Synthetic injection assignment

Seed: 20261115.

Each evaluation patch appears exactly once.

s25w071:
- 11 synthetically modified patches.
- 33 untouched patches.
- Injection prevalence: 11/44 = 25.00%.

s24w068:
- 20 synthetically modified patches.
- 58 untouched patches.
- Injection prevalence: 20/78 = 25.64%.

Combined:
- 31 modified patches.
- 91 untouched patches.
- Injection prevalence: 31/122 = 25.41%.

Assignments must be deterministic and recorded
by tile, row, column, defect type and severity.

Use an independent reproducible random generator
per tile. Do not use Python's salted hash().

Artifact labels cannot depend on model scores
or observed evaluation performance.

### 12.3 Synthetic artifact definitions

Inject exactly one artifact in each modified patch.

Type A: elevation spike.
- Modify one interior pixel.
- Severity levels: +60 m and +120 m.

Type B: localized depression.
- Modify one interior 2 x 2 block.
- Severity levels: -40 m and -80 m.

Type C: strip elevation offset.
- Modify one interior full-height column.
- Severity levels: +30 m and +60 m.

Type D: missing-data block.
- Invalidate a central-interior 2 x 2 block
  at lower severity, or a 3 x 3 block
  at higher severity.

The generator must preserve original source DEMs.

For each modified patch, select injection
locations reproducibly from permitted interior
positions, except the full-height strip.

Balance types and severities as evenly as
integer sample counts permit on each tile.

Record actual counts for all eight
type-severity combinations.

Synthetic modifications are experimental labels,
not verified sensor, stereo, or mapping errors.

### 12.4 Descriptor and modeling safeguards

Use the same numerical patch-descriptor
definitions for ML and robust baseline.

The descriptor implementation must explicitly
handle invalid values and missing-data fraction.

Candidate descriptors:
- Missing-data fraction.
- Median absolute adjacent elevation difference.
- 95th-percentile adjacent elevation difference.
- Maximum adjacent elevation difference.
- Plane-detrended elevation roughness.
- Maximum absolute local residual deviation.

Exact computational definitions and any required
numerical edge-case handling must be specified
and tested before the first ML-B model fit.

Training:
- IsolationForest on 81 clean development patches.
- Model seed: 20261115.
- No synthetic evaluation data during fitting.
- No evaluation-driven hyperparameter tuning.
- A larger anomaly score means more anomalous.

Baseline:
- Development-fitted robust median/MAD
  deviation scoring on the same descriptors.
- Explicit handling for zero-MAD descriptors.
- Local-gradient information included.

Cutoffs:
- Each method uses its own development-clean
  anomaly-score 95th percentile.
- No holdout-derived decision thresholds.

### 12.5 Metrics and predeclared gates

Primary metric:
- Patch-level average precision (AP) using
  known synthetic labels.
- Report AP pooled and separately per tile.
- Report injection prevalence and raw counts.

Original protocol requirement:
- ML-B pooled AP must exceed robust-baseline
  pooled AP by at least 0.05 absolute.

Additional prospective safeguards:
- No evaluation tile may have ML-B AP below
  robust-baseline AP.
- Evaluation false-positive rate on untouched
  patches must not exceed the robust baseline
  by more than 0.05 absolute on either tile.

Report precision-recall behavior, clean-patch
false alarms, defect-type recall, and model
settings without tuning on evaluation scores.

All requirements must pass for a numerical GO.

Even a numerical GO validates only the
specified synthetic-defect experiment.

### 12.6 Scientific limitations and integrity

Untouched comparison patches are not independently
proven free of real DEM artifacts.

Synthetic injection does not establish that the
model recognizes genuine NASADEM or CTX defects.

Do not use CTX hillshade as independent DEM truth.

Do not claim physical rover safety, Mars-to-Earth
transfer, or validated real-world artifact detection.

Keep the original NASADEM values and masks intact.

Preserve the physical Pareto baseline.

Do not change the design or gates after inspecting
ML-B holdout performance.

Phase 6 remains frozen.


## 13. ML-B Descriptor Definitions

These definitions specify section 12.4 before
any ML-B model fitting or real holdout evaluation.

Input: 10 x 10 grid, 100 m pixel spacing,
elevation in meters, projected EPSG:32719.

NoData is represented internally as NaN.
Infinite values are invalid.
Require at least 75 finite cells and at least
60 valid horizontal/vertical adjacent pairs.

Six descriptors, in fixed order:

1. missing_fraction:
   Missing (NaN) cells divided by 100.

2. adjacent_abs_diff_p50_m:
   Median absolute elevation difference between
   all valid horizontal and vertical adjacent pairs.

3. adjacent_abs_diff_p95_m:
   95th percentile of the same absolute differences,
   using NumPy linear percentile interpolation.

4. adjacent_abs_diff_max_m:
   Maximum of the same absolute differences.

5. plane_residual_rms_m:
   Root mean square residual after least-squares
   fitting z = a + bx + cy to valid cells,
   with projected local 100 m coordinate spacing.

6. local_median_residual_max_m:
   Maximum absolute difference between each valid
   interior elevation and median of its eight
   neighboring cells, excluding its center.
   Require at least four finite neighbors.

Reject patches that cannot produce finite
results for all six descriptors.

Do not replace missing cells with zero elevation.
Do not modify original DEM files or source arrays.

Identical descriptors must be used for ML-B
and its robust-statistical comparator.

Synthetic tests must confirm behavior under:
- Clean planar terrain.
- Isolated positive elevation spike.
- Localized negative depression.
- Strip elevation offset.
- Missing-data block.
- Vertical elevation translation.
- Invalid input and non-mutation checks.

These descriptors are not proof of actual
DEM processing errors or physical rover hazards.


## 14. Frozen ML-B Model Specifications

These algorithm settings are established before
the first ML-B model fit and holdout evaluation.

### 14.1 Development training

Use exactly 81 clean patches from s25w070.

All nine-by-nine development locations must exist
and satisfy the frozen land/coverage requirements.

Use all six descriptors defined in section 13.

No geographic evaluation patch, injected artifact,
or synthetic evaluation label enters fitting.

### 14.2 Isolation Forest

Development-only StandardScaler.

IsolationForest configuration:
- n_estimators: 300
- max_samples: 64
- max_features: 1.0
- bootstrap: False
- contamination: auto
- random_state: 20261115
- n_jobs: 1

Anomaly score is negative sklearn score_samples:
larger values indicate greater anomaly.

The model's built-in contamination decision
threshold is not used for this experiment.

### 14.3 Robust statistical comparator

Use the identical six-feature matrix.

Fit per-feature medians using development only.

Scale positive MAD by 1.4826.

For MAD <= 1e-9, use the larger of:
- Development IQR divided by 1.349.
- A fixed feature-specific minimum scale.

Minimum scales in feature order:
- Missing fraction: 0.01.
- Five elevation descriptors: 1.0 meter each.

The robust anomaly score is the maximum
absolute median-centered, scale-normalized
deviation across all six descriptors.

Both methods include the same local
elevation-gradient information.

### 14.4 Thresholds and comparison

For each method independently, set the cutoff
to the 95th percentile of development-clean
anomaly scores using linear interpolation.

Classify a patch as flagged only if its
anomaly score is strictly greater than
its method's development cutoff.

Scores and thresholds are never recalibrated
using held-out evaluation observations.

Patch-level AP uses continuous anomaly scores,
not binary cutoff predictions.

False-positive rate is the fraction of untouched
evaluation patches flagged by each method.

Preserve section 12.5 acceptance criteria:
- Pooled ML-B AP advantage >= 0.05 absolute.
- ML-B AP no lower on either evaluation tile.
- ML-B clean false-positive rate no more than
  0.05 absolute higher on either evaluation tile.

Record actual AP, prevalence, counts and FPR
whether the numerical outcome passes or fails.

These specifications assess synthetic anomalies
only, not verified real DEM processing errors.
