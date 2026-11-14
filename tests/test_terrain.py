import numpy as np
import pytest

from science.terrain import summarize_patch


def test_flat_terrain():
    z = np.full((5, 5), 900.0)
    r = summarize_patch(z, 20.0)

    assert r["usable"]
    assert r["slope_deg"] == pytest.approx(0, abs=1e-8)
    assert r["relief_p95_p05_m"] == pytest.approx(0)
    assert r["roughness_rms_m"] == pytest.approx(0, abs=1e-8)


def test_planar_slope():
    x = np.tile(np.arange(7), (7, 1))
    z = 1000.0 + x * 10.0

    r = summarize_patch(z, 10.0)

    assert r["usable"]
    assert r["slope_deg"] == pytest.approx(45.0, abs=1e-8)
    assert r["roughness_rms_m"] == pytest.approx(0, abs=1e-8)


def test_irregular_terrain():
    z = np.zeros((7, 7), dtype=float)
    z[3, 3] = 15.0

    r = summarize_patch(z, 20.0)

    assert r["usable"]
    assert r["roughness_rms_m"] > 0


def test_insufficient_coverage():
    z = np.ones((5, 5), dtype=float)
    z[0, :] = np.nan

    r = summarize_patch(z, 20.0)

    assert not r["usable"]
    assert r["valid_fraction"] == pytest.approx(0.8)
    assert r["slope_deg"] is None


def test_explicit_nodata_mask():
    z = np.full((5, 5), 1000.0)
    z[0, 0] = -32767.0

    valid = z != -32767.0
    r = summarize_patch(z, 20.0, valid_mask=valid)

    assert r["usable"]
    assert r["valid_cells"] == 24
    assert r["slope_deg"] == pytest.approx(0, abs=1e-8)
