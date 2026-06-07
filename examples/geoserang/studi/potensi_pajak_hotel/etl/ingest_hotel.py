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

from __future__ import annotations

import os
import sys
from typing import Any

import pandas as pd
from dotenv import load_dotenv

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from scripts.etl_utils import (  # noqa: E402
    KOLOM_HOTEL,
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

    for _, row in df[df["omzet_confidence"] == "low"].iterrows():
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

    for _, row in df[df["omzet_confidence"] == "unparseable"].iterrows():
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

    df["jumlah_kamar"] = pd.to_numeric(df["jumlah_kamar"], errors="coerce")
    for idx, r in df[pd.isna(df["jumlah_kamar"])].iterrows():
        issues.append(
            {
                "baris": idx + 2,
                "nama_usaha": r["nama_usaha"],
                "kolom_masalah": "jumlah_kamar",
                "nilai_asli": r["jumlah_kamar"],
                "tindakan": "Diisi 0",
                "confidence_akhir": "low",
            }
        )
    df["jumlah_kamar"] = df["jumlah_kamar"].fillna(0).astype(int)

    df["tarif_rata"] = pd.to_numeric(df["tarif_rata"], errors="coerce")
    for idx, r in df[pd.isna(df["tarif_rata"])].iterrows():
        issues.append(
            {
                "baris": idx + 2,
                "nama_usaha": r["nama_usaha"],
                "kolom_masalah": "tarif_rata",
                "nilai_asli": r["tarif_rata"],
                "tindakan": "Diisi 0",
                "confidence_akhir": "low",
            }
        )
    df["tarif_rata"] = df["tarif_rata"].fillna(0.0)

    df["okupansi_persen"] = pd.to_numeric(df["okupansi_persen"], errors="coerce")
    for idx, r in df[(df["okupansi_persen"] < 0) | (df["okupansi_persen"] > 100)].iterrows():
        issues.append(
            {
                "baris": idx + 2,
                "nama_usaha": r["nama_usaha"],
                "kolom_masalah": "okupansi_persen",
                "nilai_asli": r["okupansi_persen"],
                "tindakan": "Dibatasi 0-100",
                "confidence_akhir": "low",
            }
        )
    df["okupansi_persen"] = df["okupansi_persen"].clip(0, 100)

    df["npwp_valid"] = df["npwp"].apply(validate_npwp)
    for idx, r in df[~df["npwp_valid"]].iterrows():
        issues.append(
            {
                "baris": idx + 2,
                "nama_usaha": r["nama_usaha"],
                "kolom_masalah": "npwp",
                "nilai_asli": r["npwp"],
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
# 3. Transform
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

    parser = argparse.ArgumentParser(description="ETL Data Hotel → Supabase")
    parser.add_argument("--csv", required=True, help="Path ke CSV hotel")
    parser.add_argument("--dry-run", action="store_true", help="Hanya validasi, tanpa load ke DB")
    args = parser.parse_args()

    df = read_csv(args.csv)
    df, issues = validate(df)
    df = transform(df)

    csv_dir = os.path.dirname(args.csv)
    simpan_laporan(issues, os.path.join(csv_dir, "laporan_masalah.csv"))

    if args.dry_run:
        print("DRY-RUN: Data tidak dimuat ke database")
        print(df[["nama_usaha", "jumlah_kamar", "tarif_rata", "omzet_bulanan"]].head())
        return

    load_to_supabase(df, "hotel_lapangan", KOLOM_HOTEL)
    print("ETL selesai.")


if __name__ == "__main__":
    main()
