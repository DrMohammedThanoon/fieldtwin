
# FieldTwin — Website Design and User Experience

**Version:** 1.0  
**Project:** NASA Space Apps Challenge 2026  
**Execution Plan:** FieldTwin v6.2  
**Status:** Design specification; implementation pending.

## 1. Design Vision

FieldTwin is an interactive scientific decision-support application for discovering and evaluating Earth analog locations suitable for Mars rover mobility and navigation field-testing.

**Tagline:**
Find where Earth can test Mars — and prove where the analogy breaks.

The interface must transform scientific evidence into a clear, understandable experience for NASA Space Apps judges.

The website should answer five questions:

1. What Mars rover task are we trying to support?
2. Where and how did we search Earth?
3. What did the measured terrain comparisons show?
4. Where does the Earth–Mars analogy fail?
5. What rover test could be conducted at the recommended site?

The application must never substitute appearance for scientific evidence.

## 2. Design Principles

### Scientific credibility
Every important result must be linked to real data, documented methods, and appropriately qualified conclusions.

### Clear storytelling
The interface must guide judges from a specific Mars mission need to a defensible Earth field-test recommendation.

### Visual simplicity
Maps, comparisons, and scientific measurements take priority over decorative graphics.

### Interactive exploration
Users should be able to explore verified candidates, inspect measurements, and understand why one site was recommended.

### Transparent uncertainty
Missing evidence, limitations, and sensitivity must remain visible.

### Accessibility
The website must be readable, responsive, keyboard accessible, and usable without requiring an account.

### Reproducibility
The application must link to the source repository, data documentation, methods, and citations.

## 3. Information Architecture

The application contains four connected views:

1. Mission
2. Search
3. Comparison
4. Transfer / Rover Test

Navigation must preserve the logical scientific sequence.

The user should be able to move between views without losing the context of the selected Mars reference or Earth candidate.

The recommended demonstration follows:

Mission → Search → Comparison → Transfer / Rover Test

Desktop navigation may use a top navigation bar.

Mobile navigation must provide equivalent access using a responsive layout.

## 4. Screen 1 — Mission

### Objective

Explain the scientific question, Mars reference terrain, and rover capability that motivates the search for an Earth analog.

### Main components

**A. Mission introduction**
- FieldTwin name and tagline.
- Short explanation of the project.
- Clearly defined Mars rover mobility/navigation objective.

**B. Mars reference**
- Documented Mars region.
- Actual dataset or terrain imagery when available.
- Source identification.
- Spatial scale and elevation information.
- Relevant terrain characteristics.

**C. Engineering problem**
Explain which rover behavior or navigation limitation needs testing.

Examples of possible tasks, not predetermined project findings:
- Terrain traversability.
- Slope-related mobility.
- Navigation through rough terrain.
- Route planning under terrain constraints.

The team must select and document one primary task.

**D. Scientific approach**
Present a concise sequence:

Mars reference → Measured terrain features → Earth search → Candidate comparison → Rover field-test recommendation.

### Primary user action

**Explore Earth Candidates**

Navigates to the Search screen.

### Scientific constraints

Do not invent a Mars reference location.

Do not present a Mars image as an elevation model.

Do not display Mars coordinates as Earth GPS locations.

## 5. Screen 2 — Search

### Objective

Show where FieldTwin searched for suitable Earth analogs and how the candidate-selection process was performed.

### Main components

**A. Interactive Earth map**
- MapLibre GL JS.
- Real geographic search footprint.
- Verified Earth candidate locations.
- Known analog and negative control when appropriate.
- Scientific layer attribution.

**B. Search methodology panel**
- Search region definition.
- Dataset coverage.
- Terrain screening features.
- Candidate inclusion criteria.
- Exclusion criteria.
- Areas not searched.

**C. Candidate exploration**
A selected candidate may display:
- Verified location name or identifier.
- Geographic coordinates.
- Dataset coverage.
- Terrain descriptors.
- Data completeness.
- Scientific qualification or uncertainty.

**D. Search filters**
Filters may be implemented for:
- Candidate category.
- Data availability.
- Measured slope or relief ranges.
- Control or reference status.

Filters must operate only on verified, precomputed candidate data.

### Primary user action

**Compare Selected Candidate**

Navigates to the Comparison screen.

### Scientific constraints

Do not imply a global search if only one Earth region was analyzed.

Do not display fabricated candidates or coordinates.

Do not present unexplored locations as evaluated.

## 6. Screen 3 — Comparison

### Objective

Explain why candidate Earth locations are more or less suitable for the selected Mars rover-testing task.

### Main components

**A. Mars terrain reference**
- Measured terrain descriptors.
- Analysis units.
- Physical analysis scale.
- Data source and processing limitations.

**B. Earth candidate comparison**
- Selected Earth candidate.
- Documented known analog.
- Negative control.

**C. Terrain feature visualization**
Possible comparisons:
- Slope distributions.
- Local relief.
- Terrain roughness.
- Feature-normalized comparison profiles.

Use actual measurements and labeled units.

**D. Ranking evidence**
- Transparent physical-feature baseline.
- Documented ranking criteria.
- Missing-data treatment.
- Sensitivity or uncertainty indicators.

**E. AI/ML comparison — conditional**
Show ML results only when an actual model has been evaluated.

When ML is retained:
- Display its measured performance.
- Identify the evaluation protocol.
- Compare against the interpretable baseline.
- Explain uncertainty and limitations.

If ML does not demonstrate sufficient value, show the interpretable baseline and explain the decision.

### Primary user action

**Evaluate Analog Transfer**

Navigates to the Transfer / Rover Test screen.

### Scientific constraints

Do not invent similarity percentages.

Do not label subjective rankings as validated ground truth.

Do not display unmeasured AI accuracy or superiority claims.

Do not interpret ranking stability alone as proof of suitability.

## 7. Screen 4 — Transfer / Rover Test

### Objective

Translate the terrain comparison into a mission-useful field-test recommendation while making the limitations of the analogy explicit.

### Main components

**A. Recommended candidate**
- Verified location identifier.
- Supported suitability rationale.
- Key measured terrain similarities.
- Evidence and uncertainty.

**B. Analog Transfer Matrix**

Each property must be classified as:

- WORKS
- DOES NOT TRANSFER
- UNKNOWN

Properties may include:
- Slope and topographic relief.
- Terrain roughness.
- Surface material characteristics.
- Gravity.
- Atmospheric conditions.
- Radiation environment.
- Other mission-specific factors.

**C. Proposed rover field test**
Include:
- Test objective.
- Proposed site or bounded test area.
- Rover capability to evaluate.
- Experimental setup requirements.
- Proposed performance measurements.
- Scientific limitations.
- Requirements for future on-site verification.

**D. Evidence and references**
- NASA data sources.
- Relevant scientific literature.
- Methodology.
- Novelty audit.
- Reproducibility resources.

### Final user action

**View Evidence and Methods**

Provides access to the relevant documentation and public GitHub repository.

### Scientific constraints

Clearly distinguish:

1. Measurements already completed.
2. Scientific interpretations supported by those measurements.
3. Proposed future experiments.
4. Unknown or unverified conditions.

Do not present a proposed rover test as completed field validation.

## 7b. Visual system update

The four views are implemented in the SamaBeyond design system (Inter / JetBrains Mono, light default with dark toggle, orange `#ff8b5d` accent, flat square panels). This supersedes the palette in §8. All displayed numbers come from FieldTwin's validated baseline export.

## 8. Visual Design System

### General direction

Use a modern scientific and aerospace-inspired interface.

The website should appear credible, professional, and visually consistent.

### Suggested palette

- Deep navy: `#0B1220`
- Surface navy: `#152238`
- Mars accent: `#D97757`
- Earth accent: `#36A9AE`
- Text white: `#F8FAFC`
- Secondary text: `#94A3B8`

These colors are design choices, not scientific classifications.

### Typography

Use a clear, accessible sans-serif font.

Suggested:
- Inter.
- System UI fonts as a fallback.

### Layout

Desktop:
- Clear top navigation.
- Wide map and visualization areas.
- Supporting evidence panels.
- Consistent margins and readable text.

Mobile:
- Responsive layouts.
- No horizontal page overflow.
- Collapsible supporting information when appropriate.
- Accessible touch targets.

### Scientific graphics

All charts must:
- Display units.
- Identify the actual measured variables.
- Explain scale.
- Distinguish observations from derived quantities.
- Show uncertainty when available.
- Avoid misleading axis ranges.

Do not use decorative precision or unsupported scientific scores.

## 9. Mapping Requirements

Use MapLibre GL JS for Earth mapping.

Supported display elements:
- Earth basemap.
- Verified candidate points or polygons.
- Documented search boundaries.
- GeoJSON overlays.
- Map legend.
- Source attribution.

The basemap provider must permit the intended public usage.

Provide a fallback if external map tiles fail.

Mars should use an appropriate planetary image, raster visualization, or independent evidence panel.

Never interpret Mars planetary latitude/longitude as terrestrial GPS coordinates.

If future Mars spatial mapping is added, use correct planetary spatial references.

## 10. Data and Frontend Architecture

Scientific processing must remain independent of the user interface.

Data flow:

NASA Earth/Mars products
    ↓
Python scientific processing
    ↓
Validated features and comparisons
    ↓
Small JSON / GeoJSON outputs
    ↓
React + TypeScript frontend
    ↓
Interactive FieldTwin experience

The browser must not:
- Download large raw DEM files.
- Retrain scientific models.
- Silently regenerate unverified results.
- Claim analysis of unsampled locations.

Scientific results must originate from validated outputs.

## 11. Interactive Behavior

Required interactions:
- Navigate between all four screens.
- Select verified Earth candidates.
- Inspect source and terrain information.
- Compare measured candidate features.
- Review uncertainty and limitations.
- Navigate from a selected candidate to its transfer assessment.
- Access scientific citations and documentation.

Optional interactions:
- Feature visibility toggles.
- Candidate filters.
- Precomputed scenario comparisons.
- Transparent weight exploration.

If weights can change interactively, distinguish exploratory rankings from the validated baseline.

Do not imply that a new scientific analysis has been executed when the website only changes the visualization.

## 12. Loading, Missing-Data and Error States

The interface must explicitly handle:

**Loading**
Show an appropriate progress indicator while loading public assets.

**Missing data**
Explain that a feature or observation is unavailable rather than displaying a fabricated value.

**Unverified candidate**
State that scientific validation is incomplete.

**Map service unavailable**
Show a meaningful fallback view and retain access to candidate evidence.

**Scientific comparison unavailable**
Do not display a ranking until the required validated outputs exist.

## 13. Evidence and Citations

Each scientific result must have traceable supporting information.

Provide access to:
- Dataset names.
- Product or granule identifiers.
- NASA source URLs.
- Scientific methodology.
- Analysis scale and units.
- Model evaluation when applicable.
- Known limitations.
- Literature references.

The design should enable judges to distinguish observations, computed features, interpretations, and proposed tests.

## 14. Accessibility and Usability

Target recognized web accessibility best practices.

Requirements:
- Keyboard-operable navigation and controls.
- Visible keyboard focus.
- Readable text contrast.
- Semantic headings and buttons.
- Labels for interactive controls.
- Accessible chart explanations.
- Usable error messages.
- Responsive desktop and mobile layouts.
- Avoid relying on color alone to communicate scientific categories.

## 15. Demonstration Experience

A judge should be able to understand the entire scientific story in a short walkthrough.

Recommended sequence:

1. Understand the rover mission need.
2. Examine the documented Mars reference.
3. Open the Earth search region.
4. Explore verified candidates.
5. Compare the candidate, known analog, and control.
6. Examine actual terrain measurements and uncertainty.
7. Understand why the recommendation is defensible.
8. Review the Analog Transfer Matrix.
9. Understand the proposed rover field test.
10. Access source data, methods, and GitHub.

No registration or sign-in should be required.

## 16. Acceptance Criteria

The frontend design is complete when:

- [ ] Four connected views are implemented.
- [ ] Navigation functions correctly.
- [ ] All displayed scientific results come from validated sources.
- [ ] Mars and Earth spatial references remain distinct.
- [ ] The Earth map uses real geographic data.
- [ ] Candidate and control comparisons are understandable.
- [ ] Measurement units and uncertainty are visible.
- [ ] The selected candidate's evidence is traceable.
- [ ] Analog transfer limitations are explicit.
- [ ] Proposed experiments are not misrepresented as completed tests.
- [ ] The application is responsive.
- [ ] Keyboard navigation is functional.
- [ ] Error and missing-data states work.
- [ ] A public no-login deployment is available.
- [ ] The production build succeeds.
- [ ] Scientific citations and GitHub links are accessible.

## 17. References

NASA Space Apps Challenge:
https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=details

MapLibre GL JS:
https://maplibre.org/maplibre-gl-js/docs/

React:
https://react.dev/

Vite:
https://vite.dev/guide/

Web Accessibility Initiative:
https://www.w3.org/WAI/

---

**Design principle:** The best FieldTwin interface is the one that makes scientific evidence understandable, inspectable, and difficult to misinterpret.
