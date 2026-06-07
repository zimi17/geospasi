from __future__ import annotations

import json
import os
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.abspath(os.path.join(HERE, "..", "examples", "geoserang", "data", "spasial"))
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "examples", "geoserang", "data"))

COORD_DECIMALS = 5
MAX_SIZE_MB = 50
KEEP_PROPS: dict[str, list[str]] = {
    "Desa": ["desa", "kecamatan", "kabupaten", "provinsi"],
    "Kecamatan": ["kecamatan", "kabupaten"],
    "Jalan": ["nama_jalan", "fungsi", "status"],
    "Sungai": ["nama_sungai", "tipe"],
    "default": [],
}


def simplify_geojson(data: dict[str, Any], layer_name: str) -> dict[str, Any]:
    keep = KEEP_PROPS.get(layer_name, KEEP_PROPS["default"])
    for feat in data.get("features", []):
        geom = feat.get("geometry")
        if geom and geom["type"] in ("Polygon", "MultiPolygon", "LineString", "MultiLineString"):
            coords = geom["coordinates"]
            _round_coords(coords, geom["type"])
        elif geom and geom["type"] == "Point":
            geom["coordinates"] = [
                round(float(geom["coordinates"][0]), COORD_DECIMALS),
                round(float(geom["coordinates"][1]), COORD_DECIMALS),
            ]

        props = feat.get("properties", {})
        if keep:
            feat["properties"] = {k: props.get(k) for k in keep}
        else:
            feat["properties"] = {}
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


def process_all() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    if not os.path.isdir(RAW_DIR):
        print(f"ERROR: {RAW_DIR} tidak ditemukan")
        sys.exit(1)

    files = sorted(f for f in os.listdir(RAW_DIR) if f.endswith(".geojson"))
    ok, skip = 0, 0
    for fname in files:
        src = os.path.join(RAW_DIR, fname)
        size_mb = os.path.getsize(src) >> 20
        if size_mb > MAX_SIZE_MB:
            print(f"[SKIP] {fname} — {size_mb}MB > {MAX_SIZE_MB}MB")
            skip += 1
            continue

        layer_name = fname.replace(".geojson", "")
        out = os.path.join(OUT_DIR, fname)
        print(f"[PROCESS] {fname} ({size_mb}MB)...", end=" ", flush=True)

        with open(src) as f:
            data = json.load(f)
        simplified = simplify_geojson(data, layer_name)
        with open(out, "w") as f:
            json.dump(simplified, f)
        out_mb = os.path.getsize(out) >> 20
        print(f"→ {out_mb}MB")
        ok += 1

    print(f"\nSelesai: {ok} file disederhanakan, {skip} dilewati (>50MB)")


if __name__ == "__main__":
    process_all()
