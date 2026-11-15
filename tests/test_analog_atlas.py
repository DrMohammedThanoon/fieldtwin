import json
from pathlib import Path

from science.analog_atlas import CRITERIA, OUT, ROOT, STATUS, climate_criteria

D = json.loads(OUT.read_text())


def test_status_and_criteria():
    assert D["status"] == STATUS
    assert len(D["criteria"]) == 13
    assert sum(c["kind"] == "measured" for c in D["criteria"]) == 4


def test_vectors_valid():
    for s in D["sites"] + D["offworld_sites"]:
        assert len(s["vec"]) == 13 and all(0 <= v <= 1 for v in s["vec"]), s["id"]


def test_coordinates_valid():
    for s in D["sites"]:
        assert -90 <= s["lat"] <= 90 and -180 <= s["lon"] <= 180, s["id"]
    for s in D["offworld_sites"]:
        assert s["body"] == "mars" and -90 <= s["lat"] <= 90 and -180 <= s["lon"] <= 180, s["id"]


def test_sources_present():
    for s in D["sites"] + D["offworld_sites"]:
        assert s["src"] and all(u.startswith("https://") for _, u in s["src"]), s["id"]


def test_climate_criteria_match_formulas():
    for s in D["sites"]:
        p = s["power"]
        calc = climate_criteria({**p, "P": p["P"] / 365.25})
        for i, (key, *_r) in enumerate(CRITERIA[:4]):
            assert abs(calc[key] - s["vec"][i]) < 0.01, (s["id"], key)  # P stored as integer mm/yr
    assert all(s["vec"][:4] == [1, 1, 1, 1] for s in D["offworld_sites"])


def test_no_precomputed_ranking_and_nothing_validated():
    keys = {k for s in D["sites"] + D["offworld_sites"] for k in s} | set(D)
    assert not {k for k in keys if "rank" in k or "score" in k or "similarity" in k}
    assert not list((ROOT / "outputs" / "validated").glob("*atlas*"))
