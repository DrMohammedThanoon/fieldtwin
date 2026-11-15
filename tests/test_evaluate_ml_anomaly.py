"""Synthetic verification of frozen ML-B evaluation.

No real NASADEM geographic holdouts are loaded.
"""

from copy import deepcopy

import numpy as np
import pytest
from sklearn.metrics import average_precision_score

from science.evaluate_ml_anomaly import (
    evaluate_anomaly_tile,
    summarize_anomaly_evaluation,
)
from science.ml_anomaly_injection import EVALUATION_DESIGN
from science.ml_anomaly_model import (
    fit_anomaly_screeners,
)


@pytest.fixture(scope="module")
def model():
    development = []

    for row in range(9):
        for col in range(9):
            y, x = np.indices((10, 10))

            elevation = (
                1000.0
                + 2.1 * y
                + 1.7 * x
                + (0.08 + 0.025 * row) * (x - 4.5) ** 2
                + (0.05 + 0.030 * col) * (y - 4.5) ** 2
                + (0.6 + 0.4 * ((row + col) % 5))
                * np.sin(
                    (x + 0.25 * row)
                    * (y + 0.35 * col) / 8.0
                )
            )

            development.append({
                "tile": "s25w070",
                "row": row,
                "col": col,
                "partition": "development",
                "land_fraction": 1.0,
                "valid_fraction": 1.0,
                "stencil_fraction": 1.0,
                "elevation": elevation,
            })

    return fit_anomaly_screeners(development)


def make_holdout(tile):
    spec = EVALUATION_DESIGN[tile]

    even = [
        (r, c) for r in range(9) for c in range(9)
        if (r + c) % 2 == 0
    ][:spec["candidate"]]

    odd = [
        (r, c) for r in range(9) for c in range(9)
        if (r + c) % 2 == 1
    ][:spec["assessment"]]

    records = []

    for row, col in even + odd:
        y, x = np.indices((10, 10))

        elevation = (
            1100.0
            + 1.5 * y
            + 2.0 * x
            + (0.11 + 0.02 * row) * (x - 4.5) ** 2
            + (0.08 + 0.02 * col) * (y - 4.5) ** 2
            + np.sin((x + row) * (y + col) / 9.0)
        )

        records.append({
            "tile": tile,
            "row": row,
            "col": col,
            "partition": (
                "candidate" if (row + col) % 2 == 0
                else "assessment"
            ),
            "land_fraction": 1.0,
            "valid_fraction": 1.0,
            "stencil_fraction": 1.0,
            "elevation": elevation,
        })

    return records


def test_tile_counts_prevalence_and_artifacts(model):
    for tile, spec in EVALUATION_DESIGN.items():
        result = evaluate_anomaly_tile(
            model, tile, make_holdout(tile)
        )

        assert result["count"] == spec["eligible"]
        assert result["positives"] == spec["positive"]
        assert result["clean"] == (
            spec["eligible"] - spec["positive"]
        )
        assert len(result["records"]) == spec["eligible"]
        assert len(result["defect_recall"]) == 8

        assert 0 <= result["forest_ap"] <= 1
        assert 0 <= result["robust_ap"] <= 1
        assert 0 <= result["forest_fpr"] <= 1
        assert 0 <= result["robust_fpr"] <= 1


def test_reproducibility_order_and_nonmutation(model):
    records = make_holdout("s25w071")
    original = [
        record["elevation"].copy()
        for record in records
    ]

    first = evaluate_anomaly_tile(
        model, "s25w071", records
    )
    repeated = evaluate_anomaly_tile(
        model, "s25w071", list(reversed(records))
    )

    assert first == repeated

    for record, snapshot in zip(records, original):
        np.testing.assert_array_equal(
            record["elevation"], snapshot
        )


def test_actual_average_precision_and_false_alarms(model):
    result = evaluate_anomaly_tile(
        model, "s24w068", make_holdout("s24w068")
    )

    rows = result["records"]
    labels = [r["label"] for r in rows]

    assert result["forest_ap"] == pytest.approx(
        average_precision_score(
            labels,
            [r["forest_score"] for r in rows],
        )
    )

    assert result["robust_ap"] == pytest.approx(
        average_precision_score(
            labels,
            [r["robust_score"] for r in rows],
        )
    )

    clean = [r for r in rows if r["label"] == 0]

    assert result["forest_fpr"] == pytest.approx(
        sum(r["forest_flag"] for r in clean) / len(clean)
    )

    assert result["robust_fpr"] == pytest.approx(
        sum(r["robust_flag"] for r in clean) / len(clean)
    )


def test_pooled_gates_and_score_integrity(model):
    a = evaluate_anomaly_tile(
        model, "s25w071", make_holdout("s25w071")
    )
    b = evaluate_anomaly_tile(
        model, "s24w068", make_holdout("s24w068")
    )

    summary = summarize_anomaly_evaluation([a, b])

    assert summary["count"] == 122
    assert summary["positives"] == 31
    assert summary["clean"] == 91

    assert summary["absolute_ap_gain"] == pytest.approx(
        summary["forest_ap"] - summary["robust_ap"]
    )

    expected_go = (
        summary["pooled_ap_gate"]
        and summary["per_tile_ap_gate"]
        and summary["per_tile_fpr_gate"]
    )

    assert summary["numerical_go"] == expected_go

    with pytest.raises(ValueError):
        summarize_anomaly_evaluation([a, a])

    with pytest.raises(ValueError):
        summarize_anomaly_evaluation([a])


def test_invalid_holdout_rejected_and_no_refitting(model):
    tile = "s25w071"
    records = make_holdout(tile)

    threshold_before = (
        model.forest_threshold,
        model.robust_threshold,
    )
    scaler_mean_before = model.scaler.mean_.copy()

    evaluate_anomaly_tile(model, tile, records)

    assert threshold_before == (
        model.forest_threshold,
        model.robust_threshold,
    )

    np.testing.assert_array_equal(
        scaler_mean_before, model.scaler.mean_
    )

    water = deepcopy(records)
    water[0]["land_fraction"] = 0.5

    with pytest.raises(ValueError):
        evaluate_anomaly_tile(model, tile, water)

    duplicate = deepcopy(records)
    duplicate[1]["row"] = duplicate[0]["row"]
    duplicate[1]["col"] = duplicate[0]["col"]

    with pytest.raises(ValueError):
        evaluate_anomaly_tile(model, tile, duplicate)

    missing = deepcopy(records[:-1])

    with pytest.raises(ValueError):
        evaluate_anomaly_tile(model, tile, missing)
