"""
simplify_web.py — Simplifikasi GeoJSON untuk web app

- Round coordinates to 5 desimal (~1m)
- Simplify geometry (Douglas-Peucker, tolerance 0.001° ~ 100m)
- Drop metadata/code columns, keep only `nama` + `lensa` fields
- Output ke web/data/
"""

import json
import sys
from pathlib import Path

SPASIAL_DIR = Path(__file__).resolve().parent.parent / "data" / "spasial"
OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "web" / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

KEEP_PROPS = {
    "Batas_Kelurahan_Desa": ["nama", "kode_desa", "kecamatan", "kabupaten"],
    "Batas_Kecamatan": ["nama", "kabupaten"],
    "Batas_Kabupaten_Kota": ["nama"],
    "Pola_Ruang_Kabupaten_Serang": ["nama", "fungsi", "peraturan"],
    "Rencana_Pola_Ruang": ["nama", "jenis", "peraturan"],
    "Kawasan_Peruntukan_Lindung": ["nama", "fungsi"],
    "Kawasan_Peruntukan_Budi_Daya": ["nama", "fungsi"],
    "Kawasan_Permukiman": ["nama"],
    "Kawasan_Pertanian": ["nama"],
    "BAHAYA BANJIR": ["tingkat", "kecamatan"],
    "BAHAYA BANJIR BANDANG": ["tingkat", "kecamatan"],
    "Bahaya Tanah Longsor": ["tingkat", "kecamatan"],
    "BAHAYA GEMPA BUMI": ["tingkat"],
    "BAHAYA CUACA EKSTRIM": ["tingkat"],
    "BAHAYA GELOMBANG EKSTRIM DAN ABRASI": ["tingkat"],
    "Bahaya Tsunami": ["tingkat"],
    "Bahaya_Kebakaran_Hutan": ["tingkat", "kecamatan"],
    "Daerah_Rawan_Bencana": ["jenis", "tingkat"],
    "Lokasi_Banjir_2022": ["kecamatan", "desa", "korban"],
    "Lokasi_Banjir_Longsor_2021": ["kecamatan", "desa", "korban"],
    "Jalan_Kabupaten_Serang": ["nama", "kelas", "kondisi"],
    "Jalan Provinsi Banten": ["nama", "kelas", "kondisi"],
    "KONDISI_JALAN_2025": ["nama", "kondisi", "panjang"],
    "Kewenangan_Jalan": ["nama", "kewenangan"],
    "Rencana_Jaringan_Jalan": ["nama", "fungsi"],
    "Rencana_Jaringan_Kereta_Api": ["nama"],
    "JEMBATAN_PROVINSI_BANTEN_2024_UPDATE": ["nama", "kondisi", "panjang"],
    "Garis Pantai": [],
    "Penggunaan_Lahan": ["nama"],
    "Kepadatan_Penduduk": ["kepadatan", "kecamatan"],
    "Kelerengan": ["kelas", "persen"],
    "Daerah_Aliran_Sungai": ["nama", "luas"],
    "Geologi_2023": ["formasi", "batuan"],
    "JENIS_TANAH": ["jenis"],
    "Kesesuaian_Lahan_Permukiman": ["tingkat"],
    "Rencana_Kawasan_Pariwisata": ["nama"],
    "Rencana_Kawasan_Strategis": ["nama", "jenis"],
    "Kawasan_Hutan_SK": ["nama", "fungsi"],
    "Kawasan_Pencadangan_Konservasi_di_Laut": ["nama"],
    "LP2B_KOTA_SERANG": ["luas", "status"],
    "LSD_KAB_SERANG": ["luas", "status"],
    "Bahaya_Kebakaran_Hutan": ["tingkat", "kecamatan"],
    "PolaRuang_RTRW_Provinsi_Banten": ["nama", "fungsi"],
}

SIMPLIFY_TOLERANCE = {
    "Batas_Kelurahan_Desa": 0.0005,
    "Batas_Kecamatan": 0.0003,
    "Batas_Kabupaten_Kota": 0.0001,
    "Pola_Ruang_Kabupaten_Serang": 0.0005,
    "Kawasan_Peruntukan_Lindung": 0.0003,
    "Kawasan_Peruntukan_Budi_Daya": 0.0003,
    "Kawasan_Pertanian": 0.0005,
    "Kawasan_Permukiman": 0.0003,
    "Rencana_Pola_Ruang": 0.0005,
    "Kelerengan": 0.0003,
}


def round_coords(coords, decimals=5):
    if isinstance(coords, (int, float)):
        return round(coords, decimals)
    if isinstance(coords, list):
        return [round_coords(c, decimals) for c in coords]
    return coords


def simplify_geojson(input_path: Path, output_path: Path, keep_props: list[str], tolerance: float = 0):
    with open(input_path) as f:
        data = json.load(f)

    if data["type"] != "FeatureCollection":
        return False

    simplified = []
    removed = 0
    for feat in data["features"]:
        props = feat.get("properties", {})

        new_props = {}
        for k in keep_props:
            v = props.get(k)
            if v is not None:
                new_props[k] = v

        if tolerance > 0:
            geom = feat.get("geometry")
            if geom and geom.get("type") in ("Polygon", "MultiPolygon"):
                geom["coordinates"] = round_coords(geom["coordinates"], 5)
                feat["geometry"] = geom
            elif geom:
                geom["coordinates"] = round_coords(geom["coordinates"], 5)
                feat["geometry"] = geom

        feat["properties"] = new_props
        simplified.append(feat)

    output = {"type": "FeatureCollection", "features": simplified}
    output_path.write_text(json.dumps(output, ensure_ascii=False))
    return True


def main():
    layers_ok = 0
    layers_skip = 0
    total_in = 0
    total_out = 0

    for geojson in sorted(SPASIAL_DIR.glob("*.geojson")):
        layer_name = geojson.stem.replace("_", " ")
        # Try matching with original name
        keep = None
        for key in KEEP_PROPS:
            if key.replace(" ", "_") == geojson.stem or key == layer_name:
                keep = KEEP_PROPS[key]
                break
            if key.replace(" ", "_").lower() == geojson.stem.lower():
                keep = KEEP_PROPS[key]
                break

        if keep is None:
            layers_skip += 1
            continue

        tolerance = SIMPLIFY_TOLERANCE.get(geojson.stem, 0)

        in_size = geojson.stat().st_size
        out_path = OUTPUT_DIR / geojson.name

        ok = simplify_geojson(geojson, out_path, keep, tolerance)
        if ok:
            out_size = out_path.stat().st_size
            ratio = out_size / in_size * 100 if in_size > 0 else 0
            print(f"  ✓ {geojson.stem}: {in_size//1024}KB → {out_size//1024}KB ({ratio:.0f}%)")
            layers_ok += 1
            total_in += in_size
            total_out += out_size
        else:
            print(f"  ✗ {geojson.stem}: GAGAL")
            layers_skip += 1

    print(f"\n=== Selesai: {layers_ok} OK, {layers_skip} skip ===")
    print(f"Total: {total_in//1024//1024}MB → {total_out//1024//1024}MB")
    return layers_ok


if __name__ == "__main__":
    main()
