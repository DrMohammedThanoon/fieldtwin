
# FieldTwin — Scientific Data Sources

**Project:** NASA Space Apps Challenge 2026
**Status:** Dataset acquisition pending
**Execution Plan:** v6.2

## 1. Purpose

This document records the scientific datasets used by FieldTwin.

Every dataset must have a verifiable source, identifier,
spatial reference, resolution, and processing history.

Do not record datasets as acquired until their files
have actually been downloaded and verified.

## 2. Official NASA Resources

Challenge resources:
https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=resources

### Mars

NASA Planetary Data System:
https://pds.nasa.gov/

MOLA:
https://pds-geosciences.wustl.edu/missions/mgs/mola.html

Potential CTX-derived terrain models:
https://stac.astrogeology.usgs.gov/docs/data/mars/ctxdtms/

### Earth

NASA Earthdata Search:
https://search.earthdata.nasa.gov/

NASADEM_HGT.001:
https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_HGT.001

NASADEM_SC.001:
https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_SC.001

## 3. Dataset Verification Template

For each actual dataset, record:

- Dataset name:
- Mission or instrument:
- Product / granule ID:
- Official source URL:
- Download URL:
- Date accessed:
- Planetary body:
- Geographic coverage:
- Coordinate reference system:
- Horizontal resolution:
- Vertical units and datum:
- No-data and quality masks:
- Processing provenance:
- License and attribution:
- File verification:
- Checksum (if available):
- Validation status:

## 4. Current Dataset Status

| Dataset | Status |
|---|---|
| Mars MOLA | Not yet acquired |
| Mars regional DTM | Not yet selected |
| NASADEM_HGT.001 | Not yet acquired |
| NASADEM_SC.001 | Optional; not yet acquired |

## 5. Scientific Requirements

1. Verify actual product and granule identifiers.
2. Preserve original data provenance.
3. Validate elevation units and coordinate systems.
4. Compare Earth and Mars at compatible physical scales.
5. Document data quality and missing observations.
6. Never fabricate dataset identifiers or measurements.
7. Store large raw datasets outside Git.
8. Verify NASA challenge-resource eligibility.

## 6. Verification Gate

Dataset acquisition is complete only when actual
Earth and Mars products have been downloaded,
opened, inspected, and documented.

No scientific results are currently claimed.

## Phase 3 — Verified Dataset Inventory

Inventory recorded from actual downloaded files.
Data accessed: 2026-11-14.
Raw datasets remain excluded from Git.

### NASA MOLA — Mars regional context
- Collection: NASA PDS, MGS MOLA MEGDR, MEG016
- Identifier: `urn:nasa:pds:mgs_mola_topography_derived:data_meg016:megt90n000eb`
- Source: https://pds-geosciences.wustl.edu/missions/mgs/megdr.html
- Local file: `data/raw/mars/mola/megt90n000eb.img`
- SHA-256: `d18d9b9ab8c5516d02e157dd2cde0f1d0d160c21940e953ba22391269a545e7b`
- Limitation: 3.704 km posting; global context only

### USGS CTX — Mars detailed terrain candidate
- Collection: MRO CTX stereo DTM, USGS controlled collection
- Identifier: `T01_000893_1847_XN_04N191W__N09_065929_1853_XN_05N191W`
- Source: https://doi.org/10.5066/P9JKVWR3
- Local file: `data/raw/mars/ctx/T01_000893_1847_XN_04N191W__N09_065929_1853_XN_05N191W-DEM-geoid-adj.tif`
- SHA-256: `4888a180ba6e868cb4fc0f33478723587499cf40e780af15983b615ce62f3c51`
- Limitation: 20 m posting; 80% valid coverage; visual artifact review pending

### NASADEM — Earth elevation pilot
- Collection: NASADEM_HGT.001; NASA LP DAAC
- Identifier: `G2816781179-LPCLOUD / NASADEM_HGT_s25w070`
- Source: https://doi.org/10.5067/MEASURES/NASADEM/NASADEM_HGT.001
- Local file: `data/raw/earth/nasadem/NASADEM_HGT_s25w070.zip`
- SHA-256: `a8522f8985642512814f4cfbff3eb38a56bc30a9b7c4eda2f69ff29310f88906`
- Limitation: 1 arc-second; Atacama pilot only; not yet a validated analog

### Pending scientific requirements
- Confirm vertical datums and effective terrain resolution.
- Inspect CTX artifacts and unavailable orthoimage.
- Define bounded Earth search, known analog and negative control.
- Compute Earth–Mars features at matched physical scales.
- Record uncertainty and non-transferable conditions.
