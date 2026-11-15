"""Synthetic-only V2 benchmark tests; no real NASADEM or model binaries."""
from copy import deepcopy

import numpy as np
import pytest

from science.ml_anomaly_v2_holdout import assemble_holdout_records
from science.ml_anomaly_v2_evaluation import (
    TILES, COMBINED_HASH, METHODS, THRESHOLDS,
    _assert_frozen_plans, evaluate_records, extraction_hashes,
)


class ArtificialScores:
    def __init__(self):
        self.thresholds = THRESHOLDS.copy()

    def score(self, x):
        # Intentionally artificial; not a fitted model or benchmark result.
        x = np.asarray(x)
        z = np.asarray(x[:, 2], dtype=float)
        return {"random_forest": z / 200.0,
                "logistic_regression": z / 1000.0,
                "robust": z}

    def flags(self, x):
        scores = self.score(x)
        return {name: values > self.thresholds[name]
                for name, values in scores.items()}


def artificial_records():
    result = {}
    rr, cc = np.indices((10, 10))
    for tile in TILES:
        screens = {(r, c): np.zeros((10, 10), dtype=np.uint8)
                   for r in range(9) for c in range(9)}
        if tile == "s28w069":
            screens[(5, 2)][2:6, 2:6] = 255
        patches = {(r, c): np.asarray(1000 + rr * 0.4 + cc * 0.7, dtype=float)
                   for r in range(9) for c in range(9)
                   if not (tile == "s28w069" and (r, c) == (5, 2))}
        result[tile] = assemble_holdout_records(tile, screens, patches)
    return result


def test_frozen_assignment_inventory():
    _assert_frozen_plans()


def test_synthetic_end_to_end_population_and_gates():
    original = artificial_records()
    before = {t: [r["elevation"].copy() for r in original[t]] for t in TILES}
    evaluated = evaluate_records(original, ArtificialScores())
    summary = evaluated["summary"]
    assert summary["population"] == {
        "all": 161, "physical_positive": 36,
        "missing_positive": 12, "clean_negative": 113,
        "scored_physical_layer": 149,
    }
    assert len(evaluated["sites"]["s21w069"]) == 81
    assert len(evaluated["sites"]["s28w069"]) == 80
    assert set(summary["gates"]) == {
        "pooled_ap_advantage_at_least_0_05",
        "per_tile_ap_no_regression",
        "per_tile_fpr_excess_at_most_0_05",
        "missing_integrity_12_of_12",
    }
    assert summary["missing_detected"] == 12
    assert summary["decision"] in {"GO", "NO-GO"}
    for tile in TILES:
        for method in METHODS:
            stat = summary["tiles"][tile][method]
            assert -1e-12 <= stat["average_precision"] <= 1 + 1e-12
            assert 0 <= stat["clean_fpr"] <= 1
        assert all(np.array_equal(a["elevation"], b)
                   for a, b in zip(original[tile], before[tile]))


def test_synthetic_determinism():
    records = artificial_records()
    first = evaluate_records(records, ArtificialScores())
    second = evaluate_records(records, ArtificialScores())
    assert first == second


def test_unexpected_extra_tile_rejected():
    records = artificial_records()
    records["s25w070"] = []
    with pytest.raises(ValueError, match="methods/tiles"):
        evaluate_records(records, ArtificialScores())


def test_dropped_location_rejected():
    records = artificial_records()
    records["s21w069"].pop()
    with pytest.raises(ValueError, match="identities/order"):
        evaluate_records(records, ArtificialScores())


def test_location_reorder_rejected():
    records = artificial_records()
    records["s21w069"][0], records["s21w069"][1] = (
        records["s21w069"][1], records["s21w069"][0]
    )
    with pytest.raises(ValueError, match="identities/order"):
        evaluate_records(records, ArtificialScores())


def test_invalid_source_patch_rejected():
    records = artificial_records()
    records["s21w069"][0]["elevation"][1, 1] = np.nan
    with pytest.raises(ValueError, match="Bad clean"):
        evaluate_records(records, ArtificialScores())


def test_threshold_change_rejected():
    records = artificial_records()
    model = ArtificialScores()
    model.thresholds["random_forest"] += 0.02
    with pytest.raises(ValueError, match="thresholds"):
        evaluate_records(records, model)


def test_extraction_hash_is_deterministic_and_strict():
    records = artificial_records()
    first, combined = extraction_hashes(records)
    second, again = extraction_hashes(records)
    assert first == second and combined == again
    assert combined != COMBINED_HASH
    records["s21w069"][0]["elevation"][0, 0] += 1
    changed, changed_combined = extraction_hashes(records)
    assert changed_combined != combined
    assert changed["s28w069"] == first["s28w069"]


def test_extraction_hash_rejects_extra_tile():
    records = artificial_records()
    records["s25w070"] = []
    with pytest.raises(ValueError, match="tile set"):
        extraction_hashes(records)


def test_report_is_synthetic_only_no_real_run_invoked(monkeypatch):
    import science.ml_anomaly_v2_holdout as reader
    def forbidden(*args, **kwargs):
        raise AssertionError("Actual holdout reader called in unit test")
    monkeypatch.setattr(reader, "extract_v2_holdout_tile", forbidden)
    result = evaluate_records(artificial_records(), ArtificialScores())
    assert result["summary"]["population"]["all"] == 161


def test_deliberately_weak_random_forest_is_no_go():
    class WeakRF(ArtificialScores):
        def score(self, x):
            result = super().score(x)
            result["random_forest"] = -result["robust"]
            return result

    summary = evaluate_records(artificial_records(), WeakRF())["summary"]
    assert summary["decision"] == "NO-GO"
    assert summary["gates"]["pooled_ap_advantage_at_least_0_05"] is False


def test_incorrect_frozen_threshold_flags_rejected():
    class IncorrectFlags(ArtificialScores):
        def flags(self, x):
            result = super().flags(x)
            result["robust"] = np.logical_not(result["robust"])
            return result

    with pytest.raises(ValueError, match="Scoring or frozen flag"):
        evaluate_records(artificial_records(), IncorrectFlags())
