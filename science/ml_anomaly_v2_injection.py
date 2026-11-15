"""Prospective ML-B V2 synthetic DEM assignments and injections.

No raster loading, model fitting, scoring, or filesystem
modifications occur inside this module.

Synthetic labels depend only on geographic identity and
frozen random seeds, never on terrain characteristics.
"""

from collections import Counter

import numpy as np


SEED = 20261116
TRAIN_TILE = "s25w070"

HOLDOUT_TILES = {
    "s21w069": 0,
    "s28w069": 1,
}

ARTIFACTS = (
    ("spike", "low"),
    ("spike", "high"),
    ("depression", "low"),
    ("depression", "high"),
    ("strip", "low"),
    ("strip", "high"),
    ("missing", "low"),
    ("missing", "high"),
)

PHYSICAL_ARTIFACTS = ARTIFACTS[:6]


def _assignment(
    role, tile, row, col, label,
    category=None, replicate=0,
):
    defect, severity = (
        category if category is not None
        else (None, None)
    )

    return {
        "role": role,
        "tile": tile,
        "row": int(row),
        "col": int(col),
        "label": int(label),
        "defect_type": defect,
        "severity": severity,
        "replicate": int(replicate),
    }


def build_v2_training_plan():
    """63 sites, 63 negatives, 756 physical anomalies."""
    plan = []

    for row in range(9):
        for col in range(7):
            plan.append(
                _assignment(
                    "train", TRAIN_TILE, row, col, 0
                )
            )

            for category in PHYSICAL_ARTIFACTS:
                for replicate in range(2):
                    plan.append(
                        _assignment(
                            "train",
                            TRAIN_TILE,
                            row,
                            col,
                            1,
                            category,
                            replicate,
                        )
                    )

    positives = sum(item["label"] for item in plan)

    if len(plan) != 819 or positives != 756:
        raise RuntimeError(
            "Incorrect training allocation"
        )

    return plan


def build_v2_holdout_plan(tile):
    """Assign synthetic labels using identities only.

    The new NASADEM raster files are never opened.
    The excluded mixed-land location is omitted.
    """
    if tile not in HOLDOUT_TILES:
        raise ValueError(
            "Unregistered V2 holdout tile"
        )

    identities = [
        (row, col)
        for row in range(9)
        for col in range(9)
        if not (
            tile == "s28w069"
            and (row, col) == (5, 2)
        )
    ]

    expected = 81 if tile == "s21w069" else 80

    if len(identities) != expected:
        raise RuntimeError(
            "Invalid frozen holdout inventory"
        )

    stream = HOLDOUT_TILES[tile]

    rng = np.random.default_rng(
        np.random.SeedSequence(
            [SEED, 3, stream]
        )
    )

    positions = rng.choice(
        len(identities),
        size=24,
        replace=False,
    )

    categories = list(ARTIFACTS) * 3

    permutation = rng.permutation(24)

    categories = [
        categories[int(index)]
        for index in permutation
    ]

    chosen = {
        int(index): category
        for index, category
        in zip(positions, categories)
    }

    plan = [
        _assignment(
            "holdout",
            tile,
            row,
            col,
            int(index in chosen),
            chosen.get(index),
        )
        for index, (row, col)
        in enumerate(identities)
    ]

    counts = Counter(
        (item["defect_type"], item["severity"])
        for item in plan
        if item["label"] == 1
    )

    if (
        set(counts) != set(ARTIFACTS)
        or any(count != 3 for count in counts.values())
    ):
        raise RuntimeError(
            "Incorrect holdout category allocation"
        )

    return plan


def _candidate_positions(defect, severity):
    if defect == "spike":
        return [
            (row, col)
            for row in range(1, 9)
            for col in range(1, 9)
        ]

    if defect == "depression":
        return [
            (row, col)
            for row in range(1, 8)
            for col in range(1, 8)
        ]

    if defect == "strip":
        return [
            (0, col)
            for col in range(1, 9)
        ]

    if defect == "missing":
        size = 2 if severity == "low" else 3

        return [
            (row, col)
            for row in range(2, 9 - size)
            for col in range(2, 9 - size)
        ]

    raise ValueError("Unregistered defect type")


def _validate_assignment(a):
    required = {
        "role",
        "tile",
        "row",
        "col",
        "label",
        "defect_type",
        "severity",
        "replicate",
    }

    if not isinstance(a, dict) or set(a) != required:
        raise ValueError(
            "Unexpected assignment schema"
        )

    role = a["role"]
    tile = a["tile"]
    row = a["row"]
    col = a["col"]

    if (
        type(row) is not int
        or type(col) is not int
        or not (0 <= row <= 8 and 0 <= col <= 8)
    ):
        raise ValueError(
            "Invalid sampling coordinates"
        )

    if role == "train":
        if tile != TRAIN_TILE or col > 6:
            raise ValueError(
                "Invalid training identity"
            )

    elif role == "holdout":
        if tile not in HOLDOUT_TILES:
            raise ValueError(
                "Invalid holdout identity"
            )

        if (
            tile == "s28w069"
            and (row, col) == (5, 2)
        ):
            raise ValueError(
                "Excluded mixed-land location"
            )

    else:
        raise ValueError(
            "Unknown assignment role"
        )

    if (
        type(a["label"]) is not int
        or a["label"] not in (0, 1)
    ):
        raise ValueError(
            "Invalid synthetic label"
        )

    replicate = a["replicate"]

    if type(replicate) is not int:
        raise ValueError(
            "Invalid replicate identifier"
        )

    category = (
        a["defect_type"],
        a["severity"],
    )

    if a["label"] == 0:
        if (
            category != (None, None)
            or replicate != 0
        ):
            raise ValueError(
                "Invalid clean assignment"
            )
        return

    allowed = (
        PHYSICAL_ARTIFACTS
        if role == "train"
        else ARTIFACTS
    )

    if category not in allowed:
        raise ValueError(
            "Unregistered synthetic artifact"
        )

    maximum_replicate = (
        1 if role == "train" else 0
    )

    if not (0 <= replicate <= maximum_replicate):
        raise ValueError(
            "Invalid replicate identifier"
        )


def inject_v2_artifact(clean_patch, assignment):
    """Return a modified copy and auditable record.

    Input must be a fully finite 10 x 10 DEM.
    Source arrays are never modified.
    """
    if (
        np.ma.isMaskedArray(clean_patch)
        and np.ma.getmaskarray(clean_patch).any()
    ):
        raise ValueError(
            "Normalize masked source values first"
        )

    original = np.asarray(
        clean_patch,
        dtype=np.float64,
    )

    if (
        original.shape != (10, 10)
        or not np.isfinite(original).all()
    ):
        raise ValueError(
            "Expected fully finite 10 x 10 DEM"
        )

    _validate_assignment(assignment)

    output = original.copy()

    metadata = {
        **assignment,
        "location": None,
        "affected_cells": 0,
        "magnitude_m": None,
    }

    if assignment["label"] == 0:
        return output, metadata

    defect = assignment["defect_type"]
    severity = assignment["severity"]
    category_index = ARTIFACTS.index(
        (defect, severity)
    )

    if assignment["role"] == "train":
        tile_index = 0
        phase_index = 1
    else:
        tile_index = (
            1 + HOLDOUT_TILES[assignment["tile"]]
        )
        phase_index = 2

    seed_prefix = [
        SEED,
        phase_index,
        tile_index,
        assignment["row"],
        assignment["col"],
        category_index,
    ]

    replicate = assignment["replicate"]

    rng = np.random.default_rng(
        np.random.SeedSequence(
            seed_prefix + [replicate]
        )
    )

    candidates = _candidate_positions(
        defect, severity
    )

    position_index = int(
        rng.integers(len(candidates))
    )

    if (
        assignment["role"] == "train"
        and replicate == 1
    ):
        first_rng = np.random.default_rng(
            np.random.SeedSequence(
                seed_prefix + [0]
            )
        )

        first_index = int(
            first_rng.integers(len(candidates))
        )

        # Guarantee distinct replicate locations.
        if position_index == first_index:
            position_index = (
                position_index + 1
            ) % len(candidates)

    row, col = candidates[position_index]

    metadata["location"] = (row, col)

    if defect == "spike":
        magnitude = (
            60.0 if severity == "low"
            else 120.0
        )

        output[row, col] += magnitude
        affected = 1

    elif defect == "depression":
        magnitude = (
            -40.0 if severity == "low"
            else -80.0
        )

        output[
            row:row + 2,
            col:col + 2,
        ] += magnitude

        affected = 4

    elif defect == "strip":
        magnitude = (
            30.0 if severity == "low"
            else 60.0
        )

        output[:, col] += magnitude
        affected = 10

    else:
        magnitude = None

        size = (
            2 if severity == "low"
            else 3
        )

        output[
            row:row + size,
            col:col + size,
        ] = np.nan

        affected = size * size

    metadata["affected_cells"] = affected
    metadata["magnitude_m"] = magnitude

    return output, metadata
