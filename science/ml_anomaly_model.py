"""FieldTwin ML-B: development-only anomaly screeners.

Both methods fit on exactly 81 clean NASADEM
development patches, never geographic holdouts.

Larger returned scores indicate greater anomaly.
These are numerical QA scores, not verified defects.
"""

from dataclasses import dataclass

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from science.ml_anomaly_features import (
    FEATURE_NAMES,
    anomaly_feature_matrix,
)


DEVELOPMENT_TILE = "s25w070"
TRAINING_COUNT = 81
RANDOM_SEED = 20261115
N_ESTIMATORS = 300
MAX_SAMPLES = 64
THRESHOLD_PERCENTILE = 95.0

ROBUST_SCALE_FLOORS = np.array(
    [0.01, 1.0, 1.0, 1.0, 1.0, 1.0],
    dtype=float,
)


@dataclass(frozen=True)
class FittedAnomalyScreeners:
    """Two calibrated development-only anomaly methods."""

    scaler: StandardScaler
    forest: IsolationForest
    robust_center: np.ndarray
    robust_scale: np.ndarray
    forest_threshold: float
    robust_threshold: float
    training_count: int
    feature_names: tuple


def _robust_scores(features, center, scale):
    """Maximum absolute feature-wise robust deviation."""
    standardized = np.abs(
        (features - center) / scale
    )

    scores = np.max(standardized, axis=1)

    if not np.isfinite(scores).all():
        raise ValueError("Non-finite robust anomaly scores")

    return scores


def _validate_development(records):
    if len(records) != TRAINING_COUNT:
        raise ValueError("Expected 81 development patches")

    locations = set()

    for record in records:
        row = record["row"]
        col = record["col"]

        if (
            record["tile"] != DEVELOPMENT_TILE
            or record["partition"] != "development"
            or record["land_fraction"] != 1.0
            or record["valid_fraction"] != 1.0
            or record["stencil_fraction"] < 0.95
        ):
            raise ValueError(
                "Development provenance or eligibility violation"
            )

        if not (
            isinstance(row, int)
            and isinstance(col, int)
            and 0 <= row <= 8
            and 0 <= col <= 8
        ):
            raise ValueError("Invalid development location")

        identity = (row, col)

        if identity in locations:
            raise ValueError("Duplicate development patch")

        locations.add(identity)

        elevation = np.asarray(
            record["elevation"],
            dtype=float,
        )

        if (
            elevation.shape != (10, 10)
            or not np.isfinite(elevation).all()
        ):
            raise ValueError(
                "Invalid clean development elevation"
            )

    expected = {
        (row, col)
        for row in range(9)
        for col in range(9)
    }

    if locations != expected:
        raise ValueError("Development grid incomplete")


def fit_anomaly_screeners(development_records):
    """Fit both methods exclusively on development DEMs."""
    _validate_development(development_records)

    ordered = sorted(
        development_records,
        key=lambda r: (r["row"], r["col"]),
    )

    features = anomaly_feature_matrix(
        [r["elevation"] for r in ordered]
    )

    if features.shape != (TRAINING_COUNT, 6):
        raise RuntimeError("Unexpected training matrix")

    # ML model: development-only standardization.
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    forest = IsolationForest(
        n_estimators=N_ESTIMATORS,
        max_samples=MAX_SAMPLES,
        contamination="auto",
        max_features=1.0,
        bootstrap=False,
        random_state=RANDOM_SEED,
        n_jobs=1,
    )
    forest.fit(scaled)

    # Baseline: development-only median/MAD statistics.
    center = np.median(features, axis=0)

    mad = np.median(
        np.abs(features - center),
        axis=0,
    )

    q25, q75 = np.percentile(
        features,
        [25, 75],
        axis=0,
        method="linear",
    )

    fallback = np.maximum(
        (q75 - q25) / 1.349,
        ROBUST_SCALE_FLOORS,
    )

    robust_scale = np.where(
        mad > 1e-9,
        1.4826 * mad,
        fallback,
    )

    if (
        not np.isfinite(robust_scale).all()
        or np.any(robust_scale <= 0)
    ):
        raise RuntimeError("Invalid robust scales")

    # Reverse Isolation Forest's native orientation:
    # larger scores must mean more anomalous.
    forest_clean_scores = -forest.score_samples(
        scaled
    )

    robust_clean_scores = _robust_scores(
        features,
        center,
        robust_scale,
    )

    # Thresholds use development-clean scores only.
    forest_threshold = float(
        np.percentile(
            forest_clean_scores,
            THRESHOLD_PERCENTILE,
            method="linear",
        )
    )

    robust_threshold = float(
        np.percentile(
            robust_clean_scores,
            THRESHOLD_PERCENTILE,
            method="linear",
        )
    )

    if not np.isfinite(
        [forest_threshold, robust_threshold]
    ).all():
        raise RuntimeError("Invalid development thresholds")

    return FittedAnomalyScreeners(
        scaler=scaler,
        forest=forest,
        robust_center=center.copy(),
        robust_scale=robust_scale.copy(),
        forest_threshold=forest_threshold,
        robust_threshold=robust_threshold,
        training_count=TRAINING_COUNT,
        feature_names=FEATURE_NAMES,
    )


def score_anomaly_patches(model, patches):
    """Score DEM arrays without fitting or changing cutoffs.

    The caller supplies either untouched or synthetically
    modified patches. No labels enter scoring.
    """
    if not isinstance(model, FittedAnomalyScreeners):
        raise TypeError("Expected fitted anomaly screeners")

    if (
        model.training_count != TRAINING_COUNT
        or model.feature_names != FEATURE_NAMES
    ):
        raise ValueError("Model specification mismatch")

    features = anomaly_feature_matrix(patches)

    scaled = model.scaler.transform(features)

    forest_scores = -model.forest.score_samples(
        scaled
    )

    robust_scores = _robust_scores(
        features,
        model.robust_center,
        model.robust_scale,
    )

    if not np.isfinite(forest_scores).all():
        raise ValueError("Non-finite Isolation Forest scores")

    return {
        "forest_scores": forest_scores,
        "robust_scores": robust_scores,
        "forest_flags": (
            forest_scores > model.forest_threshold
        ),
        "robust_flags": (
            robust_scores > model.robust_threshold
        ),
    }
