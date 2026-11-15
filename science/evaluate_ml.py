"""FieldTwin ML-A: frozen geographic holdout evaluation.

Compare unsupervised terrain discovery with three
non-ML candidate-selection methods under identical
candidate budgets and development-fitted feature scaling.

The metric measures terrain-descriptor representation,
NOT validated Mars-analog suitability.
"""

import numpy as np
from sklearn.metrics import pairwise_distances

from science.ml_discovery import (
    SELECTION_BUDGET,
    EXPECTED_CANDIDATES,
    select_ml_candidates,
)
from science.ml_terrain import (
    EVALUATION_TILES,
    FEATURE_KEYS,
    feature_matrix,
)


RANDOM_SEEDS = tuple(range(20261115, 20261145))

EXPECTED_ASSESSMENT = {
    "s25w071": 22,
    "s24w068": 39,
}


def _ordered(records):
    return sorted(records, key=lambda r: (r["row"], r["col"]))


def _validate_partitions(candidates, assessment):
    """Validate the frozen disjoint geographic partitions."""
    if not candidates or not assessment:
        raise ValueError("Empty evaluation partition")

    tiles = {
        r["tile"] for r in candidates + assessment
    }
    if len(tiles) != 1:
        raise ValueError("Mixed evaluation tiles")

    tile = next(iter(tiles))
    if tile not in EVALUATION_TILES:
        raise ValueError("Unregistered evaluation tile")

    if len(candidates) != EXPECTED_CANDIDATES[tile]:
        raise ValueError("Candidate count mismatch")

    if len(assessment) != EXPECTED_ASSESSMENT[tile]:
        raise ValueError("Assessment count mismatch")

    for records, required_partition in (
        (candidates, "candidate"),
        (assessment, "assessment"),
    ):
        if any(
            r["partition"] != required_partition
            or r.get("land_fraction") != 1.0
            or r["valid_fraction"] < 0.95
            or r["stencil_fraction"] < 0.95
            for r in records
        ):
            raise ValueError("Invalid evaluation eligibility")

    ids_a = {
        (r["row"], r["col"]) for r in candidates
    }
    ids_b = {
        (r["row"], r["col"]) for r in assessment
    }

    if (
        len(ids_a) != len(candidates)
        or len(ids_b) != len(assessment)
        or not ids_a.isdisjoint(ids_b)
    ):
        raise ValueError("Duplicate or overlapping partitions")

    return tile


def _farthest_first(vectors, first, budget):
    """Select by maximin distance with index tie-breaking."""
    n = len(vectors)
    if not (0 <= first < n and 1 <= budget <= n):
        raise ValueError("Invalid selection parameters")

    selected = [first]
    remaining = set(range(n)) - {first}

    while len(selected) < budget:
        distances = pairwise_distances(
            vectors,
            vectors[selected],
            metric="euclidean",
        )
        nearest = distances.min(axis=1)

        chosen = min(
            remaining,
            key=lambda i: (-float(nearest[i]), i),
        )
        selected.append(chosen)
        remaining.remove(chosen)

    return selected


def geographic_baseline(candidates, budget=8):
    """Registered spatial farthest-first comparator."""
    ordered = _ordered(candidates)
    coords = np.asarray(
        [[r["x_m"], r["y_m"]] for r in ordered],
        dtype=float,
    )
    return _farthest_first(coords, 0, budget)


def physical_baseline(model, candidates, budget=8):
    """Registered development-standardized feature baseline."""
    ordered = _ordered(candidates)
    scaled = model.scaler.transform(feature_matrix(ordered))

    # The fitted development feature mean is zero
    # after StandardScaler.
    distances = np.linalg.norm(scaled, axis=1)
    first = min(
        range(len(ordered)),
        key=lambda i: (float(distances[i]), i),
    )
    return _farthest_first(scaled, first, budget)


def representation_distance(model, selected, assessment):
    """Mean nearest-selection distance in five-feature space.

    Assessment observations are used ONLY for scoring.
    """
    chosen = model.scaler.transform(feature_matrix(selected))
    holdout = model.scaler.transform(feature_matrix(assessment))

    distances = pairwise_distances(
        holdout,
        chosen,
        metric="euclidean",
    )

    result = float(distances.min(axis=1).mean())
    if not np.isfinite(result):
        raise ValueError("Non-finite representation distance")
    return result


def evaluate_tile(model, candidate_records, assessment_records):
    """Evaluate one fixed holdout tile without model refitting."""
    candidates = _ordered(candidate_records)
    assessment = _ordered(assessment_records)
    tile = _validate_partitions(candidates, assessment)

    if model.training_count != 81:
        raise ValueError("Unexpected model training count")
    if tuple(model.feature_names) != FEATURE_KEYS:
        raise ValueError("Model feature definition mismatch")

    positions = {
        (r["row"], r["col"]): i
        for i, r in enumerate(candidates)
    }

    ml_sites = select_ml_candidates(model, candidates)
    ml_indices = [
        positions[(r["row"], r["col"])]
        for r in ml_sites
    ]

    geographic_indices = geographic_baseline(candidates)
    physical_indices = physical_baseline(model, candidates)

    def score(indices):
        if len(indices) != SELECTION_BUDGET:
            raise ValueError("Incorrect selection budget")
        if len(set(indices)) != SELECTION_BUDGET:
            raise ValueError("Repeated selected candidate")
        return representation_distance(
            model,
            [candidates[i] for i in indices],
            assessment,
        )

    ml_score = score(ml_indices)
    geographic_score = score(geographic_indices)
    physical_score = score(physical_indices)

    random_scores = []
    for seed in RANDOM_SEEDS:
        rng = np.random.default_rng(seed)
        indices = rng.choice(
            len(candidates),
            size=SELECTION_BUDGET,
            replace=False,
        ).tolist()
        random_scores.append(score(indices))

    random_scores = np.asarray(random_scores, dtype=float)

    if geographic_score <= 0 or physical_score <= 0:
        raise ValueError("Invalid comparator denominator")

    gain_vs_geographic = (
        (geographic_score - ml_score) / geographic_score
    )
    ratio_vs_physical = ml_score / physical_score

    geographic_gate = gain_vs_geographic >= 0.10
    physical_gate = ratio_vs_physical <= 1.05

    return {
        "tile": tile,
        "development_samples": model.training_count,
        "candidate_samples": len(candidates),
        "assessment_samples": len(assessment),
        "selection_budget": SELECTION_BUDGET,
        "metric": "mean_nearest_standardized_feature_distance",
        "scores": {
            "ml": ml_score,
            "geographic": geographic_score,
            "physical": physical_score,
            "random_mean": float(random_scores.mean()),
            "random_std": float(random_scores.std()),
            "random_min": float(random_scores.min()),
            "random_max": float(random_scores.max()),
            "random_trials": len(random_scores),
        },
        "relative_gain_vs_geographic": float(
            gain_vs_geographic
        ),
        "ratio_vs_physical": float(ratio_vs_physical),
        "geographic_gate": bool(geographic_gate),
        "physical_gate": bool(physical_gate),
        "both_gates_pass": bool(
            geographic_gate and physical_gate
        ),
        "selected_ml_sites": ml_sites,
        "scientific_limit": (
            "Descriptor coverage only; not independently "
            "validated analog suitability"
        ),
    }
