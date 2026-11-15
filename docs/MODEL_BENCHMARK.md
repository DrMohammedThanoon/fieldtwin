# FieldTwin — Pre-registered Model Benchmark

Status: CONDITIONAL PROTOCOL — NOT YET ACTIVATED
Created: 2026-11-15
Phase: 5
Branch: feat/validation

## 1. Scientific objective

Determine whether an optional unsupervised ML method adds
measurable value over the existing interpretable Pareto baseline
for identifying Earth terrain potentially useful for DEM-scale
Mars rover route-planning and mobility-algorithm field tests.

This is not a physical rover safety or site-access assessment.

## 2. Evidence available before registration

Phase 4 examined a bounded 81-point Atacama pilot and
reported six terrain comparisons: PILOT_A through PILOT_D,
ARADS_PLAYA, and LASCAR_CONTROL.

These are exploratory observations, not independent training
labels or confirmatory test cases.

The Mars CTX stereo DTM remains provisional.
Four pilot candidates are Pareto Front 1 at the evaluated scales.
No unique validated analog winner exists.

ARADS documents historical rover-testing activity, not
independently validated positive terrain relevance.
Lascar is a deliberately contrasting negative control.

No independent expert relevance ratings or geographically
held-out evaluation results have been obtained.

## 3. Candidate universe and geographic separation

Development evidence:
- Existing bounded Atacama pilot and its documented controls.
- Existing source and search-scope manifests.

Confirmatory evaluation requires newly documented Earth
candidate regions geographically separate from the pilot.
Their names, geographic bounds, source products, exclusions,
candidate counts, and selection procedure must be locked
before confirmatory scores are inspected.

Do not treat adjacent DEM pixels or overlapping analysis
windows as independent samples.

Partition geographically coherent regions, not random pixels.
Require non-overlapping footprints and protective buffers
based on analysis-window size and spatial dependence.
Document geographic group IDs and buffer justification.

Use at least three genuinely separate held-out geographic
groups, with at least five eligible rated candidates per group,
before attempting the specified nDCG@5 comparison.

If these requirements cannot be satisfied, the confirmatory
benchmark is not executable; do not substitute pilot results.

## 4. Fixed physical baseline

Source of truth: science/baseline.py

Features:
- slope_deg
- relief_p95_p05_m
- roughness_rms_m

Compute absolute Mars-reference-to-Earth differences.
Minimize all three dimensions using Pareto dominance.
Assign successive non-dominated fronts.

No feature weights, learned normalization, invented similarity
percentage, or within-front preference are permitted.

Represent candidates within the same Pareto front as tied.

Primary analysis:
- 1000 m square windows
- 100 m processing grid
- At least 95% valid coverage

Processing-grid spacing must not be presented as effective
sensor resolution.

## 5. Conditional ML comparator

Prespecified candidate:
StandardScaler followed by PCA with two components,
then Euclidean distance to the Mars reference in the
transformed feature space.

Use exactly the three baseline terrain features.

Fit preprocessing and PCA only on eligible development
data within each geographic evaluation fold.
Transform held-out sites without refitting.
Apply the same fitted transformation to the Mars reference.

The ML retrieval score is negative transformed distance.
Larger scores mean closer similarity in PCA space.

No additional imagery, labels, terrain features, or external
data are available exclusively to the ML comparator.

No tuning on held-out scores is allowed.
If training data or geographic independence are inadequate,
do not fit the comparator.

This is a proposed comparator, not an established improvement.

## 6. Independent relevance evidence

A meaningful external target is required before evaluating
ranked recommendations.

Preferred evidence:
Blinded ordinal assessments from at least two qualified
robotics, planetary-terrain, or field-testing reviewers,
supported by independently documented site characteristics.

Proposed relevance rubric:
0 = unsuitable for the specified test objective
1 = weak relevance or major unresolved limitations
2 = plausible relevance with documented restrictions
3 = strong task-specific relevance supported by evidence

Reviewers must not see baseline/ML scores, predicted ranks,
or system-generated analog recommendations while rating.

Record reviewer expertise, evidence sources, disagreements,
missing ratings, and the prespecified adjudication process.

Terrain-feature similarity alone cannot serve as independent
ground truth. Historical ARADS use is not a positive label.

If these ratings are unavailable or scientifically circular,
no validated ML-superiority claim is permitted.

## 7. Primary evaluation metric

Primary metric: independently rated nDCG@5.

Compute nDCG@5 separately within each eligible held-out
geographic group and summarize groups with equal weighting.

For the Pareto baseline, use negative front indices as
ranking scores, retaining within-front ties.

Use tie-aware nDCG rather than arbitrary alphabetical
or randomly selected ordering within fronts.

For the ML comparator, use negative PCA-space distance.

Groups with fewer than five eligible rated sites, missing
usable relevance evidence, or zero ideal DCG cannot support
the confirmatory primary comparison.

Do not silently discard such groups; report exclusions.

## 8. Secondary analyses

- Control behavior, without treating ARADS as positive truth
- Known-analog Recall@5 only if valid independent labels exist
- Top-k and Pareto-front stability
- 600 m and 2000 m window sensitivity
- 200 m processing-grid sensitivity
- Feature removal and preprocessing sensitivity
- Missingness and coverage-based abstention
- Hypothetical elevation perturbations and rank stability
- Geographic-group variability
- Runtime and data-processing cost
- Source provenance and scientific interpretability
- Alternative explanations for apparent improvements

Previously explored perturbations are sensitivity scenarios,
not calibrated DEM error distributions.

Report missing or unperformed analyses explicitly.

## 9. Uncertainty and sample size

Report:
- Number of independent geographic groups
- Candidate counts per group
- Number and qualifications of independent raters
- Missing and excluded observations
- Per-group metric values and paired differences
- Mean paired nDCG@5 difference
- Geographic-group-level uncertainty intervals
- Reviewer disagreement and sensitivity to adjudication

Use a 95% geographically clustered bootstrap interval
for the paired difference when the independent group count
supports meaningful inference.

Do not bootstrap individual pixels or overlapping windows
as independent observations.

With few geographic groups, describe uncertainty as
insufficient for strong generalization claims.

## 10. Predeclared ML go/no-go criterion

The team's provisional acceptance threshold is:

Mean held-out improvement in nDCG@5 >= +0.05 absolute,
with a 95% geographic-group uncertainty interval whose
lower bound exceeds zero, and no material degradation in
robustness, provenance, missingness handling, or scientific
interpretability.

This is a project-specific decision threshold,
NOT a NASA-prescribed requirement.

If the independent evidence, sample size, or uncertainty
requirements are insufficient, classify the comparison as
NOT VALIDATED, not as a demonstrated ML improvement.

If the ML method does not meet the complete standard,
retain the physical Pareto baseline as FieldTwin's primary
scientific engine.

No alternate metric may replace the primary success criterion
after held-out results have been inspected.

## 11. Activation and reproducibility gates

Before any ML implementation or fitting:
1. Document eligible independent geographic regions.
2. Lock geographic groups, exclusions, and source provenance.
3. Establish independent reference relevance evidence.
4. Confirm sufficient eligible sites per evaluation group.
5. Freeze the evaluation protocol and model specification.

Then, only if these gates pass:
- Implement science/model.py and science/evaluate.py.
- Add tests/test_model_comparison.py.
- Record real results in outputs/validated/model_comparison.json.
- Run the specified model comparison tests.
- Report complete results, including failures.

If the gates cannot be satisfied, record an evidence-limited
no-go decision and continue with the validated Pareto baseline.

### Phase 5.4 — Geographic feasibility assessment

Assessment date: 2026-11-15
Status: NOT ACTIVATED — independent evidence insufficient.

Verified from science/earth_candidate_pilot.py:

- Exploratory sampling grid: 9 x 9 (81 defined locations).
- Geographic extent: latitude -24.9 to -24.1;
  longitude -69.9 to -69.1.
- NASADEM search tile: s25w070.
- Analysis window: 2000 m.
- Processing grids: 100 m and 200 m.
- Initial candidate screening: slope and relief differences.
- This screening is distinct from the later three-feature
  Pareto baseline implemented in science/baseline.py.

Evidence limitations:

- The defined 81 locations are not 81 independent
  confirmatory evaluation cases.
- Pilot selection results have already been examined.
- No independently rated geographic holdout set is verified.
- No independent expert relevance labels are verified.
- Existing control sites do not substitute for positive
  task-specific relevance evidence.
- Geographic separation alone does not eliminate spatial
  dependence; buffers and group definitions require review.

Decision:

Do not train, fit, tune, or promote an ML comparator on
the assumption that the current pilot validates it.

The predeclared benchmark may be activated only after
independent relevance evidence and sufficiently separated
evaluation regions have been established and documented.

Until then, retain the interpretable three-feature Pareto
baseline as the primary scientific method.

This is an evidence-limited hold decision, not proof that
ML cannot add value. No confirmatory ML result exists.

## 12. Scientific limitations

The evaluation cannot establish physical rover safety,
traction, sinkage, obstacle clearance, site access,
or validated Mars-to-Earth environmental transfer.

A high similarity rank is not proof of operational suitability.
The provisional Mars DTM and unequal source sensor
characteristics remain material limitations.

## 13. Methodology references

Execution plan:
FieldTwin_CrossPlatform_Execution_Plan_v6.2.md

Baseline:
science/baseline.py
docs/BENCHMARK_PROTOCOL.md
docs/PHASE4_BASELINE_RESULTS.md

Official documentation:
https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html
https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html
https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
