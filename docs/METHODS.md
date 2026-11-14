
# FieldTwin — Scientific Methodology

**Version:** 1.0
**Execution Plan:** FieldTwin v6.2
**Status:** Proposed methodology — implementation pending

## 1. Research Objective

Identify an Earth terrain location suitable for testing a specific Mars rover mobility or navigation capability.

Evaluate the scientific strength and limitations of the Earth–Mars terrain analogy using real observations.

## 2. Scientific Workflow

The planned methodology consists of:

1. Define the Mars rover-testing task.
2. Select a documented Martian terrain reference.
3. Acquire verified NASA Mars elevation data.
4. Define a bounded Earth search area.
5. Acquire verified NASA Earth elevation data.
6. Validate spatial references, units, and data quality.
7. Harmonize effective physical analysis scales.
8. Extract relevant terrain descriptors.
9. Implement an interpretable similarity baseline.
10. Compare candidates with a known analog and negative control.
11. Evaluate uncertainty and ranking stability.
12. Benchmark optional ML against the baseline.
13. Audit novelty and existing analog uses.
14. Develop the Analog Transfer Matrix.
15. Recommend a defensible rover field-test application.

## 3. Data Sources

### Mars

Primary source: NASA Planetary Data System.

Potential products:
- MOLA for regional topographic context.
- Verified CTX-derived DTM for local elevation analysis.

CTX imagery must not be treated as elevation data.

### Earth

Primary source: NASA Earthdata Search.

Planned datasets:
- NASADEM_HGT.001.
- NASADEM_SC.001 as an optional supporting product.

Actual downloaded products and granule IDs will be recorded in `data/SOURCES.md`.

## 4. Spatial Comparability

Earth and Mars observations must be analyzed using their respective valid spatial reference systems.

Terrain characteristics must be compared at compatible physical scales, expressed in meters.

Different source resolutions, datums, missing observations, and processing methods must be documented.

The exact harmonization method will be established after inspecting the selected datasets.

## 5. Terrain Features

Candidate descriptors include:

- Slope distributions.
- Local elevation relief.
- Terrain roughness.

Final definitions, window sizes, sampling methods, units, and quality criteria must be documented before interpreting results.

## 6. Interpretable Baseline

A transparent physical-feature comparison will serve as the primary baseline.

Its specification must include:

- Feature normalization.
- Similarity or distance calculation.
- Feature weighting.
- Missing-data treatment.
- Candidate ranking.
- Sensitivity analysis.

No ranking results are available yet.

## 7. Scientific Controls

Include:

**Known analog:** An independently documented Earth location with relevant planetary analog characteristics.

**Negative control:** A justified Earth location expected to be dissimilar for the selected testing objective.

Actual locations will be determined through evidence-based selection.

## 8. Uncertainty and Validation

Evaluate:

- Data quality and coverage.
- Effective spatial resolution.
- Feature measurement uncertainty.
- Weight sensitivity.
- Resolution sensitivity.
- Ranking stability.
- Geographic sampling bias.
- Missing observations.

Results will be reported in `docs/VALIDATION.md`.

## 9. Optional AI/ML Evaluation

AI/ML may be retained only if it demonstrates measurable value over the interpretable baseline.

Before evaluation, document the protocol in `docs/MODEL_BENCHMARK.md`.

Use independent reference evidence and geographically separated evaluation areas where feasible.

Record actual metrics and scientific limitations.

Do not claim ML superiority without supporting evidence.

## 10. Novelty Assessment

Review scientific literature and documented planetary analog uses for the leading candidates.

Differentiate between:
- Known analogs.
- Under-recognized candidate locations.
- New mission-specific applications.
- Insufficient evidence.

Record findings in `docs/NOVELTY_AUDIT.md`.

## 11. Analog Transfer Assessment

For the recommended candidate, evaluate which terrain and environmental characteristics transfer meaningfully to the selected rover-testing task.

Use:

- WORKS
- DOES NOT TRANSFER
- UNKNOWN

Explicitly consider gravity, atmosphere, radiation, and other relevant physical limitations.

## 12. Reproducibility

The scientific implementation must provide:

- Version-controlled Python scripts.
- Verified dataset identifiers.
- Documented processing parameters.
- Automated tests.
- Reproducible numerical outputs.
- Scientific references.
- Explicit limitations.

Large raw datasets will not be committed to Git.

## 13. Implementation Status

- [ ] Mars reference selected.
- [ ] Earth search area defined.
- [ ] NASA datasets acquired and verified.
- [ ] Terrain descriptors implemented.
- [ ] Baseline implemented and evaluated.
- [ ] Scientific controls evaluated.
- [ ] Uncertainty analysis completed.
- [ ] Optional ML benchmark completed, if applicable.
- [ ] Novelty audit completed.
- [ ] Analog Transfer Matrix completed.
- [ ] Final recommendation scientifically validated.

**Current status:** No scientific measurements or results have been produced.

## 14. References

NASA PDS:
https://pds.nasa.gov/

NASA Earthdata:
https://search.earthdata.nasa.gov/

NASADEM_HGT.001:
https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_HGT.001

NASA Space Apps Challenge:
https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=details

---

**Scientific requirement:** Every finding must be based on reproducible observations, defensible methods, and explicitly documented limitations.
