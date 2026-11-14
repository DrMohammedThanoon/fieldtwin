# FIELDTWIN — Cross-Platform, Step-by-Step Execution Plan

**Version 6.2 | 13 November 2026 | Standalone | Owner: SamaBeyond / six-person team**  
**Target:** NASA Space Apps Challenge 2026 — Riyadh local event  
**Challenge:** [Identify Earth Locations that Analog the Permanent Moon Base Locations and Mars](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=details)  
**Challenge-author introduction:** https://www.youtube.com/watch?v=Qiz_Pny-xjo  
**Tagline:** *Find where Earth can test Mars — and prove where the analogy breaks.*

> **How to use:** Attach this document to a fresh AI chat/agent or give it to any teammate. The agent must guide the human through **one verified action at a time**, identifying macOS/Windows first, showing the exact command/menu, asking for its output, fixing errors, and **never assuming success**. Follow the companion independent starter prompt when available. No Esri license, local GPU, Windows-only software, or prior chat is required.
>
> **Timing:** This plan has **no artificial timebox or date-dependent implementation sequence**. Environment familiarization, study and planning can begin immediately. However, the official NASA event opens project submission on **14 November 2026, 09:00 local time**; check the current participation rules regarding when actual competition implementation may start, and comply with them. Do not represent the absence of a schedule here as permission to break hackathon rules.

## A. Challenge, product and scientific winning hypothesis

NASA seeks **one or more Earth locations/processes** useful for Moon/Mars exploration analogs, supported by actual NASA/partner observations. Explain **what matches, how well, where the analogy fails**, and how a future exploration team would use the site. A credible *single Mars case* is allowed; both planets are not mandatory. The challenge author explicitly encourages a **surprising site, previously under-recognized mission use, or new comparison method**. Appearance alone is not evidence. No Earth site reproduces Mars gravity, atmosphere or radiation.

**Problem:** Roboticists often choose familiar deserts or volcanic landscapes by resemblance instead of measuring whether the terrain can exercise a *specific* rover navigation/mobility method.

**FieldTwin:** Choose a real Martian regional terrain reference; specify a rover-mobility/navigation field-test task; search a documented Earth region; compare physically meaningful terrain descriptors at **matched effective spatial resolution**; rank candidate sites against a known analog and a negative control; report uncertainty and non-transferable conditions; output **one defensible candidate plus a reproducible field-test proposal**. The preferred NASA-to-NASA source path is **Planetary Data System (PDS) → Mars** and **Earthdata Search → Earth**, both explicitly listed by the challenge.

**The five judge-visible answers:** (1) What Mars task? (2) Where/how did we search Earth? (3) What did the measurements show? (4) What *doesn't* transfer? (5) What real rover test would this location support?

**Differentiator, not a promise:** A reproducible, auditable *site-discovery procedure* and an **Analog Transfer Matrix**. Never claim a completely new site without a documented literature and known-analog search. A new *mission-specific use of an existing site* can be an honest and valuable result.

**Success criteria:** Working public interactive map + Mars evidence panel + ranked Earth candidates + real measurements and source IDs + known/negative controls + robustness analysis + limitations/transfer card + reproducible GitHub repository + concise demonstration. The build must still work without Esri.

## B. Primary stack — all operating systems

| Layer | Default | Purpose | Needed where |
|---|---|---|---|
| Editor | **VS Code** | Write, debug, inspect results | macOS / Windows |
| Versioning | **Git + GitHub + optional GitHub CLI (`gh`)** | Team branches, PRs, Issues, releases | macOS / Windows + web |
| Python environment | **Miniforge (conda-forge), Python 3.12** | Stable geospatial dependencies | Each member doing analysis |
| Scientific processing | **NumPy, Pandas, SciPy, xarray, Rasterio, rioxarray, GeoPandas, Shapely, PyProj, PyArrow** | Planetary/Earth terrain preparation, statistics, spatial outputs | Python environment |
| AI/ML | **scikit-learn** | Interpretable baseline, clustering/retrieval, measured comparisons | Python environment |
| GIS validation | **QGIS LTR** | Inspect DEMs, masks, projections, outputs | Standalone macOS / Windows app |
| Frontend | **React + TypeScript + Vite** | Four-view exploration interface | Node.js + VS Code |
| Mapping | **MapLibre GL JS** | Earth candidate map, GeoJSON overlays | Browser/frontend |
| Data contract | **GeoTIFF → feature tables / GeoJSON / JSON** | Keep big rasters out of frontend | Files, not separate applications |
| Public deployment | **GitHub Pages or Vercel** | Anonymous judge-facing app | Cloud |
| Optional cloud | **Esri ArcGIS Online/Notebooks/Experience Builder** | Fast GIS services *if confirmed* | Browser; never critical path |

**M1, 8-GB RAM and ordinary Windows laptops:** Suitable for a *small, region-focused dataset* and classical ML. Avoid global DEMs in memory, unnecessary GPU deep learning, Docker/PostGIS/ArcGIS Pro as prerequisites. Use tiled/windowed raster reads and downsample for display, retaining source granules and original analysis resolution. For very large rasters, use a stronger teammate machine or authorized cloud compute, but keep scripts identical. Mars must retain its planetary reference system; don't display Mars lat/long on an Earth basemap.

### Official installers / accounts (do not install duplicates)

- VS Code: https://code.visualstudio.com/download ; [mac](https://code.visualstudio.com/docs/setup/mac) / [Windows](https://code.visualstudio.com/docs/setup/windows)
- Git: https://git-scm.com/downloads ; GitHub account: https://github.com/ ; optional CLI: https://cli.github.com/
- Miniforge: https://conda-forge.org/download/ — choose **MacOSX-arm64** for Apple M1, **MacOSX-x86_64** for Intel Mac, **Windows-x86_64** for conventional Intel/AMD PCs, or the supported Windows ARM64 installer where applicable. Windows users initially run the **Miniforge Prompt**.
- QGIS long-term release: https://qgis.org/download/ (prefer 3.44 LTR at this writing; re-check)
- Node.js stable LTS: https://nodejs.org/en/download ; Vite: https://vite.dev/guide/
- NASA accounts if required for data: https://urs.earthdata.nasa.gov/ ; NASA PDS: https://pds.nasa.gov/ (many public datasets don't require credentials)
- Vercel optional: https://vercel.com/ ; MapLibre: https://maplibre.org/maplibre-gl-js/docs/

**Credentials:** GitHub login/2FA and repository permission; optional Earthdata Login for protected downloads; optional Vercel access; optional Esri credentials only when actually issued. **Never paste passwords, tokens, private SSH keys, .env contents or personal keys into an AI chat or repository.** Use browser/device-code authorization or OS credential manager. If a NASA source is public, do not invent a token requirement.

## C. Agent/operator interaction contract — REQUIRED

For **every step**, the agent must produce only:

1. **Step ID, goal, machine/shell** (macOS zsh, Windows PowerShell or Windows Miniforge Prompt).
2. **One command or one short dependent command block**, OR an exact GUI path. Never both OS commands mixed without labels.
3. **Expected output** and **pass criterion**.
4. **Safety/credentials note** if relevant.
5. **STOP:** ask operator to paste the command output or describe the screenshot/error (redact secrets). **Do not proceed** until verified.

If it fails: classify (command absent, wrong architecture/PATH, permissions, network, package conflict, data/CRS, git auth, deployment); diagnose with the **smallest safe check**; provide a specific fix; rerun the failed step; no destructive cleanup without explicit approval. At the end of each successful **phase**, show `git status`, run appropriate tests, commit with the phase ID, push an assigned branch, open a Pull Request and request a second reviewer. A browser-only agent must give instructions instead of claiming it executed them.

### Phase 0 — discover the machine; install only missing tools

**0.1 OS/architecture/RAM/disk inspection** (run the correct block, then send its actual output):

macOS Terminal (zsh):
```bash
uname -m
sw_vers -productVersion
sysctl -n hw.memsize
df -h .
```
Windows PowerShell:
```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object Caption,OSArchitecture
Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory
Get-PSDrive -PSProvider FileSystem
```
**Pass:** exact OS/architecture/available disk known. For >8 GB working rasters favor a machine with ample RAM and disk. Do not guess capacity.

**0.2 Check existing tools** (macOS zsh and Windows PowerShell; use the same read-only commands):
```text
git --version
gh --version
code --version
conda --version
node --version
npm --version
```
**Pass:** record working versions and missing commands. `code` not found may only mean the VS Code command-line launcher is not in PATH. `conda` not found on Windows PowerShell does not mean Miniforge is missing—check **Miniforge Prompt**. Install **only** missing tools using the linked official installers and restart the shell. For each missing item, the agent gives one installer/verification step and waits. A local Python installation is **required for the default local science route**; only an explicitly chosen cloud/notebook route can avoid it. Node is needed only by frontend developers.

**0.3 VS Code extensions** (Extensions → search names): Python, Pylance, Jupyter, ESLint, Prettier. Optional: GitLens. **Pass:** interpreter can be selected in the editor after Phase 2.

### Phase 1 — GitHub, team permissions and the mandatory scaffold

**1.1 Authenticate GitHub CLI** (after Git/GitHub CLI are installed):
```bash
gh auth login
```
Choose GitHub.com → HTTPS → authenticate through browser; when asked, allow Git credential helper. **Do not print `gh auth token`.** Verify with `gh auth status`. If `gh` isn't available, use GitHub web UI and Git Credential Manager. Confirm organization/repo ownership and six invited collaborators (GitHub repository → Settings → Collaborators/Teams). A private repo can be made public for judging after rights/security review.

**1.2 Create an empty repository** in a writable folder:

macOS zsh:
```bash
mkdir -p ~/Projects/fieldtwin
cd ~/Projects/fieldtwin
git init -b main
```
Windows PowerShell:
```powershell
New-Item -ItemType Directory -Force -Path "$HOME\Projects\fieldtwin"
Set-Location "$HOME\Projects\fieldtwin"
git init -b main
```
**Pass:** `git status` shows branch `main`, no existing conflicting repository. If six members join later, they `git clone <ACTUAL_REPO_URL>` instead of running `git init` again.

**1.3 Create EXACT mandatory architecture** using VS Code Explorer → New File/New Folder (cross-platform, avoids fragile shell quoting). Agent must verify the resulting tree against:

```text
fieldtwin/
├── PRD.md                    # product scope; measurable acceptance gates
├── AGENTS.md                 # agent rules, ownership, stop-and-confirm protocol
├── DESIGN.md                 # four-screen UX, scientific visual rules
├── README.md                 # setup, run, test, reproduction, public demo
├── .env.example              # names of optional variables, never secrets
├── .gitignore
├── LICENSE                   # appropriate license, check third-party material
├── environment.yml          # cross-OS conda dependencies
├── science/
│   ├── __init__.py
│   ├── sources.py
│   ├── terrain.py
│   ├── baseline.py
│   ├── model.py
│   └── evaluate.py
├── notebooks/
├── data/
│   ├── SOURCES.md            # actual source/granule IDs + official eligibility
│   ├── SEARCH_SCOPE.md       # all areas searched, exclusions, resolution
│   ├── raw/                  # NOT committed
│   └── processed/            # large files NOT committed
├── app/                      # React/Vite/MapLibre frontend
├── gis/
│   └── layer_manifest.json   # IDs/URL/rights for optional Esri or tile sources
├── outputs/
│   └── validated/            # small distributable cards/GeoJSON/charts
├── tests/
├── docs/
│   ├── METHODS.md
│   ├── VALIDATION.md
│   ├── LIMITATIONS.md
│   ├── NOVELTY_AUDIT.md
│   ├── AI_USAGE.md
│   ├── REFERENCES.md
│   └── DEMO.md
└── .github/workflows/        # add CI after basic tests are green
```

Git does not track empty directories; put a `.gitkeep` in required empty directories. Agent must create concise content for all five mandatory root files; do not leave them as empty placeholders. `.env.example` may say `# no secrets or API keys required for open data` until necessary. Add safe `.gitignore` exclusions for `.env`, `data/raw/`, `data/processed/`, `node_modules/`, `dist/`, conda caches, `.ipynb_checkpoints/`, binary DEMs and secrets. **Do not ignore** `.env.example`, small validated assets, source manifests or Python source. Record machine instructions in README.

**1.4 Git initial checkpoint** (after scaffold exists):
```bash
git status
git add PRD.md AGENTS.md DESIGN.md README.md .env.example .gitignore LICENSE environment.yml science notebooks data app gis outputs tests docs .github
git commit -m "phase-01: scaffold mandatory FieldTwin repository"
gh repo create fieldtwin --private --source=. --remote=origin --push
```
Use your real chosen repository name/owner, not an invented URL. `gh repo create` will offer account/organization selection; approve only after verifying. If repo exists, instead add the actual remote (`git remote add origin <ACTUAL_URL>`) and `git push -u origin main`. **Pass:** repo opens in browser with all five root files and `git log -1 --oneline` matches the commit. Configure branch protection/PR review as allowed, then invite six collaborators.

**Every following work item:** `git switch main` → `git pull --ff-only` → `git switch -c feat/<specific-task>` → edit/test → `git add <specific files>` → `git commit -m "phase-XX: <verified result>"` → `git push -u origin <branch>` → `gh pr create --fill` → independent review/checks → merge → `git pull --ff-only`. Avoid six people editing the same data notebook. Use GitHub Issues with **owner, input, test, artifact, fallback**. Never force-push main.

### Phase 2 — install and verify portable Python environment

**2.1** Install Miniforge for your actual CPU/OS from the official downloads. On Windows prefer **Miniforge Prompt** for commands; do not add competing Python distributions to PATH blindly. On macOS use Terminal. Check `conda --version` and `conda info` (platform should fit `osx-arm64`, `osx-64`, `win-64`, or `win-arm64` as relevant). **Stop and show error before proceeding if unavailable.**

**2.2** Agent writes this versioned `environment.yml` at repository root:
```yaml
name: fieldtwin
channels:
  - conda-forge
dependencies:
  - python=3.12
  - numpy
  - pandas
  - scipy
  - scikit-learn
  - rasterio
  - rioxarray
  - xarray
  - geopandas
  - shapely
  - pyproj
  - pyarrow
  - matplotlib
  - jupyterlab
  - pytest
```
**2.3** Run in Miniforge Prompt or a shell with conda:
```bash
conda env create -f environment.yml
conda activate fieldtwin
python -c "import numpy, pandas, scipy, sklearn, rasterio, geopandas; print('FIELDTWIN_SCIENCE_OK')"
```
If environment already exists, use `conda env update -n fieldtwin -f environment.yml --prune` **only after inspecting what it would change**; avoid deleting packages without approval. **Pass:** printout exactly includes `FIELDTWIN_SCIENCE_OK`. Then select `fieldtwin` interpreter in VS Code. Run `python -m pytest -q` once the smoke tests exist. Stage a `feat/science-env` PR and record `conda list --explicit` output in a *local* diagnostics file if package conflicts arise; do not commit cross-OS exact-build export as universal environment.

### Phase 3 — NASA resources and scientifically admissible data

**3.1 Official-source gate.** Open the [official NASA Challenge Resources tab](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=resources), read the 2026 guide, and record at least **one actually used NASA dataset from a source on that page** for Global Awards eligibility [NASA GO-team guidance](https://github.com/nasa/spaceapps/discussions/1849). The **11 official entries** are NASA Earthdata Search, NASA Worldview, **NASA Planetary Data System (PDS)**, LRO, LRO Diviner, CSA RADARSAT Constellation, RADARSAT-1, the CSA SAR Python Tutorial, Copernicus Data Space, ESA Open Science Catalogue, and JAXA G-Portal. These are *portals, instrument archives and a tutorial*, not eleven downloadable datasets. The **primary two for FieldTwin** are **PDS + Earthdata**. Optional sources must be licensed and technically justified. If the Resources tab is inaccessible, use a saved official page copy, mark eligibility **unverified until confirmed**, and do not invent a matching dataset.

**3.2 Mars-side sequence (PDS first).** Use [PDS MOLA](https://pds-geosciences.wustl.edu/missions/mgs/mola.html) / [MOLA MEGDRs](https://pds-geosciences.wustl.edu/missions/mgs/megdr.html) to screen the planet and select a Mars target region. For regional terrain measurements, seek an **actual, downloadable CTX stereo-derived digital terrain model (DTM/DEM)** through [PDS MRO archives](https://pds-geosciences.wustl.edu/missions/mro/default.htm), [PDS paired CTX/HiRISE DTM bundle](https://doi.org/10.17189/ervc-mr85), or [USGS Astrogeology CTX DTMs](https://stac.astrogeology.usgs.gov/docs/data/mars/ctxdtms/). **CTX imagery (~6 m pixels) is not itself an elevation model; USGS CTX DTMs (~20 m posting) are derived products and must retain both image-source and processing provenance.** Do not assume a ready-made DTM exists for any particular target. Choose a different real region/product if needed; do not make creating a DTM from raw stereo pairs a mandatory 48-hour task.

**3.3 Earth-side sequence (Earthdata first).** Use [NASA Earthdata Search](https://search.earthdata.nasa.gov/) to identify **NASADEM_HGT.001** (measured/merged elevation, [catalog DOI](https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_HGT.001)) for a bounded Earth search footprint. Use **NASADEM_SC.001** (precomputed slope/aspect/curvature, [catalog DOI](https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_SC.001)) as a supporting product or cross-check. Recompute *final comparative* terrain descriptors at matching **effective physical scales**, rather than directly comparing precomputed Earth slope pixels with a Martian DTM at different scales. Copernicus GLO-30/Sentinel-2 and Worldview are **optional** screening or corroboration resources, not required replacements for NASA products.

**3.4 Data contract and verification.** In `data/SOURCES.md`, record the exact NASA collection/product name **plus the actual downloaded granule or PDS product ID**, URL/DOI, originating instrument/mission, processing provenance, access date, body, geographic footprint, planetary reference/CRS, horizontal spacing, vertical datum and units, no-data/quality mask, citation, license and checksum when feasible. In `data/SEARCH_SCOPE.md`, record candidate sampling, exclusions, known analog and negative control, geographic limits, and searched/not-searched areas. Store bulky raw files outside Git. Prove each Earth and Mars file is readable using `rasterio.open(...).profile` and `bounds` **only if the file format is supported**; otherwise first use the documented PDS conversion procedure and verify its metadata. Do not invent pixel values or claim data availability before download. **Pass:** both official NASA portals documented, exact Earth/Mars usable products downloaded and opened, metadata/units checked, and eligibility verified. Commit manifests/tests in a dedicated `feat/nasa-pds-earthdata` branch and PR before proceeding.

### Phase 4 — feature extraction and numerical baseline

**4.1** Write `science/terrain.py`: validate geometry/masks/no-data, match **physical analysis scale**, derive slope distributions, local relief and roughness at stated meters. Use correct body-specific CRS; use derived numerical descriptors for comparison, never naively reproject Mars to Earth. Validate units and per-region effective coverage, with a small automated test synthetic DEM under `tests/`.

**4.2** Write `science/baseline.py`: transparent feature normalization + interpretable multi-criteria distance, missing-data penalties and documented weights. Include one independently documented *known analog* and one deliberately *dissimilar* control, both from actual Earth data. If weighting is subjective, perform sensitivity rather than present a fictional universal similarity percentage.

**4.3** Run only on a small target area and handful of Earth candidates first. **Pass:** reproducible baseline output in `outputs/validated/`, source IDs and plots, tests, and a `feat/terrain-baseline` PR. Never state an unseen site's rank or “new discovery” before calculation.

### Phase 5 — real AI value, validation and the Blue/Red kill gates

**5.1** Implement an **optional** learned/unsupervised similarity method in `science/model.py` (e.g., nearest-neighbor retrieval with learned scaling or clustering). Specify training labels/data if supervised. Compare honestly with the baseline; do not add a neural network simply to decorate the project.

**5.2** In `science/evaluate.py`, test: known analog vs negative control; held-out **geographic regions** rather than adjacent-pixel random train/test; terrain resolution sensitivity; feature/weight sensitivity; missingness and uncertainty; rank stability; alternate explanations. Use no fabricated precision/accuracy claims.

**5.3 Explicit ML-versus-physical-baseline benchmark (mandatory if ML is proposed).** **Before** tuning ML or inspecting its held-out results, create `docs/MODEL_BENCHMARK.md` specifying: (a) the rover-testing task and eligible geographic candidate universe; (b) baseline inputs, physical features, normalization and weighting; (c) the ML method and the *same* data access, feature/compute budgets, and ranking candidate set wherever feasible; (d) geographic holdout regions and controls with no spatial leakage; (e) the independent evidence for reference-site relevance, ideally blinded human/planetary-geology/robotics ratings (do not invent ground-truth analog labels); (f) **one primary metric** such as expert-rated **nDCG@5**, with secondary known-analog Recall@5, top-k stability under feature/resolution perturbations, uncertainty/abstention behavior, runtime and coverage; (g) an improvement threshold chosen **before evaluation** and how sample size/uncertainty will be reported. An *illustrative* provisional criterion is ≥0.05 absolute nDCG@5 improvement on geographically held-out, independently rated examples, **without degrading** scientific robustness or provenance. This threshold is a team decision target, **not a NASA standard**; revise only *before* seeing results and explain why. If reference labels are inadequate, report descriptive results honestly and **do not claim validated ML superiority**. An alternative measurable ML contribution is allowed (e.g., equivalent evidence quality with demonstrably better region coverage or analyst time), but its metric, baseline, threshold and validity safeguards must also be predeclared. Save real metrics, sample sizes and limitations to `outputs/validated/model_comparison.json` and `docs/MODEL_BENCHMARK.md`. Create `tests/test_model_comparison.py`; after implementation run `python -m pytest -q tests/test_model_comparison.py`. **Go/no-go:** retain ML only if its *measured, reproducible* benefit meets the declared standard without worse scientific failure modes; otherwise ship the simpler interpretable physical-feature ranking as the primary scientific engine and state that ML did not demonstrate extra value. Never invent metrics or claim that rank stability alone proves site suitability.

**5.4** Literature-check top candidates/alternate names and existing planetary analog uses; record query/date/sources in `docs/NOVELTY_AUDIT.md`. Classify candidate as **known analog**, **under-recognized candidate**, **new proposed mission use**, or **insufficient evidence**. Create an **Analog Transfer Matrix** (`WORKS / DOES NOT TRANSFER / UNKNOWN`) and proposed rover-testing protocol. **Pass:** at least one defensible site/use, documented flaws, controls and robust evidence; if AI does not help, ship the baseline instead. Commit through `feat/validation`.

### Phase 6 — frontend and interactive map (not dependent on Esri)

**6.1** Install Node.js LTS if `node --version`/`npm --version` fail. From repo root:
```bash
npm create vite@latest app -- --template react-ts
cd app
npm install
npm install maplibre-gl
npm run dev
```
If `app/` contains README/placeholders, **inspect and preserve them** before scaffolding; Vite may refuse to overwrite a nonempty folder. Let the agent choose a safe temp folder and move generated files after review. **Pass:** the Vite page loads in browser on the displayed local address. Use `npm run build` before PR; record `package-lock.json` in Git and do not commit `node_modules`.

**6.2** Implement four views, in this order: **Mission** (Mars reference and reason for rover test); **Search** (actual screened Earth footprint, filters/exclusions); **Compare** (candidate, known analog, control, measured units, uncertainty); **Transfer** (what matches, what fails, proposed field test, source citations). Use MapLibre with a compatible basemap provider subject to usage/attribution; public GeoJSON and static JSON from `outputs/validated`. **Do not display Mars locations as Earth GPS pins**. Avoid external map services requiring judges to log in. Use `README.md` for the frontend run/build commands.

**6.3** Separate scientific analysis from presentation: the website reads precomputed, validated outputs; browser must not download raw DEMs or retrain models. Optionally add user-adjustable precomputed/transparent weights without inventing unexplored-site inference. **Pass:** full user journey, mobile desktop responsiveness, full citations, sensible no-data/error states, `npm run build`, `feat/frontend` PR.

### Phase 7 — optional Esri acceleration, not a rebuild

Only if sponsorship **actually activates**, the agent compares concrete benefit to remaining cost. Candidate additions: ArcGIS Online hosted feature layers, premium terrain, Advanced Notebooks/ArcPy, imagery analysis, Experience Builder, credits. If used, record Esri item IDs, permissions, dataset rights and credit usage in `gis/layer_manifest.json`; keep `science/*.py` executable outside Esri. **ArcGIS Online Notebook web tools may not be anonymously callable**; do not make them the public judge's primary backend. If Esri is slow, unavailable or merely duplicates local tools, **ignore it**. No separate Windows/ArcGIS Pro requirement for Mac members.

### Phase 8 — deployment, reproducibility, evaluation and submission

**8.1** Choose **Vercel** (import GitHub repo; set root directory to `app`, build `npm run build`, output `dist`) or GitHub Pages (configure Vite base path accordingly). Public link should serve actual static results and properly attributed maps. Test **incognito, no accounts** and from another device. Record URL and associated Git tag/commit in `README.md`.

**8.2** Verify a fresh clone can run `conda env create -f environment.yml`, scientific smoke tests, `cd app && npm ci && npm run build`, and load the precomputed demo. Pin/record package versions through `environment.yml`, `package-lock.json` and `docs/METHODS.md`. Optional CI via GitHub Actions for small unit tests only; see [GitHub Python CI](https://docs.github.com/en/actions/tutorials/build-and-test-code/python). Never put bulky/proprietary rasters or secrets in CI.

**8.3** Create `docs/DEMO.md` and official submission: challenge solved, link, code, actual NASA-listed resources, data provenance, quantitative validation, limitations, ethics/AI-use disclosure, attribution, short video/slides within **current 2026 instructions**. Check the app publicly, submit within the NASA local deadline, and preserve links through global judging. Confirm with rules whether later edits are permitted.

**8.4** Final GitHub checkpoint: `git status` clean, reviewed PRs merged, `npm run build` green, `python -m pytest -q` green, public demo accessible, `git tag v1.0-submission` then `git push origin v1.0-submission` after final approval. Create a release if useful. Freeze submission version; do not silently edit scientific claims after submission.

## D. Blue Team / Red Team — phase-wide rejection criteria

| Gate | Evidence required | If failed |
|---|---|---|
| NASA eligibility | ≥1 actually used NASA dataset traceable to an official listed resource; prefer Earthdata + PDS; record IDs | Stop submission-eligibility claim; verify/replace source |
| Real science | Earth and Mars measured, matched physical scale and reliable metadata | Change target/scale; no visual-only similarity |
| Honest search | Search footprint, filters, candidates/controls documented | Do not claim discovery |
| ML contribution | Predeclared `docs/MODEL_BENCHMARK.md`; geographic holdouts, independent reference relevance, primary/secondary metrics; actual baseline-vs-ML results in `outputs/validated/model_comparison.json` | Keep the physical-feature baseline if ML does not meet its declared measurable-value threshold or evidence is inadequate |
| Novelty | Literature and known-site audit | Describe new proposed use rather than “first-ever” site |
| Reproducibility | GitHub code, manifests, tests, versions | Fix before polishing visuals |
| Public delivery | No-login map, sources, results, fallback | Fix hosting; static snapshot before deadlines |
| Judge clarity | Show mission → discovery → evidence → limitations → test | Simplify dashboard/story |

## E. Working roles (adjust only when the team confirms skills)

- **Dr. Mohammed Ibrahim Thanoon:** scientific/AI lead; method, model evaluation, final approval.
- **Abdulrahman Jaber Alabdali:** GIS/remote sensing, Earth/Mars data and QGIS checks.
- **Abdulrahman Alazori:** frontend/integration, GitHub workflow and public deployment.
- **Abdullah Almutiri:** data engineering and automated tests (confirm specialty).
- **Nouf Alzahrani:** physical plausibility, uncertainty and Mars–Earth limitations.
- **Hafsa:** novelty/literature audit, references, demonstration and submission (confirm skills).

Each member should use a separate feature branch. Pull requests require **one independent reviewer**. Resolve scientific disputes through measurement and source evidence, not authority of an AI agent. A branch name and commit message should communicate its phase and verification.

## F. Quick recovery playbook

- `command not found` → inspect installation, shell, PATH; use official installer, restart terminal.
- Windows `conda` missing in VS Code → test **Miniforge Prompt**; consider `conda init powershell` only after verifying installation, then reopen PowerShell.
- `rasterio`/GDAL dependency conflict → use conda-forge Miniforge; don't mix arbitrary pip GDAL binaries.
- Apple M1 wrong architecture → verify `uname -m` and conda `osx-arm64` rather than using Rosetta x86 accidentally.
- Windows Python resolves to Microsoft Store → activate the conda environment and verify `python -c "import sys; print(sys.executable)"`.
- GitHub push 403 → verify `gh auth status` and repo permission; never request the user's token in chat.
- Merge conflict → pause; inspect `git status`, resolve carefully with teammate; **do not** `git reset --hard` or force push without approval.
- Mars data has unfamiliar CRS → pause; inspect PDS metadata, units and planetary datum; never run unverified Earth reprojection.
- Public map missing tiles → check attribution, CORS, basemap provider credentials/terms, and offer a static fallback.
- Download link/internet fails → reduce region or use another documented open source; never fabricate missing observation values.

## G. Official references and final operating instruction

- [NASA official challenge](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=details) and [Resources tab](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=resources)
- [NASA 2026 event/submission dates](https://www.spaceappschallenge.org/2026/) and [GO Team resource/AI clarification](https://github.com/nasa/spaceapps/discussions/1849)
- [NASA PDS](https://pds.nasa.gov/) → [Mars MOLA](https://pds-geosciences.wustl.edu/missions/mgs/mola.html) / [PDS CTX+HiRISE DEM bundle](https://doi.org/10.17189/ervc-mr85); [NASA Earthdata Search](https://search.earthdata.nasa.gov/) → [NASADEM HGT](https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_HGT.001) / [NASADEM SC](https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_SC.001); [NASA Analog Explorer](https://science.nasa.gov/solar-system/analog-explorer/)
- [GitHub Hello World/PRs](https://docs.github.com/en/get-started/using-github/hello-world), [GitHub CLI Quickstart](https://docs.github.com/en/github-cli/github-cli/quickstart)
- [Miniforge](https://conda-forge.org/download/), [QGIS](https://qgis.org/download/), [Vite](https://vite.dev/guide/), [VS Code](https://code.visualstudio.com/docs/)

**Start the agent with:** Identify the current OS, shell, resources, credentials *by presence only*, existing repo state and current phase. Issue **Phase 0.1 only**. Wait for actual output, verify, and then continue one action at a time. No fake completions, no unrequested large command bundles, and no assumptions that a remote platform has executed anything.
