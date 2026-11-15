
# FieldTwin

### Find where Earth can test Mars — and prove where the analogy breaks.

**NASA Space Apps Challenge 2026**

**Challenge:** [Identify Earth Locations that Analog the Permanent Moon Base Locations and Mars](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=details)

**Status:** Scientific baseline and ML experiments completed; evidence-limited Phase 5 closeout recorded; frontend not yet implemented.

## 1. Overview

FieldTwin is a scientific decision-support system that investigates real Earth locations as analog field-testing sites for Mars rover mobility and navigation.

Rather than choosing Earth locations solely because they resemble Mars visually, FieldTwin uses documented Earth and Martian terrain data to evaluate physical terrain characteristics at compatible spatial scales.

The project aims to identify one defensible Earth candidate or mission-specific analog use and propose a practical rover field-testing application.

FieldTwin explicitly identifies the limitations of Earth–Mars comparisons.

## 2. Research Question

Which documented Earth location provides terrain characteristics useful for testing a specific Mars rover mobility or navigation capability, and which physical and environmental differences limit the validity of that analog?

## 3. Scientific Approach

The intended workflow is:

1. Identify a documented Mars terrain reference.
2. Define a specific rover testing requirement.
3. Establish a bounded Earth search region.
4. Obtain traceable NASA Earth and Mars data.
5. Verify data quality, units, and spatial references.
6. Calculate comparable terrain descriptors.
7. Establish an interpretable physical-feature baseline.
8. Evaluate candidates against a known analog and negative control.
9. Assess uncertainty and ranking robustness.
10. Evaluate optional ML against the baseline.
11. Investigate novelty and prior analog uses.
12. Recommend a defensible candidate and proposed rover field test.

The project does not claim a completed discovery or validated result until the required measurements and evaluations have been performed.

## 4. Application Experience

The proposed public website contains four connected views.

### Mission

Introduces the Mars reference, rover engineering problem, and scientific objective.

### Search

Displays the documented Earth search region, verified candidates, inclusion criteria, and exclusions.

### Comparison

Presents measured terrain comparisons, the known analog, negative control, uncertainty, and interpretable ranking results.

### Transfer / Rover Test

Explains which conditions transfer between Earth and Mars, which do not, and what rover experiment could be conducted.

See `DESIGN.md` for the complete interface specification.

## 5. Technology Stack

| Component | Technology |
|---|---|
| Editor | Visual Studio Code |
| Version control | Git and GitHub |
| Python environment | Miniforge / conda-forge |
| Scientific language | Python 3.12 |
| Numerical analysis | NumPy, Pandas, SciPy |
| Geospatial processing | Rasterio, rioxarray, GeoPandas, Shapely, PyProj |
| Machine learning | scikit-learn, if scientifically justified |
| GIS inspection | QGIS LTR |
| Frontend | React, TypeScript, Vite |
| Interactive maps | MapLibre GL JS |
| Deployment | GitHub Pages or Vercel |
| Optional GIS services | Esri, if access is confirmed |

No paid GIS subscription, dedicated GPU, Docker, or Windows-only application is required for the default workflow.

## 6. Repository Structure

```text
FieldTwin/
├── PRD.md
├── AGENTS.md
├── DESIGN.md
├── README.md
├── .env.example
├── .gitignore
├── LICENSE
├── environment.yml
├── science/
│   ├── sources.py
│   ├── terrain.py
│   ├── baseline.py
│   ├── model.py
│   └── evaluate.py
├── notebooks/
├── data/
│   ├── SOURCES.md
│   ├── SEARCH_SCOPE.md
│   ├── raw/
│   └── processed/
├── gis/
├── app/
├── outputs/
│   └── validated/
├── tests/
├── docs/
└── .github/
    └── workflows/
```

This is the required target architecture. Not all listed files have been implemented yet.

## 7. Development Environment

The project supports:

- macOS Apple Silicon.
- macOS Intel.
- Windows Intel/AMD.
- Windows ARM where required dependencies are supported.

### macOS setup

Install or verify:

1. Visual Studio Code.
2. Git and optional GitHub CLI.
3. Miniforge matching the CPU architecture.
4. QGIS LTR.
5. Node.js LTS and npm.
6. VS Code extensions: Python, Pylance, Jupyter, ESLint, and Prettier.

Apple Silicon users must use the appropriate ARM64 installer.

Official installers:

- VS Code: https://code.visualstudio.com/download
- Git: https://git-scm.com/downloads
- GitHub CLI: https://cli.github.com/
- Miniforge: https://conda-forge.org/download/
- QGIS: https://qgis.org/download/
- Node.js: https://nodejs.org/en/download

### Windows setup

Install the same supported tools using their Windows installers.

For Miniforge:

- Use the installer matching Windows architecture.
- Run Conda commands initially in Miniforge Prompt.
- Verify the platform and environment before installing scientific dependencies.

Do not mix Windows PowerShell and macOS shell commands.

## 8. Scientific Python Environment

The project uses an isolated Conda environment named `fieldtwin`.

After `environment.yml` is created and reviewed, execute from the repository root:

```bash
conda env create -f environment.yml
conda activate fieldtwin
```

Verify the environment:

```bash
python --version
python -c "import numpy, pandas, scipy, sklearn, rasterio, geopandas; print('FIELDTWIN_SCIENCE_OK')"
```

Expected Python version: 3.12.x.

Expected successful import message:

```text
FIELDTWIN_SCIENCE_OK
```

These commands are setup and reproducibility instructions. The scientific environment was created and verified during Phase 2; independent fresh-clone verification remains outstanding.

## 9. Scientific Tests

Once the scientific modules and tests exist, execute:

```bash
python -m pytest -q
```

For the optional ML benchmark, after its test file exists:

```bash
python -m pytest -q tests/test_model_comparison.py
```

Do not report tests as passed until they have actually executed successfully.

## 10. Frontend Development

The Phase 6 scientific frontend is in `app/`:

```bash
cd app
npm ci
npm run dev
```

The development server will display its local address.

To verify production readiness:

```bash
npm run build
```

`package-lock.json` is committed for reproducible dependency installation. See `app/README.md` for the exact evidence inputs, map fallback, and scientific limits. A public deployment has not yet been verified.

## 11. Scientific Data Sources

Primary official data sources:

### Mars

NASA Planetary Data System:

https://pds.nasa.gov/

MOLA terrain context:

https://pds-geosciences.wustl.edu/missions/mgs/mola.html

Potential CTX-derived digital terrain models:

https://stac.astrogeology.usgs.gov/docs/data/mars/ctxdtms/

### Earth

NASA Earthdata Search:

https://search.earthdata.nasa.gov/

NASADEM_HGT.001:

https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_HGT.001

NASADEM_SC.001:

https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_SC.001

The team must verify actual products and downloaded granules before analysis.

Dataset provenance will be documented in `data/SOURCES.md`.

Search scope and exclusions will be documented in `data/SEARCH_SCOPE.md`.

## 12. Data Management

Large raw or processed datasets must not be committed to Git.

Expected directories:

- `data/raw/` — original downloaded datasets.
- `data/processed/` — intermediate scientific data.
- `outputs/validated/` — small verified outputs suitable for sharing.

Track dataset identifiers, source URLs, processing details, and relevant licenses.

The browser consumes verified JSON/GeoJSON results instead of downloading raw elevation models.

Keep Earth and Mars planetary coordinate systems separate.

## 13. ML Evaluation Policy

An interpretable physical-feature baseline is mandatory.

Machine learning is optional and must demonstrate a measurable benefit over the baseline.

Before ML evaluation, create:

`docs/MODEL_BENCHMARK.md`

Record actual comparison results in:

`outputs/validated/model_comparison.json`

If ML does not satisfy the predeclared scientific evaluation criteria, retain the baseline and report the outcome transparently.

## 14. Collaboration

FieldTwin is developed by a six-person team.

Each implementation task should have:

- A GitHub Issue.
- An assigned owner.
- A defined output.
- Verification criteria.
- A feature branch.
- A Pull Request.
- At least one independent reviewer.

No team member should force-push the main branch or commit credentials.

See `AGENTS.md` for collaboration and Blue Team/Red Team review procedures.

## 15. Scientific Reproducibility

Scientific results must be traceable to:

- Actual NASA dataset and product identifiers.
- Documented geographic search areas.
- Processing methods and software versions.
- Correct units and spatial references.
- Automated tests.
- Known analog and negative control.
- Uncertainty and robustness evaluation.
- Scientific limitations and novelty audit.

A public ranking alone is not sufficient evidence of analog suitability.

## 16. Public Demonstration

The final application must:

1. Be accessible without login.
2. Present all four connected views.
3. Display actual verified results.
4. Include scientific citations.
5. Explain limitations.
6. Link to reproducibility documentation.
7. Work on desktop and mobile.
8. Provide a reasonable fallback if external map services fail.

**Public demo URL:** Not deployed yet.

**Submission version:** Not released yet.

Actual URLs and release identifiers will be recorded after verification.

## 17. Security

Never commit:

- Passwords or API tokens.
- Private SSH keys.
- Local `.env` files.
- Confidential information.
- Restricted imagery without authorization.
- Large raw terrain datasets.

Use `.env.example` for configuration documentation only.

## 18. Project Documentation

- `PRD.md` — requirements and scientific acceptance criteria.
- `AGENTS.md` — collaboration and AI-agent operating rules.
- `DESIGN.md` — frontend experience and visualization requirements.
- `FieldTwin_CrossPlatform_Execution_Plan_v6.2.md` — implementation sequence.
- `docs/METHODS.md` — scientific methodology, when completed.
- `docs/VALIDATION.md` — evaluation evidence, when completed.
- `docs/LIMITATIONS.md` — scientific limitations, when completed.
- `docs/NOVELTY_AUDIT.md` — prior analog research, when completed.
- `docs/AI_USAGE.md` — AI assistance disclosure, when completed.
- `docs/REFERENCES.md` — supporting references, when completed.
- `docs/DEMO.md` — public demonstration guide, when completed.

## 19. Official References

NASA Space Apps Challenge:
https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=details

Official Challenge Resources:
https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=resources

NASA PDS:
https://pds.nasa.gov/

NASA Earthdata:
https://www.earthdata.nasa.gov/

GitHub Documentation:
https://docs.github.com/

QGIS Documentation:
https://docs.qgis.org/

MapLibre Documentation:
https://maplibre.org/maplibre-gl-js/docs/

---

**FieldTwin principle:** Scientific evidence first. Reproducible comparisons second. Clear presentation throughout.
