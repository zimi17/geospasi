"""
ingest_ckan.py — ETL untuk scraping Open Data Kab. Serang via CKAN API

API Base: https://opendata.serangkab.go.id/en_AU/api/3/action/
Lisensi: ODC-BY / CC-BY (ataset terbuka untuk publik)

Penggunaan:
    # Cari dataset terkait pajak
    python shared/scripts/ingest_ckan.py --q pajak --rows 5

    # Download semua resource dari dataset tertentu
    python shared/scripts/ingest_ckan.py --dataset-id pendapatan --download

    # Daftar semua dataset dari organisasi BAPENDA
    python shared/scripts/ingest_ckan.py --org bappeda-serangkab --rows 50

    # Export semua dataset ke CSV (metadata)
    python shared/scripts/ingest_ckan.py --export-all shared/data/ckan_catalog.csv
"""

import argparse
import csv
import os
import sys
from pathlib import Path

import requests

CKAN_BASE = "https://opendata.serangkab.go.id/en_AU/api/3/action"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def ckan_request(endpoint: str, params: dict | None = None) -> dict:
    url = f"{CKAN_BASE}/{endpoint}"
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if not data.get("success"):
        print(f"  [GAGAL] {endpoint}: {data.get('error', 'unknown error')}")
        return {}
    return data.get("result", {})


def search_datasets(q: str = "", rows: int = 10, org: str = "", tags: str = ""):
    params = {"rows": rows, "sort": "metadata_modified desc"}
    if q:
        params["q"] = q
    if org:
        params["fq"] = f"organization:{org}"
    if tags:
        params["fq"] = f"tags:{tags}"

    result = ckan_request("package_search", params)
    datasets = result.get("results", [])
    print(f"\n{'='*60}")
    print(f"Pencarian: q='{q}' org='{org}' tags='{tags}'")
    print(f"Total ditemukan: {result.get('count', 0)}")
    print(f"Ditampilkan: {len(datasets)}")
    print(f"{'='*60}")

    for ds in datasets:
        org_name = ds.get("organization", {}).get("title", "-")
        n_res = ds.get("num_resources", 0)
        updated = ds.get("metadata_modified", "")[:10]
        print(f"\n[{ds['name']}]")
        print(f"  Judul     : {ds['title']}")
        print(f"  Organisasi: {org_name}")
        print(f"  Resource  : {n_res} file")
        print(f"  Diperbarui: {updated}")
        print(f"  Lisensi   : {ds.get('license_title', '-')}")
        for res in ds.get("resources", []):
            fmt = res.get("format", "?").upper()
            size = res.get("size", 0)
            size_str = f"{size} byte" if size < 1024 else f"{size/1024:.0f} KB"
            print(f"    [{fmt}] {res['name']} ({size_str})")
            print(f"           {res['url']}")

    return datasets


def download_resource(resource: dict, dest_dir: Path = DATA_DIR):
    url = resource["url"]
    name = resource.get("name", resource["id"])
    safe_name = "".join(c if c.isalnum() or c in "._- " else "_" for c in name)
    safe_name = safe_name.strip()[:100]

    if not safe_name.endswith(".csv"):
        safe_name += ".csv"

    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / safe_name

    print(f"  Download: {safe_name}")
    r = requests.get(url, timeout=60)
    if r.status_code == 200:
        dest_path.write_bytes(r.content)
        size = len(r.content)
        print(f"    -> Tersimpan: {dest_path} ({size} byte)")
        return str(dest_path)
    else:
        print(f"    -> GAGAL: HTTP {r.status_code}")
        return None


def download_dataset(dataset_id: str, dest_dir: Path = DATA_DIR):
    result = ckan_request("package_show", {"id": dataset_id})
    if not result:
        return

    print(f"\nDataset: {result['title']} ({result['name']})")
    print(f"Resource: {result.get('num_resources', 0)} file")

    for res in result.get("resources", []):
        if res.get("format", "").upper() in ("CSV", "XLSX"):
            download_resource(res, dest_dir)


def list_datasets_by_org(org_name: str, rows: int = 100):
    return search_datasets(org=org_name, rows=rows)


def export_all_catalog(output_path: str | None = None):
    """Export metadata semua dataset ke CSV."""
    if output_path is None:
        output_path = str(DATA_DIR / "ckan_catalog.csv")

    rows = []
    page = 0
    limit = 100

    while True:
        result = ckan_request("package_search", {
            "rows": limit, "start": page * limit,
            "sort": "metadata_modified desc"
        })
        datasets = result.get("results", [])
        if not datasets:
            break

        for ds in datasets:
            org = ds.get("organization", {})
            rows.append({
                "id": ds["id"],
                "name": ds["name"],
                "title": ds["title"],
                "organization": org.get("title", ""),
                "org_id": org.get("id", ""),
                "notes": ds.get("notes", "").replace("\n", " ")[:200],
                "num_resources": ds.get("num_resources", 0),
                "license": ds.get("license_title", ""),
                "created": ds.get("metadata_created", "")[:10],
                "updated": ds.get("metadata_modified", "")[:10],
                "url": f"https://opendata.serangkab.go.id/en_AU/dataset/{ds['name']}",
            })
        page += 1
        print(f"  Halaman {page}: {len(datasets)} dataset")

        if len(datasets) < limit:
            break

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nEkspor selesai: {len(rows)} dataset -> {path}")
    return path


def main():
    parser = argparse.ArgumentParser(
        description="CKAN ETL — Open Data Kab. Serang"
    )
    parser.add_argument("--q", help="Kata kunci pencarian")
    parser.add_argument("--rows", type=int, default=10, help="Jumlah hasil")
    parser.add_argument("--org", help="Filter organisasi (slug)")
    parser.add_argument("--tags", help="Filter tag")
    parser.add_argument("--dataset-id", help="ID/nama dataset untuk detail/download")
    parser.add_argument("--download", action="store_true",
                        help="Download resource dari dataset")
    parser.add_argument("--export-all", metavar="PATH",
                        help="Export semua dataset ke CSV metadata")

    args = parser.parse_args()

    if args.export_all:
        export_all_catalog(args.export_all)
        return

    if args.dataset_id:
        if args.download:
            download_dataset(args.dataset_id)
        else:
            search_datasets(q=args.dataset_id, rows=1)
        return

    search_datasets(
        q=args.q or "",
        rows=args.rows,
        org=args.org or "",
        tags=args.tags or "",
    )


if __name__ == "__main__":
    main()
