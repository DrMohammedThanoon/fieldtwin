"""Six-site Earth-Mars Pareto comparison pilot."""

from pathlib import Path
import numpy as np
import rasterio
from rasterio.warp import transform

from science.scale_sensitivity import sources
from science.terrain import metric_patch, summarize_patch
from science.baseline import (
    BASELINE_KEYS,
    absolute_differences,
    pareto_layers,
)


def projected_center(path, lon, lat):
    with rasterio.open(path) as src:
        x, y = transform(
            src.crs, "EPSG:32719", [lon], [lat]
        )
    return x[0], y[0]


def features(path, crs, center, window):
    grid, valid = metric_patch(
        path,
        center_xy=center,
        target_crs=crs,
        window_m=window,
        pixel_size_m=100,
    )

    result = summarize_patch(
        grid, 100, valid_mask=valid
    )

    assert result["usable"], str(path)
    return result


def main():
    mars, earth = sources()

    arads = Path("data/raw/earth/nasadem/s25w071.hgt")
    lascar = Path("data/raw/earth/nasadem/s24w068.hgt")

    assert arads.is_file(), "ARADS DEM missing"
    assert lascar.is_file(), "Lasc ar DEM missing"

    locations = {
        "PILOT_A": (earth[1], -69.6, -24.5),
        "PILOT_B": (earth[1], -69.9, -24.4),
        "PILOT_C": (earth[1], -69.9, -24.3),
        "PILOT_D": (earth[1], -69.9, -24.2),
        "ARADS_PLAYA": (
            arads, -70.138175, -24.101642
        ),
        "LASCAR_CONTROL": (
            lascar, -67.73, -23.37
        ),
    }

    for window in (1000, 2000):
        reference = features(
            mars[1], mars[2], mars[3], window
        )

        differences = {}

        for name, (path, lon, lat) in locations.items():
            center = projected_center(path, lon, lat)

            result = features(
                path, "EPSG:32719", center, window
            )

            differences[name] = absolute_differences(
                reference, result
            )

            assert all(
                np.isfinite(differences[name][key])
                for key in BASELINE_KEYS
            )

        fronts = pareto_layers(differences)

        print(f"\nWINDOW: {window} m | GRID: 100 m")
        print(
            "Front | Site | dSlope_deg | "
            "dRelief_m | dRoughness_m"
        )

        for number, front in enumerate(fronts, 1):
            for name in front:
                r = differences[name]

                print(
                    f"{number} | {name} | "
                    f"{r['slope_deg']:.4f} | "
                    f"{r['relief_p95_p05_m']:.4f} | "
                    f"{r['roughness_rms_m']:.4f}"
                )

    print("\nNo similarity weights or suitability scores.")
    print("FIELDTWIN_BASELINE_PARETO_OK")


if __name__ == "__main__":
    main()
