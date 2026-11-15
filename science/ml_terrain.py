"""Deterministic NASADEM sampling for FieldTwin ML-A.

Extracts physical terrain features without fitting ML models.
Geographic partitions follow docs/ML_DISCOVERY_PROTOCOL.md.
"""

from pathlib import Path

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.transform import from_origin
from rasterio.warp import reproject, transform

from science.terrain import (
    local_slope_percentiles,
    metric_patch,
    summarize_patch,
)


TILE_BOUNDS = {
    "s25w070": (-69.9, -69.1, -24.9, -24.1),
    "s25w071": (-70.9, -70.1, -24.9, -24.1),
    "s24w068": (-67.9, -67.1, -23.9, -23.1),
}

DEVELOPMENT_TILE = "s25w070"
EVALUATION_TILES = ("s25w071", "s24w068")

FEATURE_KEYS = (
    "slope_deg",
    "relief_p95_p05_m",
    "roughness_rms_m",
    "local_slope_p50_deg",
    "local_slope_p90_deg",
)

TARGET_CRS = "EPSG:32719"
WINDOW_M = 1000
CELL_M = 100
GRID_POINTS = 9
MIN_COVERAGE = 0.95


def find_tile(tile, root=Path("data/raw/earth/nasadem")):
    """Locate exactly one existing NASADEM HGT file."""
    if tile not in TILE_BOUNDS:
        raise ValueError(f"Unknown tile: {tile}")

    paths = sorted(root.rglob(f"{tile}.hgt"))

    if len(paths) != 1:
        raise ValueError(
            f"Expected exactly one {tile}.hgt; found {len(paths)}"
        )

    with rasterio.open(paths[0]) as src:
        if src.crs is None or src.crs.to_epsg() != 4326:
            raise ValueError(f"Unexpected CRS for {tile}")

    return paths[0]


def predefined_centers(tile):
    """Generate the frozen 9x9 geographic sampling grid."""
    if tile not in TILE_BOUNDS:
        raise ValueError(f"Unknown tile: {tile}")

    west, east, south, north = TILE_BOUNDS[tile]

    points = []

    for row, lat in enumerate(
        np.linspace(south, north, GRID_POINTS)
    ):
        for col, lon in enumerate(
            np.linspace(west, east, GRID_POINTS)
        ):
            points.append({
                "row": row,
                "col": col,
                "lat": float(lat),
                "lon": float(lon),
            })

    return points


def partition(tile, row, col):
    """Return the frozen geographic/evaluation partition."""
    if tile == DEVELOPMENT_TILE:
        return "development"

    if tile not in EVALUATION_TILES:
        raise ValueError(f"Unknown evaluation tile: {tile}")

    return (
        "candidate"
        if (row + col) % 2 == 0
        else "assessment"
    )



def _land_fractions(tile, points, x, y, hgt_path):
    """Screen complete terrain windows using NASADEM SWB.

    SWB classification: 0 = land, 255 = water.
    A window is eligible only when every screening cell
    is land-classified.
    """
    root = Path("data/raw/earth/nasadem")
    matches = sorted(root.rglob(f"{tile}.swb"))

    if len(matches) != 1:
        raise ValueError(
            f"Expected one SWB mask for {tile}; "
            f"found {len(matches)}"
        )

    fractions = []
    cells = round(WINDOW_M / CELL_M)

    with rasterio.open(hgt_path) as src:
        expected_size = src.width * src.height

        if matches[0].stat().st_size != expected_size:
            raise ValueError(f"Invalid SWB size: {tile}")

        water = np.memmap(
            matches[0],
            dtype=np.uint8,
            mode="r",
            shape=(src.height, src.width),
        )

        codes = set(np.unique(water).tolist())

        if not codes.issubset({0, 255}):
            raise ValueError(
                f"Unexpected SWB classification: {tile}"
            )

        for point, cx, cy in zip(points, x, y):
            screen = np.full(
                (cells, cells),
                127,
                dtype=np.uint8,
            )

            reproject(
                source=water,
                destination=screen,
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=from_origin(
                    cx - WINDOW_M / 2,
                    cy + WINDOW_M / 2,
                    CELL_M,
                    CELL_M,
                ),
                dst_crs=TARGET_CRS,
                dst_nodata=127,
                resampling=Resampling.nearest,
            )

            if np.any(
                (screen != 0) & (screen != 255)
            ):
                raise ValueError(
                    f"Unclassified SWB cells: {tile}, "
                    f"row={point['row']}, "
                    f"col={point['col']}"
                )

            fractions.append(
                float(np.mean(screen == 0))
            )

    if len(fractions) != len(points):
        raise RuntimeError("SWB sampling count mismatch")

    return fractions


def extract_tile_features(tile, *, return_exclusions=False):
    """Extract land-eligible descriptors from 81 fixed centers.

    Optionally return excluded-window records for auditing.
    No ML fitting occurs here.
    """
    path = find_tile(tile)
    points = predefined_centers(tile)

    x, y = transform(
        "EPSG:4326",
        TARGET_CRS,
        [p["lon"] for p in points],
        [p["lat"] for p in points],
    )

    land_fractions = _land_fractions(
        tile, points, x, y, path
    )

    records = []
    excluded = []

    for point, cx, cy, land_fraction in zip(
        points, x, y, land_fractions
    ):
        if land_fraction < 1.0:
            excluded.append({
                "tile": tile,
                "row": point["row"],
                "col": point["col"],
                "lat": point["lat"],
                "lon": point["lon"],
                "land_fraction": land_fraction,
                "reason": "SWB_NOT_FULLY_LAND",
            })
            continue
        grid, valid = metric_patch(
            path,
            center_xy=(cx, cy),
            target_crs=TARGET_CRS,
            window_m=WINDOW_M,
            pixel_size_m=CELL_M,
        )

        terrain = summarize_patch(
            grid,
            CELL_M,
            valid_mask=valid,
            min_valid_fraction=MIN_COVERAGE,
        )

        slopes = local_slope_percentiles(
            grid,
            CELL_M,
            valid_mask=valid,
            min_stencil_fraction=MIN_COVERAGE,
        )

        if not terrain["usable"] or not slopes["usable"]:
            raise ValueError(
                f"Ineligible terrain: {tile}, "
                f"row={point['row']}, col={point['col']}"
            )

        merged = {**terrain, **slopes}

        features = np.asarray(
            [merged[key] for key in FEATURE_KEYS],
            dtype=float,
        )

        if not np.all(np.isfinite(features)):
            raise ValueError(
                f"Non-finite features: {tile}, "
                f"row={point['row']}, col={point['col']}"
            )

        record = {
            "tile": tile,
            "row": point["row"],
            "col": point["col"],
            "lat": point["lat"],
            "lon": point["lon"],
            "x_m": float(cx),
            "y_m": float(cy),
            "partition": partition(
                tile, point["row"], point["col"]
            ),
            "valid_fraction": terrain["valid_fraction"],
            "stencil_fraction": slopes["stencil_fraction"],
            "land_fraction": land_fraction,
        }

        record.update({
            key: float(value)
            for key, value in zip(FEATURE_KEYS, features)
        })

        records.append(record)

    if len(records) + len(excluded) != GRID_POINTS ** 2:
        raise RuntimeError("Unexpected sampling count")

    if return_exclusions:
        return records, excluded

    return records


def feature_matrix(records):
    """Create a finite five-column feature matrix."""
    if not records:
        raise ValueError("No terrain records supplied")

    values = np.asarray(
        [[record[key] for key in FEATURE_KEYS]
         for record in records],
        dtype=float,
    )

    if values.ndim != 2 or values.shape[1] != len(FEATURE_KEYS):
        raise ValueError("Invalid feature dimensions")

    if not np.all(np.isfinite(values)):
        raise ValueError("Invalid feature matrix")

    return values
