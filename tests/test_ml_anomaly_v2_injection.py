"""Tests for prospective ML-B V2 synthetic defects."""

from collections import Counter

import numpy as np
import pytest

from science.ml_anomaly_v2_injection import (
    ARTIFACTS,
    PHYSICAL_ARTIFACTS,
    SEED,
    build_v2_training_plan,
    build_v2_holdout_plan,
    inject_v2_artifact,
)


def terrain():
    rows, cols = np.indices((10, 10))

    return (
        1000 + 0.3 * rows + 1.7 * cols
    ).astype(float)


def test_frozen_training_inventory():
    plan = build_v2_training_plan()

    assert len(plan) == 819
    assert sum(a["label"] for a in plan) == 756

    sites = {
        (a["row"], a["col"])
        for a in plan
    }

    assert len(sites) == 63
    assert all(
        a["tile"] == "s25w070"
        and a["col"] <= 6
        for a in plan
    )

    actual = Counter(
        (a["defect_type"], a["severity"])
        for a in plan if a["label"]
    )

    assert actual == {
        category: 126
        for category in PHYSICAL_ARTIFACTS
    }

    for row in range(9):
        for col in range(7):
            count = sum(
                (a["row"], a["col"]) == (row, col)
                for a in plan
            )

            assert count == 13

    assert SEED == 20261116


@pytest.mark.parametrize(
    "tile,expected",
    [
        ("s21w069", 81),
        ("s28w069", 80),
    ],
)
def test_holdout_assignments_are_reproducible(
    tile, expected
):
    first = build_v2_holdout_plan(tile)
    second = build_v2_holdout_plan(tile)

    assert first == second
    assert len(first) == expected
    assert sum(a["label"] for a in first) == 24

    actual = Counter(
        (a["defect_type"], a["severity"])
        for a in first if a["label"]
    )

    assert actual == {
        category: 3
        for category in ARTIFACTS
    }

    identities = {
        (a["row"], a["col"])
        for a in first
    }

    assert len(identities) == expected

    if tile == "s28w069":
        assert (5, 2) not in identities


def test_original_holdouts_are_rejected():
    with pytest.raises(ValueError):
        build_v2_holdout_plan("s25w071")


@pytest.mark.parametrize(
    "category,changed,magnitude",
    [
        (("spike", "low"), 1, 60.0),
        (("spike", "high"), 1, 120.0),
        (("depression", "low"), 4, -40.0),
        (("depression", "high"), 4, -80.0),
        (("strip", "low"), 10, 30.0),
        (("strip", "high"), 10, 60.0),
    ],
)
def test_physical_defect_and_source_preservation(
    category, changed, magnitude
):
    assignment = next(
        a for a in build_v2_training_plan()
        if a["label"]
        and (
            a["defect_type"],
            a["severity"],
        ) == category
    )

    original = terrain()
    before = original.copy()

    output, metadata = inject_v2_artifact(
        original, assignment
    )

    assert np.array_equal(original, before)
    assert np.isfinite(output).all()

    differences = output - original

    assert np.count_nonzero(differences) == changed

    assert np.allclose(
        differences[differences != 0],
        magnitude,
    )

    assert metadata["affected_cells"] == changed
    assert metadata["magnitude_m"] == magnitude

    repeated, repeated_metadata = inject_v2_artifact(
        original, assignment
    )

    assert np.array_equal(output, repeated)
    assert metadata == repeated_metadata


@pytest.mark.parametrize(
    "severity,missing",
    [
        ("low", 4),
        ("high", 9),
    ],
)
def test_missing_blocks_are_holdout_only(
    severity, missing
):
    assignment = next(
        a for a in build_v2_holdout_plan("s28w069")
        if a["defect_type"] == "missing"
        and a["severity"] == severity
    )

    original = terrain()

    output, metadata = inject_v2_artifact(
        original, assignment
    )

    assert np.isnan(output).sum() == missing

    assert np.array_equal(
        original, terrain()
    )

    assert metadata["affected_cells"] == missing
    assert metadata["magnitude_m"] is None


def test_training_replicates_have_distinct_locations():
    plan = build_v2_training_plan()

    for defect, severity in PHYSICAL_ARTIFACTS:
        assignments = [
            a for a in plan
            if a["row"] == 3
            and a["col"] == 3
            and a["defect_type"] == defect
            and a["severity"] == severity
        ]

        assert len(assignments) == 2

        first = inject_v2_artifact(
            terrain(), assignments[0]
        )[1]

        second = inject_v2_artifact(
            terrain(), assignments[1]
        )[1]

        assert first["location"] != second["location"]


def test_clean_assignment_creates_separate_copy():
    assignment = next(
        a for a in build_v2_training_plan()
        if not a["label"]
    )

    source = terrain()

    output, metadata = inject_v2_artifact(
        source, assignment
    )

    assert np.array_equal(output, source)
    assert output is not source
    assert metadata["affected_cells"] == 0


def test_invalid_inputs_are_rejected():
    assignment = build_v2_training_plan()[1]

    with pytest.raises(ValueError):
        inject_v2_artifact(
            np.zeros((9, 10)), assignment
        )

    z = terrain()
    z[2, 2] = np.nan

    with pytest.raises(ValueError):
        inject_v2_artifact(z, assignment)

    z = terrain()
    z[2, 2] = np.inf

    with pytest.raises(ValueError):
        inject_v2_artifact(z, assignment)

    with pytest.raises(ValueError):
        inject_v2_artifact(
            terrain(),
            {**assignment, "col": 8},
        )

    with pytest.raises(ValueError):
        inject_v2_artifact(
            terrain(),
            {**assignment, "replicate": 3},
        )

    with pytest.raises(ValueError):
        inject_v2_artifact(
            terrain(),
            {
                **assignment,
                "defect_type": "missing",
            },
        )


def test_masked_source_values_are_rejected():
    z = np.ma.array(terrain())

    z.mask = np.zeros(
        (10, 10),
        dtype=bool,
    )

    z.mask[0, 0] = True

    with pytest.raises(ValueError):
        inject_v2_artifact(
            z,
            build_v2_training_plan()[0],
        )
