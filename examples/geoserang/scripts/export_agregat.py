from __future__ import annotations

import json
import os
from typing import Any
from urllib.request import Request, urlopen

import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def query_supabase() -> pd.DataFrame | None:
    supabase_url = os.getenv("SUPABASE_URL", "https://vhthvtampaedrxiadmlc.supabase.co")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")
    if not service_key:
        print("WARN: SUPABASE_SERVICE_KEY tidak ditemukan, fallback ke CSV")
        return None

    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
    }

    url = f"{supabase_url}/rest/v1/restoran_lapangan?select=desa,status,omzet_bulanan"
    req = Request(url, headers=headers)
    try:
        with urlopen(req) as resp:
            rows: list[dict[str, Any]] = json.loads(resp.read().decode())
            if not rows:
                return None
            df = pd.DataFrame(rows)
            df["omzet_bulanan"] = pd.to_numeric(df["omzet_bulanan"], errors="coerce")
            agg = df.groupby("desa", as_index=False).agg(
                jumlah_restoran=("status", "count"),
                terdaftar=("status", lambda x: (x == "terdaftar").sum()),
                tidak_terdaftar=("status", lambda x: (x == "tidak_terdaftar").sum()),
                total_omzet=("omzet_bulanan", "sum"),
                rata_omzet=("omzet_bulanan", "mean"),
            )
            agg["total_omzet"] = agg["total_omzet"].fillna(0)
            agg["rata_omzet"] = agg["rata_omzet"].fillna(0)
            print("INFO: Data dari Supabase (REST API)")
            return agg
    except Exception as e:
        print(f"WARN: Gagal query Supabase ({e}), fallback ke CSV")
        return None


def csv_fallback() -> pd.DataFrame | None:
    csv_path = os.path.join(ROOT, "potensi_pajak_restoran", "data", "restoran_anyar.csv")
    if not os.path.exists(csv_path):
        print("ERROR: Tidak ada data di Supabase maupun CSV")
        return None

    df = pd.read_csv(csv_path)
    agg = (
        df.groupby("desa")
        .agg(
            jumlah_restoran=("id", "count"),
            terdaftar=("status", lambda x: (x == "terdaftar").sum()),
            tidak_terdaftar=("status", lambda x: (x == "tidak_terdaftar").sum()),
            total_omzet=("omzet_bulanan", lambda x: pd.to_numeric(x, errors="coerce").sum()),
            rata_omzet=("omzet_bulanan", lambda x: pd.to_numeric(x, errors="coerce").mean()),
        )
        .reset_index()
    )
    print("INFO: Data dari CSV fallback")
    return agg


def main() -> int:
    agg = query_supabase()

    if agg is None:
        agg = csv_fallback()
        if agg is None:
            return 1

    desa_path = os.path.join(ROOT, "potensi_pajak_restoran", "data", "desa_anyar.geojson")
    with open(desa_path) as f:
        desa_geojson: dict[str, Any] = json.load(f)

    for feature in desa_geojson["features"]:
        desa_name = feature["properties"]["desa"]
        match = agg[agg["desa"] == desa_name]
        if not match.empty:
            row = match.iloc[0]
            feature["properties"].update(
                {
                    "jumlah_restoran": int(row["jumlah_restoran"]),
                    "terdaftar": int(row["terdaftar"]),
                    "tidak_terdaftar": int(row["tidak_terdaftar"]),
                    "total_omzet": float(row["total_omzet"]),
                    "rata_omzet": float(round(row["rata_omzet"], 0)),
                }
            )

    output = {
        "type": "FeatureCollection",
        "features": desa_geojson["features"],
    }

    out_path = os.path.join(ROOT, "potensi_pajak_restoran", "data", "agregat_desa.geojson")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"OK: {out_path} — {len(desa_geojson['features'])} desa ditulis")
    return 0


if __name__ == "__main__":
    exit(main())
