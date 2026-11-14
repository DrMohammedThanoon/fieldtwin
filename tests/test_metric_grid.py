import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin

from science.terrain import metric_patch, summarize_patch


@pytest.fixture
def synthetic_dem(tmp_path):
    path = tmp_path / "synthetic.tif"
    z = np.tile(
        100 + 2 * np.arange(40, dtype=np.float32),
        (40, 1),
    )

    with rasterio.open(
        path, "w", driver="GTiff",
        height=40, width=40, count=1,
        dtype="float32", crs="EPSG:32619",
        transform=from_origin(500000, 10000, 50, 50),
        nodata=-32768,
    ) as dst:
        dst.write(z, 1)

    return path


def test_metric_grid_and_known_slope(synthetic_dem):
    grid, valid = metric_patch(
        synthetic_dem,
        center_xy=(501000, 9000),
        target_crs="EPSG:32619",
    )

    assert grid.shape == (20, 20)
    assert valid.all()

    features = summarize_patch(
        grid, 50, valid_mask=valid
    )

    expected = np.degrees(np.arctan(2 / 50))
    assert features["slope_deg"] == pytest.approx(
        expected, abs=1e-5
    )
    assert features["roughness_rms_m"] == pytest.approx(
        0, abs=1e-5
    )


def test_nodata_preservation(synthetic_dem):
    with rasterio.open(synthetic_dem, "r+") as dst:
        z = dst.read(1)
        z[20, 20] = -32768
        dst.write(z, 1)

    grid, valid = metric_patch(
        synthetic_dem,
        center_xy=(501000, 9000),
        target_crs="EPSG:32619",
    )

    assert valid.sum() == 399
    assert np.isnan(grid[10, 10])


def test_reject_geographic_target(synthetic_dem):
    with pytest.raises(ValueError, match="projected"):
        metric_patch(
            synthetic_dem,
            center_xy=(-69.9, -24.1),
            target_crs="EPSG:4326",
        )


def test_reject_fractional_grid(synthetic_dem):
    with pytest.raises(ValueError, match="whole cells"):
        metric_patch(
            synthetic_dem,
            center_xy=(501000, 9000),
            target_crs="EPSG:32619",
            window_m=1030,
        )
