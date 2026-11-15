"""Toy-only tests for ML-B V2 scoring and leakage guards."""

import numpy as np
import pytest

from science.ml_anomaly_v2_injection import (
    build_v2_training_plan,
)
from science.ml_anomaly_v2_model import (
    CALIBRATION_SITES,
    MODEL_NAMES,
    PHYSICAL_FEATURE_NAMES,
    calibration_thresholds,
    fit_robust_reference,
    fit_v2_models,
    physical_feature_matrix,
    score_robust,
    threshold_flags,
)


@pytest.fixture(scope="module")
def toy_case():
    """Artificial numeric features, not NASADEM data."""
    plan = build_v2_training_plan()
    rng = np.random.default_rng(7391)

    train = rng.normal(size=(819, 5))
    labels = np.array(
        [item["label"] for item in plan]
    )

    train[:, 0] += labels * 3.0
    calibration = rng.normal(size=(18, 5))

    return train, plan, calibration


@pytest.fixture(scope="module")
def toy_models(toy_case):
    train, plan, calibration = toy_case

    return fit_v2_models(
        train,
        plan,
        calibration,
        CALIBRATION_SITES,
    )


def test_five_original_physical_descriptors():
    assert len(PHYSICAL_FEATURE_NAMES) == 5
    assert "missing_fraction" not in PHYSICAL_FEATURE_NAMES

    z = np.arange(100, dtype=float).reshape(10, 10)
    original = z.copy()

    result = physical_feature_matrix([z, z])

    assert result.shape == (2, 5)
    assert np.isfinite(result).all()
    assert np.array_equal(z, original)


@pytest.mark.parametrize("invalid", [np.nan, np.inf])
def test_integrity_alert_cannot_be_ml_scored(invalid):
    z = np.ones((10, 10))
    z[3, 3] = invalid

    with pytest.raises(ValueError):
        physical_feature_matrix([z])


def test_robust_zero_mad_fallback_and_max_score():
    clean = np.array([
        [0, 1, 9, 0, 0],
        [0, 3, 9, 2, 0],
        [0, 5, 9, 4, 0],
    ], dtype=float)

    center, scale = fit_robust_reference(clean)

    assert np.array_equal(
        center, [0, 3, 9, 2, 0]
    )
    assert np.allclose(
        scale,
        [1, 2 * 1.4826, 1, 2 * 1.4826, 1],
    )

    values = score_robust(
        np.array([[2, 3, 9, 2, 0]], dtype=float),
        center,
        scale,
    )

    assert np.allclose(values, [2.0])


def test_frozen_estimator_specifications(toy_models):
    rf = toy_models.random_forest
    lr = toy_models.logistic_regression

    assert rf.n_estimators == 300
    assert rf.max_depth == 8
    assert rf.min_samples_leaf == 3
    assert rf.max_features == "sqrt"
    assert rf.class_weight == "balanced_subsample"
    assert rf.bootstrap is True
    assert rf.random_state == 20261116
    assert rf.n_jobs == 1

    assert lr.named_steps["scaler"].__class__.__name__ == (
        "StandardScaler"
    )

    classifier = lr.named_steps["classifier"]

    assert classifier.class_weight == "balanced"
    assert classifier.solver == "lbfgs"
    assert classifier.max_iter == 5000
    assert classifier.random_state == 20261116


def test_three_finite_score_vectors(toy_models):
    example = np.zeros((4, 5), dtype=float)
    original = example.copy()

    scores = toy_models.score(example)
    flags = toy_models.flags(example)

    assert set(scores) == set(MODEL_NAMES)
    assert set(flags) == set(MODEL_NAMES)

    for name in MODEL_NAMES:
        assert scores[name].shape == (4,)
        assert flags[name].shape == (4,)
        assert np.isfinite(scores[name]).all()
        assert flags[name].dtype == bool

    for name in MODEL_NAMES[:2]:
        assert np.all(scores[name] >= 0)
        assert np.all(scores[name] <= 1)

    assert np.array_equal(example, original)


def test_calibration_uses_linear_percentile():
    scores = {
        name: np.arange(18, dtype=float)
        for name in MODEL_NAMES
    }

    thresholds = calibration_thresholds(scores)

    for threshold in thresholds.values():
        assert threshold == pytest.approx(16.15)


def test_threshold_comparison_is_strict():
    values = {
        name: np.array([0.4, 0.5, 0.6])
        for name in MODEL_NAMES
    }

    limits = {name: 0.5 for name in MODEL_NAMES}
    flags = threshold_flags(values, limits)

    for result in flags.values():
        assert result.tolist() == [False, False, True]


def test_calibration_identity_leakage_rejected(toy_case):
    train, plan, calibration = toy_case

    wrong_sites = list(CALIBRATION_SITES)
    wrong_sites[0] = ("s21w069", 0, 0)

    with pytest.raises(
        ValueError, match="Calibration identities"
    ):
        fit_v2_models(
            train, plan, calibration, wrong_sites
        )


def test_training_assignment_leakage_rejected(toy_case):
    train, plan, calibration = toy_case

    changed = [dict(item) for item in plan]
    changed[0]["tile"] = "s28w069"

    with pytest.raises(
        ValueError, match="Training assignments"
    ):
        fit_v2_models(
            train, changed, calibration, CALIBRATION_SITES
        )


def test_training_order_mismatch_rejected(toy_case):
    train, plan, calibration = toy_case

    changed = list(plan)
    changed[0], changed[1] = changed[1], changed[0]

    with pytest.raises(
        ValueError, match="Training assignments"
    ):
        fit_v2_models(
            train, changed, calibration, CALIBRATION_SITES
        )


def test_nonfinite_and_wrong_shape_rejected(toy_models):
    with pytest.raises(ValueError):
        toy_models.score(
            np.full((2, 5), np.nan)
        )

    with pytest.raises(ValueError):
        toy_models.score(
            np.zeros((2, 6))
        )


def test_prospective_holdout_not_used_in_tests():
    # The unit tests fit artificial feature matrices
    # only; no NASADEM raster loading occurs here.
    assert CALIBRATION_SITES == tuple(
        ("s25w070", row, col)
        for row in range(9)
        for col in (7, 8)
    )
