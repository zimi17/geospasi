"""
ingest_hotel.py — ETL Pilot Pajak Hotel Kec. Anyar

Alur:
  1. Baca CSV hotel
  2. Validasi & bersihkan (parse omzet, okupansi, NPWP)
  3. Transform
  4. Load ke Supabase via REST API
  5. Generate laporan masalah CSV

Penggunaan:
    python ingest_hotel.py --csv data/hotel_anyar.csv
    python ingest_hotel.py --csv data/hotel_anyar.csv --dry-run

Prasyarat:
    File .env dengan SUPABASE_URL dan SUPABASE_SERVICE_KEY
    Jalankan shared/sql/rls_policies.sql dulu di Supabase SQL Editor
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pandas as pd
import numpy as np
from dotenv import load_dotenv

from shared.etl_utils import (
    read_csv,
    parse_revenue,
    validate_npwp,
    fuzzy_duplicates,
    simpan_laporan,
    load_to_supabase,
    KOLOM_HOTEL,
)

load_dotenv()


# ---------------------------------------------------------------------------
# 1. Konfigurasi
# ---------------------------------------------------------------------------

def load_config():
    return {
        "csv_path": None,
        "dry_run": False,
    }


# ---------------------------------------------------------------------------
# 2. Validasi
# ---------------------------------------------------------------------------

def validate(df):
    issues = []

    omzet_parsed = df["omzet_bulanan"].apply(parse_revenue)
    df["omzet_bulanan"] = omzet_parsed.apply(lambda x: x[0])
    df["omzet_confidence"] = omzet_parsed.apply(lambda x: x[1])

    for _, row in df[df["omzet_confidence"] == "low"].iterrows():
        issues.append({
            "baris": row.name + 2, "nama_usaha": row["nama_usaha"],
            "kolom_masalah": "omzet_bulanan", "nilai_asli": row["omzet_bulanan"],
            "tindakan": "Diambil nilai tengah", "confidence_akhir": "low",
        })

    for _, row in df[df["omzet_confidence"] == "unparseable"].iterrows():
        issues.append({
            "baris": row.name + 2, "nama_usaha": row["nama_usaha"],
            "kolom_masalah": "omzet_bulanan", "nilai_asli": row["omzet_bulanan"],
            "tindakan": "Tidak bisa diparse, diisi NULL", "confidence_akhir": "unparseable",
        })

    df["jumlah_kamar"] = pd.to_numeric(df["jumlah_kamar"], errors="coerce")
    for idx, r in df[pd.isna(df["jumlah_kamar"])].iterrows():
        issues.append({
            "baris": idx + 2, "nama_usaha": r["nama_usaha"],
            "kolom_masalah": "jumlah_kamar", "nilai_asli": r["jumlah_kamar"],
            "tindakan": "Diisi 0", "confidence_akhir": "low",
        })
    df["jumlah_kamar"] = df["jumlah_kamar"].fillna(0).astype(int)

    df["tarif_rata"] = pd.to_numeric(df["tarif_rata"], errors="coerce")
    for idx, r in df[pd.isna(df["tarif_rata"])].iterrows():
        issues.append({
            "baris": idx + 2, "nama_usaha": r["nama_usaha"],
            "kolom_masalah": "tarif_rata", "nilai_asli": r["tarif_rata"],
            "tindakan": "Diisi 0", "confidence_akhir": "low",
        })
    df["tarif_rata"] = df["tarif_rata"].fillna(0.0)

    df["okupansi_persen"] = pd.to_numeric(df["okupansi_persen"], errors="coerce")
    for idx, r in df[(df["okupansi_persen"] < 0) | (df["okupansi_persen"] > 100)].iterrows():
        issues.append({
            "baris": idx + 2, "nama_usaha": r["nama_usaha"],
            "kolom_masalah": "okupansi_persen", "nilai_asli": r["okupansi_persen"],
            "tindakan": "Dibatasi 0-100", "confidence_akhir": "low",
        })
    df["okupansi_persen"] = df["okupansi_persen"].clip(0, 100)

    df["npwp_valid"] = df["npwp"].apply(validate_npwp)
    for idx, r in df[~df["npwp_valid"]].iterrows():
        issues.append({
            "baris": idx + 2, "nama_usaha": r["nama_usaha"],
            "kolom_masalah": "npwp", "nilai_asli": r["npwp"],
            "tindakan": "Diisi NULL", "confidence_akhir": "low",
        })

    dups = fuzzy_duplicates(df["nama_usaha"])
    for name, original in dups.items():
        idx = df[df["nama_usaha"] == name].index[0]
        issues.append({
            "baris": idx + 2, "nama_usaha": name,
            "kolom_masalah": "nama_usaha", "nilai_asli": name,
            "tindakan": f"Kemungkinan duplikat dari '{original}'",
            "confidence_akhir": "low",
        })

    issues_df = pd.DataFrame(issues) if issues else pd.DataFrame()
    return df, issues_df


# ---------------------------------------------------------------------------
# 3. Transform
# ---------------------------------------------------------------------------

def transform(df):
    if "lat" not in df.columns:
        df["lat"] = np.nan
        df["lon"] = np.nan
        df["geocode_confidence"] = "none"
    return df


# ---------------------------------------------------------------------------
# 4. CLI
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="ETL Data Hotel → Supabase")
    parser.add_argument("--csv", required=True, help="Path ke CSV hotel")
    parser.add_argument("--dry-run", action="store_true", help="Hanya validasi, tanpa load ke DB")
    args = parser.parse_args()

    config = load_config()
    config["csv_path"] = args.csv
    config["dry_run"] = args.dry_run

    df = read_csv(config["csv_path"])
    df, issues = validate(df)
    df = transform(df)

    csv_dir = os.path.dirname(config["csv_path"])
    simpan_laporan(issues, os.path.join(csv_dir, "laporan_masalah.csv"))

    if config["dry_run"]:
        print("DRY-RUN: Data tidak dimuat ke database")
        print(df[["nama_usaha", "jumlah_kamar", "tarif_rata", "omzet_bulanan"]].head())
        return

    load_to_supabase(df, "hotel_lapangan", KOLOM_HOTEL)
    print("ETL selesai.")


if __name__ == "__main__":
    main()
