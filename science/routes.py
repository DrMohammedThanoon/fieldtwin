"""DEM-scale grid routing for exploratory rover tests.

Uses eight-connected Dijkstra shortest-path search.
Slope constraints are experimental, not rover safety limits.
"""

import heapq
import math

import numpy as np


class NoRouteError(RuntimeError):
    """No route satisfies the specified constraints."""


def shortest_route(
    elevation_m,
    cell_size_m,
    start,
    goal,
    max_slope_deg=None,
):
    """Find the shortest valid route between grid-cell centers.

    An optional maximum center-to-center grade constrains
    traversable edges. This is not wheel-scale hazard detection.
    """
    z = np.asarray(elevation_m, dtype=float)

    if z.ndim != 2 or min(z.shape) < 2:
        raise ValueError("A 2D grid of at least 2x2 is required")

    if not math.isfinite(cell_size_m) or cell_size_m <= 0:
        raise ValueError("Cell spacing must be positive meters")

    if max_slope_deg is not None:
        if not math.isfinite(max_slope_deg) or not (
            0 <= max_slope_deg < 90
        ):
            raise ValueError("Invalid slope limit")

    rows, cols = z.shape
    valid = np.isfinite(z)

    for point in (start, goal):
        if (
            len(point) != 2
            or any(not isinstance(v, (int, np.integer))
                   for v in point)
            or not (0 <= point[0] < rows)
            or not (0 <= point[1] < cols)
            or not valid[point]
        ):
            raise ValueError("Invalid or missing-data endpoint")

    directions = [
        (dr, dc)
        for dr in (-1, 0, 1)
        for dc in (-1, 0, 1)
        if dr != 0 or dc != 0
    ]

    distances = np.full(z.shape, np.inf)
    distances[start] = 0.0
    previous = {}

    queue = [(0.0, start[0], start[1])]

    while queue:
        distance, r, c = heapq.heappop(queue)

        if distance > distances[r, c]:
            continue

        if (r, c) == goal:
            break

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if not valid[nr, nc]:
                continue

            # Do not pass diagonally through missing-data corners.
            if dr != 0 and dc != 0:
                if not valid[r + dr, c] or not valid[r, c + dc]:
                    continue

            step_m = cell_size_m * math.hypot(dr, dc)
            height_change = abs(z[nr, nc] - z[r, c])
            slope = math.degrees(
                math.atan2(height_change, step_m)
            )

            if (
                max_slope_deg is not None
                and slope > max_slope_deg + 1e-10
            ):
                continue

            alternative = distance + step_m

            if alternative < distances[nr, nc] - 1e-10:
                distances[nr, nc] = alternative
                previous[(nr, nc)] = (r, c)
                heapq.heappush(
                    queue, (alternative, nr, nc)
                )

    if not np.isfinite(distances[goal]):
        raise NoRouteError("No feasible route")

    path = [goal]
    while path[-1] != start:
        path.append(previous[path[-1]])
    path.reverse()

    slopes = []

    for (r1, c1), (r2, c2) in zip(path[:-1], path[1:]):
        step_m = cell_size_m * math.hypot(
            r2 - r1, c2 - c1
        )
        slopes.append(math.degrees(math.atan2(
            abs(z[r2, c2] - z[r1, c1]), step_m
        )))

    return {
        "path": path,
        "distance_m": float(distances[goal]),
        "steps": len(slopes),
        "maximum_slope_deg": float(max(slopes, default=0)),
        "mean_slope_deg": float(np.mean(slopes)) if slopes else 0.0,
        "p90_slope_deg": float(np.percentile(slopes, 90))
            if slopes else 0.0,
        "experimental_slope_limit_deg": max_slope_deg,
    }
