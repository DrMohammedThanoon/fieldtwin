"""Transparent, unweighted terrain comparison baseline."""

import numpy as np

BASELINE_KEYS = (
    "slope_deg",
    "relief_p95_p05_m",
    "roughness_rms_m",
)


def absolute_differences(reference, candidate):
    """Calculate absolute differences for baseline features."""
    result = {}

    for key in BASELINE_KEYS:
        a = float(reference[key])
        b = float(candidate[key])

        if not np.isfinite(a) or not np.isfinite(b):
            raise ValueError(f"Invalid feature: {key}")

        result[key] = abs(a - b)

    return result


def pareto_layers(errors):
    """Group candidates into successive Pareto fronts.

    All feature differences are minimized.
    No weights or arbitrary similarity scores are used.
    """
    if not errors:
        raise ValueError("No candidates supplied")

    vectors = {}

    for name, record in errors.items():
        values = np.array(
            [record[k] for k in BASELINE_KEYS],
            dtype=float,
        )

        if (
            not np.all(np.isfinite(values))
            or np.any(values < 0)
        ):
            raise ValueError(f"Invalid differences: {name}")

        vectors[name] = values

    remaining = list(vectors)
    fronts = []

    while remaining:
        front = []

        for name in remaining:
            target = vectors[name]

            dominated = any(
                np.all(vectors[other] <= target)
                and np.any(vectors[other] < target)
                for other in remaining
                if other != name
            )

            if not dominated:
                front.append(name)

        if not front:
            raise RuntimeError("Pareto sorting failed")

        fronts.append(sorted(front))
        selected = set(front)

        remaining = [
            name for name in remaining
            if name not in selected
        ]

    return fronts
