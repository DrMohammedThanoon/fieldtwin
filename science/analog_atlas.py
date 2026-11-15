"""Analog Atlas context data builder (NOT a FieldTwin measured result).

Loads the SameBeyond handoff, re-requests NASA POWER climatology for the Earth
sites, verifies it against power.csv, recomputes the four climate criteria and
writes app/src/data/analog_atlas.json. No similarity ranking is precomputed.
Usage: python -m science.analog_atlas [--offline]
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import ssl
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "context" / "analog_atlas"
CACHE = ROOT / "data" / "raw" / "power_climatology"
OUT = ROOT / "app" / "src" / "data" / "analog_atlas.json"
_CA = next((c for c in ('/etc/ssl/cert.pem', '/etc/ssl/certs/ca-certificates.crt') if Path(c).exists()), None)  # Python.org builds ship no CA bundle
STATUS = "context_literature_coded_not_validated"
TOLERANCE = 0.05  # max |POWER annual - power.csv| per variable
VEC_TOLERANCE = 0.002  # handoff vectors are rounded to 3 decimals

# json key -> (power.csv column, NASA POWER parameter)
POWER_VARS = {"T": ("T2M", "T2M"), "Tmax": ("T2M_MAX", "T2M_MAX"), "Tmin": ("T2M_MIN", "T2M_MIN"),
              "P": ("PREC_mm_day", "PRECTOTCORR"), "RH": ("RH2M", "RH2M"),
              "WS": ("WS2M", "WS2M"), "SW": ("SW_MJ", "ALLSKY_SFC_SW_DWN")}

CRITERIA = [  # key, label, kind, unit/formula
    ("arid", "Aridity", "measured", "1 - min(log10(P_mm_yr+1)/log10(1001),1); P_mm_yr = PRECTOTCORR_ANN*365.25"),
    ("dry_air", "Dry air", "measured", "1 - RH2M_ANN/100"),
    ("cold", "Cold", "measured", "clamp((25 - T2M_ANN)/60, 0, 1)"),
    ("swing", "Temperature extremes", "measured", "clamp((T2M_MAX_ANN - T2M_MIN_ANN)/80, 0, 1)"),
    ("basalt", "Basalt", "coded", "literature-coded 0-1"),
    ("impact", "Impact structure", "coded", "literature-coded 0-1"),
    ("cave", "Caves / lava tubes", "coded", "literature-coded 0-1"),
    ("ice", "Ice", "coded", "literature-coded 0-1"),
    ("evap", "Salts / evaporites", "coded", "literature-coded 0-1"),
    ("aqueous", "Ancient water", "coded", "literature-coded 0-1"),
    ("aeolian", "Wind erosion", "coded", "literature-coded 0-1"),
    ("bio", "Biosignature value", "coded", "literature-coded 0-1"),
    ("barren", "Bare surface", "coded", "literature-coded 0-1"),
]

LIMITATIONS = [
    "Context only: not a FieldTwin search result and not validated. FieldTwin's measured search is the bounded Atacama study (data/SEARCH_SCOPE.md).",
    "Only 4 of 13 criteria are measured (NASA POWER climatology, ~0.5 degree cells); 9 are literature-coded by the SameBeyond team.",
    "Mars climate criteria are fixed at 1.0 (extreme) for every Mars site.",
    "The context index is a weighted mean of coded trait closeness, not a terrain similarity, traversability or probability.",
    "Earth cannot reproduce Mars gravity (0.38 g), the thin CO2 atmosphere, or radiation.",
    "Slope, ruggedness and relief are not measured for atlas sites.",
    "Mars coordinates are planetocentric, east-positive, -180..180.",
]


# Editorial overrides of handoff text (documented in docs/ANALOG_ATLAS.md): removes an
# unsupported superlative and the banned word "match".
TEXT_OVERRIDES = {("dryvalleys", "strong"): "Cold, dry and ground ice — a commonly cited Mars climate analog."}


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def climate_criteria(p: dict) -> dict:
    """The four measured criteria. p holds POWER annual values (P in mm/day)."""
    p_yr = p["P"] * 365.25
    return {
        "arid": 1 - min(math.log10(p_yr + 1) / math.log10(1001), 1),
        "dry_air": 1 - p["RH"] / 100,
        "cold": clamp((25 - p["T"]) / 60),
        "swing": clamp((p["Tmax"] - p["Tmin"]) / 80),
    }


def power_url(template: str, lat: float, lon: float) -> str:
    return template.split(" (")[0].format(lat=lat, lon=lon)


def fetch_power(site_id: str, url: str) -> dict:
    """Annual POWER values for one site; cached under data/raw (git-ignored)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"{site_id}.json"
    if not f.exists():
        with urllib.request.urlopen(url, timeout=60, context=ssl.create_default_context(cafile=_CA)) as r:
            f.write_bytes(r.read())
    par = json.loads(f.read_text())["properties"]["parameter"]
    return {k: par[name]["ANN"] for k, (_, name) in POWER_VARS.items()}


def verify(site_id: str, got: dict, csv_row: dict) -> None:
    for k, (col, _) in POWER_VARS.items():
        diff = abs(got[k] - float(csv_row[col]))
        if diff > TOLERANCE:
            raise SystemExit(f"POWER mismatch {site_id} {k}: API {got[k]} vs power.csv {csv_row[col]} (diff {diff:.3f} > {TOLERANCE})")


def build(offline: bool = False) -> dict:
    ctx = json.loads((SRC / "analog_atlas_context.json").read_text())
    rows = {r["id"]: r for r in csv.DictReader((SRC / "power.csv").open())}
    template = ctx["_meta"]["power_api"]
    sites = []
    for s in ctx["sites"]:
        row = rows[s["id"]]
        url = power_url(template, s["lat"], s["lon"])
        if not offline:
            verify(s["id"], fetch_power(s["id"], url), row)
        power = {k: float(row[col]) for k, (col, _) in POWER_VARS.items()}
        power["P"] = round(power["P"] * 365.25)  # mm/yr, as in the handoff JSON
        calc = climate_criteria({**power, "P": float(row["PREC_mm_day"])})
        vec = list(s["vec"])
        for i, (key, *_rest) in enumerate(CRITERIA[:4]):
            if abs(calc[key] - vec[i]) > VEC_TOLERANCE:
                raise SystemExit(f"criterion {key} for {s['id']}: formula {calc[key]:.3f} vs handoff {vec[i]}")
            vec[i] = round(calc[key], 3)
        for (sid, field), text in TEXT_OVERRIDES.items():
            if sid == s["id"]:
                s = {**s, field: text}
        sites.append({**s, "vec": vec, "power": {**power, "elev": float(row["elev_m"])}, "power_url": url})
    return {
        "schema_version": 1,
        "status": STATUS,
        "criteria": [{"key": k, "label": l, "kind": kind, "basis": b} for k, l, kind, b in CRITERIA],
        "index_formula": "weighted mean of (1 - |earth - offworld|) over 13 criteria; weight x2 where off-world value >= 0.8; UI computes it from vectors and user weights",
        "provenance": {"source": "SameBeyond handoff; NASA POWER Climatology API v2.10.1, 2001-2025, retrieved 2026-11-13",
                       "power_api": template, "coordinates_note": ctx["_meta"]["coordinates_note"],
                       "units": {"T": "°C", "Tmax": "°C", "Tmin": "°C", "P": "mm/yr", "RH": "%", "WS": "m/s", "SW": "MJ/m²/day", "elev": "m"}},
        "sites": sites,
        "offworld_sites": [t for t in ctx["targets"] if t["body"] == "mars"],  # Earth + Mars only (project decision)
        "limitations": LIMITATIONS,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="skip the NASA POWER re-request (verification then covers formulas only)")
    out = build(ap.parse_args().offline)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(out['sites'])} Earth, {len(out['offworld_sites'])} off-world")


if __name__ == "__main__":
    main()
