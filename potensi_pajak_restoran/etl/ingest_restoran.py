"""
ingest_restoran.py — ETL Pilot Pajak Restoran Kec. Anyar

Alur:
  1. Baca CSV restoran (mentah atau sintetis)
  2. Validasi & bersihkan data (parse omzet, cek NPWP, fuzzy duplikasi)
  3. Geocode alamat via Nominatim (jika belum ada koordinat)
  4. Hitung confidence score tiap baris
  5. Load ke PostGIS (Supabase)
  6. Generate laporan masalah CSV

Penggunaan:
    python ingest_restoran.py --csv data/restoran_anyar.csv
    python ingest_restoran.py --csv data/restoran_anyar.csv --dry-run

Prasyarat:
    python-dotenv, geopandas, sqlalchemy, psycopg2-binary, geopy
    File .env dengan SUPABASE_DB_URL
"""

import os
import csv
import re
import sys
from difflib import SequenceMatcher

import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------------------------
# 1. Konfigurasi
# ---------------------------------------------------------------------------

def load_config():
    return {
        "db_url": os.getenv("SUPABASE_DB_URL"),
        "csv_path": None,
        "dry_run": False,
    }


# ---------------------------------------------------------------------------
# 2. Baca CSV
# ---------------------------------------------------------------------------

def read_csv(path):
    if not os.path.exists(path):
        print(f"ERROR: File tidak ditemukan: {path}")
        sys.exit(1)
    df = pd.read_csv(path, dtype=str)
    print(f"OK: {len(df)} baris dibaca dari {path}")
    return df


# ---------------------------------------------------------------------------
# 3. Validasi
# ---------------------------------------------------------------------------

def parse_revenue(value):
    """Parse string omzet menjadi angka + confidence."""
    if pd.isna(value) or str(value).strip() == "":
        return None, "unparseable"

    if isinstance(value, (int, float)):
        return float(value), "high"

    cleaned = str(value).replace("Rp", "").replace("rP", "").replace("rp", "")
    cleaned = cleaned.replace(".", "").replace(",", ".").replace(" ", "")

    if "-" in cleaned:
        parts = cleaned.split("-")
        try:
            low = float(parts[0])
            high = float(parts[1])
            return (low + high) / 2, "low"
        except ValueError:
            return None, "unparseable"

    try:
        return float(cleaned), "high"
    except ValueError:
        return None, "unparseable"


def validate_npwp(value):
    """NPWP harus 15 digit angka."""
    if pd.isna(value) or str(value).strip() in ("", "-", "0"):
        return False
    digits = re.sub(r"\D", "", str(value))
    return len(digits) == 15


def fuzzy_duplicates(names, threshold=0.85):
    """Cari kemungkinan duplikat berdasarkan kemiripan nama."""
    names = names.fillna("").tolist()
    dup_map = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            ratio = SequenceMatcher(None, names[i], names[j]).ratio()
            if ratio >= threshold:
                dup_map[names[j]] = names[i]
    return dup_map


def validate(df):
    issues = []

    omzet_parsed = df["omzet_bulanan"].apply(parse_revenue)
    df["omzet_bersih"] = omzet_parsed.apply(lambda x: x[0])
    df["omzet_confidence"] = omzet_parsed.apply(lambda x: x[1])

    low_conf = df[df["omzet_confidence"] == "low"]
    for _, row in low_conf.iterrows():
        issues.append({
            "baris": row.name + 2,
            "nama_usaha": row["nama_usaha"],
            "kolom_masalah": "omzet_bulanan",
            "nilai_asli": row["omzet_bulanan"],
            "tindakan": "Diambil nilai tengah",
            "confidence_akhir": "low",
        })

    unparseable = df[df["omzet_confidence"] == "unparseable"]
    for _, row in unparseable.iterrows():
        issues.append({
            "baris": row.name + 2,
            "nama_usaha": row["nama_usaha"],
            "kolom_masalah": "omzet_bulanan",
            "nilai_asli": row["omzet_bulanan"],
            "tindakan": "Tidak bisa diparse, diisi NULL",
            "confidence_akhir": "unparseable",
        })

    df["npwp_valid"] = df["npwp"].apply(validate_npwp)
    invalid_npwp = df[~df["npwp_valid"]]
    for _, row in invalid_npwp.iterrows():
        issues.append({
            "baris": row.name + 2,
            "nama_usaha": row["nama_usaha"],
            "kolom_masalah": "npwp",
            "nilai_asli": row["npwp"],
            "tindakan": "Diisi NULL",
            "confidence_akhir": "low",
        })

    dups = fuzzy_duplicates(df["nama_usaha"])
    for name, original in dups.items():
        idx = df[df["nama_usaha"] == name].index[0]
        issues.append({
            "baris": idx + 2,
            "nama_usaha": name,
            "kolom_masalah": "nama_usaha",
            "nilai_asli": name,
            "tindakan": f"Kemungkinan duplikat dari '{original}'",
            "confidence_akhir": "low",
        })

    issues_df = pd.DataFrame(issues) if issues else pd.DataFrame()
    return df, issues_df


# ---------------------------------------------------------------------------
# 4. Transform (placeholder — geocoding via Nominatim)
# ---------------------------------------------------------------------------

def transform(df):
    """Tambahkan koordinat dummy untuk fase 0."""
    if "lat" not in df.columns:
        df["lat"] = np.nan
        df["lon"] = np.nan
        df["geocode_confidence"] = "none"
    return df


# ---------------------------------------------------------------------------
# 5. Load ke PostGIS
# ---------------------------------------------------------------------------

def load_to_postgis(df, engine):
    df.to_sql(
        "restoran_lapangan",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )
    print(f"OK: {len(df)} baris dimuat ke tabel restoran_lapangan")


# ---------------------------------------------------------------------------
# 6. Simpan laporan masalah
# ---------------------------------------------------------------------------

def simpan_laporan(issues_df, path):
    if issues_df.empty:
        print("OK: Tidak ada masalah validasi")
        return
    issues_df.to_csv(path, index=False)
    print(f"OK: Laporan masalah disimpan ke {path}")
    print(f"    Total masalah: {len(issues_df)}")


# ---------------------------------------------------------------------------
# 7. CLI
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="ETL Data Restoran → PostGIS")
    parser.add_argument("--csv", required=True, help="Path ke CSV restoran")
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
        print(df[["nama_usaha", "omzet_bersih", "omzet_confidence", "npwp_valid"]].head())
        return

    from sqlalchemy import create_engine
    engine = create_engine(config["db_url"])
    load_to_postgis(df, engine)
    print("ETL selesai.")


if __name__ == "__main__":
    main()
