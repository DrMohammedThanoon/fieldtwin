
# FieldTwin — AI Agents and Team Collaboration

**Version:** 1.0
**Project:** NASA Space Apps Challenge 2026
**Execution Plan:** FieldTwin v6.2
**Status:** Active implementation instructions

## 1. Project Mission

FieldTwin identifies scientifically defensible Earth analog locations for Mars rover mobility and navigation field-testing.

The system compares real Earth and Mars terrain observations at compatible physical scales and recommends a location or mission-specific test application supported by reproducible evidence.

Project tagline:

"Find where Earth can test Mars — and prove where the analogy breaks."

All development must follow:
- `PRD.md` — product requirements and acceptance criteria.
- `DESIGN.md` — user experience and visualization design.
- `README.md` — installation, execution, and reproducibility.
- `FieldTwin_CrossPlatform_Execution_Plan_v6.2.md` — implementation phases and scientific gates.
- `AGENTS.md` — collaboration and AI-agent operating rules.

If documents conflict, stop and request a documented decision from the project lead. Official NASA competition rules take precedence over internal plans.

## 2. Core Scientific Principles

The following requirements are non-negotiable.

1. Never invent NASA data, measurements, coordinates, site rankings, model results, or validation metrics.
2. Use real, traceable NASA Earth and Mars datasets.
3. Record actual dataset and product identifiers.
4. Maintain correct planetary coordinate systems.
5. Compare terrain features at compatible effective physical scales.
6. Use an interpretable physical-feature baseline before evaluating ML.
7. Include a known analog and negative control.
8. Quantify uncertainty and identify scientific limitations.
9. Verify potential novelty through documented research.
10. Clearly explain which Mars conditions cannot be reproduced on Earth.
11. Never claim ML superiority without a valid measured benchmark.
12. Never describe a proposed rover experiment as a completed experiment.

A scientifically defensible small result is preferable to an unsupported large-scale claim.

## 3. AI Agent Operating Protocol

Every AI coding assistant must:

1. Read `AGENTS.md`, `PRD.md`, and the execution plan before implementing changes.
2. Identify the active phase and specific task.
3. Inspect existing files before modifying them.
4. Respect the mandatory repository architecture.
5. Give one implementation step at a time when guiding a human operator.
6. Provide commands appropriate to the user's actual operating system.
7. Explain expected results and pass/fail criteria.
8. Wait for actual command output before proceeding.
9. Diagnose failures before proposing additional changes.
10. Never claim a command, test, installation, or deployment succeeded without evidence.
11. Preserve working code and avoid unnecessary rewrites.
12. Never delete files, reset repositories, or force-push without explicit approval.
13. Never expose credentials or commit private configuration.
14. Keep scientific processing independent of the frontend.

AI-generated code is subject to the same testing and review requirements as human-written code.

## 4. Cross-Platform Requirements

Supported development environments:

- macOS Apple Silicon.
- macOS Intel.
- Windows Intel/AMD.
- Windows ARM where the selected dependencies support it.

Default technologies:

- VS Code.
- Git and GitHub.
- Miniforge / conda-forge.
- Python 3.12.
- NumPy, Pandas, SciPy.
- Rasterio, rioxarray, GeoPandas, Shapely, PyProj.
- scikit-learn.
- QGIS LTR.
- React, TypeScript, Vite.
- MapLibre GL JS.

Avoid mandatory dependencies on:
- Windows-only applications.
- Dedicated GPUs.
- Docker or database servers.
- Paid GIS services.
- ArcGIS Pro.

Esri is optional and must not become a required dependency.

Before any installation, inspect existing software and verify operating system, architecture, and permissions.

## 5. Repository Architecture

Preserve the following structure:

FieldTwin/
- PRD.md
- AGENTS.md
- DESIGN.md
- README.md
- .env.example
- .gitignore
- LICENSE
- environment.yml
- science/
- notebooks/
- data/
- gis/
- app/
- outputs/validated/
- tests/
- docs/
- .github/workflows/

Additional files may be created when technically justified.

Do not relocate or delete mandatory files without approval.

Large datasets must remain outside Git.

## 6. Scientific Development Workflow

Scientific work follows this sequence:

### Stage A — Data Verification

- Inspect official NASA challenge resources.
- Identify actual Earth and Mars products.
- Verify access and product metadata.
- Record data provenance.
- Confirm readable files.
- Document geographic search boundaries.

Required evidence:
- `data/SOURCES.md`
- `data/SEARCH_SCOPE.md`

### Stage B — Physical Terrain Analysis

- Verify elevation units and reference systems.
- Match effective physical analysis scales.
- Compute slope, relief, and roughness.
- Apply documented quality masks.
- Produce interpretable comparisons.

Primary modules:
- `science/sources.py`
- `science/terrain.py`
- `science/baseline.py`

### Stage C — Scientific Validation

- Evaluate known analog and negative control.
- Test sensitivity to resolution and feature selection.
- Assess uncertainty and ranking stability.
- Audit candidate novelty.
- Document Earth-to-Mars transfer limitations.

Required evidence:
- `docs/METHODS.md`
- `docs/VALIDATION.md`
- `docs/LIMITATIONS.md`
- `docs/NOVELTY_AUDIT.md`

### Stage D — AI/ML Evaluation

AI/ML is optional.

The interpretable physical-feature baseline must be established first.

Before evaluating an ML model, create:

`docs/MODEL_BENCHMARK.md`

Predeclare:
- Candidate universe.
- Independent reference relevance evidence.
- Geographic holdout strategy.
- Baseline and ML methods.
- Primary metric.
- Supporting metrics.
- Improvement threshold.
- Scientific failure conditions.

Store measured results in:

`outputs/validated/model_comparison.json`

Implement:

`tests/test_model_comparison.py`

If ML does not demonstrate sufficient measurable benefit, retain the simpler baseline and document the decision.

## 7. Blue Team / Red Team Review

Every major scientific or architectural decision must pass independent review.

### Blue Team Responsibilities

Develop the strongest feasible solution.

Evaluate:
- Scientific relevance.
- NASA dataset integration.
- Implementation feasibility.
- Measurable technical value.
- Reproducibility.
- Mission usefulness.
- Clarity for judges.

### Red Team Responsibilities

Challenge assumptions and identify failure modes.

Evaluate:
- Unsupported scientific claims.
- Incorrect terrain comparisons.
- Spatial resolution mismatches.
- Coordinate-system errors.
- Data leakage.
- Weak or missing controls.
- Unjustified ML complexity.
- Novelty claims without evidence.
- Misleading visualizations.
- Deployment or integration risks.

### Decision Categories

PASS:
Evidence supports the decision and relevant tests pass.

REVISE:
A correctable weakness remains.

BLOCK:
A critical scientific, security, or eligibility requirement is not satisfied.

A BLOCK decision prevents the affected result or feature from being presented as validated.

## 8. Team Responsibilities

### Dr. Mohammed Ibrahim Thanoon
Scientific and AI/ML lead.

Responsibilities:
- Scientific methodology.
- Physical baseline and ML evaluation oversight.
- Research validity.
- Final scientific approval.

### Abdulrahman Jaber Alabdali
GIS and remote sensing.

Responsibilities:
- NASA Earth and Mars data acquisition.
- Geospatial metadata and CRS checks.
- QGIS verification.
- Terrain data quality.

### Abdulrahman Alazori
Frontend, integration, and GitHub.

Responsibilities:
- React application.
- MapLibre integration.
- Scientific output integration.
- Repository collaboration.
- Public deployment.

### Abdullah Almutiri
Data engineering and testing.

Responsibilities:
- Data preparation.
- Processing scripts.
- Automated tests.
- Reproducibility checks.

### Nouf Alzahrani
Scientific interpretation.

Responsibilities:
- Physical plausibility.
- Terrain comparison limitations.
- Uncertainty.
- Earth-to-Mars transfer evaluation.

### Hafsa
Research evidence and presentation.

Responsibilities:
- Literature and novelty audit.
- References.
- Scientific storytelling.
- Demonstration and submission preparation.

Responsibilities are provisional and may be updated after confirming each member's skills.

## 9. GitHub Collaboration Rules

Each task should have a GitHub Issue specifying:
- Owner.
- Objective.
- Input.
- Expected artifact.
- Verification method.
- Fallback.

Use feature branches for implementation.

Normal workflow:

1. Synchronize the local main branch.
2. Create a task-specific feature branch.
3. Implement only the assigned changes.
4. Run relevant tests.
5. Inspect modified files.
6. Confirm no credentials or large datasets are staged.
7. Commit meaningful changes.
8. Push the feature branch.
9. Open a Pull Request.
10. Request at least one independent reviewer.
11. Merge only after passing the required checks.

Never force-push main.

Do not rewrite another member's work without coordination.

Every implementation phase must be version-controlled and reviewed.

## 10. Frontend Development Rules

The application must provide four connected views:

1. Mission.
2. Search.
3. Comparison.
4. Transfer / Rover Test.

Frontend requirements:

- Display only verified scientific results.
- Cite data and scientific claims.
- Use correct units.
- Distinguish measured results from interpretations.
- Show missing data and uncertainty.
- Keep Earth and Mars coordinate systems separate.
- Avoid displaying Mars coordinates on an Earth basemap.
- Avoid loading large DEMs into the browser.
- Use validated JSON or GeoJSON outputs.
- Support desktop and mobile layouts.
- Provide public access without authentication.

Do not create simulated scientific measurements to make the interface appear complete.

Temporary illustrative UI content must be explicitly labeled and must not be presented as real findings.

## 11. Security and Data Protection

Never commit:
- Passwords.
- API tokens.
- Private keys.
- Personal credentials.
- Local `.env` files.
- Restricted datasets without permission.
- Large raw terrain rasters.

Use `.env.example` to document configuration names only.

Avoid destructive terminal operations.

Review Git changes before staging and committing.

Use official installation sources and documented dependencies.

## 12. Definition of Done

A task is complete only when:

- The required artifact exists.
- Its location matches the repository architecture.
- Its functionality or scientific content is verified.
- Applicable tests pass.
- Source evidence is recorded.
- Relevant limitations are documented.
- No secrets or inappropriate large files are included.
- The change is committed to a feature branch.
- The Pull Request has been reviewed and merged when required.

A feature must not be marked complete merely because its code was generated.

## 13. Final Scientific and Submission Gate

Before submission, verify:

- NASA data eligibility.
- Actual Earth and Mars measurements.
- Reproducible physical-feature analysis.
- Known analog and negative control.
- Scientific uncertainty.
- ML evidence if ML is retained.
- Novelty audit.
- Analog Transfer Matrix.
- Proposed rover test.
- Working four-view public application.
- No-login public demonstration.
- GitHub repository and reproducibility.
- Scientific citations and limitations.
- Compliance with official 2026 competition rules.

The team must prefer validated evidence over visual complexity.

---

**Operating principle:** Every result must be traceable, every important claim must be defensible, and every implementation phase must be verifiable.
