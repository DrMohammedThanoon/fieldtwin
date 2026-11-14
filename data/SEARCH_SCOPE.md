
# FieldTwin — Earth Analog Search Scope

**Version:** 1.0
**Execution Plan:** FieldTwin v6.2
**Status:** Search area and candidates not yet selected

## 1. Purpose

This document defines and records the geographical scope, candidate-selection procedure, controls, and exclusions used by FieldTwin.

It ensures that all Earth analog recommendations are traceable to a documented and reproducible search.

No candidate ranking or geographical discovery is currently claimed.

## 2. Mars Reference

- Mars reference region: To be selected
- Mission or rover-testing objective: To be defined
- Terrain dataset: To be verified
- Spatial coverage: Pending
- Effective analysis scale: Pending
- Terrain characteristics: Pending

The Mars reference must be supported by actual verified observations.

## 3. Earth Search Region

- Search region name: To be selected
- Country or geographical area: Pending
- Search boundary coordinates: Pending
- Boundary GeoJSON or polygon: Pending
- Search area: Pending
- Elevation dataset: NASADEM_HGT.001 (planned)
- Dataset coverage: Pending verification
- Effective analysis scale: Pending

Only areas actually analyzed may be reported as searched.

## 4. Candidate Selection Method

The intended selection workflow is:

1. Define a bounded Earth search area.
2. Verify NASA elevation-data coverage.
3. Identify valid terrain-analysis locations.
4. Apply documented inclusion and exclusion criteria.
5. Calculate comparable terrain features.
6. Compare candidate features against the Mars reference.
7. Rank candidates using an interpretable baseline.
8. Evaluate controls and scientific uncertainty.

The final sampling procedure, feature thresholds, and weighting must be documented before scientific conclusions are reported.

## 5. Inclusion Criteria

Final criteria will be determined from the mission-testing objective and dataset characteristics.

Possible criteria include:

- Valid elevation data.
- Sufficient terrain coverage.
- Compatible effective spatial resolution.
- Appropriate terrain characteristics.
- Potential relevance to rover mobility or navigation.

These are proposed screening considerations, not finalized thresholds.

## 6. Exclusion Criteria

Possible exclusions include:

- Missing or unreliable elevation observations.
- Insufficient valid terrain coverage.
- Incompatible spatial analysis scale.
- Terrain outside the documented search boundary.
- Locations that cannot support the defined mission-testing objective.

All actual exclusions must be recorded with their reasons.

## 7. Reference and Control Sites

### Known Analog

- Site name: Not selected
- Coordinates: Pending
- Scientific reference: Pending
- Selection justification: Pending
- Dataset coverage: Pending

The known analog must be independently documented.

### Negative Control

- Site name: Not selected
- Coordinates: Pending
- Selection justification: Pending
- Dataset coverage: Pending

The negative control must provide a scientifically justified dissimilar comparison.

## 8. Candidate Inventory

| Candidate ID | Location | Coordinates | Data status | Evaluation status |
|---|---|---|---|---|
| Pending | Not selected | Pending | Not acquired | Not evaluated |

No candidate has been scientifically evaluated yet.

## 9. Search Limitations

The final report must explicitly describe:

- Areas searched.
- Areas not searched.
- Dataset coverage limitations.
- Spatial-resolution limitations.
- Candidate-sampling limitations.
- Missing observations.
- Potential selection bias.
- Uncertainty affecting rankings.

FieldTwin must never describe a bounded regional search as an exhaustive global survey.

## 10. Novelty and Discovery Claims

A high-ranked candidate is not automatically a new discovery.

Potential novelty requires a separate literature and existing-analog audit documented in:

`docs/NOVELTY_AUDIT.md`

Possible classifications:

- Known analog.
- Under-recognized candidate.
- New proposed mission-specific use.
- Insufficient evidence.

## 11. Verification Gate

Search-scope validation requires:

- [ ] Mars reference documented.
- [ ] Rover-testing objective defined.
- [ ] Earth search boundary recorded.
- [ ] Actual NASA data coverage verified.
- [ ] Inclusion criteria documented.
- [ ] Exclusion criteria documented.
- [ ] Candidate-selection procedure reproducible.
- [ ] Known analog independently supported.
- [ ] Negative control justified.
- [ ] Geographic limitations disclosed.

**Current status:** Not yet validated.

---

**Scientific principle:** FieldTwin can claim only what its documented geographical search and measurements support.
