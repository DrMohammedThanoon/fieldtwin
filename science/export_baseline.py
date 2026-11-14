"""Export measured Earth-Mars terrain comparisons.

Unweighted Pareto sorting; no suitability score or
claim of physical rover-safety validation.
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from science.scale_sensitivity import sources
from science.benchmark_baseline import projected_center, features
from science.baseline import (
    BASELINE_KEYS,
    absolute_differences,
    pareto_layers,
)


OUTPUT = Path("outputs/validated")
WINDOWS = (1000, 2000)
GRID_M = 100

FEATURE_LABELS = (
    ("slope_deg", "Plane-fit slope difference (degrees)"),
    ("relief_p95_p05_m", "Relief difference (m)"),
    ("roughness_rms_m", "Roughness difference (m)"),
)


def numeric_features(record):
    return {
        key: float(record[key])
        for key in BASELINE_KEYS
    }


def main():
    mars, earth = sources()

    arads = Path("data/raw/earth/nasadem/s25w071.hgt")
    lascar = Path("data/raw/earth/nasadem/s24w068.hgt")

    locations = {
        "PILOT_A": (earth[1], -69.6, -24.5, "pilot"),
        "PILOT_B": (earth[1], -69.9, -24.4, "pilot"),
        "PILOT_C": (earth[1], -69.9, -24.3, "pilot"),
        "PILOT_D": (earth[1], -69.9, -24.2, "pilot"),
        "ARADS_PLAYA": (
            arads, -70.138175, -24.101642,
            "historical_rover_test_reference",
        ),
        "LASCAR_CONTROL": (
            lascar, -67.73, -23.37,
            "negative_control",
        ),
    }

    for name, (path, _, _, _) in locations.items():
        assert Path(path).is_file(), f"Missing DEM: {name}"

    data = {
        "schema_version": "1.0",
        "scientific_status": "exploratory_not_field_validated",
        "method": "unweighted_absolute_difference_pareto",
        "no_unique_winner_inferred": True,
        "analysis_grid_m": GRID_M,
        "analysis_windows_m": list(WINDOWS),
        "matched_analysis_grid_is_not_equal_effective_resolution": True,
        "feature_keys": list(BASELINE_KEYS),
        "source_manifest": "data/SOURCES.md",
        "search_scope_document": "data/SEARCH_SCOPE.md",
        "mars_reference": {
            "source_file": Path(mars[1]).name,
            "target_crs": str(mars[2]),
            "center_projected_xy_m": [
                float(v) for v in mars[3]
            ],
            "role": "provisional_CTX_DTM_reference",
        },
        "sites": {},
        "evaluations": {},
        "limitations": [
            "The Mars CTX DTM remains a provisional reference.",
            "Common grid spacing does not prove matched effective resolution.",
            "ARADS field-test history is not independent terrain-match validation.",
            "The negative control is not an exhaustive exclusion test.",
            "Pareto fronts represent feature trade-offs, not suitability scores.",
            "No rock, soil, traction, accessibility or rover-safety validation.",
        ],
    }

    for name, (path, lon, lat, role) in locations.items():
        data["sites"][name] = {
            "longitude_deg": lon,
            "latitude_deg": lat,
            "role": role,
            "source_product": "NASADEM_HGT.001",
            "source_file": Path(path).name,
            "analysis_crs": "EPSG:32719",
        }

    for window in WINDOWS:
        reference = features(
            mars[1], mars[2], mars[3], window
        )
        ref_values = numeric_features(reference)

        differences = {}
        site_features = {}

        for name, (path, lon, lat, _) in locations.items():
            center = projected_center(path, lon, lat)

            candidate = features(
                path, "EPSG:32719", center, window
            )

            site_features[name] = numeric_features(candidate)
            differences[name] = absolute_differences(
                reference, candidate
            )

        fronts = pareto_layers(differences)
        front_index = {
            name: number
            for number, front in enumerate(fronts, 1)
            for name in front
        }

        entries = []

        for name in locations:
            entries.append({
                "site_id": name,
                "features": site_features[name],
                "absolute_differences": {
                    key: float(differences[name][key])
                    for key in BASELINE_KEYS
                },
                "pareto_front": front_index[name],
            })

        data["evaluations"][str(window)] = {
            "window_m": window,
            "grid_m": GRID_M,
            "mars_reference_features": ref_values,
            "pareto_fronts": fronts,
            "candidates": entries,
        }

        assert len(entries) == 6
        assert sum(map(len, fronts)) == 6

    OUTPUT.mkdir(parents=True, exist_ok=True)

    json_path = OUTPUT / "terrain_baseline.json"
    json_path.write_text(
        json.dumps(
            data, indent=2, ensure_ascii=False,
            allow_nan=False,
        ) + "\n",
        encoding="utf-8",
    )

    fig, axes = plt.subplots(
        2, 3, figsize=(17, 11),
        layout="constrained",
    )

    for row, window in enumerate(WINDOWS):
        records = data["evaluations"][str(window)]["candidates"]
        records = sorted(
            records,
            key=lambda x: (
                x["pareto_front"], x["site_id"]
            ),
        )

        labels = [
            f"F{r['pareto_front']}  {r['site_id']}"
            for r in records
        ]

        for col, (key, description) in enumerate(FEATURE_LABELS):
            ax = axes[row, col]

            values = [
                r["absolute_differences"][key]
                for r in records
            ]

            assert np.isfinite(values).all()

            positions = np.arange(len(records))

            ax.barh(positions, values)
            ax.set_yticks(positions, labels=labels)
            ax.invert_yaxis()
            ax.set_title(
                f"{window} m window\n{description}"
            )
            ax.set_xlabel("Absolute difference; lower is closer")
            ax.grid(axis="x", alpha=0.2)

    fig.suptitle(
        "FieldTwin: Earth-Mars DEM Feature Differences\n"
        "Pareto front labels F1/F2/F3; "
        "no weighted similarity or rover suitability score",
        fontsize=15,
    )

    image_path = OUTPUT / "terrain_baseline.png"
    fig.savefig(image_path, dpi=170)
    plt.close(fig)

    # Confirm files are readable after generation.
    check = json.loads(json_path.read_text())
    assert set(check["evaluations"]) == {"1000", "2000"}
    assert image_path.stat().st_size > 1000

    print("FIELDTWIN_BASELINE_EXPORT_OK")

    for path in (json_path, image_path):
        print(
            path.as_posix(),
            "|",
            path.stat().st_size,
            "bytes",
        )

    for window in WINDOWS:
        fronts = data["evaluations"][str(window)]["pareto_fronts"]
        print(f"{window}m Pareto fronts:", fronts)

    print(
        "No winner, similarity percentage, or "
        "operational rover suitability inferred."
    )


if __name__ == "__main__":
    main()
