"""FieldTwin ML-A: unsupervised terrain-pattern discovery.

Fit only on development terrain. Select candidates only
from the eligible geographic candidate partition.

Clusters describe physical terrain patterns.
They do not represent validated Mars analog suitability.
"""

from dataclasses import dataclass

import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from science.ml_terrain import (
    DEVELOPMENT_TILE,
    EVALUATION_TILES,
    FEATURE_KEYS,
    feature_matrix,
)


RANDOM_SEED = 20261115
N_CLUSTERS = 8
SELECTION_BUDGET = 8

EXPECTED_CANDIDATES = {
    "s25w071": 22,
    "s24w068": 39,
}


@dataclass(frozen=True)
class TerrainDiscoveryModel:
    """Development-fitted ML-A transformations and clusters."""

    scaler: StandardScaler
    pca: PCA
    clustering: MiniBatchKMeans
    training_count: int
    feature_names: tuple


def _check_unique_positions(records):
    """Reject duplicated geographic sampling positions."""
    positions = [
        (r["tile"], r["row"], r["col"])
        for r in records
    ]

    if len(positions) != len(set(positions)):
        raise ValueError("Duplicate geographic sampling positions")


def fit_discovery_model(development_records):
    """Fit ML-A using exactly the 81 development windows.

    No evaluation-tile data are accepted for fitting.
    """
    if len(development_records) != 81:
        raise ValueError("Expected 81 development records")

    if any(
        r["tile"] != DEVELOPMENT_TILE
        or r["partition"] != "development"
        or r.get("land_fraction") != 1.0
        for r in development_records
    ):
        raise ValueError("Training partition or land violation")

    _check_unique_positions(development_records)

    ordered = sorted(
        development_records,
        key=lambda r: (r["row"], r["col"]),
    )

    features = feature_matrix(ordered)

    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    pca = PCA(
        n_components=2,
        svd_solver="full",
    )
    embedded = pca.fit_transform(scaled)

    clustering = MiniBatchKMeans(
        n_clusters=N_CLUSTERS,
        batch_size=32,
        n_init=10,
        random_state=RANDOM_SEED,
    )
    clustering.fit(embedded)

    if clustering.cluster_centers_.shape != (8, 2):
        raise RuntimeError("Unexpected cluster center dimensions")

    if not np.isfinite(clustering.cluster_centers_).all():
        raise RuntimeError("Non-finite cluster centers")

    return TerrainDiscoveryModel(
        scaler=scaler,
        pca=pca,
        clustering=clustering,
        training_count=len(ordered),
        feature_names=FEATURE_KEYS,
    )


def select_ml_candidates(model, candidate_records, budget=8):
    """Select distinct sites nearest to learned centroids.

    Candidate selection never accesses assessment records
    and never fits or updates an existing ML model.
    """
    if budget != SELECTION_BUDGET:
        raise ValueError("Selection budget differs from protocol")

    if not isinstance(model, TerrainDiscoveryModel):
        raise TypeError("Expected a fitted terrain discovery model")

    if model.training_count != 81:
        raise ValueError("Unexpected model training population")

    if model.feature_names != FEATURE_KEYS:
        raise ValueError("Feature definition mismatch")

    tiles = {r["tile"] for r in candidate_records}

    if len(tiles) != 1:
        raise ValueError("Candidates must belong to one tile")

    tile = next(iter(tiles))

    if tile not in EVALUATION_TILES:
        raise ValueError("Not a registered evaluation tile")

    if len(candidate_records) != EXPECTED_CANDIDATES[tile]:
        raise ValueError("Unexpected candidate-pool size")

    if any(
        r["partition"] != "candidate"
        or r.get("land_fraction") != 1.0
        for r in candidate_records
    ):
        raise ValueError("Assessment or ineligible terrain supplied")

    _check_unique_positions(candidate_records)

    ordered = sorted(
        candidate_records,
        key=lambda r: (r["row"], r["col"]),
    )

    features = feature_matrix(ordered)
    scaled = model.scaler.transform(features)
    embedded = model.pca.transform(scaled)

    centers = model.clustering.cluster_centers_

    if not np.isfinite(embedded).all():
        raise ValueError("Invalid candidate embedding")

    remaining = set(range(len(ordered)))
    selected = []

    for cluster_id, center in enumerate(centers):
        if not remaining:
            raise RuntimeError("Candidate pool exhausted")

        def choice_key(index):
            distance = float(
                np.linalg.norm(embedded[index] - center)
            )
            return (
                distance,
                ordered[index]["row"],
                ordered[index]["col"],
            )

        chosen = min(remaining, key=choice_key)
        distance = choice_key(chosen)[0]

        record = ordered[chosen]

        selected.append({
            "tile": tile,
            "row": record["row"],
            "col": record["col"],
            "lat": record["lat"],
            "lon": record["lon"],
            "cluster_id": cluster_id,
            "centroid_distance_pca": distance,
        })

        remaining.remove(chosen)

    if len(selected) != budget:
        raise RuntimeError("Incorrect selection count")

    return selected
