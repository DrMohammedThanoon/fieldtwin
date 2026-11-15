"""Synthetic tests for the FieldTwin ML-A evaluation pipeline.

No real holdout performance is calculated here.
"""

import numpy as np
import pytest
from types import SimpleNamespace
from sklearn.preprocessing import StandardScaler

from science.ml_discovery import fit_discovery_model
from science.evaluate_ml import (
    _farthest_first,
    _validate_partitions,
    evaluate_tile,
    representation_distance,
)
from science.ml_terrain import FEATURE_KEYS


def make_record(tile, row, col, partition):
    """Generate deterministic synthetic terrain descriptors."""
    features = (
        float(row + 0.3 * col + 1),
        float(2 * col + 0.4 * row + 1),
        float((3 * row + 5 * col) % 17 + 1),
        float((row - col) ** 2 + 0.2),
        float(np.sin(row / 2) + np.cos(col / 3) + 3),
    )

    record = {
        "tile": tile,
        "row": row,
        "col": col,
        "lat": -24.9 + row * 0.1,
        "lon": -70.9 + col * 0.1,
        "x_m": float(col * 10000),
        "y_m": float(row * 10000),
        "partition": partition,
        "land_fraction": 1.0,
        "valid_fraction": 1.0,
        "stencil_fraction": 1.0,
    }

    record.update(dict(zip(FEATURE_KEYS, features)))
    return record


def make_evaluation():
    tile = "s25w071"

    candidate_positions = [
        (r, c)
        for r in range(9)
        for c in range(9)
        if (r + c) % 2 == 0
    ][:22]

    assessment_positions = [
        (r, c)
        for r in range(9)
        for c in range(9)
        if (r + c) % 2 == 1
    ][:22]

    candidates = [
        make_record(tile, r, c, "candidate")
        for r, c in candidate_positions
    ]

    assessment = [
        make_record(tile, r, c, "assessment")
        for r, c in assessment_positions
    ]

    return candidates, assessment


def test_farthest_first_known_geometry():
    points = np.arange(5, dtype=float).reshape(-1, 1)

    assert _farthest_first(
        points, first=0, budget=3
    ) == [0, 4, 2]


def test_partition_validation_and_land_rejection():
    candidates, assessment = make_evaluation()

    assert _validate_partitions(
        candidates, assessment
    ) == "s25w071"

    bad = [dict(r) for r in candidates]
    bad[0]["partition"] = "assessment"

    with pytest.raises(ValueError):
        _validate_partitions(bad, assessment)

    water = [dict(r) for r in assessment]
    water[0]["land_fraction"] = 0.0

    with pytest.raises(ValueError):
        _validate_partitions(candidates, water)

    duplicates = [dict(r) for r in assessment]
    duplicates[1]["row"] = duplicates[0]["row"]
    duplicates[1]["col"] = duplicates[0]["col"]

    with pytest.raises(ValueError):
        _validate_partitions(candidates, duplicates)


def test_representation_distance_known_value():
    scaler = StandardScaler().fit(
        np.array([[0.0] * 5, [2.0] * 5])
    )
    model = SimpleNamespace(scaler=scaler)

    selected = [
        dict(zip(FEATURE_KEYS, [0.0] * 5)),
    ]
    assessment = [
        dict(zip(FEATURE_KEYS, [1.0] * 5)),
    ]

    result = representation_distance(
        model, selected, assessment
    )

    assert result == pytest.approx(np.sqrt(5))


def test_synthetic_end_to_end_no_assessment_selection_leakage():
    development = [
        make_record("s25w070", r, c, "development")
        for r in range(9)
        for c in range(9)
    ]

    model = fit_discovery_model(development)
    candidates, assessment = make_evaluation()

    result = evaluate_tile(
        model, candidates, assessment
    )

    assert result["development_samples"] == 81
    assert result["candidate_samples"] == 22
    assert result["assessment_samples"] == 22
    assert result["selection_budget"] == 8
    assert len(result["selected_ml_sites"]) == 8
    assert result["scores"]["random_trials"] == 30

    assert all(
        np.isfinite(value)
        for key, value in result["scores"].items()
        if key != "random_trials"
    )

    # Change reserved assessment features substantially.
    # This may change scores but must not change selection.
    changed = [dict(r) for r in assessment]

    for record in changed:
        for key in FEATURE_KEYS:
            record[key] += 1000.0

    repeated = evaluate_tile(
        model, candidates, changed
    )

    assert (
        result["selected_ml_sites"]
        == repeated["selected_ml_sites"]
    )

    assert (
        result["both_gates_pass"]
        ==
        (
            result["geographic_gate"]
            and result["physical_gate"]
        )
    )
