"""Synthetic-only tests for prospective V2 holdout loader."""

import numpy as np
import pytest

from science.ml_anomaly_v2_injection import (
    build_v2_holdout_plan,
)
from science.ml_anomaly_v2_holdout import (
    EXPECTED_ELIGIBLE,
    assemble_holdout_records,
    extract_v2_holdout_tile,
    frozen_holdout_grid,
    validate_holdout_land_screens,
)


def synthetic_screens(tile):
    screens = {
        (row, col): np.zeros(
            (10, 10), dtype=np.uint8
        )
        for row in range(9)
        for col in range(9)
    }

    if tile == "s28w069":
        screens[(5, 2)][2:6, 2:6] = 255

    return screens


def synthetic_elevations(tile):
    eligible = validate_holdout_land_screens(
        tile, synthetic_screens(tile)
    )

    rr, cc = np.indices((10, 10))

    return {
        identity: (
            1000 + rr * 0.5 + cc * 1.5
        ).astype(float)
        for identity in eligible
    }


@pytest.mark.parametrize(
    "tile,south,expected",
    [
        ("s21w069", -20.9, 81),
        ("s28w069", -27.9, 80),
    ],
)
def test_frozen_grid(tile, south, expected):
    grid = frozen_holdout_grid(tile)

    assert len(grid) == 81
    assert grid[0]["row"] == 0
    assert grid[0]["col"] == 0
    assert grid[0]["lat"] == south
    assert grid[0]["lon"] == -68.9

    assert grid[-1]["row"] == 8
    assert grid[-1]["col"] == 8
    assert grid[-1]["lat"] == pytest.approx(
        south + 0.8
    )
    assert grid[-1]["lon"] == -68.1

    assert EXPECTED_ELIGIBLE[tile] == expected

    assert all(
        np.isfinite(
            [p["x_m"], p["y_m"]]
        ).all()
        for p in grid
    )


@pytest.mark.parametrize(
    "tile,expected",
    [
        ("s21w069", 81),
        ("s28w069", 80),
    ],
)
def test_frozen_land_eligibility(tile, expected):
    eligible = validate_holdout_land_screens(
        tile, synthetic_screens(tile)
    )

    assert len(eligible) == expected
    assert all(
        fraction == 1.0
        for fraction in eligible.values()
    )

    plan = build_v2_holdout_plan(tile)

    assert set(eligible) == {
        (a["row"], a["col"])
        for a in plan
    }

    if tile == "s28w069":
        assert (5, 2) not in eligible


def test_frozen_mixed_fraction():
    screens = synthetic_screens("s28w069")

    assert np.mean(
        screens[(5, 2)] == 0
    ) == pytest.approx(0.84)


def test_missing_frozen_exclusion_rejected():
    screens = synthetic_screens("s28w069")
    screens[(5, 2)][:] = 0

    with pytest.raises(
        ValueError, match="exclusion inventory"
    ):
        validate_holdout_land_screens(
            "s28w069", screens
        )


def test_unexpected_exclusion_rejected():
    screens = synthetic_screens("s21w069")
    screens[(0, 0)][1, 1] = 255

    with pytest.raises(
        ValueError, match="exclusion inventory"
    ):
        validate_holdout_land_screens(
            "s21w069", screens
        )


def test_water_only_exclusion_rejected():
    screens = synthetic_screens("s28w069")
    screens[(5, 2)][:] = 255

    with pytest.raises(
        ValueError, match="mixed"
    ):
        validate_holdout_land_screens(
            "s28w069", screens
        )


def test_invalid_swb_code_rejected():
    screens = synthetic_screens("s21w069")
    screens[(0, 0)][0, 0] = 127

    with pytest.raises(
        ValueError, match="SWB class"
    ):
        validate_holdout_land_screens(
            "s21w069", screens
        )


def test_missing_swb_identity_rejected():
    screens = synthetic_screens("s21w069")
    del screens[(0, 0)]

    with pytest.raises(
        ValueError, match="81-site"
    ):
        validate_holdout_land_screens(
            "s21w069", screens
        )


@pytest.mark.parametrize(
    "tile,expected",
    [
        ("s21w069", 81),
        ("s28w069", 80),
    ],
)
def test_assemble_synthetic_holdouts(tile, expected):
    screens = synthetic_screens(tile)
    patches = synthetic_elevations(tile)

    original = {
        key: value.copy()
        for key, value in patches.items()
    }

    records = assemble_holdout_records(
        tile, screens, patches
    )

    assert len(records) == expected

    assert {
        (r["row"], r["col"])
        for r in records
    } == set(patches)

    for record in records:
        identity = (
            record["row"],
            record["col"]
        )

        assert record["tile"] == tile
        assert record["partition"] == "holdout"
        assert record["land_fraction"] == 1.0
        assert record["valid_fraction"] == 1.0
        assert record["elevation"].shape == (10, 10)
        assert np.isfinite(
            record["elevation"]
        ).all()

        assert np.array_equal(
            patches[identity],
            original[identity],
        )

        assert record["elevation"] is not (
            patches[identity]
        )

    records[0]["elevation"][0, 0] += 1000

    assert np.array_equal(
        patches[
            (records[0]["row"], records[0]["col"])
        ],
        original[
            (records[0]["row"], records[0]["col"])
        ],
    )


@pytest.mark.parametrize(
    "bad_value",
    [np.nan, np.inf],
)
def test_nonfinite_elevation_rejected(bad_value):
    patches = synthetic_elevations("s21w069")
    patches[(0, 0)][3, 3] = bad_value

    with pytest.raises(
        ValueError, match="Nonfinite"
    ):
        assemble_holdout_records(
            "s21w069",
            synthetic_screens("s21w069"),
            patches,
        )


def test_missing_elevation_identity_rejected():
    patches = synthetic_elevations("s21w069")
    del patches[(0, 0)]

    with pytest.raises(
        ValueError, match="identities"
    ):
        assemble_holdout_records(
            "s21w069",
            synthetic_screens("s21w069"),
            patches,
        )


def test_wrong_patch_dimensions_rejected():
    patches = synthetic_elevations("s21w069")
    patches[(0, 0)] = np.zeros((9, 10))

    with pytest.raises(
        ValueError, match="shaped"
    ):
        assemble_holdout_records(
            "s21w069",
            synthetic_screens("s21w069"),
            patches,
        )


def test_original_evaluation_tiles_rejected():
    for tile in (
        "s25w070",
        "s25w071",
        "s24w068",
    ):
        with pytest.raises(ValueError):
            frozen_holdout_grid(tile)

        with pytest.raises(ValueError):
            extract_v2_holdout_tile(tile)
