
# FieldTwin — Scientific and Technical References

**Version:** 1.0
**Project:** NASA Space Apps Challenge 2026
**Execution Plan:** FieldTwin v6.2
**Status:** Initial reference registry — scientific verification ongoing

## 1. Purpose

This document maintains the official scientific, technical, and research references associated with FieldTwin.

References must support actual project decisions, methods, dataset usage, or scientific conclusions.

Listing a resource does not mean its data have already been downloaded or analyzed.

## 2. NASA Space Apps Challenge

### NASA Space Apps Challenge 2026

Official website:
https://www.spaceappschallenge.org/2026/

### Official Challenge

Identify Earth Locations that Analog the Permanent Moon Base Locations and Mars.

https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=details

### Official Challenge Resources

https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=resources

### NASA Space Apps Data and AI Guidance

https://github.com/nasa/spaceapps/discussions/1849

The team must verify the applicable eligibility and submission requirements.

## 3. Mars Scientific Data

### NASA Planetary Data System (PDS)

https://pds.nasa.gov/

Purpose:
Official archive and discovery source for planetary mission data.

Status:
Source identified; actual products pending verification.

### Mars Orbiter Laser Altimeter (MOLA)

https://pds-geosciences.wustl.edu/missions/mgs/mola.html

Purpose:
Martian regional topographic context.

Status:
Candidate data source; actual product pending selection.

### PDS CTX / HiRISE DTM Products

https://doi.org/10.17189/ervc-mr85

Purpose:
Potential source of stereo-derived Martian digital terrain models.

Status:
Product availability for the selected Mars region not yet verified.

### USGS Astrogeology CTX DTMs

https://stac.astrogeology.usgs.gov/docs/data/mars/ctxdtms/

Purpose:
Potential regional Mars elevation products derived from CTX observations.

Status:
Candidate source; actual DTM pending verification.

Important:
CTX imagery is not itself a digital terrain model.

Derived products require documentation of their source observations and processing provenance.

## 4. Earth Scientific Data

### NASA Earthdata Search

https://search.earthdata.nasa.gov/

Purpose:
Discover and access NASA Earth observation datasets.

Status:
Source identified; data acquisition pending.

### NASADEM_HGT.001

https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_HGT.001

Purpose:
Primary planned Earth elevation dataset.

Status:
Not yet acquired.

### NASADEM_SC.001

https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_SC.001

Purpose:
Optional supporting slope and curvature information.

Status:
Not yet acquired.

Final Earth–Mars terrain comparisons must use compatible effective physical analysis scales.

## 5. Planetary Analogs and Scientific Research

### NASA Analog Explorer

https://science.nasa.gov/solar-system/analog-explorer/

Purpose:
Background research into the use of Earth environments for planetary exploration.

### NASA Technical Reports Server

https://ntrs.nasa.gov/

Purpose:
NASA technical publications and scientific reports.

### USGS Astrogeology

https://astrogeology.usgs.gov/

Purpose:
Planetary geospatial data, maps, and supporting documentation.

### Additional Literature Discovery

Google Scholar:
https://scholar.google.com/

Crossref:
https://search.crossref.org/

Actual publications must be recorded with their authors, titles, publication dates, DOI or stable URL, and relevance to FieldTwin.

Research discovery tools are not substitutes for citing the original publications.

## 6. Software and Technical Documentation

### Python

https://docs.python.org/3.12/

### Conda / Miniforge

https://docs.conda.io/

https://github.com/conda-forge/miniforge

### QGIS

https://docs.qgis.org/

### Rasterio

https://rasterio.readthedocs.io/

### GeoPandas

https://geopandas.org/

### scikit-learn

https://scikit-learn.org/stable/

### React

https://react.dev/

### Vite

https://vite.dev/guide/

### MapLibre GL JS

https://maplibre.org/maplibre-gl-js/docs/

### GitHub

https://docs.github.com/

Software documentation should be cited when supporting implementation choices, numerical methods, or reproducibility procedures.

## 7. Scientific Reference Recording Template

For each publication or scientific resource actually used, record:

**Reference ID:**

**Title:**

**Author(s) / Organization:**

**Publication date:**

**Journal / Publisher:**

**DOI or official URL:**

**Date accessed:**

**Scientific topic:**

**FieldTwin component supported:**

**Specific claim or method supported:**

**Relevant limitations:**

**Verification status:**

## 8. Dataset Citation Requirements

For every actual NASA dataset, record:

- Official collection name.
- Product or granule identifier.
- Instrument and mission.
- Data provider.
- DOI or official landing page.
- Actual file identifier.
- Acquisition or access date.
- Processing provenance.
- Required attribution.

The detailed data inventory is maintained in:

`data/SOURCES.md`

This reference document provides the corresponding citations.

Do not cite only a general data portal when a specific product citation is available.

## 9. Reference Quality Rules

1. Prefer official NASA and USGS sources for mission data.
2. Prefer peer-reviewed literature for scientific claims.
3. Use primary research publications where possible.
4. Verify that cited sources support the specific claim.
5. Record exact product identifiers.
6. Do not invent publication details or DOIs.
7. Distinguish source documentation from actual measurements.
8. Record conflicting findings and relevant uncertainty.
9. Preserve stable links and attribution.
10. Update the reference registry when new evidence is used.

## 10. Research and Citation Status

| Reference area | Status |
|---|---|
| NASA challenge information | Identified |
| Official NASA resources | Listed; eligibility to verify |
| Mars dataset product citations | Pending |
| Earth dataset granule citations | Pending |
| Terrain-analysis literature | Pending |
| Known analog literature | Pending |
| Negative control justification | Pending |
| Scientific novelty literature | Pending |
| Rover mobility research | Pending |
| Software documentation | Initial sources listed |

No dataset acquisition, published novelty finding, or completed scientific result is claimed in this document.

## 11. Final Verification Checklist

- [ ] Actual NASA datasets cited.
- [ ] Product and granule identifiers recorded.
- [ ] Data provider attribution verified.
- [ ] Terrain processing methods supported by references.
- [ ] Known analog references documented.
- [ ] Negative control justification documented.
- [ ] Rover field-test recommendations supported.
- [ ] Novelty claims cross-checked against prior literature.
- [ ] Scientific limitations cited.
- [ ] All public application citations checked.
- [ ] Broken links reviewed.
- [ ] Final reference list approved by the scientific lead.

**Current status:** Initial reference structure completed; scientific bibliography and dataset citations pending.

---

**Reference principle:** Every scientific claim must be traceable to real evidence, and every source must support the claim for which it is cited.
