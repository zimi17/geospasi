"""
etl_utils.py — Fungsi umum ETL untuk semua sumber data SPASI

Fungsi:
  - parse_revenue()    : Parse string omzet ke float + confidence
  - validate_npwp()    : Validasi NPWP 15 digit
  - fuzzy_duplicates() : Deteksi duplikat nama fuzzy
  - read_csv()         : Baca CSV dengan error handling
  - simpan_laporan()   : Simpan laporan masalah ke CSV
  - load_to_supabase() : Load DataFrame ke Supabase via REST API
  - generate_hotel_sql(): Generate SQL untuk tabel hotel
"""

from __future__ import annotations

import json
import os
import re
import sys
from difflib import SequenceMatcher
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pandas as pd

# ---------------------------------------------------------------------------
# Kolom wajib per sumber data
# ---------------------------------------------------------------------------

KOLOM_RESTORAN = {
    "nama_usaha",
    "pemilik",
    "alamat",
    "desa",
    "kecamatan",
    "npwp",
    "omzet_bulanan",
    "kategori",
    "status",
    "lat",
    "lon",
    "geocode_confidence",
    "omzet_confidence",
    "npwp_valid",
}

KOLOM_HOTEL = {
    "nama_usaha",
    "pemilik",
    "alamat",
    "desa",
    "kecamatan",
    "npwp",
    "jumlah_kamar",
    "tarif_rata",
    "okupansi_persen",
    "omzet_bulanan",
    "omzet_confidence",
    "status",
    "npwp_valid",
    "lat",
    "lon",
    "geocode_confidence",
}


# ---------------------------------------------------------------------------
# Parse omzet
# ---------------------------------------------------------------------------


def parse_revenue(value: Any) -> tuple[float | None, str]:
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


# ---------------------------------------------------------------------------
# Validasi NPWP
# ---------------------------------------------------------------------------


def validate_npwp(value: Any) -> bool:
    if pd.isna(value) or str(value).strip() in ("", "-", "0"):
        return False
    digits = re.sub(r"\D", "", str(value))
    return len(digits) == 15


# ---------------------------------------------------------------------------
# Fuzzy duplicate detection
# ---------------------------------------------------------------------------


def fuzzy_duplicates(names: pd.Series, threshold: float = 0.85) -> dict[str, str]:
    name_list: list[str] = names.fillna("").tolist()
    dup_map: dict[str, str] = {}
    for i in range(len(name_list)):
        for j in range(i + 1, len(name_list)):
            ratio = SequenceMatcher(None, name_list[i], name_list[j]).ratio()
            if ratio >= threshold:
                dup_map[name_list[j]] = name_list[i]
    return dup_map


# ---------------------------------------------------------------------------
# Baca CSV
# ---------------------------------------------------------------------------


def read_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        print(f"ERROR: File tidak ditemukan: {path}")
        sys.exit(1)
    df = pd.read_csv(path, dtype=str)
    print(f"OK: {len(df)} baris dibaca dari {path}")
    return df


# ---------------------------------------------------------------------------
# Simpan laporan masalah
# ---------------------------------------------------------------------------


def simpan_laporan(issues_df: pd.DataFrame, path: str) -> None:
    if issues_df.empty:
        print("OK: Tidak ada masalah validasi")
        return
    issues_df.to_csv(path, index=False)
    print(f"OK: Laporan masalah disimpan ke {path}")
    print(f"    Total masalah: {len(issues_df)}")


# ---------------------------------------------------------------------------
# Load ke Supabase via REST API
# ---------------------------------------------------------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://vhthvtampaedrxiadmlc.supabase.co")
SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")


def load_to_supabase(
    df: pd.DataFrame,
    table_name: str,
    allowed_columns: set[str],
) -> None:
    if not SERVICE_KEY:
        print("ERROR: SUPABASE_SERVICE_KEY tidak ditemukan di .env")
        sys.exit(1)

    cols = list(allowed_columns & set(df.columns))
    rows = df[cols].copy()
    rows = rows.where(pd.notna(rows), None)

    if "npwp_valid" in rows.columns:
        rows["npwp_valid"] = (
            rows["npwp_valid"].astype(object).where(rows["npwp_valid"].notna(), None)
        )

    records: list[dict[str, Any]] = json.loads(rows.to_json(orient="records", default_handler=str))
    headers = {
        "apikey": SERVICE_KEY,
        "Authorization": f"Bearer {SERVICE_KEY}",
        "Content-Type": "application/json",
    }
    url = f"{SUPABASE_URL}/rest/v1/{table_name}"
    body = json.dumps(records).encode()

    req = Request(url, data=body, headers=headers, method="POST")
    try:
        with urlopen(req) as resp:
            raw = resp.read().decode()
            inserted = len(json.loads(raw)) if raw else len(records)
            print(f"OK: {inserted} baris dimuat ke {table_name} via REST API")
    except HTTPError as e:
        err = e.read().decode()
        print(f"ERROR {e.code}: {err[:500]}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Generate SQL untuk tabel hotel
# ---------------------------------------------------------------------------

SQL_HOTEL = """
CREATE TABLE IF NOT EXISTS hotel_lapangan (
    id SERIAL PRIMARY KEY,
    nama_usaha TEXT,
    pemilik TEXT,
    alamat TEXT,
    desa TEXT,
    kecamatan TEXT DEFAULT 'Anyar',
    npwp TEXT,
    jumlah_kamar INTEGER,
    tarif_rata NUMERIC,
    okupansi_persen NUMERIC,
    omzet_bulanan NUMERIC,
    omzet_confidence TEXT,
    status TEXT,
    npwp_valid BOOLEAN,
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    geocode_confidence TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE hotel_lapangan ENABLE ROW LEVEL SECURITY;

CREATE POLICY select_hotel_publik ON hotel_lapangan
    FOR SELECT USING (true);

CREATE POLICY insert_hotel_service ON hotel_lapangan
    FOR INSERT WITH CHECK (auth.role() = 'service_role');

CREATE POLICY update_hotel_service ON hotel_lapangan
    FOR UPDATE USING (auth.role() = 'service_role');

CREATE POLICY delete_hotel_service ON hotel_lapangan
    FOR DELETE USING (auth.role() = 'service_role');
"""
