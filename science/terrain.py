
import numpy as np


def summarize_patch(
    elevation_m,
    pixel_size_m,
    valid_mask=None,
    min_valid_fraction=0.95,
):
    """Summarize a terrain patch on a uniform metric grid.

    Elevation and pixel spacing must be in meters.
    The caller must exclude documented NoData values.
    """
    z = np.asarray(elevation_m, dtype=np.float64)

    if z.ndim != 2 or min(z.shape) < 3:
        raise ValueError("A 2D grid of at least 3x3 is required")

    if not np.isfinite(pixel_size_m) or pixel_size_m <= 0:
        raise ValueError("Pixel size must be positive meters")

    if not 0 < min_valid_fraction <= 1:
        raise ValueError("Invalid minimum coverage threshold")

    valid = np.isfinite(z)

    if valid_mask is not None:
        mask = np.asarray(valid_mask, dtype=bool)
        if mask.shape != z.shape:
            raise ValueError("Validity mask shape mismatch")
        valid &= mask

    coverage = float(valid.mean())
    rows, cols = z.shape

    result = {
        "valid_fraction": coverage,
        "valid_cells": int(valid.sum()),
        "total_cells": int(z.size),
        "width_m": float(cols * pixel_size_m),
        "height_m": float(rows * pixel_size_m),
        "usable": False,
        "slope_deg": None,
        "relief_p95_p05_m": None,
        "roughness_rms_m": None,
    }

    if coverage < min_valid_fraction or valid.sum() < 3:
        return result

    yy, xx = np.indices(z.shape, dtype=np.float64)
    x = (xx[valid] - (cols - 1) / 2) * pixel_size_m
    y = (yy[valid] - (rows - 1) / 2) * pixel_size_m
    heights = z[valid]

    design = np.column_stack((x, y, np.ones_like(x)))
    coefficients, _, rank, _ = np.linalg.lstsq(
        design, heights, rcond=None
    )

    if rank < 3:
        return result

    dx, dy = coefficients[:2]
    predicted = design @ coefficients
    residuals = heights - predicted

    result.update({
        "usable": True,
        "slope_deg": float(
            np.degrees(np.arctan(np.hypot(dx, dy)))
        ),
        "relief_p95_p05_m": float(
            np.percentile(heights, 95)
            - np.percentile(heights, 5)
        ),
        "roughness_rms_m": float(
            np.sqrt(np.mean(residuals ** 2))
        ),
    })

    return result


def metric_patch(
    path, *,
    center_xy,
    target_crs,
    window_m=1000,
    pixel_size_m=50,
):
    """Return a metric terrain grid and its valid-data mask.

    center_xy must be in the target CRS, not lon/lat.
    Use a planet-appropriate projected CRS with meter units.
    """
    import rasterio
    from rasterio.crs import CRS
    from rasterio.enums import Resampling
    from rasterio.transform import from_origin
    from rasterio.warp import reproject

    target = CRS.from_user_input(target_crs)

    if not target.is_projected:
        raise ValueError("Target CRS must be projected")

    if not np.isclose(target.linear_units_factor[1], 1.0):
        raise ValueError("Target CRS units must be meters")

    if (
        not np.isfinite(window_m)
        or not np.isfinite(pixel_size_m)
        or window_m <= 0
        or pixel_size_m <= 0
    ):
        raise ValueError("Window and spacing must be positive")

    cells = round(window_m / pixel_size_m)
    if cells < 3 or not np.isclose(
        cells * pixel_size_m, window_m, rtol=0, atol=1e-8
    ):
        raise ValueError("Window must contain whole cells")

    if len(center_xy) != 2 or not np.all(np.isfinite(center_xy)):
        raise ValueError("Invalid projected center coordinates")

    cx, cy = center_xy
    dst_transform = from_origin(
        cx - window_m / 2,
        cy + window_m / 2,
        pixel_size_m,
        pixel_size_m,
    )

    grid = np.full((cells, cells), np.nan, dtype=np.float32)

    with rasterio.open(path) as src:
        if src.crs is None:
            raise ValueError("Source CRS missing")

        reproject(
            source=rasterio.band(src, 1),
            destination=grid,
            src_transform=src.transform,
            src_crs=src.crs,
            src_nodata=src.nodata,
            dst_transform=dst_transform,
            dst_crs=target,
            dst_nodata=np.nan,
            resampling=Resampling.average,
        )

    return grid, np.isfinite(grid)


def local_slope_percentiles(
    elevation_m,
    pixel_size_m,
    valid_mask=None,
    min_stencil_fraction=0.95,
):
    """Calculate local slope using valid 3x3-centered stencils.

    Uses central differences on an equally spaced metric grid.
    Invalid cells and their affected neighbor stencils are excluded.
    """
    z = np.asarray(elevation_m, dtype=np.float64)

    if z.ndim != 2 or min(z.shape) < 3:
        raise ValueError("At least a 3x3 elevation grid is required")
    if not np.isfinite(pixel_size_m) or pixel_size_m <= 0:
        raise ValueError("Pixel spacing must be positive meters")
    if not 0 < min_stencil_fraction <= 1:
        raise ValueError("Invalid stencil coverage threshold")

    valid = np.isfinite(z)

    if valid_mask is not None:
        mask = np.asarray(valid_mask, dtype=bool)
        if mask.shape != z.shape:
            raise ValueError("Validity mask shape mismatch")
        valid &= mask

    stencil = (
        valid[1:-1, 1:-1]
        & valid[1:-1, :-2]
        & valid[1:-1, 2:]
        & valid[:-2, 1:-1]
        & valid[2:, 1:-1]
    )

    coverage = float(stencil.mean())
    result = {
        "stencil_fraction": coverage,
        "stencil_count": int(stencil.sum()),
        "usable": False,
        "local_slope_p50_deg": None,
        "local_slope_p90_deg": None,
    }

    if coverage < min_stencil_fraction or not stencil.any():
        return result

    dzdx = (
        z[1:-1, 2:] - z[1:-1, :-2]
    ) / (2 * pixel_size_m)

    dzdy = (
        z[2:, 1:-1] - z[:-2, 1:-1]
    ) / (2 * pixel_size_m)

    slopes = np.degrees(
        np.arctan(np.hypot(dzdx[stencil], dzdy[stencil]))
    )

    result.update({
        "usable": True,
        "local_slope_p50_deg": float(np.percentile(slopes, 50)),
        "local_slope_p90_deg": float(np.percentile(slopes, 90)),
    })
    return result
