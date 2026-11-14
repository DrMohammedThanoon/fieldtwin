
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
