from __future__ import annotations

import json
import os
import sys
import time
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

WFS_URL = (
    "https://gistaru.bantenprov.go.id:8866/geoserver/webgis_sipr/ows"
    "?service=WFS&version=2.0.0&request=GetFeature"
    "&typeName=webgis_sipr:{layer}"
    "&outputFormat=application/json"
    "&srsName=EPSG:4326"
    "&count=10000"
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(HERE, "..", "data", "spasial"))
LAYER_FILE = os.path.join(HERE, "gistaru_layers.json")

PRIORITY_LAYERS: dict[str, list[str]] = {
    "high": [
        "Kecamatan",
        "Desa",
        "Rencana_Pola_Ruang",
        "Kawasan_Peruntukan_Budi_Daya",
        "Kawasan_Peruntukan_Lindung",
        "Kawasan_Pertanian",
        "Kawasan_Pemukiman",
        "Jalan",
        "Sungai",
        "Garis_Pantai",
    ],
    "medium": [
        "Bangunan_Publik",
        "Fasilitas_Pendidikan",
        "Fasilitas_Kesehatan",
        "Titik_Bencana",
        "Zona_Rawan_Banjir",
        "Zona_Rawan_Gempa",
        "Zona_Rawan_Tanah_Longsor",
        "Zona_Rawan_Tsunami",
        "Titik_Banjir",
        "Puskesmas",
        "Sekolah",
        "Rumah_Sakit",
    ],
}

DELAY = 1.5
MAX_RETRIES = 3


def fetch_layer(layer_name: str, output_path: str) -> bool:
    url = WFS_URL.format(layer=layer_name)
    print(f"[GET] {layer_name}...", end=" ", flush=True)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = Request(url, headers={"User-Agent": "SPASI-ETL/1.0"})
            with urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode())
            features = data.get("features", [])
            if not features:
                print("SKIP (0 features)")
                return False

            with open(output_path, "w") as f:
                json.dump(data, f)
            print(f"OK ({len(features)} fitur, {os.path.getsize(output_path) >> 20}MB)")
            return True
        except URLError as e:
            print(f"RETRY {attempt}/{MAX_RETRIES} ({e})", end=" ", flush=True)
            if attempt < MAX_RETRIES:
                time.sleep(DELAY * attempt)
        except json.JSONDecodeError as e:
            print(f"PARSE ERROR: {e}")
            return False
    print("FAIL")
    return False


def load_layer_list() -> list[dict[str, Any]]:
    if not os.path.exists(LAYER_FILE):
        print(f"ERROR: {LAYER_FILE} tidak ditemukan. Jalankan scan_layers() dulu.")
        sys.exit(1)
    with open(LAYER_FILE) as f:
        result: list[dict[str, Any]] = json.load(f)
        return result


def download_all() -> None:
    layers = load_layer_list()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    priority_map = {}
    for prio, names in PRIORITY_LAYERS.items():
        for n in names:
            priority_map[n] = prio

    ordered = sorted(layers, key=lambda x: priority_map.get(x["name"], "low"))

    ok, fail = 0, 0
    for layer in ordered:
        name = layer["name"]
        fname = f"{name}.geojson"
        out = os.path.join(OUTPUT_DIR, fname)
        if os.path.exists(out):
            print(f"[SKIP] {name} — sudah ada ({os.path.getsize(out) >> 20}MB)")
            ok += 1
            continue
        if fetch_layer(name, out):
            ok += 1
        else:
            fail += 1
        time.sleep(DELAY)

    print(f"\nSelesai: {ok} OK, {fail} gagal")


def scan_layers() -> None:
    url = (
        "https://gistaru.bantenprov.go.id:8866/geoserver/webgis_sipr/ows"
        "?service=WFS&version=2.0.0&request=DescribeFeatureType"
    )
    req = Request(url)
    try:
        with urlopen(req, timeout=30) as resp:
            raw = resp.read().decode()
    except URLError as e:
        print(f"Gagal scan: {e}")
        sys.exit(1)

    import re

    matches = re.findall(r'name="webgis_sipr:(\w+)"', raw)
    if not matches:
        matches = re.findall(r'typeName="webgis_sipr:(\w+)"', raw)

    layers = [{"name": m} for m in sorted(set(matches))]
    with open(LAYER_FILE, "w") as f:
        json.dump(layers, f, indent=2)
    print(f"OK: {len(layers)} layer ditemukan → {LAYER_FILE}")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--scan":
        scan_layers()
    else:
        download_all()


if __name__ == "__main__":
    main()
