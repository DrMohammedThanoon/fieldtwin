"""Reproducible, hypothetical DEM route-feasibility stress test."""

from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter

from science.scale_sensitivity import sources
from science.benchmark_baseline import projected_center
from science.terrain import metric_patch
from science.routes import shortest_route, NoRouteError
from science.multi_route_benchmark import PAIRS, LIMITS


def feasible(grid, start, goal, limit):
    try:
        shortest_route(
            grid, 100, start, goal, max_slope_deg=limit
        )
        return True
    except NoRouteError:
        return False


def main():
    rng = np.random.default_rng(20261114)
    mars, earth = sources()
    arads = Path("data/raw/earth/nasadem/s25w071.hgt")
    lascar = Path("data/raw/earth/nasadem/s24w068.hgt")

    sites = [
        ("MARS", mars[1], mars[2], mars[3]),
        ("PILOT_B", earth[1], "EPSG:32719",
         projected_center(earth[1], -69.9, -24.4)),
        ("ARADS", arads, "EPSG:32719",
         projected_center(arads, -70.138175, -24.101642)),
        ("LASCAR", lascar, "EPSG:32719",
         projected_center(lascar, -67.73, -23.37)),
    ]

    searches = 0

    print("FIELDTWIN ROUTE UNCERTAINTY EXPERIMENT")
    print("Window: 1000 m | Grid: 100 m")
    print("Seed: 20261114 | Trials per scenario: 30")
    print("Assumed SD: 1 m and 3 m (not calibrated errors)")

    for name, path, crs, center in sites:
        grid, valid = metric_patch(
            path, center_xy=center, target_crs=crs,
            window_m=1000, pixel_size_m=100,
        )
        assert valid.all(), f"Invalid grid: {name}"

        original = {
            limit: [
                feasible(grid, start, goal, limit)
                for start, goal in PAIRS
            ]
            for limit in LIMITS
        }
        searches += len(LIMITS) * len(PAIRS)

        print(f"\n{name}")

        for model in ("independent", "correlated"):
            for sd in (1.0, 3.0):
                counts = {
                    limit: {"feasible": 0, "changed": 0}
                    for limit in LIMITS
                }

                for _ in range(30):
                    noise = rng.standard_normal(grid.shape)
                    if model == "correlated":
                        noise = gaussian_filter(
                            noise, sigma=2.0, mode="reflect"
                        )

                    noise -= noise.mean()
                    assert noise.std() > 0
                    noisy = grid + sd * noise / noise.std()

                    for index, (start, goal) in enumerate(PAIRS):
                        for limit in LIMITS:
                            result = feasible(
                                noisy, start, goal, limit
                            )
                            searches += 1
                            counts[limit]["feasible"] += int(result)
                            counts[limit]["changed"] += int(
                                result != original[limit][index]
                            )

                for limit in LIMITS:
                    record = counts[limit]
                    print(
                        f"{model} | SD={sd:.1f} m | "
                        f"limit={limit:g} deg | "
                        f"original={sum(original[limit])}/5 | "
                        f"feasible={record['feasible']}/150 | "
                        f"changed={record['changed']}/150"
                    )

    assert searches == 4840, searches
    print("\nRoute searches:", searches)
    print("Results are not calibrated safety probabilities.")
    print("FIELDTWIN_ROUTE_UNCERTAINTY_OK")


if __name__ == "__main__":
    main()
