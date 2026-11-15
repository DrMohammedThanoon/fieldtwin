"""Synthetic verification of ML-B numerical descriptors."""

import numpy as np
import pytest

from science.ml_anomaly_features import (
    FEATURE_NAMES,
    anomaly_feature_matrix,
    describe_dem_patch,
)


def plane():
    row, col = np.indices((10, 10))
    return 1000.0 + 3.0 * row + 2.0 * col


def test_clean_plane():
    result = describe_dem_patch(plane())

    assert tuple(result) == FEATURE_NAMES
    assert result["missing_fraction"] == 0.0
    assert result["adjacent_abs_diff_max_m"] == 3.0
    assert result["adjacent_abs_diff_p95_m"] == 3.0
    assert result["plane_residual_rms_m"] < 1e-8
    assert result["local_median_residual_max_m"] < 1e-8


def test_spike_increases_local_discontinuity():
    clean = plane()
    damaged = clean.copy()
    damaged[4, 5] += 120.0

    before = describe_dem_patch(clean)
    after = describe_dem_patch(damaged)

    assert (
        after["adjacent_abs_diff_max_m"]
        > before["adjacent_abs_diff_max_m"]
    )
    assert after["local_median_residual_max_m"] > 100
    assert after["missing_fraction"] == 0.0


def test_depression_and_strip():
    clean = plane()

    depression = clean.copy()
    depression[4:6, 4:6] -= 40.0

    strip = clean.copy()
    strip[:, 5] += 30.0

    for damaged in (depression, strip):
        result = describe_dem_patch(damaged)
        assert result["adjacent_abs_diff_max_m"] >= 28
        assert result["plane_residual_rms_m"] > 0


def test_missing_block():
    damaged = plane()
    damaged[3:6, 4:7] = np.nan

    result = describe_dem_patch(damaged)

    assert result["missing_fraction"] == pytest.approx(0.09)
    assert np.isfinite(list(result.values())).all()


def test_height_translation_invariance():
    original = describe_dem_patch(plane())
    translated = describe_dem_patch(plane() + 5000.0)

    np.testing.assert_allclose(
        list(original.values()),
        list(translated.values()),
        atol=1e-8,
        rtol=1e-9,
    )


def test_invalid_inputs_rejected():
    with pytest.raises(ValueError):
        describe_dem_patch(np.ones((9, 10)))

    with pytest.raises(ValueError):
        describe_dem_patch(np.full((10, 10), np.nan))

    invalid = plane()
    invalid[0, 0] = np.inf

    with pytest.raises(ValueError):
        describe_dem_patch(invalid)

    with pytest.raises(ValueError):
        describe_dem_patch(plane(), pixel_size_m=90)


def test_input_unchanged_and_matrix_shape():
    original = plane()
    original[4, 4] = np.nan

    snapshot = original.copy()
    describe_dem_patch(original)

    np.testing.assert_array_equal(original, snapshot)

    matrix = anomaly_feature_matrix(
        [plane(), original]
    )
    assert matrix.shape == (2, 6)
    assert np.isfinite(matrix).all()
