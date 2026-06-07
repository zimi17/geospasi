"""
export_agregat.py — Export data agregat dari Supabase ke GeoJSON

Workflow:
  1. Koneksi ke Supabase
  2. Query data agregat per desa
  3. Tulis sebagai GeoJSON fitur poligon
  4. Commit ke repo (dijalankan oleh GitHub Actions)

Output:
  potensi_pajak_restoran/data/agregat_desa.geojson
"""

import os
import json
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text

load_dotenv()


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def csv_fallback():
    csv_path = os.path.join(ROOT, "potensi_pajak_restoran", "data", "restoran_anyar.csv")
    if not os.path.exists(csv_path):
        print("ERROR: Tidak ada data di Supabase maupun CSV")
        return None

    df = pd.read_csv(csv_path)
    df = df.groupby("desa").agg(
        jumlah_restoran=("id", "count"),
        terdaftar=("status", lambda x: (x == "terdaftar").sum()),
        tidak_terdaftar=("status", lambda x: (x == "tidak_terdaftar").sum()),
        total_omzet=("omzet_bulanan", lambda x: pd.to_numeric(x, errors="coerce").sum()),
        rata_omzet=("omzet_bulanan", lambda x: pd.to_numeric(x, errors="coerce").mean()),
    ).reset_index()
    print("INFO: Data dari CSV fallback")
    return df


def main():
    db_url = os.getenv("SUPABASE_DB_URL")
    df = None

    if db_url:
        try:
            engine = create_engine(db_url)
            query = text("""
                SELECT
                    desa,
                    COUNT(*) AS jumlah_restoran,
                    COUNT(*) FILTER (WHERE status = 'terdaftar') AS terdaftar,
                    COUNT(*) FILTER (WHERE status = 'tidak_terdaftar') AS tidak_terdaftar,
                    COALESCE(SUM(omzet_bulanan), 0) AS total_omzet,
                    COALESCE(AVG(omzet_bulanan), 0) AS rata_omzet
                FROM restoran_lapangan
                GROUP BY desa
            """)
            df = pd.read_sql(query, engine)
            if df.empty:
                df = None
        except Exception as e:
            print(f"WARN: Gagal konek Supabase ({e}), fallback ke CSV")
            df = None

    if df is None:
        df = csv_fallback()
        if df is None:
            return 1

    # Baca batas desa dari file GeoJSON
    desa_path = os.path.join(ROOT, "potensi_pajak_restoran", "data", "desa_anyar.geojson")
    with open(desa_path) as f:
        desa_geojson = json.load(f)

    # Gabung data agregat dengan geometri
    features = []
    for feature in desa_geojson["features"]:
        desa_name = feature["properties"]["desa"]
        match = df[df["desa"] == desa_name]
        if not match.empty:
            row = match.iloc[0]
            feature["properties"].update({
                "jumlah_restoran": int(row["jumlah_restoran"]),
                "terdaftar": int(row["terdaftar"]),
                "tidak_terdaftar": int(row["tidak_terdaftar"]),
                "total_omzet": float(row["total_omzet"]),
                "rata_omzet": float(round(row["rata_omzet"], 0)),
            })
        features.append(feature)

    output = {
        "type": "FeatureCollection",
        "features": features,
    }

    out_path = os.path.join(ROOT, "potensi_pajak_restoran", "data", "agregat_desa.geojson")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"OK: {out_path} — {len(features)} desa ditulis")
    return 0


if __name__ == "__main__":
    exit(main())
