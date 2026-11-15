"""ML-B V2 deterministic DEM integrity screening.

This layer does not use machine learning.

Input must be a 10 x 10 elevation array in meters,
with source NoData values already normalized to NaN.

The input array is never modified.
"""

from dataclasses import dataclass

import numpy as np


PATCH_SHAPE = (10, 10)
MIN_VALID_CELLS = 75


@dataclass(frozen=True)
class DEMIntegrityResult:
    valid_count: int
    nan_count: int
    inf_count: int
    missing_fraction: float
    valid_fraction: float
    reason_codes: tuple

    @property
    def is_alert(self):
        return bool(self.reason_codes)

    @property
    def can_score_ml(self):
        return not self.is_alert


def inspect_dem_integrity(patch):
    """Screen a normalized DEM patch without modifying it.

    NaN is missing elevation. Positive or negative
    infinity is invalid elevation.

    All 100 cells must be finite for ML scoring.
    At fewer than 75 valid cells, report an additional
    insufficient-coverage reason.

    Raw raster NoData sentinels must first be
    converted to NaN by the raster loading layer.
    """
    if np.ma.isMaskedArray(patch):
        if np.ma.getmaskarray(patch).any():
            raise ValueError(
                "Convert masked DEM cells to NaN first"
            )

    z = np.asarray(patch, dtype=np.float64)

    if z.shape != PATCH_SHAPE:
        raise ValueError(
            f"Expected {PATCH_SHAPE} DEM patch; got {z.shape}"
        )

    nan_count = int(np.isnan(z).sum())
    inf_count = int(np.isinf(z).sum())
    valid_count = int(np.isfinite(z).sum())

    if nan_count + inf_count + valid_count != z.size:
        raise RuntimeError("Invalid DEM cell accounting")

    reasons = []

    if nan_count:
        reasons.append("MISSING_ELEVATION")

    if inf_count:
        reasons.append("INVALID_INFINITE_ELEVATION")

    if valid_count < MIN_VALID_CELLS:
        reasons.append("INSUFFICIENT_VALID_COVERAGE")

    return DEMIntegrityResult(
        valid_count=valid_count,
        nan_count=nan_count,
        inf_count=inf_count,
        missing_fraction=float(nan_count / z.size),
        valid_fraction=float(valid_count / z.size),
        reason_codes=tuple(reasons),
    )
