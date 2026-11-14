import numpy as np
import pytest

from science.terrain import (
    summarize_patch,
    local_slope_percentiles,
)


def test_flat_and_planar_terrain():
    flat = np.ones((7, 7)) * 100
    r = local_slope_percentiles(flat, 10)
    assert r["usable"]
    assert r["local_slope_p90_deg"] == pytest.approx(0)

    plane = np.tile(np.arange(7) * 10, (7, 1))
    r = local_slope_percentiles(plane, 10)
    assert r["local_slope_p50_deg"] == pytest.approx(45)
    assert r["local_slope_p90_deg"] == pytest.approx(45)


def test_opposing_slopes_not_cancelled():
    profile = np.array([0, 10, 20, 30, 20, 10, 0])
    terrain = np.tile(profile, (7, 1))

    global_result = summarize_patch(terrain, 10)
    local_result = local_slope_percentiles(terrain, 10)

    assert global_result["slope_deg"] == pytest.approx(
        0, abs=1e-8
    )
    assert local_result["local_slope_p90_deg"] > 40


def test_nodata_stencils_excluded():
    z = np.ones((5, 5)) * 100
    z[2, 2] = -32768

    r = local_slope_percentiles(
        z, 10, valid_mask=(z != -32768)
    )

    assert r["stencil_count"] == 4
    assert not r["usable"]
    assert r["local_slope_p90_deg"] is None
