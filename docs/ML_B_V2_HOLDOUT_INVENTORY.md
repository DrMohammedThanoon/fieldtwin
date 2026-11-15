# FieldTwin — ML-B V2 Geographic Holdout Inventory

Date: 2026-11-15
Status: DATA ELIGIBILITY RECORDED;
MODEL AND BENCHMARK DESIGN NOT YET FROZEN

## 1. Purpose

Reserve two previously unused NASADEM
geographic regions for prospective ML-B V2
synthetic anomaly-detection evaluation.

Original ML-A and ML-B results remain unchanged.

This document records data eligibility only.
It does not assert model performance.

## 2. Source datasets

Dataset: NASADEM_HGT V001.

New NASA Earthdata granules:

- s21w069:
  G2816779959-LPCLOUD

- s28w069:
  G2816782394-LPCLOUD

Both original archives passed ZIP integrity
checks and were imported with their matching
HGT elevation and SWB water-mask files.

Source rasters:
data/raw/earth/nasadem/

## 3. Geographic sampling design

Grid: 9 rows x 9 columns per tile.
Spacing: 0.1 degrees between centers.
Patch footprint: 1000 m x 1000 m.
Analysis grid: 10 x 10 cells at 100 m.
Target projection: EPSG:32719.

s21w069:
- Latitude centers: -20.9 through -20.1.
- Longitude centers: -68.9 through -68.1.
- Both sequences advance by +0.1 degrees.

s28w069:
- Latitude centers: -27.9 through -27.1.
- Longitude centers: -68.9 through -68.1.
- Both sequences advance by +0.1 degrees.

Rows and columns are indexed from 0 through 8.

Sampling coordinates must not be moved or
reselected after inspecting model performance.

## 4. Eligibility criteria

Use the full 10 x 10 projected SWB screen.

An eligible patch requires:
- Every screened SWB cell classified as land (0).
- No water (255) or mixed-class coverage.
- All 100 resampled elevation cells finite.
- Valid source elevation and geographic metadata.

The 100 m grid is an analysis resolution,
not the native resolution of NASADEM.

No excluded samples may enter the evaluation.

## 5. Observed pre-model inventory

The following values were recorded from the
successful user-reported STEP 5-ML.B.29 audit.

| Tile | Proposed | Eligible | Excluded |
|---|---:|---:|---:|
| s21w069 | 81 | 81 | 0 |
| s28w069 | 81 | 80 | 1 |
| Total | 162 | 161 | 1 |

s21w069:
- Fully land: 81.
- Fully water: 0.
- Mixed: 0.
- Incomplete elevation: 0.

s28w069:
- Fully land: 80.
- Fully water: 0.
- Mixed: 1.
- Incomplete elevation among fully land: 0.

Excluded geographic identity:
- Tile: s28w069.
- Row: 5.
- Column: 2.
- Land fraction: 0.84.
- Reason: SWB_NOT_FULLY_LAND.

This excluded window is permanently omitted
from the prospective V2 holdout inventory.

Total eligible geographic windows: 161.

## 6. Separation from original experiments

Original ML-B development:
- s25w070.

Original inspected geographic holdouts:
- s25w071.
- s24w068.

The new regions have not been used for
model fitting, anomaly scoring, or
benchmark-based tuning in FieldTwin.

Geographic separation does not establish
independence of terrain populations, sensor
errors, or source-data processing.

The existing development data may support
exploratory V2 development, provided all
limitations and previous benchmark exposure
are disclosed.

## 7. Prospective evaluation safeguards

The 161 eligible locations are reserved.

Before any new-region anomaly scoring:
- Define V2 model architecture.
- Specify deterministic integrity checks.
- Specify the ML contribution separately.
- Ensure the comparator receives equivalent
  integrity-check information.
- Freeze the injection assignment and seeds.
- Freeze class prevalence and defect severities.
- Freeze scoring, acceptance, and FPR limits.
- Implement and pass synthetic tests.
- Commit the finalized V2 protocol and code.

Do not tune on s21w069 or s28w069 scores.

Do not use the new evaluation populations
for feature selection, threshold calibration,
or model fitting.

Do not claim ML superiority merely because
a deterministic missing-data check succeeds.

## 8. Current scientific decision

Geographic data eligibility: VERIFIED.

V2 evaluation population: 161 eligible windows.

V2 model implementation: NOT STARTED.

V2 benchmark specifications:
NOT YET FULLY PREREGISTERED.

Independent performance validation:
NOT ESTABLISHED.

Original ML-B decision: NO-GO.

Original ML-A findings: PRESERVED.

Phase 6: FROZEN.

## 9. References

NASA LP DAAC:
https://lpdaac.usgs.gov/products/nasadem_hgtv001/

Original scientific protocol:
docs/ML_DISCOVERY_PROTOCOL.md

Original ML-B experimental results:
docs/ML_B_RESULTS.md

Root-cause diagnostic:
docs/ML_B_FAILURE_ANALYSIS.md
