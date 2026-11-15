# FieldTwin frontend

Phase 6 React + TypeScript + Vite demonstration. It presents the measured six-site comparison and clearly labels the science as exploratory. It runs without Esri or authentication.

## Run locally

From `app/`:

```sh
npm ci
npm run dev
```

For a production build, run `npm run build`, then `npm run preview` to serve it locally. Vite's relative base setting permits static hosting under a repository path. A public deployment has not yet been verified.

## Evidence used

- `src/data/terrain_baseline.json` is a byte-for-byte copy of `../outputs/validated/terrain_baseline.json`. Recopy it only when the validated scientific export changes under a separate reviewed scientific process. Compare the two files with `cmp` before release.
- The route table reproduces the 60-search results in `../docs/PHASE4_BASELINE_RESULTS.md`. The proposed field protocol and limitations follow `../docs/PHASE5_SCIENTIFIC_CLOSEOUT.md` and `../docs/ANALOG_TRANSFER_MATRIX.md`.
- Dataset and granule identifiers are documented in `../data/SOURCES.md`; the geographical study is in `../data/SEARCH_SCOPE.md`.
- The browser uses only small validated JSON and derived presentation text. It does not load DEM rasters, models, or perform new terrain analysis.

## Map and limits

The MapLibre Earth map uses the standard OpenStreetMap raster tile service with visible attribution. Users retain the complete site list and coordinates if map tiles or WebGL are unavailable. Mars is presented separately and is never placed on the Earth basemap. For significant public traffic, choose a tile provider whose terms and capacity fit the deployment.

The four pilot sites are nondominated only within this six-site, three-feature comparison. The Mars CTX reference remains provisional; effective source resolution and DEM accuracy are not established as matched. Numerical routes under 3° and 10° grade limits are exploratory; no physical rover field test has been performed. The app does not present ML as a validated site-selection engine.
