"""FieldTwin ML-B V2 prospective NASADEM extraction.

This module is restricted to two frozen geographic
holdouts. It does not perform model fitting, anomaly
scoring, threshold selection, or synthetic injection.

Original NASADEM rasters are never modified.
"""

from pathlib import Path

import numpy as np
import rasterio

from rasterio.enums import Resampling
from rasterio.transform import from_origin
from rasterio.warp import reproject, transform


SOURCE_ROOT = Path("data/raw/earth/nasadem")

TARGET_CRS = "EPSG:32719"
PIXEL_SIZE_M = 100.0
WINDOW_SIZE_M = 1000.0
PATCH_SHAPE = (10, 10)

TILE_ORIGINS = {
    "s21w069": (-20.9, -68.9),
    "s28w069": (-27.9, -68.9),
}

EXPECTED_ELIGIBLE = {
    "s21w069": 81,
    "s28w069": 80,
}

FROZEN_EXCLUSIONS = {
    "s21w069": frozenset(),
    "s28w069": frozenset({(5, 2)}),
}


def frozen_holdout_grid(tile):
    """Return the 81 preregistered geographic centers."""
    if tile not in TILE_ORIGINS:
        raise ValueError(
            "Unregistered V2 holdout tile"
        )

    south, west = TILE_ORIGINS[tile]

    points = []

    for row in range(9):
        for col in range(9):
            points.append({
                "tile": tile,
                "row": row,
                "col": col,
                "lat": round(
                    south + row * 0.1, 10
                ),
                "lon": round(
                    west + col * 0.1, 10
                ),
            })

    xs, ys = transform(
        "EPSG:4326",
        TARGET_CRS,
        [p["lon"] for p in points],
        [p["lat"] for p in points],
    )

    for point, x, y in zip(points, xs, ys):
        point["x_m"] = float(x)
        point["y_m"] = float(y)

        if not np.isfinite([x, y]).all():
            raise ValueError(
                "Invalid projected geographic center"
            )

    return points


def validate_holdout_land_screens(tile, screens):
    """Enforce full-land selection on all 81 SWB screens.

    The input maps (row, col) to 10 x 10 uint8 arrays.

    Codes:
    - 0: land
    - 255: water

    The frozen excluded location must be mixed,
    not silently added or replaced.
    """
    points = frozen_holdout_grid(tile)

    identities = {
        (p["row"], p["col"])
        for p in points
    }

    if (
        not isinstance(screens, dict)
        or set(screens) != identities
    ):
        raise ValueError(
            "Incorrect 81-site SWB inventory"
        )

    land_fractions = {}
    excluded = set()

    for identity in sorted(identities):
        source = screens[identity]

        if (
            np.ma.isMaskedArray(source)
            and np.ma.getmaskarray(source).any()
        ):
            raise ValueError("Masked SWB screen")

        screen = np.asarray(source)

        if (
            screen.shape != PATCH_SHAPE
            or screen.dtype != np.uint8
        ):
            raise ValueError(
                "Invalid SWB screen shape or dtype"
            )

        if not np.isin(screen, [0, 255]).all():
            raise ValueError(
                "Unexpected SWB class"
            )

        fraction = float(
            np.mean(screen == 0)
        )

        land_fractions[identity] = fraction

        if fraction < 1.0:
            excluded.add(identity)

    if excluded != FROZEN_EXCLUSIONS[tile]:
        raise ValueError(
            "Frozen SWB exclusion inventory changed"
        )

    for identity in excluded:
        fraction = land_fractions[identity]

        if not (0.0 < fraction < 1.0):
            raise ValueError(
                "Expected mixed land/water exclusion"
            )

    eligible = identities - excluded

    if len(eligible) != EXPECTED_ELIGIBLE[tile]:
        raise ValueError(
            "Incorrect eligible holdout count"
        )

    return {
        identity: land_fractions[identity]
        for identity in sorted(eligible)
    }


def assemble_holdout_records(
    tile, screens, elevation_patches
):
    """Assemble fully eligible DEMs from supplied arrays.

    This pure function supports tests with artificial
    arrays, without accessing NASADEM files.
    """
    eligible = validate_holdout_land_screens(
        tile, screens
    )

    if (
        not isinstance(elevation_patches, dict)
        or set(elevation_patches) != set(eligible)
    ):
        raise ValueError(
            "Elevation identities differ from frozen eligibility"
        )

    points = {
        (p["row"], p["col"]): p
        for p in frozen_holdout_grid(tile)
    }

    records = []

    for identity in sorted(eligible):
        original = elevation_patches[identity]

        if (
            np.ma.isMaskedArray(original)
            and np.ma.getmaskarray(original).any()
        ):
            raise ValueError(
                "Unnormalized masked DEM"
            )

        patch = np.asarray(
            original,
            dtype=np.float64,
        )

        if (
            patch.shape != PATCH_SHAPE
            or not np.isfinite(patch).all()
        ):
            raise ValueError(
                "Nonfinite or incorrectly shaped DEM patch"
            )

        point = points[identity]

        records.append({
            "tile": tile,
            "row": point["row"],
            "col": point["col"],
            "lat": point["lat"],
            "lon": point["lon"],
            "x_m": point["x_m"],
            "y_m": point["y_m"],
            "partition": "holdout",
            "land_fraction": eligible[identity],
            "valid_fraction": 1.0,
            "elevation": patch.copy(),
        })

    if len(records) != EXPECTED_ELIGIBLE[tile]:
        raise RuntimeError(
            "Final holdout inventory mismatch"
        )

    return records


def _source_paths(tile):
    """Validate exact local NASADEM source filenames."""
    if tile not in TILE_ORIGINS:
        raise ValueError(
            "Unregistered V2 holdout tile"
        )

    hgt = SOURCE_ROOT / f"{tile}.hgt"
    swb = SOURCE_ROOT / f"{tile}.swb"

    expected_sizes = {
        hgt: 3601 * 3601 * 2,
        swb: 3601 * 3601,
    }

    for path, expected_size in expected_sizes.items():
        if (
            not path.is_file()
            or path.is_symlink()
            or path.stat().st_size != expected_size
        ):
            raise ValueError(
                f"Invalid NASADEM source: {path}"
            )

    return hgt, swb


def extract_v2_holdout_tile(tile):
    """Read one frozen holdout tile without ML scoring.

    The entire SWB inventory is checked before any
    elevation patch is extracted.

    Do not call until the prospective extraction
    implementation has passed verification.
    """
    points = frozen_holdout_grid(tile)
    hgt_path, swb_path = _source_paths(tile)

    expected_south = int(tile[1:3]) * -1
    expected_west = int(tile[4:7]) * -1

    with rasterio.open(hgt_path) as src:
        if (
            src.crs is None
            or src.crs.to_epsg() != 4326
            or src.count != 1
            or src.width != 3601
            or src.height != 3601
            or src.nodata != -32768
        ):
            raise ValueError(
                "Unexpected NASADEM source metadata"
            )

        bounds = src.bounds

        if not all((
            abs(bounds.left - expected_west) < 0.001,
            abs(bounds.right - (expected_west + 1)) < 0.001,
            abs(bounds.bottom - expected_south) < 0.001,
            abs(bounds.top - (expected_south + 1)) < 0.001,
        )):
            raise ValueError(
                "NASADEM geographic bounds mismatch"
            )

        water = np.memmap(
            swb_path,
            dtype=np.uint8,
            mode="r",
            shape=(3601, 3601),
        )

        if not set(
            np.unique(water).tolist()
        ).issubset({0, 255}):
            raise ValueError(
                "Unexpected NASADEM water-mask classes"
            )

        screens = {}

        for point in points:
            identity = (
                point["row"],
                point["col"],
            )

            screen = np.full(
                PATCH_SHAPE,
                127,
                dtype=np.uint8,
            )

            target = from_origin(
                point["x_m"] - WINDOW_SIZE_M / 2,
                point["y_m"] + WINDOW_SIZE_M / 2,
                PIXEL_SIZE_M,
                PIXEL_SIZE_M,
            )

            reproject(
                source=water,
                destination=screen,
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=target,
                dst_crs=TARGET_CRS,
                dst_nodata=127,
                resampling=Resampling.nearest,
                num_threads=1,
            )

            screens[identity] = screen

        eligible = validate_holdout_land_screens(
            tile, screens
        )

        point_lookup = {
            (p["row"], p["col"]): p
            for p in points
        }

        elevation_patches = {}

        for identity in sorted(eligible):
            point = point_lookup[identity]

            patch = np.full(
                PATCH_SHAPE,
                np.nan,
                dtype=np.float64,
            )

            target = from_origin(
                point["x_m"] - WINDOW_SIZE_M / 2,
                point["y_m"] + WINDOW_SIZE_M / 2,
                PIXEL_SIZE_M,
                PIXEL_SIZE_M,
            )

            reproject(
                source=rasterio.band(src, 1),
                destination=patch,
                src_nodata=-32768,
                dst_transform=target,
                dst_crs=TARGET_CRS,
                dst_nodata=np.nan,
                resampling=Resampling.bilinear,
                num_threads=1,
            )

            if not np.isfinite(patch).all():
                raise ValueError(
                    f"Incomplete DEM at {tile} {identity}"
                )

            elevation_patches[identity] = patch

    records = assemble_holdout_records(
        tile,
        screens,
        elevation_patches,
    )

    provenance = {
        "source_path": str(hgt_path),
        "water_mask_path": str(swb_path),
        "source_crs": "EPSG:4326",
        "source_nodata": -32768,
        "target_crs": TARGET_CRS,
        "target_grid_shape": PATCH_SHAPE,
        "target_pixel_size_m": PIXEL_SIZE_M,
        "source_resampling": "bilinear",
        "mask_resampling": "nearest",
    }

    for record in records:
        record["provenance"] = provenance.copy()

    return records
