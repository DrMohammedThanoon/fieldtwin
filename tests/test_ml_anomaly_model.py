"""Synthetic tests for FieldTwin ML-B anomaly models.

No real NASADEM data or geographic holdouts are used.
"""

from dataclasses import replace

import numpy as np
import pytest

from science.ml_anomaly_features import (
    FEATURE_NAMES,
    anomaly_feature_matrix,
)
from science.ml_anomaly_model import (
    RANDOM_SEED,
    N_ESTIMATORS,
    MAX_SAMPLES,
    fit_anomaly_screeners,
    score_anomaly_patches,
)


@pytest.fixture(scope="module")
def development():
    records = []

    for row in range(9):
        for col in range(9):
            y, x = np.indices((10, 10))

            elevation = (
                1000.0
                + 2.1 * y
                + 1.7 * x
                + (0.08 + 0.025 * row) * (x - 4.5) ** 2
                + (0.05 + 0.030 * col) * (y - 4.5) ** 2
                + (0.6 + 0.4 * ((row + col) % 5))
                * np.sin(
                    (x + 0.25 * row)
                    * (y + 0.35 * col) / 8.0
                )
            )

            records.append({
                "tile": "s25w070",
                "row": row,
                "col": col,
                "partition": "development",
                "land_fraction": 1.0,
                "valid_fraction": 1.0,
                "stencil_fraction": 1.0,
                "elevation": elevation,
            })

    return records


@pytest.fixture(scope="module")
def fitted(development):
    return fit_anomaly_screeners(development)


def test_model_configuration_and_training(fitted):
    assert fitted.training_count == 81
    assert fitted.feature_names == FEATURE_NAMES

    assert fitted.forest.n_estimators == N_ESTIMATORS == 300
    assert fitted.forest.max_samples == MAX_SAMPLES == 64
    assert fitted.forest.random_state == RANDOM_SEED
    assert fitted.forest.contamination == "auto"
    assert fitted.forest.bootstrap is False

    assert fitted.scaler.n_features_in_ == 6
    assert fitted.robust_center.shape == (6,)
    assert fitted.robust_scale.shape == (6,)

    assert np.isfinite(fitted.robust_center).all()
    assert np.isfinite(fitted.robust_scale).all()
    assert np.all(fitted.robust_scale > 0)


def test_development_only_calibration(fitted, development):
    features = anomaly_feature_matrix(
        [r["elevation"] for r in development]
    )

    scaled = fitted.scaler.transform(features)

    forest_scores = -fitted.forest.score_samples(scaled)

    robust_scores = np.max(
        np.abs(
            (features - fitted.robust_center)
            / fitted.robust_scale
        ),
        axis=1,
    )

    expected_forest_threshold = np.percentile(
        forest_scores, 95, method="linear"
    )
    expected_robust_threshold = np.percentile(
        robust_scores, 95, method="linear"
    )

    assert fitted.forest_threshold == pytest.approx(
        expected_forest_threshold
    )
    assert fitted.robust_threshold == pytest.approx(
        expected_robust_threshold
    )

    # With strict > 95th-percentile thresholds,
    # no more than four of 81 training cases
    # should be above either threshold.
    assert np.sum(
        forest_scores > fitted.forest_threshold
    ) <= 4

    assert np.sum(
        robust_scores > fitted.robust_threshold
    ) <= 4


def test_deterministic_training(fitted, development):
    repeated = fit_anomaly_screeners(
        list(reversed(development))
    )

    patches = [
        r["elevation"] for r in development[:12]
    ]

    first = score_anomaly_patches(fitted, patches)
    second = score_anomaly_patches(repeated, patches)

    np.testing.assert_allclose(
        first["forest_scores"],
        second["forest_scores"],
        rtol=0,
        atol=1e-12,
    )

    np.testing.assert_allclose(
        first["robust_scores"],
        second["robust_scores"],
        rtol=0,
        atol=1e-12,
    )

    assert repeated.forest_threshold == pytest.approx(
        fitted.forest_threshold
    )
    assert repeated.robust_threshold == pytest.approx(
        fitted.robust_threshold
    )


def test_invalid_training_inputs_rejected(development):
    with pytest.raises(ValueError):
        fit_anomaly_screeners(development[:-1])

    wrong_tile = [dict(r) for r in development]
    wrong_tile[0]["tile"] = "s25w071"

    with pytest.raises(ValueError):
        fit_anomaly_screeners(wrong_tile)

    duplicated = [dict(r) for r in development]
    duplicated[1]["row"] = duplicated[0]["row"]
    duplicated[1]["col"] = duplicated[0]["col"]

    with pytest.raises(ValueError):
        fit_anomaly_screeners(duplicated)

    ineligible = [dict(r) for r in development]
    ineligible[0]["land_fraction"] = 0.5

    with pytest.raises(ValueError):
        fit_anomaly_screeners(ineligible)

    invalid = [dict(r) for r in development]
    elevation = invalid[0]["elevation"].copy()
    elevation[0, 0] = np.nan
    invalid[0]["elevation"] = elevation

    with pytest.raises(ValueError):
        fit_anomaly_screeners(invalid)


def test_anomaly_scores_flags_and_nonmutation(
    fitted, development
):
    clean = development[0]["elevation"].copy()
    spike = clean.copy()
    missing = clean.copy()

    spike[4, 5] += 120.0
    missing[3:6, 4:7] = np.nan

    snapshot = clean.copy()
    spike_snapshot = spike.copy()
    missing_snapshot = missing.copy()

    patches = [clean, spike, missing]

    result = score_anomaly_patches(
        fitted, patches
    )

    for key in ("forest_scores", "robust_scores"):
        assert result[key].shape == (3,)
        assert np.isfinite(result[key]).all()

    for key in ("forest_flags", "robust_flags"):
        assert result[key].shape == (3,)
        assert result[key].dtype == np.bool_

    np.testing.assert_array_equal(
        clean, snapshot
    )
    np.testing.assert_array_equal(
        spike, spike_snapshot
    )
    np.testing.assert_array_equal(
        missing, missing_snapshot
    )

    assert np.array_equal(
        result["forest_flags"],
        result["forest_scores"]
        > fitted.forest_threshold,
    )

    assert np.array_equal(
        result["robust_flags"],
        result["robust_scores"]
        > fitted.robust_threshold,
    )

    features = anomaly_feature_matrix(patches)

    expected_robust_scores = np.max(
        np.abs(
            (features - fitted.robust_center)
            / fitted.robust_scale
        ),
        axis=1,
    )

    np.testing.assert_allclose(
        result["robust_scores"],
        expected_robust_scores,
    )


def test_zero_mad_fallback_and_scoring_guards(
    fitted, development
):
    # All clean development patches have zero
    # missing-data fraction. The frozen fallback
    # must prevent division by zero.
    assert fitted.robust_center[0] == 0.0
    assert fitted.robust_scale[0] == pytest.approx(0.01)

    with pytest.raises(ValueError):
        score_anomaly_patches(
            fitted, [np.ones((9, 10))]
        )

    with pytest.raises(ValueError):
        score_anomaly_patches(
            fitted, [np.full((10, 10), np.nan)]
        )

    altered = replace(
        fitted,
        feature_names=("wrong",),
    )

    with pytest.raises(ValueError):
        score_anomaly_patches(
            altered,
            [development[0]["elevation"]],
        )
