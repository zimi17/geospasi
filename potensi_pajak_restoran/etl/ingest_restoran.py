"""
ingest_restoran.py — ETL Pilot Pajak Restoran Kec. Anyar

Alur:
  1. Baca CSV restoran
  2. Validasi & bersihkan data
  3. Transform (geocode placeholder)
  4. Load ke Supabase via REST API
  5. Generate laporan masalah CSV

Penggunaan:
    python ingest_restoran.py --csv data/restoran_anyar.csv
    python ingest_restoran.py --csv data/restoran_anyar.csv --dry-run

Prasyarat:
    File .env dengan SUPABASE_URL dan SUPABASE_SERVICE_KEY
"""

from __future__ import annotations

import os
import sys
from typing import Any

import pandas as pd
from dotenv import load_dotenv

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from shared.etl_utils import (  # noqa: E402
    KOLOM_RESTORAN,
    fuzzy_duplicates,
    load_to_supabase,
    parse_revenue,
    read_csv,
    simpan_laporan,
    validate_npwp,
)

load_dotenv()


# ---------------------------------------------------------------------------
# 2. Validasi
# ---------------------------------------------------------------------------


def validate(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    issues: list[dict[str, Any]] = []

    omzet_parsed = df["omzet_bulanan"].apply(parse_revenue)
    df["omzet_bulanan"] = omzet_parsed.apply(lambda x: x[0])
    df["omzet_confidence"] = omzet_parsed.apply(lambda x: x[1])

    low_conf = df[df["omzet_confidence"] == "low"]
    for _, row in low_conf.iterrows():
        issues.append(
            {
                "baris": row.name + 2,
                "nama_usaha": row["nama_usaha"],
                "kolom_masalah": "omzet_bulanan",
                "nilai_asli": row["omzet_bulanan"],
                "tindakan": "Diambil nilai tengah",
                "confidence_akhir": "low",
            }
        )

    unparseable = df[df["omzet_confidence"] == "unparseable"]
    for _, row in unparseable.iterrows():
        issues.append(
            {
                "baris": row.name + 2,
                "nama_usaha": row["nama_usaha"],
                "kolom_masalah": "omzet_bulanan",
                "nilai_asli": row["omzet_bulanan"],
                "tindakan": "Tidak bisa diparse, diisi NULL",
                "confidence_akhir": "unparseable",
            }
        )

    df["npwp_valid"] = df["npwp"].apply(validate_npwp)
    for _, row in df[~df["npwp_valid"]].iterrows():
        issues.append(
            {
                "baris": row.name + 2,
                "nama_usaha": row["nama_usaha"],
                "kolom_masalah": "npwp",
                "nilai_asli": row["npwp"],
                "tindakan": "Diisi NULL",
                "confidence_akhir": "low",
            }
        )

    dups = fuzzy_duplicates(df["nama_usaha"])
    for name, original in dups.items():
        idx = df[df["nama_usaha"] == name].index[0]
        issues.append(
            {
                "baris": idx + 2,
                "nama_usaha": name,
                "kolom_masalah": "nama_usaha",
                "nilai_asli": name,
                "tindakan": f"Kemungkinan duplikat dari '{original}'",
                "confidence_akhir": "low",
            }
        )

    issues_df = pd.DataFrame(issues) if issues else pd.DataFrame()
    return df, issues_df


# ---------------------------------------------------------------------------
# 3. Transform (placeholder — geocoding via Nominatim)
# ---------------------------------------------------------------------------


def transform(df: pd.DataFrame) -> pd.DataFrame:
    if "lat" not in df.columns:
        df["lat"] = None
        df["lon"] = None
        df["geocode_confidence"] = "none"
    return df


# ---------------------------------------------------------------------------
# 4. CLI
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="ETL Data Restoran → Supabase")
    parser.add_argument("--csv", required=True, help="Path ke CSV restoran")
    parser.add_argument("--dry-run", action="store_true", help="Hanya validasi, tanpa load ke DB")
    args = parser.parse_args()

    df = read_csv(args.csv)
    df, issues = validate(df)
    df = transform(df)

    csv_dir = os.path.dirname(args.csv)
    simpan_laporan(issues, os.path.join(csv_dir, "laporan_masalah.csv"))

    if args.dry_run:
        print("DRY-RUN: Data tidak dimuat ke database")
        print(df[["nama_usaha", "omzet_bulanan", "omzet_confidence", "npwp_valid"]].head())
        return

    load_to_supabase(df, "restoran_lapangan", KOLOM_RESTORAN)
    print("ETL selesai.")


if __name__ == "__main__":
    main()
