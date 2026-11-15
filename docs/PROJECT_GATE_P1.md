# FieldTwin — Project Gate P1

Date: 2026-11-15
Decision: CONDITIONAL GO — PHASE 6 IMPLEMENTATION ONLY
Scientific baseline: PRESERVED
ML-B V1: NO-GO
ML-B V2: NO-GO

## 1. NASA challenge

Identify Earth Locations that Analog the Permanent
Moon Base Locations and Mars.

Official challenge:
https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/

FieldTwin's specific mission use is comparative,
DEM-informed rover route-selection research.

The project addresses the challenge through
measured terrain characteristics, documented
Earth analog candidates and an interactive tool.

A newly validated analog discovery has not
been demonstrated.

## 2. Verified capabilities

- Real NASADEM terrestrial elevation analysis.
- Provisional USGS Mars CTX terrain reference.
- Reproducible physical terrain descriptors.
- Two analysis windows: 1000 m and 2000 m.
- Common computational grid: 100 m.
- Unweighted physical Pareto comparisons.
- Four exploratory Earth candidate locations.
- ARADS historical rover-testing reference.
- Láscar negative control.
- Exploratory grid-based route experiments.
- Hypothetical elevation uncertainty analysis.
- Documented Analog Transfer Matrix.
- Reproducible scientific tests and provenance.
- Synthetic missing-data integrity: 12/12 detected.

The common computational grid does not imply
equal effective source-data resolution.

## 3. Scientific limitations

- No uniquely validated Earth analog winner.
- No demonstrated first-ever analog discovery.
- Mars stereo-derived DTM remains provisional.
- No independently validated positive
  topographic suitability labels.
- No completed candidate-specific novelty audit.
- No physical rover field validation.
- Rover grade limits remain hypothetical.
- Route feasibility is not rover safety.
- Missing-data integrity evidence is synthetic.
- ML-B V1 and V2 failed scientific acceptance.
- No validated real-world ML anomaly detector.

## 4. Phase 6 approval

CONDITIONAL GO for building a scientifically
transparent, public, no-login web demonstration.

This approval authorizes development and testing
only. It is not a scientific GO for a uniquely
suitable analog site or a GO for unvalidated ML.

The application must use verified, precomputed
scientific artifacts. It must not invent
measurements, coordinates or scientific rankings.

## 5. Approved four-screen architecture

### Screen 1 — Mission

Explain the Mars terrain reference and the
DEM-informed rover route-selection objective.

Clearly label provisional Mars terrain quality.

### Screen 2 — Search

Show the actual bounded Earth study locations,
source provenance, known reference and negative
control.

Use real Earth coordinates, not invented markers.
Do not put Mars coordinates on an Earth basemap.

### Screen 3 — Comparison

Show measured descriptors, differences,
Pareto fronts and explicit multiple-candidate
nondominance.

Do not designate a unique winning location.

Display source, scale, uncertainty and
limitations alongside rankings.

### Screen 4 — Transfer / Rover Test

Show the exploratory route-planning experiments
and Analog Transfer Matrix.

Separate DEM-supported properties, properties
requiring further evidence, and conditions
that cannot directly transfer Earth-to-Mars.

Do not describe simulations as field testing.

## 6. Explicit exclusions

The judge-facing application must not claim:

- A scientifically proven unique analog winner.
- First-ever discovery of an analog location.
- Random Forest superiority over comparators.
- Operationally validated anomaly detection.
- Certified rover traversal or navigation safety.
- Physical reproduction of Mars gravity,
  atmosphere, soil mechanics or radiation.
- An actually conducted field rover experiment.

ML study findings may appear only as
clearly labeled experimental limitations,
not validated site-selection intelligence.

## 7. Open submission-critical work

1. Review candidate novelty using authoritative
   scientific literature and documented searches.
2. Identify a defensible candidate-specific
   engineering use or label the shortlist
   exploratory if evidence remains insufficient.
3. Reconcile outdated status statements in
   source, validation and demo documentation
   with the completed scientific work.
4. Build and test a public four-screen web app.
5. Verify judge-facing sources and accessibility.
6. Prepare presentation, team attribution,
   AI-use disclosure and official submission.

The final presentation must distinguish
completed experimental work from proposed work.

## 8. Engineering and deployment

Default frontend: React, TypeScript, Vite.
Default Earth mapping: MapLibre GL JS.
Public access: no mandatory sign-in.
Esri: optional, never a critical dependency.

Keep existing scientific files and frozen
experimental results unchanged.

A public deployment and actual NASA submission
require separate verification.

## 9. Project-level decision

BLUE TEAM:
Existing scientific measurements, route experiments
and documented limitations justify building an
interactive research demonstration.

RED TEAM:
The current evidence does not justify a unique
analog winner, verified novelty or operational
machine-learning performance.

FINAL:
CONDITIONAL GO for Phase 6 implementation.
NO-GO for unsupported scientific claims.
Submission readiness remains UNVERIFIED.

## 10. References

NASA Space Apps 2026 challenge:
https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/

NASA Space Apps 2026 dates and submission:
https://www.spaceappschallenge.org/2026/

NASA LP DAAC NASADEM:
https://lpdaac.usgs.gov/products/nasadem_hgtv001/

Internal evidence:
- docs/PHASE4_BASELINE_RESULTS.md
- docs/ANALOG_TRANSFER_MATRIX.md
- docs/ML_B_V2_FINAL_RESULTS.md
- outputs/validated/terrain_baseline.json
