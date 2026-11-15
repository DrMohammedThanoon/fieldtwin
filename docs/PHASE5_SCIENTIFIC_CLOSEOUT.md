# FieldTwin — Phase 5 Scientific Closeout

Date: 2026-11-15
Scientific disposition: EVIDENCE-LIMITED CLOSURE
Project checkpoint: 139d345
Unique validated analog winner: NONE
Operational rover validation: NONE
ML-B V1: NO-GO
ML-B V2: NO-GO
Phase 6: CONDITIONALLY AUTHORIZED UNDER PROJECT GATE P1

## 1. Scientific objective

Investigate Earth terrain as a potential analog for
DEM-informed Mars rover route-selection experiments.

The assessed properties are terrain-scale slope,
elevation relief, roughness, and numerical
route behavior under hypothetical constraints.

This is an exploratory research and engineering
demonstration, not a validated site certification.

## 2. Literature and novelty evidence

Review date: 2026-11-15.

Sources reviewed:

[N1] NASA, Atacama Rover Astrobiology Drilling
Studies (ARADS).
https://www.nasa.gov/universe/atacama-rover-astrobiology-drilling-studies-arads/

[N2] NASA NTRS, Field Analog Lessons-learned in
the ARADS Deployments, document 20240000586.
https://ntrs.nasa.gov/citations/20240000586

[N3] Bapna et al., The Atacama Desert Trek:
Outcomes, ICRA 1998. Nomad robotic exploration.
https://publications.ri.cmu.edu/the-atacama-desert-trek-outcomes

[N4] Cabrol and Wettergreen, Robotic Astrobiology:
Searching for Life with Rovers, 2006. LITA/Zoe.
https://publications.ri.cmu.edu/robotic-astrobiology-searching-for-life-with-rovers

[N5] The Atacama Desert in Northern Chile as an
Analog Model of Mars, Frontiers, 2022.
https://doi.org/10.3389/fspas.2021.810426

[N6] USGS Astrogeology, CTX DTMs:
products, quality and artifacts.
https://stac.astrogeology.usgs.gov/docs/data/mars/ctxdtms/

[N7] Smithsonian Global Volcanism Program:
Lascar, volcano number 355100.
https://volcano.si.edu/volcano.cfm?vn=355100

[N8] Kim et al., Multi-resolution digital terrain
models and their potential for Mars landing site
assessments, Planetary and Space Science, 2013.
https://doi.org/10.1016/j.pss.2013.06.001

[N9] NASA LP DAAC, NASADEM HGT V001.
https://lpdaac.usgs.gov/products/nasadem_hgtv001/

[N10] NASA Space Apps 2026 selected challenge.
https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/

The research search was bounded to these
institutional and published sources and related
Atacama rover navigation/analog topics.

Representative search topics:
- NASA Atacama autonomous rover navigation ARADS
- Nomad Atacama Desert Trek planetary exploration
- Life in the Atacama Zoe rover navigation
- Mars CTX DTM artifacts and topographic accuracy
- Mars landing site multi-resolution terrain models
- Lascar volcano Chile Smithsonian
- Atacama Desert planetary analog review

This is not an exhaustive systematic review of
all site-specific scientific publications.

## 3. Novelty verdict

The Atacama Desert is already widely documented
as a planetary analog.

Rover navigation and autonomous field experiments
have been conducted there before FieldTwin.

Multi-resolution Mars topography analysis is
also established in published literature.

Therefore FieldTwin cannot claim:
- First identification of Atacama as a Mars analog.
- First use of Atacama for rover navigation.
- First terrain-based Mars landing-site assessment.
- A previously undiscovered analog at any pilot point.
- A validated new rover-testing methodology.

The project contribution can be described as
its own documented integration and exploratory
application of geographic screening, transparent
terrain comparisons, route feasibility and
scientific transfer limitations.

No claim of methodological priority is made.

## 4. Candidate-by-candidate classification

| Site | Classification | Evidence-based conclusion |
|---|---|---|
| PILOT_A | Insufficient evidence | Nondominated in tested physical comparisons; no independently supported novel-site or rover-use claim |
| PILOT_B | Insufficient evidence for novelty | Nondominated; selected for an illustrative route-planning example, not as a validated best analog |
| PILOT_C | Insufficient evidence | Nondominated; distinct site-specific novelty and suitability not established |
| PILOT_D | Insufficient evidence | Nondominated; robustness does not establish site suitability or priority |
| ARADS_PLAYA | Established regional analog context | NASA ARADS confirms Atacama field-testing precedent; exact match of this GIS point to a historical campaign footprint requires independent verification |
| LASCAR_CONTROL | Documented volcanic comparison/control | Rugged negative control in the selected DEM benchmark, not a generally unsuitable region or approved field-test site |

ARADS is not an independent positive label for
the specific DEM-based route-selection objective.

Láscar is an active volcano documented by
Smithsonian; the numerical negative-control role
does not provide field-access or safety approval.

Four pilot locations occupy Pareto Front 1 at
both tested analysis windows. No unique winner
may be inferred from their relative fronts.

## 5. Defensible candidate-specific use

Selected presentation case: PILOT_B.

Selection rationale:
The repository includes reproducible
DEM-scale route experiments for Pilot B,
alongside Mars, ARADS, and Láscar cases.

Pilot B is a demonstrator of the method,
not a scientifically certified superior analog.

The testable engineering question is:

Can a rover-route planning algorithm produce
different candidate paths when a DEM-derived
grade constraint is introduced, and how stable
are these numerical paths under assumed
elevation perturbations?

FieldTwin has evaluated this question at the
desktop DEM-grid level.

It has not established that a physical rover
can safely execute those paths.

## 6. Proposed future physical field experiment

This is a proposal only; no field rover experiment
has been performed by FieldTwin.

Before any deployment:

1. Confirm land access, permissions and safety.
2. Obtain an independent local terrain survey.
3. Characterize actual rocks, soil and obstacles.
4. Specify real rover geometry, traction and
   certified operating constraints.
5. Plan surveyed start/goal and trial corridors.
6. Compare planned and traversed paths.
7. Measure actual distance, grade, slip,
   energy, localization error and recoveries.
8. Test reproducibility across repeated trials.
9. Report differences between simulation and
   measured vehicle behavior.
10. Document which findings cannot transfer
    to Martian gravity and environmental factors.

No outcomes are predicted or invented here.

## 7. Physical baseline and uncertainty

Existing evidence:
- Real NASADEM Earth terrain.
- Provisional USGS CTX stereo-derived Mars DTM.
- 1000 m and 2000 m analysis windows.
- 100 m computational analysis grid.
- Three baseline descriptors: slope,
  local relief and detrended RMS roughness.
- Unweighted Pareto comparison.
- Four pilot candidates nondominated.
- ARADS and Láscar comparative controls.
- 60 DEM-level route searches.
- 4840 searches including synthetic elevation
  perturbation stress tests.

A shared 100 m grid does not imply identical
effective source resolution or DEM accuracy.

The assumed 3-degree and 10-degree grade limits
are not certified rover operating limits.

Hypothetical perturbations are not calibrated
probability estimates.

Mars CTX artifacts and independent elevation
quality remain unresolved.

## 8. ML scientific decision

ML-A:
Exploratory pattern discovery only; no validated
site-ranking benefit established.

ML-B V1:
NO-GO under its experiment.

ML-B V2:
NO-GO under the frozen prospective benchmark.
Random Forest pooled AP was 0.974571;
Logistic Regression pooled AP was 0.975984;
robust comparator pooled AP was 0.610942.

Three of four preregistered V2 acceptance gates
failed. The separate deterministic synthetic
missing-block screen detected 12/12 examples.

ML-B evaluates synthetic elevation anomalies,
not relative relevance of Earth analog sites.

Therefore ML-B AP must NOT be compared with
physical Pareto ranks as though these were
the same supervised task.

A validated ML-versus-Pareto site-ranking
benchmark with independently judged labels
has not been established.

No such superiority claim is retained.

No model_comparison.json is fabricated to
represent an experiment not performed.

The physical baseline remains FieldTwin's
primary scientific comparison method.

## 9. Evidence and limitations

- No independently validated positive terrain
  analog for the stated rover navigation task.
- No proven new site discovery.
- No unique recommended analog winner.
- No tested rover traction or physical mobility.
- No proof that the computational path is safe.
- No verified site-specific novelty for pilots.
- No verified field access or survey data.
- No resolved independent CTX accuracy estimate.
- No operational ML anomaly detection claim.

This is an evidence-limited scientific result.
The inability to support a stronger conclusion
is explicitly reported rather than concealed.

## 10. Presentation permissions

Permitted:
- Present four exploratory candidate sites.
- Explain Pareto nondominance without a winner.
- Present Pilot B as a route-testing example.
- Compare the known regional ARADS context.
- Explain Láscar's tested negative-control role.
- Show actual measured features and simulations.
- Display scientific provenance and uncertainty.
- Explain a proposed future field-test protocol.

Not permitted:
- Announce a unique or newly discovered analog.
- Declare Pilot B the best real-world field site.
- Claim a first-ever Atacama rover navigation use.
- Claim verified physical rover performance.
- Claim ML superiority or deployment reliability.
- Hide provisional terrain quality or missing data.

## 11. Phase 5 disposition

The scientific investigations are closed at
their currently supported evidence level.

Existing results are preserved, including
failed ML benchmarks and unresolved limitations.

The original goal of a uniquely validated
Earth-analog recommendation is NOT achieved.
This is an explicitly unmet research objective,
not a claimed success.

Further independent relevance labeling,
field verification or newly preregistered ML
research would constitute separate future work.

Phase 6 development is conditionally permitted
by docs/PROJECT_GATE_P1.md. This scientific
closeout does not itself certify submission
readiness or authorize unverified claims.

## 12. Internal evidence registry

- docs/PROJECT_GATE_P1.md
- docs/PHASE4_BASELINE_RESULTS.md
- docs/ANALOG_TRANSFER_MATRIX.md
- docs/ML_B_RESULTS.md
- docs/ML_B_FAILURE_ANALYSIS.md
- docs/ML_B_V2_PROTOCOL.md
- docs/ML_B_V2_FINAL_RESULTS.md
- docs/ML_B_V2_INDEPENDENT_AUDIT.json
- outputs/validated/terrain_baseline.json
- data/SOURCES.md
- data/SEARCH_SCOPE.md
