"""FieldTwin ML-B V2 development-data preparation.

Reuse the original NASADEM anomaly patch extractor.

Only s25w070 development data is permitted.
The new evaluation tiles are not opened.

Preparation is separate from model fitting.
"""

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from science.ml_anomaly_data import extract_anomaly_tile
from science.ml_anomaly_v2_injection import (
    TRAIN_TILE,
    build_v2_training_plan,
    inject_v2_artifact,
)
from science.ml_anomaly_v2_integrity import (
    inspect_dem_integrity,
)
from science.ml_anomaly_v2_model import (
    CALIBRATION_SITES,
    physical_feature_matrix,
)


EXPECTED_SITES = frozenset(
    (row, col)
    for row in range(9)
    for col in range(9)
)

TRAINING_SITES = tuple(
    (TRAIN_TILE, row, col)
    for row in range(9)
    for col in range(7)
)


@dataclass(frozen=True)
class V2DevelopmentData:
    training_features: np.ndarray
    training_assignments: tuple
    training_sites: tuple
    calibration_features: np.ndarray
    calibration_sites: tuple


def _validated_development_patches(records):
    """Verify all 81 frozen geographic identities."""
    records = list(records)

    if len(records) != 81:
        raise ValueError(
            "Expected exactly 81 development records"
        )

    patches = {}

    required = {
        "tile", "row", "col", "partition",
        "lat", "lon", "x_m", "y_m",
        "land_fraction", "valid_fraction",
        "stencil_fraction", "elevation",
        "provenance",
    }

    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Invalid record type")

        if not required.issubset(record):
            raise ValueError(
                "Incomplete development record"
            )

        if record["tile"] != TRAIN_TILE:
            raise ValueError(
                "Evaluation tile cannot enter development"
            )

        if record["partition"] != "development":
            raise ValueError(
                "Unexpected geographic partition"
            )

        row = record["row"]
        col = record["col"]

        if (
            type(row) is not int
            or type(col) is not int
            or (row, col) not in EXPECTED_SITES
        ):
            raise ValueError(
                "Invalid development-grid identity"
            )

        identity = (row, col)

        if identity in patches:
            raise ValueError(
                "Duplicate development location"
            )

        expected_lat = -24.9 + row * 0.1
        expected_lon = -69.9 + col * 0.1

        actual_coordinates = np.asarray(
            [
                record["lat"],
                record["lon"],
                record["x_m"],
                record["y_m"],
            ],
            dtype=float,
        )

        if not np.isfinite(actual_coordinates).all():
            raise ValueError(
                "Invalid geographic coordinates"
            )

        if (
            abs(record["lat"] - expected_lat) > 1e-7
            or abs(record["lon"] - expected_lon) > 1e-7
        ):
            raise ValueError(
                "Development sampling-grid mismatch"
            )

        if (
            record["land_fraction"] != 1.0
            or record["valid_fraction"] != 1.0
            or record["stencil_fraction"] < 0.95
        ):
            raise ValueError(
                "Ineligible development patch"
            )

        provenance = record["provenance"]

        if not isinstance(provenance, dict):
            raise ValueError(
                "Missing raster provenance"
            )

        if (
            Path(str(provenance.get(
                "source_path", ""
            ))).name != "s25w070.hgt"
            or provenance.get("source_crs") != "EPSG:4326"
            or provenance.get("target_crs") != "EPSG:32719"
            or provenance.get("source_resampling") != "bilinear"
        ):
            raise ValueError(
                "Unexpected development raster provenance"
            )

        elevation = record["elevation"]

        if (
            np.ma.isMaskedArray(elevation)
            and np.ma.getmaskarray(elevation).any()
        ):
            raise ValueError(
                "Unnormalized masked elevation"
            )

        patch = np.asarray(
            elevation, dtype=np.float64
        )

        if patch.shape != (10, 10):
            raise ValueError(
                "Invalid elevation patch dimensions"
            )

        if not inspect_dem_integrity(
            patch
        ).can_score_ml:
            raise ValueError(
                "Development patch has integrity alert"
            )

        patches[identity] = patch.copy()

    if set(patches) != EXPECTED_SITES:
        raise ValueError(
            "Incomplete development location inventory"
        )

    return patches


def prepare_v2_development_records(records):
    """Generate the frozen training and calibration matrices.

    This function never loads raster files itself.
    It never fits a machine-learning model.
    """
    patches = _validated_development_patches(
        records
    )

    assignments = build_v2_training_plan()

    if len(assignments) != 819:
        raise RuntimeError(
            "Incorrect frozen training allocation"
        )

    training_patches = []

    for assignment in assignments:
        if (
            assignment["tile"] != TRAIN_TILE
            or assignment["col"] > 6
        ):
            raise RuntimeError(
                "Training partition violation"
            )

        identity = (
            assignment["row"],
            assignment["col"],
        )

        modified, _ = inject_v2_artifact(
            patches[identity],
            assignment,
        )

        if not inspect_dem_integrity(
            modified
        ).can_score_ml:
            raise RuntimeError(
                "Physical training anomaly failed integrity"
            )

        training_patches.append(modified)

    calibration_patches = []

    for tile, row, col in CALIBRATION_SITES:
        if tile != TRAIN_TILE or col < 7:
            raise RuntimeError(
                "Calibration partition violation"
            )

        calibration_patches.append(
            patches[(row, col)].copy()
        )

    train_features = physical_feature_matrix(
        training_patches
    )

    cal_features = physical_feature_matrix(
        calibration_patches
    )

    if (
        train_features.shape != (819, 5)
        or cal_features.shape != (18, 5)
        or not np.isfinite(train_features).all()
        or not np.isfinite(cal_features).all()
    ):
        raise RuntimeError(
            "Invalid prepared feature matrices"
        )

    if len({
        (a["row"], a["col"])
        for a in assignments
    }) != 63:
        raise RuntimeError(
            "Incorrect training-site inventory"
        )

    if {
        (site[1], site[2])
        for site in CALIBRATION_SITES
    } & {
        (site[1], site[2])
        for site in TRAINING_SITES
    }:
        raise RuntimeError(
            "Training/calibration overlap"
        )

    train_features.setflags(write=False)
    cal_features.setflags(write=False)

    return V2DevelopmentData(
        training_features=train_features,
        training_assignments=tuple(assignments),
        training_sites=TRAINING_SITES,
        calibration_features=cal_features,
        calibration_sites=CALIBRATION_SITES,
    )


def load_v2_development_data():
    """Load only the original development tile s25w070.

    No holdout data is read by this entry point.
    """
    records = extract_anomaly_tile(TRAIN_TILE)

    return prepare_v2_development_records(
        records
    )
