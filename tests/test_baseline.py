import pytest

from science.baseline import (
    BASELINE_KEYS,
    absolute_differences,
    pareto_layers,
)


def errors(a, b, c):
    return dict(zip(BASELINE_KEYS, (a, b, c)))


def test_absolute_differences():
    a = errors(1, 10, 2)
    b = errors(3, 17, 1)

    assert absolute_differences(a, b) == errors(2, 7, 1)


def test_dominance_chain():
    rows = {
        "poor": errors(9, 9, 9),
        "best": errors(1, 1, 1),
        "middle": errors(4, 4, 4),
    }

    assert pareto_layers(rows) == [
        ["best"], ["middle"], ["poor"]
    ]


def test_tradeoffs():
    rows = {
        "slope_match": errors(0, 5, 2),
        "relief_match": errors(5, 0, 2),
        "poor": errors(8, 8, 8),
    }

    assert pareto_layers(rows) == [
        ["relief_match", "slope_match"],
        ["poor"],
    ]


def test_equal_candidates():
    rows = {
        "B": errors(1, 2, 3),
        "A": errors(1, 2, 3),
    }

    assert pareto_layers(rows) == [["A", "B"]]


@pytest.mark.parametrize(
    "value",
    [float("nan"), float("inf"), -1],
)
def test_invalid_differences(value):
    with pytest.raises(ValueError):
        pareto_layers({
            "invalid": errors(value, 2, 3)
        })
