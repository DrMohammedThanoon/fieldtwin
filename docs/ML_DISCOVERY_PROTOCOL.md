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
