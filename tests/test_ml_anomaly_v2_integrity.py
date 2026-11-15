"""Tests for the ML-B V2 deterministic integrity layer."""

import numpy as np
import pytest

from science.ml_anomaly_v2_integrity import (
    MIN_VALID_CELLS,
    inspect_dem_integrity,
)


def clean_patch():
    return np.full((10, 10), 1000.0)


def test_clean_patch_passes():
    result = inspect_dem_integrity(clean_patch())

    assert not result.is_alert
    assert result.can_score_ml
    assert result.valid_count == 100
    assert result.nan_count == 0
    assert result.inf_count == 0
    assert result.missing_fraction == 0.0
    assert result.valid_fraction == 1.0
    assert result.reason_codes == ()


@pytest.mark.parametrize(
    "block_size, expected_missing",
    [(2, 4), (3, 9)],
)
def test_missing_blocks_detected(block_size, expected_missing):
    z = clean_patch()
    z[3:3 + block_size, 3:3 + block_size] = np.nan

    original_bytes = z.tobytes()
    result = inspect_dem_integrity(z)

    assert result.is_alert
    assert not result.can_score_ml
    assert result.nan_count == expected_missing
    assert result.inf_count == 0
    assert result.missing_fraction == expected_missing / 100
    assert result.reason_codes == ("MISSING_ELEVATION",)
    assert z.tobytes() == original_bytes


@pytest.mark.parametrize("invalid", [np.inf, -np.inf])
def test_infinite_elevations_detected(invalid):
    z = clean_patch()
    z[4, 4] = invalid

    result = inspect_dem_integrity(z)

    assert result.is_alert
    assert not result.can_score_ml
    assert result.inf_count == 1
    assert result.nan_count == 0
    assert result.reason_codes == (
        "INVALID_INFINITE_ELEVATION",
    )


def test_exact_minimum_valid_coverage():
    z = clean_patch()
    z.flat[:25] = np.nan

    result = inspect_dem_integrity(z)

    assert MIN_VALID_CELLS == 75
    assert result.valid_count == 75
    assert result.reason_codes == ("MISSING_ELEVATION",)


def test_insufficient_valid_coverage():
    z = clean_patch()
    z.flat[:26] = np.nan

    result = inspect_dem_integrity(z)

    assert result.valid_count == 74
    assert result.reason_codes == (
        "MISSING_ELEVATION",
        "INSUFFICIENT_VALID_COVERAGE",
    )


def test_entirely_missing_patch():
    result = inspect_dem_integrity(
        np.full((10, 10), np.nan)
    )

    assert result.valid_count == 0
    assert result.nan_count == 100
    assert result.missing_fraction == 1.0
    assert result.is_alert


def test_mixed_missing_and_infinite():
    z = clean_patch()
    z[1, 1] = np.nan
    z[2, 2] = np.inf

    result = inspect_dem_integrity(z)

    assert result.valid_count == 98
    assert result.nan_count == 1
    assert result.inf_count == 1
    assert result.reason_codes == (
        "MISSING_ELEVATION",
        "INVALID_INFINITE_ELEVATION",
    )


@pytest.mark.parametrize(
    "shape",
    [(9, 10), (10, 9), (100,), (11, 10)],
)
def test_invalid_dimensions_rejected(shape):
    with pytest.raises(ValueError, match="Expected"):
        inspect_dem_integrity(np.zeros(shape))


def test_masked_input_rejected():
    z = np.ma.array(clean_patch())
    z.mask = np.zeros((10, 10), dtype=bool)
    z.mask[3, 3] = True

    with pytest.raises(ValueError, match="masked"):
        inspect_dem_integrity(z)


def test_finite_extreme_is_not_automatically_an_error():
    z = clean_patch()
    z[4, 4] += 120.0

    result = inspect_dem_integrity(z)

    assert result.can_score_ml
    assert not result.is_alert
