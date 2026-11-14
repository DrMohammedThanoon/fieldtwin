"""Predefined NASADEM tile search; exploratory only.

Search: 9x9 locations within s25w070.
Window: 2000 m. Processing grids: 100 m and 200 m.
Candidate comparison: absolute global slope and relief differences.
No fitted ranking weights or analog suitability claims.
"""

import numpy as np
import rasterio
from rasterio.warp import transform

from science.scale_sensitivity import sources
from science.terrain import metric_patch, summarize_patch


def measure(path, crs, center, cell):
    grid, valid = metric_patch(
        path,
        center_xy=center,
        target_crs=crs,
        window_m=2000,
        pixel_size_m=cell,
    )
    return summarize_patch(grid, cell, valid_mask=valid)


def main():
    mars, earth = sources()

    reference = {
        cell: measure(mars[1], mars[2], mars[3], cell)
        for cell in (100, 200)
    }
    assert all(r["usable"] for r in reference.values())

    lons = np.linspace(-69.9, -69.1, 9)
    lats = np.linspace(-24.9, -24.1, 9)
    locations = [(lon, lat) for lat in lats for lon in lons]

    with rasterio.open(earth[1]) as src:
        x, y = transform(
            src.crs,
            earth[2],
            [p[0] for p in locations],
            [p[1] for p in locations],
        )

    candidates = []

    for (lon, lat), cx, cy in zip(locations, x, y):
        metrics = {
            cell: measure(
                earth[1], earth[2], (cx, cy), cell
            )
            for cell in (100, 200)
        }

        if not all(
            r["usable"] and r["valid_fraction"] >= 0.95
            for r in metrics.values()
        ):
            continue

        r = metrics[200]
        m = reference[200]

        candidates.append({
            "lon": float(lon),
            "lat": float(lat),
            "metrics": metrics,
            "slope_difference": abs(
                r["slope_deg"] - m["slope_deg"]
            ),
            "relief_difference": abs(
                r["relief_p95_p05_m"]
                - m["relief_p95_p05_m"]
            ),
        })

    assert candidates, "No usable candidate locations"

    pareto = []

    for candidate in candidates:
        dominated = any(
            (
                other["slope_difference"]
                <= candidate["slope_difference"]
                and other["relief_difference"]
                <= candidate["relief_difference"]
            )
            and (
                other["slope_difference"]
                < candidate["slope_difference"]
                or other["relief_difference"]
                < candidate["relief_difference"]
            )
            for other in candidates
        )

        if not dominated:
            pareto.append(candidate)

    # Presentation order only, not a weighted suitability rank.
    pareto.sort(
        key=lambda r: (
            r["slope_difference"],
            r["relief_difference"],
            r["lat"],
            r["lon"],
        )
    )

    print("NASA Earth candidate pilot: s25w070")
    print("Sample locations:", len(locations))
    print("Usable locations:", len(candidates))
    print("Analysis window: 2000 m")
    print("Grid spacing: 100 m and 200 m")

    print("\nMars reference")
    for cell, r in reference.items():
        print(
            f"{cell} m: slope={r['slope_deg']:.4f} deg, "
            f"relief={r['relief_p95_p05_m']:.3f} m, "
            f"roughness={r['roughness_rms_m']:.3f} m"
        )

    print("\nPareto candidates:", len(pareto))
    print(
        "Lat | Lon | Slope_200_deg | Relief_200_m | "
        "Slope_difference_deg | Relief_difference_m"
    )

    for r in pareto[:10]:
        m = r["metrics"][200]
        print(
            f"{r['lat']:.4f} | {r['lon']:.4f} | "
            f"{m['slope_deg']:.4f} | "
            f"{m['relief_p95_p05_m']:.3f} | "
            f"{r['slope_difference']:.4f} | "
            f"{r['relief_difference']:.3f}"
        )

    print("\nNo analog suitability score has been assigned.")
    print("FIELDTWIN_EARTH_CANDIDATE_PILOT_OK")


if __name__ == "__main__":
    main()
