"""Frozen ML-B V2 prospective evaluation. No data I/O on import.

All acceptance gates and tile/site identities are fixed before scoring.
The core evaluates supplied records; only the guarded entrypoint reads real data.
"""
import hashlib
import json
import platform
from collections import Counter
from pathlib import Path

import joblib
import numpy as np
import rasterio
import scipy
import sklearn
from sklearn.metrics import average_precision_score

from science.ml_anomaly_features import describe_dem_patch
from science.ml_anomaly_v2_injection import (
    ARTIFACTS, build_v2_holdout_plan, inject_v2_artifact,
)
from science.ml_anomaly_v2_model import MODEL_NAMES, PHYSICAL_FEATURE_NAMES
from science.ml_anomaly_v2_integrity import inspect_dem_integrity

TILES = ("s21w069", "s28w069")
COUNTS = {"s21w069": 81, "s28w069": 80}
CLEAN_COUNTS = {"s21w069": 57, "s28w069": 56}
METHODS = ("random_forest", "logistic_regression", "robust")
THRESHOLDS = {"random_forest": 0.50608020,
              "logistic_regression": 0.03346996,
              "robust": 12.46553271}
MODEL_SHA = "175f31a414d9a8a32d1f44d258579fa4a035751bfdd67bda21a78d9807c92d94"
EXTRACTION_HASHES = {
    "s21w069": "99e1cbb7e04e9c2be53cd918c00f8bd707a7eb1c0ef819881ac4afefc1d41359",
    "s28w069": "73c923ca3bb21de8499099d5f875c9e22c203ea82b25fa540f3830ee2feefc51",
}
COMBINED_HASH = "b9e61d4f00c85219529f374d9627d56e705ed8d4072129ffac1682b1f0d30975"
MANIFEST = Path("docs/ML_B_V2_HOLDOUT_EXTRACTION.json")
ARTIFACT_REPORT = Path("docs/ML_B_V2_FITTED_ARTIFACT.json")
MODEL_PATH = Path("data/processed/ml_b_v2/v2_models.joblib")


def _file_sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()


def extraction_hashes(records_by_tile):
    """Reproduce the byte-exact SHA256 procedure of step 5-ML.B.54."""
    if set(records_by_tile) != set(TILES):
        raise ValueError("Holdout tile set mismatch")
    combined = hashlib.sha256()
    per_tile = {}
    for tile in TILES:
        records = records_by_tile[tile]
        if len(records) != COUNTS[tile]:
            raise ValueError("Holdout population mismatch")
        identities = [(r["row"], r["col"]) for r in records]
        frozen = sorted((x["row"], x["col"]) for x in build_v2_holdout_plan(tile))
        if identities != frozen:
            raise ValueError("Holdout row-major identity/order mismatch")
        digest = hashlib.sha256()
        for record in records:
            row, col = record["row"], record["col"]
            patch = np.asarray(record["elevation"])
            if (patch.shape != (10, 10) or patch.dtype != np.float64
                    or not np.isfinite(patch).all()):
                raise ValueError("Invalid source elevation patch")
            if (record["tile"] != tile or record["partition"] != "holdout"
                    or record["land_fraction"] != 1.0
                    or record["valid_fraction"] != 1.0):
                raise ValueError("Invalid source eligibility")
            digest.update(bytes((row, col)))
            digest.update(np.ascontiguousarray(patch.astype("<f8", copy=False)).tobytes())
        value = digest.hexdigest()
        per_tile[tile] = value
        combined.update(tile.encode("ascii"))
        combined.update(bytes.fromhex(value))
    return per_tile, combined.hexdigest()


def _assert_frozen_plans():
    for tile in TILES:
        plan = build_v2_holdout_plan(tile)
        if len(plan) != COUNTS[tile]:
            raise ValueError("Frozen site count differs")
        ids = [(a["row"], a["col"]) for a in plan]
        if len(set(ids)) != len(ids):
            raise ValueError("Duplicate frozen identities")
        positives = [a for a in plan if a["label"] == 1]
        negatives = [a for a in plan if a["label"] == 0]
        categories = Counter((a["defect_type"], a["severity"]) for a in positives)
        if (len(positives) != 24 or len(negatives) != CLEAN_COUNTS[tile]
                or set(categories) != set(ARTIFACTS)
                or any(v != 3 for v in categories.values())
                or sum(a["defect_type"] == "missing" for a in positives) != 6):
            raise ValueError("Frozen defect inventory changed")


def evaluate_records(records_by_tile, models):
    """Pure scorer; callers must separately verify real-data fingerprints.

    Used on artificial inputs in tests, and on verified real holdouts at step 60.
    No fitting or calibration occurs here.
    """
    _assert_frozen_plans()
    if set(records_by_tile) != set(TILES) or tuple(MODEL_NAMES) != METHODS:
        raise ValueError("Unexpected evaluation methods/tiles")
    if len(PHYSICAL_FEATURE_NAMES) != 5:
        raise ValueError("Wrong number of physical descriptors")
    for method in METHODS:
        if (method not in models.thresholds or
            not np.isclose(models.thresholds[method], THRESHOLDS[method],
                           rtol=0, atol=5e-7)):
            raise ValueError("Frozen model thresholds changed")

    site_outputs, evaluation_batches = {}, {}
    missing_detected = 0
    for tile in TILES:
        rows = records_by_tile[tile]
        plan = build_v2_holdout_plan(tile)
        expected_ids = sorted((a["row"], a["col"]) for a in plan)
        if len(rows) != COUNTS[tile] or [(r["row"], r["col"]) for r in rows] != expected_ids:
            raise ValueError("Frozen holdout identities/order differ")
        assignment_map = {(a["row"], a["col"]): a for a in plan}
        features, labels, metas = [], [], []
        output = []
        for rec in rows:
            assignment = assignment_map[(rec["row"], rec["col"])]
            orig = np.asarray(rec["elevation"])
            if (rec["tile"] != tile or rec["partition"] != "holdout"
                or rec["land_fraction"] != 1.0 or rec["valid_fraction"] != 1.0
                or orig.shape != (10, 10) or not np.isfinite(orig).all()):
                raise ValueError("Bad clean source patch or provenance")
            label = int(assignment["label"])
            defect = assignment["defect_type"] if label else None
            if label:
                modified, injection_metadata = inject_v2_artifact(orig.copy(), assignment)
                if not isinstance(injection_metadata, dict):
                    raise ValueError("Missing frozen injection metadata")
            else:
                modified = orig.copy()
            modified = np.asarray(modified)
            if modified.shape != (10, 10):
                raise ValueError("Invalid injected artifact shape")
            integrity = inspect_dem_integrity(modified)
            missing_flag = bool(integrity.nan_count or integrity.inf_count)
            metadata = {"tile": tile, "row": rec["row"], "col": rec["col"],
                        "label": label, "defect_type": defect,
                        "severity": assignment["severity"] if label else None,
                        "integrity_flag": missing_flag}
            if defect == "missing":
                missing_detected += int(missing_flag)
                output.append(metadata)
                continue
            if missing_flag:
                raise ValueError("Non-missing site unexpectedly invalid")
            descriptors = describe_dem_patch(modified)
            vector = np.asarray([descriptors[name] for name in PHYSICAL_FEATURE_NAMES],
                                dtype=np.float64)
            if vector.shape != (5,) or not np.isfinite(vector).all():
                raise ValueError("Invalid physical descriptors")
            features.append(vector)
            labels.append(label)
            metas.append(metadata)
            output.append(metadata)
        if len(features) != COUNTS[tile] - 6 or sum(labels) != 18:
            raise ValueError("Incorrect physical evaluation population")
        matrix = np.asarray(features, dtype=np.float64)
        matrix.setflags(write=False)
        scores = models.score(matrix)
        flags = models.flags(matrix)
        for method in METHODS:
            vals = np.asarray(scores[method], dtype=float)
            marked = np.asarray(flags[method], dtype=bool)
            if (vals.shape != (len(matrix),) or marked.shape != vals.shape
                    or not np.isfinite(vals).all()
                    or not np.array_equal(marked, vals > models.thresholds[method])):
                raise ValueError("Scoring or frozen flag mismatch")
            for meta, score, flag in zip(metas, vals, marked):
                meta.setdefault("scores", {})[method] = float(score)
                meta.setdefault("physical_flags", {})[method] = bool(flag)
        evaluation_batches[tile] = (np.asarray(labels, dtype=int), scores, flags)
        site_outputs[tile] = output
    metrics = {"tiles": {}, "pooled": {}, "gates": {}}
    for tile in TILES:
        labels, scores, flags = evaluation_batches[tile]
        per_method = {}
        for method in METHODS:
            ap = float(average_precision_score(labels, scores[method]))
            fpr = float(np.mean(np.asarray(flags[method])[labels == 0]))
            tpr = float(np.mean(np.asarray(flags[method])[labels == 1]))
            per_method[method] = {"average_precision": ap, "clean_fpr": fpr,
                                  "physical_tpr": tpr}
        metrics["tiles"][tile] = per_method
    all_labels = np.concatenate([evaluation_batches[tile][0] for tile in TILES])
    for method in METHODS:
        all_scores = np.concatenate([evaluation_batches[tile][1][method] for tile in TILES])
        metrics["pooled"][method] = {
            "average_precision": float(average_precision_score(all_labels, all_scores))}
    rf_ap = metrics["pooled"]["random_forest"]["average_precision"]
    best_other = max(metrics["pooled"][m]["average_precision"] for m in METHODS if m != "random_forest")
    pooled_gate = rf_ap - best_other >= 0.05 - 1e-12
    per_tile_ap = all(
        metrics["tiles"][tile]["random_forest"]["average_precision"] + 1e-12 >=
        metrics["tiles"][tile][other]["average_precision"]
        for tile in TILES for other in METHODS if other != "random_forest")
    per_tile_fpr = all(
        metrics["tiles"][tile]["random_forest"]["clean_fpr"] <=
        metrics["tiles"][tile][other]["clean_fpr"] + 0.05 + 1e-12
        for tile in TILES for other in METHODS if other != "random_forest")
    integrity_gate = missing_detected == 12
    metrics["gates"] = {"pooled_ap_advantage_at_least_0_05": bool(pooled_gate),
                        "per_tile_ap_no_regression": bool(per_tile_ap),
                        "per_tile_fpr_excess_at_most_0_05": bool(per_tile_fpr),
                        "missing_integrity_12_of_12": bool(integrity_gate)}
    metrics["missing_detected"] = int(missing_detected)
    metrics["decision"] = "GO" if all(metrics["gates"].values()) else "NO-GO"
    metrics["population"] = {"all": 161, "physical_positive": 36,
                             "missing_positive": 12, "clean_negative": 113,
                             "scored_physical_layer": 149}
    return {"summary": metrics, "sites": site_outputs}


def run_frozen_benchmark():
    """Guarded real-data entrypoint. DO NOT CALL BEFORE STEP 60."""
    from science.ml_anomaly_v2_holdout import extract_v2_holdout_tile
    import joblib

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    report = json.loads(ARTIFACT_REPORT.read_text(encoding="utf-8"))
    if manifest.get("combined_extraction_sha256") != COMBINED_HASH:
        raise ValueError("Unfrozen extraction inventory")
    if manifest.get("evaluation_module_sha256") != _file_sha(Path(__file__)):
        raise ValueError("Prospective scoring implementation is not frozen")
    if manifest.get("thresholds") != THRESHOLDS:
        raise ValueError("Frozen threshold manifest mismatch")
    if _file_sha("docs/ML_B_V2_PROTOCOL.md") != manifest.get("frozen_protocol_sha256"):
        raise ValueError("Frozen protocol fingerprint changed")
    if _file_sha(ARTIFACT_REPORT) != "261458adf491446138d05a9941aa26faba7a2edec8ad39c43a42e851f330e4a5":
        raise ValueError("Fitted artifact provenance changed")
    if _file_sha(MODEL_PATH) != MODEL_SHA or report.get("artifact_sha256") != MODEL_SHA:
        raise ValueError("Fitted model fingerprint mismatch")
    version = report.get("software_versions", {})
    actual = {"python": platform.python_version(), "numpy": np.__version__,
              "scipy": scipy.__version__, "scikit_learn": sklearn.__version__,
              "rasterio": rasterio.__version__, "joblib": joblib.__version__}
    if any(actual[k] != version.get(k) for k in actual):
        raise ValueError("Fitted model environment mismatch")
    for path, digest in manifest.get("source_file_sha256", {}).items():
        if _file_sha(path) != digest:
            raise ValueError("Original NASADEM input changed")
    records = {tile: extract_v2_holdout_tile(tile) for tile in TILES}
    tile_hashes, combined = extraction_hashes(records)
    if tile_hashes != EXTRACTION_HASHES or combined != COMBINED_HASH:
        raise ValueError("Extracted holdout patch fingerprint changed")
    # Only this locally created, verified joblib file is trusted.
    models = joblib.load(MODEL_PATH)
    for method in METHODS:
        if float(models.thresholds[method]) != float(report["methods"][method]["calibration_threshold"]):
            raise ValueError("Reloaded model threshold differs from committed provenance")
    result = evaluate_records(records, models)
    for path, digest in manifest.get("source_file_sha256", {}).items():
        if _file_sha(path) != digest:
            raise ValueError("Source raster mutated during evaluation")
    if _file_sha(MODEL_PATH) != MODEL_SHA:
        raise ValueError("Fitted model changed during evaluation")
    return result
