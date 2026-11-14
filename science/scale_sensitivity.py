"""Exploratory Earth–Mars terrain scale sensitivity.

No analog ranking or validated similarity claim.
"""
from pathlib import Path
import numpy as np
import rasterio
from rasterio.warp import transform

from science.terrain import metric_patch, summarize_patch


def sources():
    ctx = list(
        Path("data/raw/mars/ctx").glob("*-DEM-geoid-adj.tif")
    )
    earth = Path("data/raw/earth/nasadem/s25w070.hgt")

    if len(ctx) != 1 or not earth.is_file():
        raise RuntimeError("Expected Mars CTX and Earth NASADEM data")

    with rasterio.open(ctx[0]) as ds:
        mars_crs = ds.crs
        mars_center = (
            (ds.bounds.left + ds.bounds.right) / 2,
            (ds.bounds.bottom + ds.bounds.top) / 2,
        )

    with rasterio.open(earth) as ds:
        x, y = transform(
            ds.crs, "EPSG:32719", [-69.9], [-24.1]
        )

    return [
        ("MARS", ctx[0], mars_crs, mars_center),
        ("EARTH", earth, "EPSG:32719", (x[0], y[0])),
    ]


def main():
    configs = [
        (300, 50),
        (500, 50),
        (1000, 50),
        (1000, 100),
    ]

    print(
        "Planet | Window_m | Cell_m | Coverage_% | "
        "Slope_deg | Relief_m | Roughness_m"
    )

    results = {}

    for planet, path, crs, center in sources():
        for window, cell in configs:
            grid, valid = metric_patch(
                path,
                center_xy=center,
                target_crs=crs,
                window_m=window,
                pixel_size_m=cell,
            )

            r = summarize_patch(
                grid, cell, valid_mask=valid
            )

            assert r["usable"], (
                f"{planet}: unusable {window}/{cell}"
            )
            assert r["valid_fraction"] >= 0.95
            assert all(np.isfinite(r[key]) for key in (
                "slope_deg",
                "relief_p95_p05_m",
                "roughness_rms_m",
            ))

            results[(planet, window, cell)] = r

            print(
                f"{planet:5} | {window:8} | {cell:6} | "
                f"{100*r['valid_fraction']:10.2f} | "
                f"{r['slope_deg']:9.4f} | "
                f"{r['relief_p95_p05_m']:8.3f} | "
                f"{r['roughness_rms_m']:11.4f}"
            )

    print("\nResolution sensitivity at 1000 m window")
    for planet in ("MARS", "EARTH"):
        a = results[(planet, 1000, 50)]
        b = results[(planet, 1000, 100)]

        print(f"{planet}:")
        for key in (
            "slope_deg",
            "relief_p95_p05_m",
            "roughness_rms_m",
        ):
            print(
                f"  {key}: "
                f"{a[key]:.4f} -> {b[key]:.4f}"
            )

    print("\nFIELDTWIN_SCALE_SENSITIVITY_OK")


if __name__ == "__main__":
    main()
