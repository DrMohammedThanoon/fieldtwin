"""Smoke tests for FieldTwin's scientific Python environment."""

import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from rasterio.io import MemoryFile
from rasterio.transform import from_origin


def test_numpy_calculations():
    elevations = np.array([100.0, 120.0, 140.0])
    assert np.mean(elevations) == 120.0
    assert np.ptp(elevations) == 40.0


def test_rasterio_in_memory_raster():
    elevations = np.array(
        [[100, 110], [120, 130]], dtype=np.float32
    )

    profile = {
        "driver": "GTiff",
        "height": 2,
        "width": 2,
        "count": 1,
        "dtype": "float32",
        "crs": "EPSG:4326",
        "transform": from_origin(10, 20, 0.01, 0.01),
    }

    with MemoryFile() as memory_file:
        with memory_file.open(**profile) as dataset:
            dataset.write(elevations, 1)

        with memory_file.open() as dataset:
            np.testing.assert_array_equal(
                dataset.read(1), elevations
            )
            assert dataset.crs.to_epsg() == 4326


def test_geopandas_coordinate_transformation():
    points = gpd.GeoDataFrame(
        geometry=[Point(0, 0)],
        crs="EPSG:4326",
    )

    projected = points.to_crs("EPSG:3857")

    assert np.isclose(projected.geometry.x.iloc[0], 0)
    assert np.isclose(projected.geometry.y.iloc[0], 0)
