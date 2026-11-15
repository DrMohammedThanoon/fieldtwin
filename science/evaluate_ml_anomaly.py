"""FieldTwin ML-B: frozen synthetic-defect evaluation.

No fitting or threshold selection occurs here.

Synthetic labels are experimental ground truth
for injected changes, not actual NASADEM defects.
"""

from collections import Counter

import numpy as np
from sklearn.metrics import (
    average_precision_score,
    precision_recall_curve,
)

from science.ml_anomaly_injection import (
    EVALUATION_DESIGN,
    build_injection_plan,
    inject_dem_artifact,
)
from science.ml_anomaly_model import (
    FittedAnomalyScreeners,
    score_anomaly_patches,
)


MIN_AP_GAIN = 0.05
MAX_FPR_INCREASE = 0.05


def _validate_model(model):
    if not isinstance(model, FittedAnomalyScreeners):
        raise TypeError("Expected fitted ML-B screeners")

    if model.training_count != 81:
        raise ValueError("Unexpected training population")

    if not np.isfinite([
        model.forest_threshold,
        model.robust_threshold,
    ]).all():
        raise ValueError("Invalid frozen thresholds")


def evaluate_anomaly_tile(model, tile, records):
    """Evaluate one predefined geographic holdout.

    The model and its thresholds are read-only.
    Each patch receives exactly one fixed assignment.
    """
    _validate_model(model)

    if tile not in EVALUATION_DESIGN:
        raise ValueError("Unregistered evaluation tile")

    ordered = sorted(
        records, key=lambda r: (r["row"], r["col"])
    )

    plan = build_injection_plan(tile, ordered)

    if len(plan) != len(ordered):
        raise RuntimeError("Injection inventory mismatch")

    injected = []
    audits = []

    for record, assignment in zip(ordered, plan):
        if (
            record["tile"] != assignment["tile"]
            or record["row"] != assignment["row"]
            or record["col"] != assignment["col"]
            or record["partition"]
            != assignment["partition"]
        ):
            raise ValueError("Injection identity mismatch")

        original = np.asarray(
            record["elevation"], dtype=np.float64
        )

        if (
            original.shape != (10, 10)
            or not np.isfinite(original).all()
        ):
            raise ValueError("Invalid clean elevation patch")

        modified, audit = inject_dem_artifact(
            original, assignment
        )

        if np.shares_memory(modified, original):
            raise RuntimeError("Injection reused source memory")

        injected.append(modified)
        audits.append(audit)

    scores = score_anomaly_patches(model, injected)

    labels = np.asarray(
        [a["label"] for a in audits],
        dtype=np.int64,
    )

    positive = int(labels.sum())
    clean = int((labels == 0).sum())

    expected = EVALUATION_DESIGN[tile]

    if (
        positive != expected["positive"]
        or clean != expected["eligible"] - positive
    ):
        raise RuntimeError("Synthetic prevalence mismatch")

    forest = np.asarray(
        scores["forest_scores"], dtype=float
    )
    robust = np.asarray(
        scores["robust_scores"], dtype=float
    )
    forest_flags = np.asarray(
        scores["forest_flags"], dtype=bool
    )
    robust_flags = np.asarray(
        scores["robust_flags"], dtype=bool
    )

    n = len(ordered)

    if any(
        a.shape != (n,)
        for a in (
            forest, robust,
            forest_flags, robust_flags
        )
    ):
        raise RuntimeError("Score array dimensions mismatch")

    if not (
        np.isfinite(forest).all()
        and np.isfinite(robust).all()
    ):
        raise ValueError("Non-finite anomaly score")

    if not np.array_equal(
        forest_flags,
        forest > model.forest_threshold,
    ):
        raise RuntimeError("Forest cutoff mismatch")

    if not np.array_equal(
        robust_flags,
        robust > model.robust_threshold,
    ):
        raise RuntimeError("Robust cutoff mismatch")

    forest_ap = float(
        average_precision_score(labels, forest)
    )
    robust_ap = float(
        average_precision_score(labels, robust)
    )

    negative_mask = labels == 0
    positive_mask = labels == 1

    forest_fp = int(
        forest_flags[negative_mask].sum()
    )
    robust_fp = int(
        robust_flags[negative_mask].sum()
    )

    forest_tp = int(
        forest_flags[positive_mask].sum()
    )
    robust_tp = int(
        robust_flags[positive_mask].sum()
    )

    forest_precision, forest_recall, _ = (
        precision_recall_curve(labels, forest)
    )
    robust_precision, robust_recall, _ = (
        precision_recall_curve(labels, robust)
    )

    rows = []

    for index, audit in enumerate(audits):
        rows.append({
            **audit,
            "forest_score": float(forest[index]),
            "robust_score": float(robust[index]),
            "forest_flag": bool(forest_flags[index]),
            "robust_flag": bool(robust_flags[index]),
        })

    defect_counts = Counter(
        (r["defect_type"], r["severity"])
        for r in rows
        if r["label"] == 1
    )

    defect_recall = []

    for defect, severity in sorted(defect_counts):
        subset = [
            r for r in rows
            if r["defect_type"] == defect
            and r["severity"] == severity
        ]

        defect_recall.append({
            "defect_type": defect,
            "severity": severity,
            "count": len(subset),
            "forest_detected": sum(
                r["forest_flag"] for r in subset
            ),
            "robust_detected": sum(
                r["robust_flag"] for r in subset
            ),
        })

    return {
        "tile": tile,
        "count": n,
        "positives": positive,
        "clean": clean,
        "prevalence": positive / n,
        "forest_ap": forest_ap,
        "robust_ap": robust_ap,
        "ap_difference": forest_ap - robust_ap,
        "forest_fpr": forest_fp / clean,
        "robust_fpr": robust_fp / clean,
        "forest_false_positives": forest_fp,
        "robust_false_positives": robust_fp,
        "forest_detected": forest_tp,
        "robust_detected": robust_tp,
        "forest_recall": forest_tp / positive,
        "robust_recall": robust_tp / positive,
        "forest_pr_curve": {
            "precision": forest_precision.tolist(),
            "recall": forest_recall.tolist(),
        },
        "robust_pr_curve": {
            "precision": robust_precision.tolist(),
            "recall": robust_recall.tolist(),
        },
        "defect_recall": defect_recall,
        "records": rows,
    }


def summarize_anomaly_evaluation(tile_results):
    """Apply original pooled and per-tile numerical gates."""
    if len(tile_results) != 2:
        raise ValueError("Expected exactly two evaluation tiles")

    by_tile = {
        result["tile"]: result
        for result in tile_results
    }

    if set(by_tile) != set(EVALUATION_DESIGN):
        raise ValueError("Geographic holdout coverage mismatch")

    if len(by_tile) != len(tile_results):
        raise ValueError("Repeated evaluation tile")

    all_rows = []

    tile_ap_pass = True
    tile_fpr_pass = True
    gate_details = {}

    for tile in EVALUATION_DESIGN:
        result = by_tile[tile]
        spec = EVALUATION_DESIGN[tile]

        rows = result["records"]

        if (
            len(rows) != spec["eligible"]
            or result["count"] != spec["eligible"]
            or result["positives"] != spec["positive"]
            or result["clean"]
            != spec["eligible"] - spec["positive"]
        ):
            raise ValueError("Invalid evaluation counts")

        ap_gate = (
            result["forest_ap"] >= result["robust_ap"]
        )
        fpr_gate = (
            result["forest_fpr"]
            <= result["robust_fpr"] + MAX_FPR_INCREASE
        )

        tile_ap_pass &= bool(ap_gate)
        tile_fpr_pass &= bool(fpr_gate)

        gate_details[tile] = {
            "ap_gate": bool(ap_gate),
            "fpr_gate": bool(fpr_gate),
        }

        all_rows.extend(rows)

    labels = np.asarray(
        [r["label"] for r in all_rows],
        dtype=int,
    )
    forest = np.asarray(
        [r["forest_score"] for r in all_rows],
        dtype=float,
    )
    robust = np.asarray(
        [r["robust_score"] for r in all_rows],
        dtype=float,
    )

    if (
        len(labels) != 122
        or int(labels.sum()) != 31
        or int((labels == 0).sum()) != 91
        or not np.isfinite(forest).all()
        or not np.isfinite(robust).all()
    ):
        raise ValueError("Invalid pooled evaluation inventory")

    forest_ap = float(
        average_precision_score(labels, forest)
    )
    robust_ap = float(
        average_precision_score(labels, robust)
    )

    gain = forest_ap - robust_ap
    pooled_gate = gain >= MIN_AP_GAIN

    return {
        "count": 122,
        "positives": 31,
        "clean": 91,
        "prevalence": 31 / 122,
        "forest_ap": forest_ap,
        "robust_ap": robust_ap,
        "absolute_ap_gain": gain,
        "pooled_ap_gate": bool(pooled_gate),
        "per_tile_ap_gate": bool(tile_ap_pass),
        "per_tile_fpr_gate": bool(tile_fpr_pass),
        "per_tile_gates": gate_details,
        "numerical_go": bool(
            pooled_gate
            and tile_ap_pass
            and tile_fpr_pass
        ),
        "scientific_limit": (
            "Synthetic defect detection only; "
            "real DEM artifact validation not established"
        ),
    }
