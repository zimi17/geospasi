from __future__ import annotations

import json
import os
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.abspath(os.path.join(HERE, "..", "examples", "geoserang", "data", "spasial"))
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "examples", "geoserang", "data"))

COORD_DECIMALS = 5
MAX_SIZE_MB = 50


def process_file(fname: str) -> None:
    src = os.path.join(RAW_DIR, fname)
    size_mb = os.path.getsize(src) >> 20
    layer_name = fname.replace(".geojson", "")
    out = os.path.join(OUT_DIR, fname)

    print(f"[PROCESS] {fname} ({size_mb}MB)...", end=" ", flush=True)
    with open(src) as f:
        data = json.load(f)

    simplified = _simplify_one(data, layer_name)
    with open(out, "w") as f:
        json.dump(simplified, f)

    out_mb = os.path.getsize(out) >> 20
    print(f"OK → {out_mb}MB")


def _simplify_one(data: dict[str, Any], layer_name: str) -> dict[str, Any]:
    keep_props = {
        "Desa": ["desa", "kecamatan"],
        "Kecamatan": ["kecamatan", "kabupaten"],
    }
    keep = keep_props.get(layer_name, [])

    for feat in data.get("features", []):
        geom = feat.get("geometry")
        if geom:
            _round_coords(geom["coordinates"], geom["type"])
        props = feat.get("properties", {})
        feat["properties"] = {k: props.get(k) for k in keep} if keep else {}
    return data


def _round_coords(coords: Any, geom_type: str) -> None:
    if geom_type.startswith("Multi"):
        for part in coords:
            for ring in part:
                for i, pt in enumerate(ring):
                    ring[i] = [
                        round(float(pt[0]), COORD_DECIMALS),
                        round(float(pt[1]), COORD_DECIMALS),
                    ]
    else:
        for ring in coords:
            for i, pt in enumerate(ring):
                ring[i] = [
                    round(float(pt[0]), COORD_DECIMALS),
                    round(float(pt[1]), COORD_DECIMALS),
                ]


def check_remaining() -> None:
    if not os.path.isdir(RAW_DIR):
        print(f"ERROR: {RAW_DIR} tidak ditemukan")
        return

    remaining = sorted(
        f
        for f in os.listdir(RAW_DIR)
        if f.endswith(".geojson") and not os.path.exists(os.path.join(OUT_DIR, f))
    )
    if not remaining:
        print("Semua file sudah diproses.")
        return

    print(f"Sisa {len(remaining)} file belum diproses:")
    for f in remaining:
        src = os.path.join(RAW_DIR, f)
        size = os.path.getsize(src) >> 20
        status = "OK" if size <= MAX_SIZE_MB else f"> {MAX_SIZE_MB}MB (skip)"
        print(f"  {f} ({size}MB) — {status}")

    for f in remaining:
        src = os.path.join(RAW_DIR, f)
        if os.path.getsize(src) >> 20 <= MAX_SIZE_MB:
            process_file(f)
        else:
            print(f"[SKIP] {f} — terlalu besar ({os.path.getsize(src) >> 20}MB)")


if __name__ == "__main__":
    check_remaining()
