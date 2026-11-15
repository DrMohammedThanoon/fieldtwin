
# FieldTwin — Scientific Limitations and Analog Transfer

**Version:** 1.0  
**Execution Plan:** FieldTwin v6.2  
**Status:** Preliminary limitations framework — site-specific evaluation pending

## 1. Purpose

FieldTwin evaluates Earth locations as potential analogs for Mars rover mobility and navigation testing.

No Earth location can reproduce every physical and environmental condition on Mars.

This document identifies known differences, limitations of the datasets and methods, and the conditions under which a proposed Earth analog may be scientifically useful.

Scientific conclusions must remain limited to the properties actually measured and validated.

## 2. Scope of the Analogy

FieldTwin primarily evaluates terrain characteristics relevant to rover mobility and navigation.

Potentially comparable properties include:

- Terrain slope.
- Elevation relief.
- Topographic roughness.
- Spatial distribution of terrain features.
- Terrain obstacles when supported by appropriate data.

These properties may support the design of rover navigation or mobility field tests.

However, similarity in topographic measurements does not automatically establish similarity in vehicle performance.

## 3. Fundamental Earth–Mars Differences

### 3.1 Gravity

Mars has substantially lower surface gravity than Earth.

Consequences may include differences in:

- Wheel loading.
- Vehicle stability.
- Wheel–surface interaction.
- Traction and slip.
- Obstacle negotiation.

An Earth field test cannot directly reproduce Martian gravity without specialized experimental methods.

### 3.2 Atmosphere

Mars has a much thinner atmosphere than Earth.

This affects environmental conditions and may influence:

- Dust behavior.
- Thermal management.
- Aerodynamic effects.
- Some sensing and mechanical systems.

Earth field tests cannot automatically validate performance under Martian atmospheric conditions.

### 3.3 Radiation

The radiation environment on Mars differs substantially from conditions at Earth's surface.

FieldTwin's terrain comparison does not assess:

- Radiation resistance of electronics.
- Long-term radiation exposure.
- Radiation-related material degradation.

Radiation performance requires separate engineering evaluation.

### 3.4 Temperature and Illumination

Mars and Earth differ in temperature regimes, atmospheric effects, and illumination conditions.

These differences may affect:

- Sensors.
- Batteries.
- Mechanical components.
- Thermal performance.
- Optical navigation.

Terrain similarity does not guarantee equivalent environmental performance.

### 3.5 Surface Materials

Similar topographic shapes do not guarantee similar surface materials.

Differences may include:

- Particle size.
- Soil cohesion.
- Bearing strength.
- Rock mechanical properties.
- Wheel–soil interaction.
- Dust characteristics.

Remote elevation measurements alone cannot establish these properties.

Separate field measurements, laboratory testing, or supporting observations may be required.

## 4. Remote-Sensing Data Limitations

### 4.1 Spatial Resolution

Earth and Mars elevation products may have different native resolutions.

Comparisons must use compatible effective physical analysis scales.

Features below the available resolution may remain undetected.

### 4.2 Elevation Accuracy

Elevation products may contain measurement or processing errors.

These errors can influence derived:

- Slopes.
- Relief.
- Roughness.
- Candidate rankings.

Actual product accuracy must be checked using source documentation.

### 4.3 Coordinate Systems and Datums

Earth and Mars use different planetary spatial reference systems.

Elevation datums and coordinate definitions must be interpreted correctly.

Mars coordinates must never be treated as Earth geographic coordinates.

### 4.4 Missing Data

Datasets may contain:

- No-data pixels.
- Coverage gaps.
- Invalid observations.
- Processing artifacts.

The analysis must report missing-data handling and valid coverage.

### 4.5 Product Provenance

Derived terrain products may incorporate additional processing beyond their original instrument observations.

FieldTwin must preserve both the original observation source and relevant processing provenance.

## 5. Terrain Similarity Limitations

FieldTwin's physical-feature comparison provides evidence of similarity only for the included measurements.

Limitations may arise from:

- Incomplete feature selection.
- Differences in analysis scale.
- Subjective feature weights.
- Candidate-sampling bias.
- Measurement uncertainty.
- Missing environmental information.
- Differences in surface material properties.

A favorable numerical ranking does not independently prove that a site is suitable for all Mars rover tests.

## 6. Machine Learning Limitations

Machine learning is optional.

Potential risks include:

- Insufficient independent reference data.
- Spatial data leakage.
- Overfitting.
- Unrepresentative geographic sampling.
- Unstable rankings.
- Poor interpretability.
- Unsupported performance claims.

A more complex model is not automatically a better scientific method.

ML may be retained only when its benefit is demonstrated using the predeclared benchmark.

If the evidence is insufficient, FieldTwin will retain the interpretable physical-feature baseline.

## 7. Geographic Search Limitations

FieldTwin uses a bounded Earth search area.

Therefore:

- Unsearched locations cannot be ranked.
- A top-ranked candidate is not necessarily the best location globally.
- Geographic sampling can influence results.
- Dataset coverage may restrict candidate selection.
- Previously documented analogs may exist outside the search region.

The complete search footprint and exclusions must be recorded in `data/SEARCH_SCOPE.md`.

## 8. Analog Transfer Matrix

The final recommendation must include an evidence-based Analog Transfer Matrix.

Classification categories:

**WORKS**  
Evidence supports transferring the specified property or test condition for the defined rover-testing objective.

**DOES NOT TRANSFER**  
A known physical difference or measurement limitation prevents direct transfer.

**UNKNOWN**  
Available evidence is insufficient to determine whether the property transfers.

### Preliminary Assessment

| Property | Preliminary assessment |
|---|---|
| Slope | UNKNOWN for real-world transfer; DEM-derived measurements completed |
| Local relief | UNKNOWN for real-world transfer; DEM-derived measurements completed |
| Terrain roughness | UNKNOWN for real-world transfer; DEM-derived measurements completed |
| Surface material behavior | UNKNOWN — field evidence pending |
| Gravity | DOES NOT TRANSFER directly |
| Atmospheric conditions | DOES NOT TRANSFER directly |
| Radiation environment | DOES NOT TRANSFER directly |
| Navigation-system performance | UNKNOWN for physical rover performance; DEM-grid route experiments completed |

These classifications are preliminary.

Terrain-property classifications must be updated after actual measurements.

Navigation performance cannot be declared validated without relevant testing.

## 9. Field-Test Limitations

A recommended Earth analog location is not equivalent to a completed rover experiment.

A real field test may require:

- Site access and safety assessment.
- On-site terrain verification.
- Ground measurements.
- Surface material characterization.
- Suitable rover hardware.
- Documented experimental procedures.
- Defined performance metrics.
- Repeatable trial conditions.

FieldTwin's initial output is a scientifically informed field-test proposal, not proof of successful Martian rover performance.

## 10. Interpretation Rules

The following distinctions must remain explicit:

1. Measured observation — supported by actual data.
2. Derived measurement — calculated using documented methods.
3. Scientific interpretation — inferred from available evidence.
4. Proposed experiment — planned but not yet performed.
5. Unknown property — insufficient evidence.

No unverified interpretation may be presented as a measured fact.

## 11. Current Limitations Status

- [ ] Mars reference data verified.
- [ ] Earth reference data verified.
- [ ] Analysis scales validated.
- [ ] Terrain uncertainty quantified.
- [ ] Candidate geographic limitations documented.
- [ ] Known analog evaluated.
- [ ] Negative control evaluated.
- [ ] Material-property evidence reviewed.
- [ ] Analog Transfer Matrix finalized.
- [ ] Field-test limitations documented for selected candidate.

**Current status:** Site-specific assessment and validation pending.

## 12. References

NASA Mars Overview:
https://science.nasa.gov/mars/

NASA Planetary Data System:
https://pds.nasa.gov/

NASA Earthdata:
https://www.earthdata.nasa.gov/

NASA Analog Explorer:
https://science.nasa.gov/solar-system/analog-explorer/

NASA Space Apps Challenge:
https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=details

---

**Scientific principle:** Terrain similarity can support a defined engineering test, but it cannot establish complete environmental equivalence between Earth and Mars.
