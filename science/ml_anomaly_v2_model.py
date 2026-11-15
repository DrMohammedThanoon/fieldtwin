"""FieldTwin ML-B V2: frozen physical-anomaly scorers.

Three comparable methods:
- Supervised Random Forest
- Supervised scaled Logistic Regression
- Clean-development-fitted robust statistical score

The deterministic integrity layer is separate.
This module performs no raster I/O.
"""

from dataclasses import dataclass

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from science.ml_anomaly_features import (
    FEATURE_NAMES,
    anomaly_feature_matrix,
)
from science.ml_anomaly_v2_injection import (
    SEED,
    TRAIN_TILE,
    build_v2_training_plan,
)
from science.ml_anomaly_v2_integrity import (
    inspect_dem_integrity,
)


PHYSICAL_FEATURE_NAMES = FEATURE_NAMES[1:]

MODEL_NAMES = (
    "random_forest",
    "logistic_regression",
    "robust",
)

CALIBRATION_SITES = tuple(
    (TRAIN_TILE, row, col)
    for row in range(9)
    for col in (7, 8)
)


def _validate_matrix(matrix, expected_rows=None):
    """Accept only finite, unmasked five-feature matrices."""
    if (
        np.ma.isMaskedArray(matrix)
        and np.ma.getmaskarray(matrix).any()
    ):
        raise ValueError("Masked physical descriptors")

    x = np.asarray(matrix, dtype=np.float64)

    if (
        x.ndim != 2
        or x.shape[1] != len(PHYSICAL_FEATURE_NAMES)
        or x.shape[0] == 0
    ):
        raise ValueError(
            "Expected nonempty five-feature matrix"
        )

    if (
        expected_rows is not None
        and x.shape[0] != expected_rows
    ):
        raise ValueError(
            f"Expected {expected_rows} feature rows"
        )

    if not np.isfinite(x).all():
        raise ValueError(
            "Nonfinite physical descriptors"
        )

    return x


def physical_feature_matrix(patches):
    """Reuse five original physical descriptors.

    The missing-data descriptor is excluded.
    Layer A must accept every patch before extraction.
    """
    patches = list(patches)

    if not patches:
        raise ValueError("Empty patch collection")

    for patch in patches:
        result = inspect_dem_integrity(patch)

        if not result.can_score_ml:
            raise ValueError(
                "Integrity-alert patch cannot enter Layer B"
            )

    six = anomaly_feature_matrix(patches)

    return _validate_matrix(six[:, 1:].copy())


def fit_robust_reference(clean_features):
    """Fit frozen robust center/scale using clean training only."""
    clean = _validate_matrix(clean_features)

    center = np.median(clean, axis=0)

    deviations = np.abs(clean - center)
    mad = np.median(deviations, axis=0)

    q25 = np.percentile(
        clean, 25, axis=0, method="linear"
    )
    q75 = np.percentile(
        clean, 75, axis=0, method="linear"
    )

    fallback = np.maximum(
        (q75 - q25) / 1.349, 1.0
    )

    scale = np.where(
        mad > 0.0,
        1.4826 * mad,
        fallback,
    )

    if (
        not np.isfinite(center).all()
        or not np.isfinite(scale).all()
        or not (scale > 0).all()
    ):
        raise ValueError("Invalid robust reference")

    return center.copy(), scale.copy()


def score_robust(features, center, scale):
    x = _validate_matrix(features)

    center = np.asarray(center, dtype=float)
    scale = np.asarray(scale, dtype=float)

    if center.shape != (5,) or scale.shape != (5,):
        raise ValueError("Invalid robust parameter shapes")

    if (
        not np.isfinite(center).all()
        or not np.isfinite(scale).all()
        or not (scale > 0).all()
    ):
        raise ValueError("Invalid robust reference")

    result = np.max(
        np.abs((x - center) / scale),
        axis=1,
    )

    if not np.isfinite(result).all():
        raise ValueError("Nonfinite robust score")

    return result


def _all_scores(rf, lr, center, scale, features):
    x = _validate_matrix(features)

    scores = {
        "random_forest": rf.predict_proba(x)[:, 1],
        "logistic_regression": lr.predict_proba(x)[:, 1],
        "robust": score_robust(x, center, scale),
    }

    for values in scores.values():
        if (
            values.shape != (len(x),)
            or not np.isfinite(values).all()
        ):
            raise ValueError("Invalid model score vector")

    return scores


def calibration_thresholds(score_vectors):
    """Freeze each method's clean calibration 95th percentile."""
    if set(score_vectors) != set(MODEL_NAMES):
        raise ValueError("Incorrect calibration methods")

    thresholds = {}

    for name in MODEL_NAMES:
        values = np.asarray(
            score_vectors[name], dtype=float
        )

        if values.shape != (18,):
            raise ValueError(
                "Expected 18 clean calibration scores"
            )

        if not np.isfinite(values).all():
            raise ValueError("Invalid calibration scores")

        thresholds[name] = float(
            np.percentile(
                values, 95, method="linear"
            )
        )

    return thresholds


def threshold_flags(score_vectors, thresholds):
    """Use strict > thresholds, never >=."""
    if (
        set(score_vectors) != set(MODEL_NAMES)
        or set(thresholds) != set(MODEL_NAMES)
    ):
        raise ValueError("Incorrect method keys")

    flags = {}

    for name in MODEL_NAMES:
        scores = np.asarray(
            score_vectors[name], dtype=float
        )
        threshold = float(thresholds[name])

        if (
            scores.ndim != 1
            or not np.isfinite(scores).all()
            or not np.isfinite(threshold)
        ):
            raise ValueError("Invalid score or threshold")

        flags[name] = scores > threshold

    return flags


@dataclass(frozen=True)
class V2FittedModels:
    random_forest: RandomForestClassifier
    logistic_regression: Pipeline
    robust_center: np.ndarray
    robust_scale: np.ndarray
    thresholds: dict

    def score(self, features):
        return _all_scores(
            self.random_forest,
            self.logistic_regression,
            self.robust_center,
            self.robust_scale,
            features,
        )

    def flags(self, features):
        return threshold_flags(
            self.score(features),
            self.thresholds,
        )


def fit_v2_models(
    training_features,
    training_assignments,
    calibration_features,
    calibration_sites,
):
    """Fit only the frozen development training/calibration design.

    Exact ordered assignment identities are required.
    The two new holdout tiles are not accepted as inputs
    to fitting or calibration metadata.
    """
    assignments = list(training_assignments)

    if assignments != build_v2_training_plan():
        raise ValueError(
            "Training assignments do not match frozen plan"
        )

    if tuple(calibration_sites) != CALIBRATION_SITES:
        raise ValueError(
            "Calibration identities do not match frozen plan"
        )

    train = _validate_matrix(
        training_features, expected_rows=819
    )
    calibration = _validate_matrix(
        calibration_features, expected_rows=18
    )

    labels = np.asarray(
        [item["label"] for item in assignments],
        dtype=int,
    )

    if (
        int(np.sum(labels == 0)) != 63
        or int(np.sum(labels == 1)) != 756
    ):
        raise RuntimeError("Incorrect training labels")

    clean_train = train[labels == 0]

    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=3,
        max_features="sqrt",
        class_weight="balanced_subsample",
        bootstrap=True,
        random_state=SEED,
        n_jobs=1,
    )

    lr = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(
            class_weight="balanced",
            solver="lbfgs",
            max_iter=5000,
            random_state=SEED,
        )),
    ])

    rf.fit(train, labels)
    lr.fit(train, labels)

    center, scale = fit_robust_reference(
        clean_train
    )

    calibrated = _all_scores(
        rf, lr, center, scale, calibration
    )

    thresholds = calibration_thresholds(
        calibrated
    )

    return V2FittedModels(
        random_forest=rf,
        logistic_regression=lr,
        robust_center=center,
        robust_scale=scale,
        thresholds=thresholds,
    )
