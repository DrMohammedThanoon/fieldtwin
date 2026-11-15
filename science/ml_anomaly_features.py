"""FieldTwin ML-B: deterministic DEM anomaly descriptors.

Source patches are 10 x 10 elevation arrays in meters
on the frozen 100 m projected grid.

NaN marks missing elevation. Infinite values are
invalid. Original input arrays are never modified.

These features characterize numerical irregularities;
they do not independently identify real sensor defects.
"""

import numpy as np


FEATURE_NAMES = (
    "missing_fraction",
    "adjacent_abs_diff_p50_m",
    "adjacent_abs_diff_p95_m",
    "adjacent_abs_diff_max_m",
    "plane_residual_rms_m",
    "local_median_residual_max_m",
)

PATCH_SHAPE = (10, 10)
PIXEL_SIZE_M = 100.0
MIN_FINITE_CELLS = 75
MIN_ADJACENT_PAIRS = 60


def describe_dem_patch(elevation, pixel_size_m=100.0):
    """Compute six deterministic patch-level descriptors.

    Adjacent differences use valid horizontal and vertical
    pairs without diagonal neighbors.

    Plane roughness is RMS residual from ordinary
    least-squares fitting of z = a + bx + cy.

    Local residual compares an interior valid cell with
    the median of its eight surrounding cells, excluding
    the center. At least four valid neighbors are required.
    """
    z = np.asarray(elevation, dtype=np.float64)

    if z.shape != PATCH_SHAPE:
        raise ValueError(
            f"Expected {PATCH_SHAPE} DEM patch; got {z.shape}"
        )

    if not np.isfinite(pixel_size_m):
        raise ValueError("Invalid pixel spacing")

    if float(pixel_size_m) != PIXEL_SIZE_M:
        raise ValueError("Unexpected pixel spacing")

    if np.isinf(z).any():
        raise ValueError("Infinite elevation is invalid")

    valid = np.isfinite(z)
    count = int(valid.sum())

    if count < MIN_FINITE_CELLS:
        raise ValueError("Insufficient valid elevations")

    missing_fraction = float(1.0 - count / z.size)

    horizontal_valid = valid[:, 1:] & valid[:, :-1]
    vertical_valid = valid[1:, :] & valid[:-1, :]

    horizontal = np.abs(
        (z[:, 1:] - z[:, :-1:])[horizontal_valid]
    )
    vertical = np.abs(
        (z[1:, :] - z[:-1, :])[vertical_valid]
    )

    adjacent = np.concatenate([horizontal, vertical])

    if adjacent.size < MIN_ADJACENT_PAIRS:
        raise ValueError("Insufficient adjacent elevations")

    rows, cols = np.indices(PATCH_SHAPE)

    x = cols[valid].astype(float) * PIXEL_SIZE_M
    y = rows[valid].astype(float) * PIXEL_SIZE_M
    measured = z[valid]

    design = np.column_stack(
        [np.ones(count), x, y]
    )

    coefficients = np.linalg.lstsq(
        design, measured, rcond=None
    )[0]

    residual = measured - design @ coefficients

    plane_rms = float(
        np.sqrt(np.mean(residual ** 2))
    )

    local_residuals = []

    for row in range(1, 9):
        for col in range(1, 9):
            if not valid[row, col]:
                continue

            neighbors = z[
                row - 1:row + 2,
                col - 1:col + 2
            ].copy()

            neighbors[1, 1] = np.nan
            neighbors = neighbors[np.isfinite(neighbors)]

            if neighbors.size < 4:
                continue

            difference = abs(
                z[row, col] - np.median(neighbors)
            )
            local_residuals.append(float(difference))

    if not local_residuals:
        raise ValueError("No valid local residual samples")

    result = {
        "missing_fraction": missing_fraction,
        "adjacent_abs_diff_p50_m": float(
            np.percentile(adjacent, 50, method="linear")
        ),
        "adjacent_abs_diff_p95_m": float(
            np.percentile(adjacent, 95, method="linear")
        ),
        "adjacent_abs_diff_max_m": float(
            adjacent.max()
        ),
        "plane_residual_rms_m": plane_rms,
        "local_median_residual_max_m": float(
            max(local_residuals)
        ),
    }

    if tuple(result) != FEATURE_NAMES:
        raise RuntimeError("Feature ordering mismatch")

    if not np.isfinite(list(result.values())).all():
        raise ValueError("Non-finite anomaly descriptor")

    return result


def anomaly_feature_matrix(patches):
    """Return the fixed six-feature matrix for DEM patches."""
    records = [
        describe_dem_patch(patch)
        for patch in patches
    ]

    if not records:
        raise ValueError("Empty patch collection")

    matrix = np.asarray(
        [
            [record[name] for name in FEATURE_NAMES]
            for record in records
        ],
        dtype=float,
    )

    if matrix.shape != (len(records), len(FEATURE_NAMES)):
        raise RuntimeError("Unexpected anomaly feature shape")

    return matrix
