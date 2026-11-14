"""Reproducible Earth–Mars terrain-processing pilot.

Exploratory measurements only; not an analog suitability score.
"""

from pathlib import Path
import numpy as np
import rasterio
from rasterio.warp import transform

from science.terrain import metric_patch, summarize_patch


def main():
    ctx_files = list(
        Path("data/raw/mars/ctx").glob("*-DEM-geoid-adj.tif")
    )
    earth_file = Path("data/raw/earth/nasadem/s25w070.hgt")

    if len(ctx_files) != 1:
        raise RuntimeError("Expected exactly one CTX DEM")

    if not earth_file.is_file():
        raise FileNotFoundError(earth_file)

    with rasterio.open(ctx_files[0]) as src:
        mars_crs = src.crs
        mars_center = (
            (src.bounds.left + src.bounds.right) / 2,
            (src.bounds.bottom + src.bounds.top) / 2,
        )

    with rasterio.open(earth_file) as src:
        earth_crs = "EPSG:32719"
        x, y = transform(
            src.crs, earth_crs,
            [-69.9], [-24.1]
        )
        earth_center = (x[0], y[0])

    datasets = [
        ("MARS CTX", ctx_files[0], mars_crs, mars_center),
        ("EARTH NASADEM", earth_file, earth_crs, earth_center),
    ]

    for name, path, crs, center in datasets:
        grid, valid = metric_patch(
            path,
            center_xy=center,
            target_crs=crs,
            window_m=1000,
            pixel_size_m=50,
        )

        result = summarize_patch(
            grid,
            pixel_size_m=50,
            valid_mask=valid,
        )

        assert grid.shape == (20, 20)
        assert result["usable"]
        assert result["valid_fraction"] >= 0.95

        features = (
            result["slope_deg"],
            result["relief_p95_p05_m"],
            result["roughness_rms_m"],
        )
        assert all(np.isfinite(value) for value in features)

        print(f"\n{name}")
        print("Grid: 20 x 20 at 50 m")
        print("Center (projected meters):",
              tuple(round(v, 2) for v in center))
        print("Coverage (%):",
              round(result["valid_fraction"] * 100, 2))
        print("Slope (degrees):",
              round(result["slope_deg"], 4))
        print("Relief P95-P05 (m):",
              round(result["relief_p95_p05_m"], 4))
        print("Roughness RMS (m):",
              round(result["roughness_rms_m"], 4))

    print("\nFIELDTWIN_REAL_PILOT_INTEGRATION_OK")


if __name__ == "__main__":
    main()
