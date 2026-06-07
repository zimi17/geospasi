"""
ingest_gistaru.py — Download semua layer spasial GISTARU Banten via WFS

GeoServer URL: https://gistaru.bantenprov.go.id:8866/geoserver/webgis_sipr/ows
CRS Default: EPSG:4326 (WGS84) untuk layer utama
Output: shared/data/spasial/{layer_name}.geojson

Layer Prioritas (Kab. Serang):
  P1: Batas_Kelurahan_Desa, Batas_Kecamatan, Pola_Ruang_Kabupaten_Serang,
      Rencana_Kawasan_Pariwisata, Kawasan_Peruntukan_Lindung,
      BAHAYA BANJIR, BAHAYA BANJIR BANDANG, Bahaya Tanah Longsor,
      Jalan_Kabupaten_Serang, Jalan Provinsi Banten, KONDISI_JALAN_2025,
      JEMBATAN_PROVINSI_BANTEN_2024_UPDATE, Penggunaan_Lahan
  P2: Kepadatan_Penduduk, Kelerengan, Daerah_Aliran_Sungai,
      BAHAYA CUACA EKSTRIM, BAHAYA GEMPA BUMI, Bahaya Tsunami,
      Kawasan_Permukiman, Kawasan_Peruntukan_Budi_Daya
  P3: Kawasan_Pertanian, Kawasan_Hutan_SK, Bahaya_Kebakaran_Hutan,
      Kawasan_Pencadangan_Konservasi_di_Laut

Total 224 layer tersedia di GeoServer (workspace: webgis_sipr).
Mapserver workspace (gistaru) untuk layer umum Banten.
"""

import json
import sys
import time
from pathlib import Path

import requests

WFS_URL = "https://gistaru.bantenprov.go.id:8866/geoserver/webgis_sipr/ows"
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "spasial"

# Layer prioritas untuk SPASI
PRIORITY_LAYERS = {
    # Lensa Tata Ruang
    "Pola_Ruang_Kabupaten_Serang": {"lensa": "Tata Ruang", "prioritas": "P1"},
    "PolaRuang_RTRW_Provinsi_Banten": {"lensa": "Tata Ruang", "prioritas": "P2"},
    "Rencana_Kawasan_Pariwisata": {"lensa": "Tata Ruang", "prioritas": "P1"},
    "Kawasan_Permukiman": {"lensa": "Tata Ruang", "prioritas": "P2"},
    "Kawasan_Pertanian": {"lensa": "Tata Ruang", "prioritas": "P3"},
    "Kawasan_Peruntukan_Lindung": {"lensa": "Tata Ruang", "prioritas": "P1"},
    "Rencana_Pola_Ruang": {"lensa": "Tata Ruang", "prioritas": "P2"},
    "Rencana_Kawasan_Strategis": {"lensa": "Tata Ruang", "prioritas": "P3"},
    "Kawasan_Peruntukan_Budi_Daya": {"lensa": "Tata Ruang", "prioritas": "P2"},

    # Lensa Batas Administrasi (digunakan semua lensa)
    "Batas_Kelurahan_Desa": {"lensa": "Dasar", "prioritas": "P1"},
    "Batas_Kecamatan": {"lensa": "Dasar", "prioritas": "P1"},
    "Batas_Kabupaten_Kota": {"lensa": "Dasar", "prioritas": "P1"},
    "Garis Pantai": {"lensa": "Dasar", "prioritas": "P2"},

    # Lensa Risiko & Bencana
    "BAHAYA BANJIR": {"lensa": "Risiko", "prioritas": "P1"},
    "BAHAYA BANJIR BANDANG": {"lensa": "Risiko", "prioritas": "P1"},
    "Bahaya Tanah Longsor": {"lensa": "Risiko", "prioritas": "P1"},
    "BAHAYA GELOMBANG EKSTRIM DAN ABRASI": {"lensa": "Risiko", "prioritas": "P2"},
    "BAHAYA GEMPA BUMI": {"lensa": "Risiko", "prioritas": "P2"},
    "Bahaya Tsunami": {"lensa": "Risiko", "prioritas": "P2"},
    "BAHAYA CUACA EKSTRIM": {"lensa": "Risiko", "prioritas": "P2"},
    "Bahaya Kekeringan": {"lensa": "Risiko", "prioritas": "P3"},
    "Bahaya Letusan GunungApi": {"lensa": "Risiko", "prioritas": "P3"},
    "Lokasi_Banjir_2022": {"lensa": "Risiko", "prioritas": "P1"},
    "Lokasi_Banjir_Longsor_2021": {"lensa": "Risiko", "prioritas": "P1"},
    "Daerah_Rawan_Bencana": {"lensa": "Risiko", "prioritas": "P2"},
    "Bahaya_Kebakaran_Hutan": {"lensa": "Risiko", "prioritas": "P3"},

    # Lensa Infrastruktur
    "Jalan_Kabupaten_Serang": {"lensa": "Infrastruktur", "prioritas": "P1"},
    "Jalan Provinsi Banten": {"lensa": "Infrastruktur", "prioritas": "P1"},
    "KONDISI_JALAN_2025": {"lensa": "Infrastruktur", "prioritas": "P1"},
    "JEMBATAN_PROVINSI_BANTEN_2024_UPDATE": {"lensa": "Infrastruktur", "prioritas": "P1"},
    "Rencana_Jaringan_Jalan": {"lensa": "Infrastruktur", "prioritas": "P2"},
    "Rencana_Terminal": {"lensa": "Infrastruktur", "prioritas": "P3"},
    "Rencana_Pelabuhan": {"lensa": "Infrastruktur", "prioritas": "P3"},
    "Rencana_Jaringan_Kereta_Api": {"lensa": "Infrastruktur", "prioritas": "P2"},
    "Rencana_Stasiun_KA": {"lensa": "Infrastruktur", "prioritas": "P3"},
    "Rencana_Bandar_Udara": {"lensa": "Infrastruktur", "prioritas": "P3"},
    "Kewenangan_Jalan": {"lensa": "Infrastruktur", "prioritas": "P2"},

    # Lensa Fisik & Lingkungan
    "Penggunaan_Lahan": {"lensa": "Fisik", "prioritas": "P1"},
    "Geologi_2023": {"lensa": "Fisik", "prioritas": "P3"},
    "JENIS_TANAH": {"lensa": "Fisik", "prioritas": "P3"},
    "Daerah_Aliran_Sungai": {"lensa": "Fisik", "prioritas": "P2"},
    "Kelerengan": {"lensa": "Fisik", "prioritas": "P2"},
    "Curah_Hujan_Rata-rata": {"lensa": "Fisik", "prioritas": "P3"},
    "Kepadatan_Penduduk": {"lensa": "Demografi", "prioritas": "P2"},
    "Kesesuaian_Lahan_Permukiman": {"lensa": "Fisik", "prioritas": "P3"},

    # Lensa Lingkungan
    "Kawasan_Hutan_SK": {"lensa": "Lingkungan", "prioritas": "P2"},
    "Kawasan_Pencadangan_Konservasi_di_Laut": {"lensa": "Lingkungan", "prioritas": "P3"},
    "LP2B_KOTA_SERANG": {"lensa": "Lingkungan", "prioritas": "P3"},
    "LSD_KAB_SERANG": {"lensa": "Lingkungan", "prioritas": "P3"},
}


def download_wfs(layer_name: str, output_dir: Path, cql_filter: str = "") -> bool:
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeName": f"webgis_sipr:{layer_name}",
        "outputFormat": "application/json",
        "srsName": "EPSG:4326",
    }
    if cql_filter:
        params["cql_filter"] = cql_filter

    safe_name = layer_name.replace(" ", "_").replace("/", "_")
    output_path = output_dir / f"{safe_name}.geojson"

    if output_path.exists() and output_path.stat().st_size > 1000:
        print(f"  [SKIP] {layer_name} — already exists ({output_path.stat().st_size:,} bytes)")
        return True

    try:
        r = requests.get(WFS_URL, params=params, timeout=120)
        if r.status_code != 200:
            print(f"  [FAIL] {layer_name} — HTTP {r.status_code}")
            return False

        data = r.json()
        features = data.get("totalFeatures", len(data.get("features", [])))
        size = len(r.content)

        if features == 0:
            print(f"  [EMPTY] {layer_name} — 0 features ({size:,} bytes)")
            return False

        output_path.write_bytes(r.content)
        print(f"  [OK] {layer_name} — {features} fitur, {size:,} bytes -> {output_path}")
        return True

    except Exception as e:
        print(f"  [ERROR] {layer_name} — {e}")
        return False


def download_all_priorities(priorities: set[str] | None = None):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    layers_to_download = {}
    for name, meta in PRIORITY_LAYERS.items():
        if priorities is None or meta["prioritas"] in priorities:
            layers_to_download[name] = meta

    print(f"\n=== Download {len(layers_to_download)} layer prioritas ===")
    print(f"Output: {DATA_DIR}\n")

    # Filter untuk Kab. Serang (kecamatan di Kab. Serang)
    cql_serang = "kabupaten LIKE '%Serang%'"
    cql_kab_serang = "kabupaten_kota LIKE '%Serang%'"

    success = 0
    failed = 0

    for name, meta in layers_to_download.items():
        label = f"[{meta['prioritas']}] [{meta['lensa']}]"
        print(f"{label} {name}")

        # Tentukan CQL filter per layer
        cql = ""
        if "Batas_Kelurahan_Desa" in name or "Batas_Kecamatan" in name:
            cql = "kabupaten LIKE '%Serang%'"
        elif "Pola_Ruang_Kabupaten_Serang" in name:
            cql = ""  # already filtered to Kab Serang
        elif "BAHAYA" in name or "Bahaya" in name:
            cql = ""  # download all
        elif "Kabupaten_Serang" in name or "Kab_Serang" in name:
            cql = ""  # already specific

        ok = download_wfs(name, DATA_DIR, cql)
        if ok:
            success += 1
        else:
            failed += 1

        time.sleep(0.5)  # Rate limiting

    print(f"\n=== Selesai: {success} OK, {failed} GAGAL ===")
    return success, failed


def list_available():
    """List semua layer yang tersedia dengan informasi prioritas."""
    print("\n=== LAYER TERSEDIA DI GISTARU BANTEN ===\n")

    by_lensa = {}
    for name, meta in PRIORITY_LAYERS.items():
        lensa = meta["lensa"]
        by_lensa.setdefault(lensa, []).append((meta["prioritas"], name))

    for lensa in sorted(by_lensa.keys()):
        print(f"\n--- {lensa} ---")
        for p, name in sorted(by_lensa[lensa]):
            status = "✓" if (DATA_DIR / f"{name.replace(' ', '_')}.geojson").exists() else " "
            print(f"  [{p}] [{status}] {name}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download GISTARU Banten layers")
    parser.add_argument("--prioritas", nargs="+", choices=["P1", "P2", "P3"],
                        help="Filter prioritas (P1, P2, P3)")
    parser.add_argument("--layer", help="Download spesifik layer")
    parser.add_argument("--list", action="store_true", help="List all layers")
    parser.add_argument("--cql", default="", help="CQL filter")

    args = parser.parse_args()

    if args.list:
        list_available()
        sys.exit(0)

    if args.layer:
        print(f"\nDownload single layer: {args.layer}")
        download_wfs(args.layer, DATA_DIR, args.cql)
        sys.exit(0)

    download_all_priorities(set(args.prioritas) if args.prioritas else None)
