from __future__ import annotations

import json
import os
import sys
from typing import Any

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.abspath(os.path.join(HERE, "..", "data", "spasial"))
DATA_DIR = os.path.abspath(os.path.join(HERE, "..", "data"))
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "web", "data"))

COORD_DECIMALS = 5


def _read_csv(name: str) -> pd.DataFrame:
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        print(f"ERROR: {path} tidak ditemukan")
        sys.exit(1)
    return pd.read_csv(path)


def _read_geojson(name: str) -> dict[str, Any]:
    path = os.path.join(RAW_DIR, name)
    if not os.path.exists(path):
        print(f"ERROR: {path} tidak ditemukan")
        sys.exit(1)
    with open(path) as f:
        result: dict[str, Any] = json.load(f)
        return result


def _write_geojson(data: dict[str, Any], name: str) -> None:
    path = os.path.join(OUT_DIR, name)
    with open(path, "w") as f:
        json.dump(data, f)
    print(f"OK: {path} ({len(data['features'])} fitur, {os.path.getsize(path) >> 10}KB)")


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


def generate_ekonomi() -> None:
    pariwisata = _read_csv("bps_pariwisata_serang.csv")
    desa_gj = _read_geojson("Batas_Kelurahan_Desa.geojson")

    lookup = {}
    for _, row in pariwisata.iterrows():
        lookup[row["desa"].strip().lower()] = {
            "hotel": int(row.get("Hotel", 0) or 0),
            "penginapan": int(row.get("Penginapan", 0) or 0),
            "menara": int(row.get("Menara Telepon Seluler", 0) or 0),
        }

    features: list[dict[str, Any]] = []
    for feat in desa_gj["features"]:
        nama = (feat["properties"].get("Kel_Desa") or "").strip().lower()
        data = lookup.get(nama, {"hotel": 0, "penginapan": 0, "menara": 0})
        feat["properties"] = {
            "desa": feat["properties"].get("Kel_Desa", ""),
            "hotel": data["hotel"],
            "penginapan": data["penginapan"],
            "menara": data["menara"],
        }
        _round_coords(feat["geometry"]["coordinates"], feat["geometry"]["type"])
        features.append(feat)

    _write_geojson({"type": "FeatureCollection", "features": features}, "ekonomi.geojson")


def generate_demografi() -> None:
    kec_df = _read_csv("bps_kecamatan_serang.csv")
    kec_gj = _read_geojson("Batas_Kecamatan.geojson")

    kec_df["total_penduduk"] = kec_df[[c for c in kec_df.columns if "Jumlah Penduduk" in c]].sum(
        axis=1
    )
    kec_df["total_laki"] = kec_df[
        [c for c in kec_df.columns if "Laki-laki" in c and "Jumlah" in c]
    ].sum(axis=1)
    kec_df["total_perempuan"] = kec_df[
        [c for c in kec_df.columns if "Perempuan" in c and "Jumlah" in c]
    ].sum(axis=1)

    lookup: dict[str, dict[str, Any]] = {}
    for _, row in kec_df.iterrows():
        nama = (row["kecamatan"] or "").strip().lower()
        lookup[nama] = {
            "penduduk": int(row["total_penduduk"]),
            "laki": int(row["total_laki"]),
            "perempuan": int(row["total_perempuan"]),
        }

    features = []
    for feat in kec_gj["features"]:
        nama = (feat["properties"].get("Kecamatan") or "").strip().lower()
        data = lookup.get(nama)
        if data is None:
            continue
        feat["properties"] = {
            "kecamatan": feat["properties"].get("Kecamatan", ""),
            "penduduk": data["penduduk"],
            "laki": data["laki"],
            "perempuan": data["perempuan"],
        }
        _round_coords(feat["geometry"]["coordinates"], feat["geometry"]["type"])
        features.append(feat)

    _write_geojson({"type": "FeatureCollection", "features": features}, "demografi.geojson")


def main() -> None:
    print("=== Generate Ekonomi ===")
    generate_ekonomi()
    print("\n=== Generate Demografi ===")
    generate_demografi()
    print("\nSelesai. Kedua file lensa siap di web/data/")


if __name__ == "__main__":
    main()
