"""FieldTwin ML-B synthetic DEM defect generator.

The generator creates reproducible experimental labels
and modified in-memory DEM patches. It does not alter
original NASADEM files.

Synthetic labels do not identify verified real defects.
"""

from collections import Counter

import numpy as np


RANDOM_SEED = 20261115

EVALUATION_DESIGN = {
    "s25w071": {
        "eligible": 44,
        "positive": 11,
        "candidate": 22,
        "assessment": 22,
        "stream": 0,
    },
    "s24w068": {
        "eligible": 78,
        "positive": 20,
        "candidate": 39,
        "assessment": 39,
        "stream": 1,
    },
}

ARTIFACT_CLASSES = (
    ("spike", "low"),
    ("spike", "high"),
    ("depression", "low"),
    ("depression", "high"),
    ("strip", "low"),
    ("strip", "high"),
    ("missing", "low"),
    ("missing", "high"),
)

# Extra assignments are distributed across distinct
# artifact types before repeating a type.
EXTRA_ORDER = (0, 3, 4, 7, 1, 2, 5, 6)


def build_injection_plan(tile, records):
    """Assign frozen labels to all eligible evaluation sites.

    Only geographic identities and fixed random seeds
    determine synthetic labels. No elevation descriptors,
    fitted model, or evaluation scores are inspected.
    """
    if tile not in EVALUATION_DESIGN:
        raise ValueError("Unregistered evaluation tile")

    spec = EVALUATION_DESIGN[tile]
    ordered = sorted(
        records,
        key=lambda r: (r["row"], r["col"]),
    )

    if len(ordered) != spec["eligible"]:
        raise ValueError("Incorrect eligible sample count")

    identities = set()
    partitions = Counter()

    for record in ordered:
        if record["tile"] != tile:
            raise ValueError("Mixed geographic tiles")

        row = record["row"]
        col = record["col"]

        if not (
            isinstance(row, int)
            and isinstance(col, int)
            and 0 <= row <= 8
            and 0 <= col <= 8
        ):
            raise ValueError("Invalid sampling-grid location")

        identity = (row, col)
        if identity in identities:
            raise ValueError("Duplicate sampling location")
        identities.add(identity)

        partition = record["partition"]
        expected = (
            "candidate" if (row + col) % 2 == 0
            else "assessment"
        )
        if partition != expected:
            raise ValueError("Geographic partition mismatch")

        if (
            record.get("land_fraction") != 1.0
            or record.get("valid_fraction", 0) < 0.95
            or record.get("stencil_fraction", 0) < 0.95
        ):
            raise ValueError("Ineligible land or DEM coverage")

        partitions[partition] += 1

    if (
        partitions["candidate"] != spec["candidate"]
        or partitions["assessment"] != spec["assessment"]
    ):
        raise ValueError("Incorrect partition inventory")

    rng = np.random.default_rng(
        np.random.SeedSequence(
            [RANDOM_SEED, spec["stream"]]
        )
    )

    chosen = sorted(
        int(i) for i in rng.choice(
            len(ordered),
            size=spec["positive"],
            replace=False,
        )
    )

    whole, remainder = divmod(
        spec["positive"],
        len(ARTIFACT_CLASSES),
    )

    categories = list(ARTIFACT_CLASSES) * whole
    categories.extend(
        ARTIFACT_CLASSES[i]
        for i in EXTRA_ORDER[:remainder]
    )

    if len(categories) != spec["positive"]:
        raise RuntimeError("Incorrect defect allocation")

    permutation = rng.permutation(len(categories))
    categories = [
        categories[int(i)]
        for i in permutation
    ]

    assignments = dict(zip(chosen, categories))
    plan = []

    for index, record in enumerate(ordered):
        category = assignments.get(index)
        defect, severity = (
            category if category is not None
            else (None, None)
        )

        plan.append({
            "tile": tile,
            "row": record["row"],
            "col": record["col"],
            "partition": record["partition"],
            "label": int(category is not None),
            "defect_type": defect,
            "severity": severity,
        })

    positives = sum(item["label"] for item in plan)
    if positives != spec["positive"]:
        raise RuntimeError("Incorrect synthetic prevalence")

    counts = Counter(
        (item["defect_type"], item["severity"])
        for item in plan
        if item["label"] == 1
    )

    if (
        set(counts) != set(ARTIFACT_CLASSES)
        or max(counts.values()) - min(counts.values()) > 1
    ):
        raise RuntimeError("Unbalanced artifact allocation")

    return plan


def inject_dem_artifact(clean_patch, assignment):
    """Apply exactly one planned synthetic artifact.

    Return a new array and an auditable injection record.
    The input array is not modified.
    """
    original = np.asarray(
        clean_patch,
        dtype=np.float64,
    )

    if original.shape != (10, 10):
        raise ValueError("Expected 10 x 10 DEM patch")

    if not np.isfinite(original).all():
        raise ValueError(
            "Expected fully finite verified source patch"
        )

    output = original.copy()

    tile = assignment["tile"]
    if tile not in EVALUATION_DESIGN:
        raise ValueError("Unregistered tile")

    row = assignment["row"]
    col = assignment["col"]
    label = assignment["label"]
    defect = assignment["defect_type"]
    severity = assignment["severity"]

    if not (
        isinstance(row, int)
        and isinstance(col, int)
        and 0 <= row <= 8
        and 0 <= col <= 8
    ):
        raise ValueError("Invalid sampling identity")

    if label == 0:
        if defect is not None or severity is not None:
            raise ValueError("Invalid clean assignment")

        return output, {
            **assignment,
            "affected_cells": 0,
            "location": None,
            "magnitude_m": None,
        }

    if label != 1 or (defect, severity) not in ARTIFACT_CLASSES:
        raise ValueError("Invalid synthetic defect assignment")

    spec = EVALUATION_DESIGN[tile]
    severity_index = int(severity == "high")

    rng = np.random.default_rng(
        np.random.SeedSequence([
            RANDOM_SEED,
            spec["stream"],
            row,
            col,
            severity_index,
        ])
    )

    if defect == "spike":
        r = int(rng.integers(1, 9))
        c = int(rng.integers(1, 9))
        magnitude = 60.0 if severity == "low" else 120.0

        output[r, c] += magnitude
        location = (r, c)
        affected = 1

    elif defect == "depression":
        r = int(rng.integers(1, 8))
        c = int(rng.integers(1, 8))
        magnitude = -40.0 if severity == "low" else -80.0

        output[r:r + 2, c:c + 2] += magnitude
        location = (r, c)
        affected = 4

    elif defect == "strip":
        c = int(rng.integers(1, 9))
        magnitude = 30.0 if severity == "low" else 60.0

        output[:, c] += magnitude
        location = ("column", c)
        affected = 10

    else:
        block_size = 2 if severity == "low" else 3

        # Central-interior placement, deterministically
        # selected from permitted central positions.
        r = int(rng.integers(3, 5))
        c = int(rng.integers(3, 5))

        output[
            r:r + block_size,
            c:c + block_size,
        ] = np.nan

        magnitude = None
        location = (r, c)
        affected = block_size ** 2

    audit = {
        **assignment,
        "affected_cells": affected,
        "location": location,
        "magnitude_m": magnitude,
    }

    return output, audit
