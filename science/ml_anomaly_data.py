"""FieldTwin ML-B: NASADEM elevation patch extraction.

Extract 10 x 10 projected elevation patches from
registered NASADEM HGT files.

Land eligibility is inherited from the previously
validated SWB-filtered terrain extractor.

No source raster is modified, and no model is fitted.
"""

from pathlib import Path

import numpy as np
import rasterio

from rasterio.enums import Resampling
from rasterio.transform import from_origin
from rasterio.warp import reproject, transform

from science.ml_terrain import extract_tile_features


SOURCE_ROOT = Path("data/raw/earth/nasadem")
TARGET_CRS = "EPSG:32719"

PATCH_CELLS = 10
PIXEL_SIZE_M = 100.0
WINDOW_SIZE_M = 1000.0

EXPECTED_COUNTS = {
    "s25w070": 81,
    "s25w071": 44,
    "s24w068": 78,
}


def locate_nasadem_hgt(tile):
    """Find exactly one registered NASADEM elevation HGT."""
    if tile not in EXPECTED_COUNTS:
        raise ValueError("Unregistered NASADEM tile")

    matches = sorted(
        SOURCE_ROOT.rglob(f"{tile}.hgt")
    )

    if len(matches) != 1:
        raise ValueError(
            f"Expected one HGT for {tile}; "
            f"found {len(matches)}"
        )

    return matches[0]


def extract_anomaly_patch(record):
    """Extract a single SWB-eligible 10 x 10 DEM patch.

    Parameters
    ----------
    record:
        A land-filtered geographic sampling record
        from science.ml_terrain.extract_tile_features.

    Returns
    -------
    dict:
        Geographic identity, source metadata,
        coverage information, and a new elevation array.
    """
    required = (
        "tile", "row", "col", "partition",
        "lat", "lon", "x_m", "y_m",
        "land_fraction",
        "valid_fraction",
        "stencil_fraction",
    )

    if any(key not in record for key in required):
        raise ValueError("Incomplete sampling record")

    tile = record["tile"]

    if tile not in EXPECTED_COUNTS:
        raise ValueError("Unregistered tile")

    if record["land_fraction"] != 1.0:
        raise ValueError("SWB-ineligible terrain window")

    if (
        record["valid_fraction"] < 0.95
        or record["stencil_fraction"] < 0.95
    ):
        raise ValueError("Insufficient DEM source coverage")

    if not (
        0 <= record["row"] <= 8
        and 0 <= record["col"] <= 8
    ):
        raise ValueError("Invalid sampling-grid identity")

    expected_partition = (
        "development"
        if tile == "s25w070"
        else (
            "candidate"
            if (record["row"] + record["col"]) % 2 == 0
            else "assessment"
        )
    )

    if record["partition"] != expected_partition:
        raise ValueError("Geographic partition mismatch")

    path = locate_nasadem_hgt(tile)

    patch = np.full(
        (PATCH_CELLS, PATCH_CELLS),
        np.nan,
        dtype=np.float64,
    )

    cx = float(record["x_m"])
    cy = float(record["y_m"])

    if not np.isfinite([cx, cy]).all():
        raise ValueError("Invalid projected coordinates")

    target_transform = from_origin(
        cx - WINDOW_SIZE_M / 2.0,
        cy + WINDOW_SIZE_M / 2.0,
        PIXEL_SIZE_M,
        PIXEL_SIZE_M,
    )

    with rasterio.open(path) as src:
        if (
            src.crs is None
            or src.crs.to_epsg() != 4326
            or src.count != 1
            or src.width != 3601
            or src.height != 3601
        ):
            raise ValueError(
                f"Unexpected NASADEM HGT metadata: {tile}"
            )

        projected_x, projected_y = transform(
            src.crs,
            TARGET_CRS,
            [float(record["lon"])],
            [float(record["lat"])],
        )

        if (
            abs(projected_x[0] - cx) > 1.0
            or abs(projected_y[0] - cy) > 1.0
        ):
            raise ValueError(
                "Geographic and projected centers disagree"
            )

        nodata = (
            -32768.0
            if src.nodata is None
            else float(src.nodata)
        )

        if nodata != -32768.0:
            raise ValueError("Unexpected HGT NoData value")

        reproject(
            source=rasterio.band(src, 1),
            destination=patch,
            src_nodata=nodata,
            dst_transform=target_transform,
            dst_crs=TARGET_CRS,
            dst_nodata=np.nan,
            resampling=Resampling.bilinear,
            num_threads=1,
        )

        source_metadata = {
            "source_path": str(path),
            "source_crs": str(src.crs),
            "source_width": src.width,
            "source_height": src.height,
            "source_nodata": nodata,
            "source_elevation_units": "meters",
            "source_resampling": "bilinear",
            "target_crs": TARGET_CRS,
            "target_pixel_size_m": PIXEL_SIZE_M,
            "target_grid_shape": (10, 10),
        }

    valid_fraction = float(
        np.isfinite(patch).mean()
    )

    # The injection generator requires fully valid
    # original DEM arrays. Never silently fill gaps.
    if valid_fraction != 1.0:
        raise ValueError(
            f"Non-finite extracted elevation: "
            f"{tile}, row={record['row']}, "
            f"col={record['col']}, "
            f"coverage={valid_fraction:.3f}"
        )

    return {
        "tile": tile,
        "row": record["row"],
        "col": record["col"],
        "partition": record["partition"],
        "lat": float(record["lat"]),
        "lon": float(record["lon"]),
        "x_m": cx,
        "y_m": cy,
        "land_fraction": 1.0,
        "valid_fraction": valid_fraction,
        "stencil_fraction": float(record["stencil_fraction"]),
        "elevation": patch,
        "provenance": source_metadata,
    }


def extract_anomaly_tile(tile):
    """Extract all registered eligible patches from one tile.

    Calls the existing SWB-aware terrain extractor.
    No water or mixed-land window may be included.
    """
    if tile not in EXPECTED_COUNTS:
        raise ValueError("Unregistered evaluation tile")

    records = extract_tile_features(tile)

    if len(records) != EXPECTED_COUNTS[tile]:
        raise ValueError(
            "Land-eligible sample inventory changed"
        )

    ordered = sorted(
        records,
        key=lambda r: (r["row"], r["col"]),
    )

    extracted = [
        extract_anomaly_patch(record)
        for record in ordered
    ]

    identities = {
        (r["row"], r["col"])
        for r in extracted
    }

    if len(identities) != EXPECTED_COUNTS[tile]:
        raise ValueError("Duplicate extracted sites")

    if any(
        item["elevation"].shape != (10, 10)
        or not np.isfinite(item["elevation"]).all()
        for item in extracted
    ):
        raise ValueError("Invalid extracted DEM array")

    return extracted
