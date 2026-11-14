import numpy as np
import pytest

from science.routes import shortest_route, NoRouteError


def ridge_with_gap():
    terrain = np.zeros((7, 9), dtype=float)
    terrain[:, 4] = 100.0
    terrain[5, 4] = 0.0
    return terrain


def test_shortest_route_on_flat_terrain():
    result = shortest_route(
        np.zeros((5, 5)), 50, (0, 0), (4, 4)
    )
    assert result["distance_m"] == pytest.approx(
        4 * 50 * np.sqrt(2)
    )
    assert result["maximum_slope_deg"] == 0


def test_slope_constraint_avoids_ridge():
    terrain = ridge_with_gap()
    direct = shortest_route(
        terrain, 50, (3, 1), (3, 7)
    )
    constrained = shortest_route(
        terrain, 50, (3, 1), (3, 7),
        max_slope_deg=10
    )

    assert constrained["distance_m"] > direct["distance_m"]
    assert direct["maximum_slope_deg"] > 10
    assert constrained["maximum_slope_deg"] <= 10
    assert (5, 4) in constrained["path"]


def test_unavoidable_ridge():
    terrain = ridge_with_gap()
    terrain[5, 4] = 100

    with pytest.raises(NoRouteError):
        shortest_route(
            terrain, 50, (3, 1), (3, 7),
            max_slope_deg=10
        )


def test_missing_data_corner_is_blocked():
    terrain = np.zeros((3, 3))
    terrain[0, 1] = np.nan
    terrain[1, 0] = np.nan

    with pytest.raises(NoRouteError):
        shortest_route(
            terrain, 50, (0, 0), (2, 2)
        )


def test_invalid_parameters():
    terrain = np.zeros((5, 5))

    with pytest.raises(ValueError):
        shortest_route(
            terrain, -50, (0, 0), (4, 4)
        )

    with pytest.raises(ValueError):
        shortest_route(
            terrain, 50, (0, 0), (4, 4),
            max_slope_deg=-1
        )
