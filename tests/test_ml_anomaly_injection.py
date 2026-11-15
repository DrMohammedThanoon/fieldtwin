"""Synthetic tests for FieldTwin ML-B artifact injection.

No real NASADEM files or model training are used.
"""

from collections import Counter

import numpy as np
import pytest

from science.ml_anomaly_injection import (
    ARTIFACT_CLASSES,
    EVALUATION_DESIGN,
    build_injection_plan,
    inject_dem_artifact,
)


def records_for(tile):
    spec = EVALUATION_DESIGN[tile]
    positions = [
        (r, c)
        for r in range(9)
        for c in range(9)
    ]

    even = [
        (r, c) for r, c in positions
        if (r + c) % 2 == 0
    ][:spec["candidate"]]

    odd = [
        (r, c) for r, c in positions
        if (r + c) % 2 == 1
    ][:spec["assessment"]]

    return [
        {
            "tile": tile,
            "row": r,
            "col": c,
            "partition": (
                "candidate" if (r + c) % 2 == 0
                else "assessment"
            ),
            "land_fraction": 1.0,
            "valid_fraction": 1.0,
            "stencil_fraction": 1.0,
        }
        for r, c in even + odd
    ]


def clean_dem():
    r, c = np.indices((10, 10))
    return 1000.0 + 3.0 * r + 2.0 * c


@pytest.mark.parametrize(
    "tile", ["s25w071", "s24w068"]
)
def test_frozen_counts_and_category_balance(tile):
    spec = EVALUATION_DESIGN[tile]
    plan = build_injection_plan(
        tile, records_for(tile)
    )

    assert len(plan) == spec["eligible"]
    assert sum(x["label"] for x in plan) == spec["positive"]
    assert sum(x["label"] == 0 for x in plan) == (
        spec["eligible"] - spec["positive"]
    )

    counts = Counter(
        (x["defect_type"], x["severity"])
        for x in plan if x["label"] == 1
    )

    assert set(counts) == set(ARTIFACT_CLASSES)
    assert max(counts.values()) - min(counts.values()) <= 1

    identities = [(x["row"], x["col"]) for x in plan]
    assert len(set(identities)) == len(plan)


def test_reproducible_without_input_order_dependence():
    for tile in EVALUATION_DESIGN:
        records = records_for(tile)

        first = build_injection_plan(tile, records)
        second = build_injection_plan(
            tile, list(reversed(records))
        )
        third = build_injection_plan(tile, records)

        assert first == second == third


@pytest.mark.parametrize(
    "defect,severity", ARTIFACT_CLASSES
)
def test_artifact_geometry_magnitude_and_nonmutation(
    defect, severity
):
    plan = build_injection_plan(
        "s25w071", records_for("s25w071")
    )

    assignment = next(
        x for x in plan
        if x["defect_type"] == defect
        and x["severity"] == severity
    )

    original = clean_dem()
    snapshot = original.copy()

    output, audit = inject_dem_artifact(
        original, assignment
    )
    repeated, repeated_audit = inject_dem_artifact(
        original, assignment
    )

    np.testing.assert_array_equal(original, snapshot)
    np.testing.assert_array_equal(output, repeated)
    assert audit == repeated_audit
    assert output.shape == (10, 10)
    assert not np.shares_memory(output, original)

    if defect == "missing":
        expected_cells = 4 if severity == "low" else 9

        assert np.isnan(output).sum() == expected_cells
        np.testing.assert_array_equal(
            output[~np.isnan(output)],
            original[~np.isnan(output)],
        )
        assert audit["affected_cells"] == expected_cells
        assert audit["magnitude_m"] is None
        return

    assert np.isfinite(output).all()

    delta = output - original
    affected = np.argwhere(delta != 0)

    expected_cells = {
        "spike": 1,
        "depression": 4,
        "strip": 10,
    }[defect]

    expected_magnitude = {
        "spike": (60.0, 120.0),
        "depression": (-40.0, -80.0),
        "strip": (30.0, 60.0),
    }[defect][int(severity == "high")]

    assert len(affected) == expected_cells
    assert audit["affected_cells"] == expected_cells
    assert audit["magnitude_m"] == expected_magnitude

    np.testing.assert_allclose(
        delta[delta != 0],
        expected_magnitude,
    )

    if defect == "spike":
        assert 1 <= affected[0, 0] <= 8
        assert 1 <= affected[0, 1] <= 8
    elif defect == "depression":
        assert len(set(affected[:, 0])) == 2
        assert len(set(affected[:, 1])) == 2
    elif defect == "strip":
        assert len(set(affected[:, 0])) == 10
        assert len(set(affected[:, 1])) == 1


def test_untouched_patch_is_a_separate_copy():
    plan = build_injection_plan(
        "s25w071", records_for("s25w071")
    )
    assignment = next(
        x for x in plan if x["label"] == 0
    )

    original = clean_dem()
    output, audit = inject_dem_artifact(
        original, assignment
    )

    np.testing.assert_array_equal(output, original)
    assert not np.shares_memory(output, original)
    assert audit["affected_cells"] == 0
    assert audit["magnitude_m"] is None


def test_reject_invalid_plan_inputs():
    tile = "s25w071"
    good = records_for(tile)

    duplicated = [dict(x) for x in good]
    duplicated[1]["row"] = duplicated[0]["row"]
    duplicated[1]["col"] = duplicated[0]["col"]

    with pytest.raises(ValueError):
        build_injection_plan(tile, duplicated)

    water = [dict(x) for x in good]
    water[0]["land_fraction"] = 0.5

    with pytest.raises(ValueError):
        build_injection_plan(tile, water)

    with pytest.raises(ValueError):
        build_injection_plan(tile, good[:-1])

    with pytest.raises(ValueError):
        build_injection_plan("unknown_tile", good)


def test_reject_invalid_injection_inputs():
    plan = build_injection_plan(
        "s25w071", records_for("s25w071")
    )
    positive = next(x for x in plan if x["label"] == 1)

    with pytest.raises(ValueError):
        inject_dem_artifact(
            np.ones((9, 10)), positive
        )

    invalid_dem = clean_dem()
    invalid_dem[0, 0] = np.nan

    with pytest.raises(ValueError):
        inject_dem_artifact(invalid_dem, positive)

    invalid_assignment = dict(positive)
    invalid_assignment["defect_type"] = "unknown"

    with pytest.raises(ValueError):
        inject_dem_artifact(
            clean_dem(), invalid_assignment
        )
