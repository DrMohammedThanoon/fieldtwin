"""Reproducible DEM-scale multi-route sensitivity benchmark.

Four terrain windows, five endpoint pairs, two slope limits.
Experimental parameters are not certified rover limits.
"""
from pathlib import Path

from science.scale_sensitivity import sources
from science.benchmark_baseline import projected_center
from science.terrain import metric_patch
from science.routes import shortest_route, NoRouteError

PAIRS = [
    ((1, 1), (8, 8)),
    ((1, 8), (8, 1)),
    ((1, 1), (8, 1)),
    ((1, 1), (1, 8)),
    ((8, 1), (8, 8)),
]
LIMITS = (3.0, 10.0)


def main():
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
    print("FIELDTWIN REPRODUCIBLE MULTI-ROUTE BENCHMARK")
    print("Window: 1000 m | Grid: 100 m")
    print("Detour averages include feasible routes only.")

    for name, path, crs, center in sites:
        grid, valid = metric_patch(
            path, center_xy=center, target_crs=crs,
            window_m=1000, pixel_size_m=100,
        )
        assert valid.all(), f"Missing terrain cells: {name}"

        # Compute each unconstrained route only once.
        baselines = []
        for start, goal in PAIRS:
            baseline = shortest_route(grid, 100, start, goal)
            baselines.append((start, goal, baseline))
            searches += 1

        print(f"\n{name}")
        for limit in LIMITS:
            feasible = 0
            infeasible = 0
            longer = 0
            detours = []

            for start, goal, baseline in baselines:
                searches += 1
                try:
                    result = shortest_route(
                        grid, 100, start, goal,
                        max_slope_deg=limit,
                    )
                except NoRouteError:
                    infeasible += 1
                    continue

                feasible += 1
                assert result["maximum_slope_deg"] <= limit + 1e-8

                extra = 100 * (
                    result["distance_m"] / baseline["distance_m"] - 1
                )
                assert extra >= -1e-7
                detours.append(extra)
                if extra > 1e-6:
                    longer += 1

            assert feasible + infeasible == len(PAIRS)
            mean = sum(detours) / len(detours) if detours else None

            summary = (
                f"  Limit {limit:g} deg | "
                f"feasible={feasible}/5 | "
                f"infeasible={infeasible}/5 | "
                f"longer={longer}"
            )
            if mean is not None:
                summary += f" | feasible_mean_detour={mean:.2f}%"
            print(summary)

    assert searches == 60, f"Expected 60, got {searches}"
    print("\nRoute searches:", searches)
    print("FIELDTWIN_MULTI_ROUTE_BENCHMARK_OK")


if __name__ == "__main__":
    main()
