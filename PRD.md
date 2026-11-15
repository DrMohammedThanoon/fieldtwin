
# FieldTwin — Product Requirements Document

**Version:** 1.0  
**Project:** NASA Space Apps Challenge 2026  
**Challenge:** Identify Earth Locations that Analog the Permanent Moon Base Locations and Mars  
**Execution Plan:** FieldTwin v6.2  
**Status:** Scientific baseline and ML experiments evaluated; no validated unique analog; frontend pending.

## 1. Product Vision

**Tagline:** Find where Earth can test Mars — and prove where the analogy breaks.

FieldTwin is a scientific decision-support application that identifies and evaluates real Earth locations as potential analog field-testing sites for Mars rover mobility and navigation.

The project combines NASA planetary and Earth observation data, geospatial terrain analysis, reproducible numerical comparisons, and an interactive web application.

FieldTwin does not claim that any Earth location perfectly reproduces Martian conditions.

## 2. Problem Statement

Earth analog sites are often chosen for their apparent resemblance to extraterrestrial landscapes.

Visual similarity alone cannot establish whether a location is suitable for testing a specific Mars rover mobility or navigation capability.

A defensible selection process must evaluate terrain properties at comparable physical scales, consider uncertainty, and explicitly identify conditions that cannot be transferred between Earth and Mars.

## 3. Proposed Solution

FieldTwin will:

1. Select one documented Martian terrain reference.
2. Define one specific Mars rover mobility or navigation testing objective.
3. Establish a bounded and documented Earth search area.
4. Acquire relevant NASA Earth and Mars datasets.
5. Extract physically meaningful terrain descriptors at compatible effective spatial scales.
6. Compare Earth candidates against the Martian reference.
7. Include a documented known analog and negative control.
8. Rank candidates using a transparent numerical baseline.
9. Evaluate optional AI/ML against that baseline.
10. Investigate candidate novelty and existing analog uses.
11. Report scientific uncertainty and non-transferable conditions.
12. Recommend one defensible Earth location or new mission-specific use.
13. Present the evidence and a proposed rover field-test protocol in a public web application.

## 4. Primary Users

- NASA Space Apps judges.
- Planetary scientists and geospatial researchers.
- Rover mobility and navigation engineers.
- Researchers planning analog field experiments.

## 5. Scientific Data Requirements

### R1 — NASA Dataset Eligibility

Use at least one actual NASA dataset originating from a source listed on the challenge's official Resources page.

Prioritize:
- NASA Planetary Data System (PDS) for Martian observations.
- NASA Earthdata Search for Earth observations.

Record actual product and granule identifiers, rather than citing only data portals.

### R2 — Mars Terrain Reference

Identify a real Mars region supported by documented terrain data.

Use MOLA for regional context where appropriate.

For local elevation comparisons, use an actual verified digital terrain model, such as an available CTX stereo-derived DTM.

CTX imagery alone must not be treated as an elevation model.

### R3 — Earth Terrain Data

Use a bounded, documented Earth search area.

Prioritize NASADEM_HGT.001 for elevation analysis.

NASADEM_SC.001 may support verification or cross-checking.

### R4 — Data Provenance

Document:
- Dataset/product/granule identifiers.
- Source and download links.
- Geographic coverage.
- Spatial resolution.
- Coordinate reference systems.
- Elevation units and datums.
- Quality masks and missing data.
- Processing provenance.
- Licensing and citation requirements.

### R5 — Scientific Comparability

Compare terrain descriptors at compatible effective physical scales.

Maintain separate Earth and Mars coordinate reference systems.

Do not place Mars coordinates on an Earth basemap.

## 6. Terrain Analysis Requirements

### R6 — Physical Descriptors

Calculate scientifically justified terrain features, including:

- Slope distributions.
- Local elevation relief.
- Terrain roughness.

Document each feature's definition, units, analysis window, and effective spatial scale.

### R7 — Interpretable Baseline

Implement an interpretable physical-feature similarity or ranking method.

Document normalization, feature weights, missing-data handling, and limitations.

Do not present subjective similarity weights as universal scientific truths.

### R8 — Controls

Include:
- At least one independently documented known analog.
- At least one deliberately dissimilar negative control.

Evaluate whether the results behave consistently with the documented reference evidence.

### R9 — Uncertainty and Robustness

Evaluate:
- Resolution sensitivity.
- Feature and weight sensitivity.
- Missing-data effects.
- Geographic coverage.
- Ranking stability.
- Relevant measurement and interpretation uncertainty.

## 7. AI/ML Requirements

### R10 — Optional AI/ML Contribution

AI/ML must demonstrate measurable value beyond the interpretable baseline.

Before model tuning, document the comparison protocol in `docs/MODEL_BENCHMARK.md`.

The protocol must identify:
- Candidate universe.
- Independent reference evidence or ratings.
- Geographic holdout strategy.
- Baseline and ML methods.
- Primary evaluation metric.
- Secondary metrics.
- Predeclared improvement threshold.
- Uncertainty and failure criteria.

An example primary metric is expert-rated nDCG@5.

An illustrative threshold is an absolute improvement of 0.05 in nDCG@5. This is a possible team-defined criterion, not a NASA requirement.

Store measured comparisons in `outputs/validated/model_comparison.json`.

If ML does not demonstrate sufficient value, retain the simpler interpretable baseline as the scientific engine.

Never fabricate model metrics or reference labels.

## 8. Novelty Requirements

### R11 — Novelty Audit

Check whether leading Earth candidates have already been identified or used as planetary analogs.

Document relevant literature, known sites, search methods, and dates.

Classify claims accurately:
- Known analog.
- Under-recognized candidate.
- New proposed mission-specific use.
- Insufficient evidence.

Do not claim a first-ever discovery without adequate evidence.

## 9. Analog Transfer Requirements

### R12 — Analog Transfer Matrix

For the recommended location, classify the relevant test properties as:

- WORKS — Supported by available evidence.
- DOES NOT TRANSFER — Known physical or environmental mismatch.
- UNKNOWN — Evidence is insufficient.

Explicitly consider gravity, atmosphere, radiation, and other mission-relevant differences.

### R13 — Rover Field-Test Proposal

Recommend a practical mobility or navigation field test specifying:

- Mission or engineering objective.
- Proposed test terrain.
- Rover behavior or capability under evaluation.
- Measurements and evaluation criteria.
- Required field validation.
- Environmental and scientific limitations.

A proposed test must not be described as a completed experiment.

## 10. Web Application Requirements

The public FieldTwin application must contain four connected views.

### View 1 — Mission

Explain the Mars reference terrain, intended rover capability, and scientific motivation.

### View 2 — Search

Display the documented Earth search region, real candidate locations, screening criteria, and exclusions.

### View 3 — Comparison

Compare candidate locations, the known analog, and the negative control using measured terrain features, uncertainty, and actual results.

### View 4 — Transfer / Rover Test

Explain which terrain properties transfer, which do not, and what rover experiment the selected location could support.

All scientific claims must link to evidence.

## 11. Technical Requirements

- React, TypeScript, and Vite for the frontend.
- MapLibre GL JS for Earth mapping.
- Python 3.12 for scientific processing.
- NumPy, Pandas, SciPy, Rasterio, GeoPandas, and scikit-learn where justified.
- QGIS for independent GIS inspection.
- Git and GitHub for source control.
- GitHub Pages or Vercel for public hosting.

The scientific analysis must remain independent of the frontend.

The frontend will consume small, validated JSON/GeoJSON outputs rather than raw terrain rasters.

The solution must operate without Esri.

Esri services may be integrated only if access is confirmed and their value justifies the additional complexity.

## 12. Nonfunctional Requirements

- Reproducible scientific methods and outputs.
- Traceable data sources.
- No fabricated measurements or claims.
- Stable public URL without login.
- Responsive desktop and mobile interface.
- Clear loading, error, and missing-data states.
- Secure handling of credentials.
- No large raw datasets committed to Git.
- Version-controlled development and independent review.

## 13. Minimum Acceptance Criteria

FieldTwin is scientifically and technically ready only when:

- [ ] At least one eligible NASA dataset is actually used and documented.
- [ ] Mars terrain data is verified and readable.
- [ ] Earth terrain data is verified and readable.
- [ ] Spatial scales and measurement units are validated.
- [ ] The Earth search area and candidate-selection method are documented.
- [ ] A reproducible terrain-feature baseline produces actual results.
- [ ] A known analog and negative control are evaluated.
- [ ] Uncertainty and robustness are documented.
- [ ] Any retained ML method passes its predeclared evaluation gate.
- [ ] The novelty audit is completed.
- [ ] An Analog Transfer Matrix is provided.
- [ ] One defensible candidate or mission-use recommendation is supported by evidence.
- [ ] The four application views function correctly.
- [ ] Scientific tests pass.
- [ ] The frontend production build succeeds.
- [ ] The public application works without authentication.
- [ ] Source code, citations, limitations, and reproducibility instructions are published.
- [ ] The submission follows the applicable NASA Space Apps 2026 rules.

## 14. Out of Scope

- Global high-resolution analysis of every Earth location.
- Full rover physics simulation as a mandatory deliverable.
- Developing a complete Mars rover.
- Training large deep-learning models without demonstrated need.
- Claims of fully reproducing Mars environmental conditions.
- Mandatory paid GIS services or GPU infrastructure.
- Unsupported claims of scientific discovery.

## 15. Official References

NASA Challenge:
https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=details

NASA Challenge Resources:
https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=resources

NASA Planetary Data System:
https://pds.nasa.gov/

NASA Earthdata Search:
https://search.earthdata.nasa.gov/

NASADEM Elevation Dataset:
https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_HGT.001

NASADEM Slope and Curvature Dataset:
https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_SC.001

NASA Space Apps Resource Guidance:
https://github.com/nasa/spaceapps/discussions/1849

---

**Document status:** Initial requirements baseline. Scientific results and implementation completion must be verified through the project's evidence, testing, and review process.

## Phase 5 verified scope clarification
Date: 2026-11-15

Scientific implementation and validation
progress supersede the initial requirements
planning status.

The four exploratory pilot locations are
nondominated; no unique analog winner
or verified first-ever site is established.

ML-B V1/V2 produced NO-GO results.
The validated physical baseline is retained.

Phase 6 development is conditionally
approved in `docs/PROJECT_GATE_P1.md`.

See `docs/PHASE5_SCIENTIFIC_CLOSEOUT.md`
for the final evidence-limited conclusion.
