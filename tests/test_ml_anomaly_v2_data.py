"""Artificial-data tests for ML-B V2 preparation."""

import numpy as np
import pytest

import science.ml_anomaly_v2_data as module

from science.ml_anomaly_v2_data import (
    CALIBRATION_SITES,
    TRAINING_SITES,
    prepare_v2_development_records,
)


def fake_records():
    records = []

    rr, cc = np.indices((10, 10))

    for row in range(9):
        for col in range(9):
            patch = (
                1000.0
                + rr * 0.7
                + cc * 1.3
                + row * 2.0
                + col * 0.5
            ).astype(float)

            records.append({
                "tile": "s25w070",
                "row": row,
                "col": col,
                "partition": "development",
                "lat": -24.9 + row * 0.1,
                "lon": -69.9 + col * 0.1,
                "x_m": 500000.0 + col * 1000,
                "y_m": 7200000.0 + row * 1000,
                "land_fraction": 1.0,
                "valid_fraction": 1.0,
                "stencil_fraction": 1.0,
                "elevation": patch,
                "provenance": {
                    "source_path": (
                        "data/raw/earth/nasadem/"
                        "s25w070.hgt"
                    ),
                    "source_crs": "EPSG:4326",
                    "target_crs": "EPSG:32719",
                    "source_resampling": "bilinear",
                },
            })

    return records


@pytest.fixture(scope="module")
def prepared():
    records = fake_records()

    original = [
        record["elevation"].copy()
        for record in records
    ]

    data = prepare_v2_development_records(
        list(reversed(records))
    )

    for before, record in zip(original, records):
        assert np.array_equal(
            before,
            record["elevation"],
        )

    return data


def test_exact_training_inventory(prepared):
    assert prepared.training_features.shape == (819, 5)

    labels = [
        a["label"]
        for a in prepared.training_assignments
    ]

    assert len(labels) == 819
    assert labels.count(0) == 63
    assert labels.count(1) == 756

    assert prepared.training_sites == TRAINING_SITES
    assert len(prepared.training_sites) == 63

    assert all(
        site[0] == "s25w070" and site[2] <= 6
        for site in prepared.training_sites
    )


def test_exact_clean_calibration_inventory(prepared):
    assert prepared.calibration_features.shape == (18, 5)
    assert prepared.calibration_sites == CALIBRATION_SITES

    training = set(prepared.training_sites)
    calibration = set(prepared.calibration_sites)

    assert len(training) == 63
    assert len(calibration) == 18
    assert not training.intersection(calibration)


def test_finite_read_only_feature_matrices(prepared):
    assert np.isfinite(
        prepared.training_features
    ).all()

    assert np.isfinite(
        prepared.calibration_features
    ).all()

    assert not prepared.training_features.flags.writeable
    assert not prepared.calibration_features.flags.writeable

    with pytest.raises(ValueError):
        prepared.training_features[0, 0] = 999.0


def test_rejects_incomplete_inventory():
    with pytest.raises(
        ValueError, match="81 development records"
    ):
        prepare_v2_development_records(
            fake_records()[:-1]
        )


def test_rejects_duplicate_identity():
    records = fake_records()

    records[-1] = {
        **records[-1],
        "row": 0,
        "col": 0,
        "lat": -24.9,
        "lon": -69.9,
    }

    with pytest.raises(
        ValueError, match="Duplicate"
    ):
        prepare_v2_development_records(records)


@pytest.mark.parametrize(
    "field,value",
    [
        ("tile", "s21w069"),
        ("partition", "assessment"),
        ("lat", -20.9),
        ("land_fraction", 0.84),
        ("valid_fraction", 0.9),
    ],
)
def test_rejects_invalid_development_metadata(
    field, value
):
    records = fake_records()
    records[0][field] = value

    with pytest.raises(ValueError):
        prepare_v2_development_records(records)


def test_rejects_holdout_source_provenance():
    records = fake_records()

    records[0]["provenance"]["source_path"] = (
        "data/raw/earth/nasadem/s21w069.hgt"
    )

    with pytest.raises(
        ValueError, match="provenance"
    ):
        prepare_v2_development_records(records)


@pytest.mark.parametrize(
    "bad_value",
    [np.nan, np.inf],
)
def test_rejects_invalid_source_dem(bad_value):
    records = fake_records()
    records[0]["elevation"][4, 4] = bad_value

    with pytest.raises(
        ValueError, match="integrity"
    ):
        prepare_v2_development_records(records)


def test_rejects_masked_source_dem():
    records = fake_records()

    masked = np.ma.array(
        records[0]["elevation"]
    )

    masked.mask = np.zeros(
        (10, 10), dtype=bool
    )

    masked.mask[3, 3] = True

    records[0]["elevation"] = masked

    with pytest.raises(
        ValueError, match="masked"
    ):
        prepare_v2_development_records(records)


def test_loader_requests_development_tile_only(
    monkeypatch
):
    requested = []
    sentinel = object()

    def fake_loader(tile):
        requested.append(tile)
        return fake_records()

    def fake_prepare(records):
        assert len(records) == 81
        return sentinel

    monkeypatch.setattr(
        module, "extract_anomaly_tile",
        fake_loader,
    )

    monkeypatch.setattr(
        module, "prepare_v2_development_records",
        fake_prepare,
    )

    assert module.load_v2_development_data() is sentinel
    assert requested == ["s25w070"]


def test_frozen_model_interface_compatible(prepared):
    from science.ml_anomaly_v2_injection import (
        build_v2_training_plan,
    )

    assert list(
        prepared.training_assignments
    ) == build_v2_training_plan()

    assert tuple(
        prepared.calibration_sites
    ) == CALIBRATION_SITES

    assert prepared.training_features.shape[1] == 5
    assert prepared.calibration_features.shape[1] == 5
