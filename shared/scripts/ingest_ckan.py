from __future__ import annotations

import csv
import json
import os
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

CKAN_URL = "https://opendata.serangkab.go.id/en_AU/api/3/action/"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(HERE, "..", "data"))


def ckan_request(action: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    url = f"{CKAN_URL}{action}"
    if params:
        import urllib.parse

        url += "?" + urllib.parse.urlencode(params)
    req = Request(url, headers={"User-Agent": "SPASI-ETL/1.0"})
    try:
        with urlopen(req, timeout=30) as resp:
            result: dict[str, Any] = json.loads(resp.read().decode())
            return result
    except URLError as e:
        print(f"ERROR CKAN: {e}")
        return {"success": False}


def search_datasets(query: str = "", rows: int = 1000) -> list[dict[str, Any]]:
    result = ckan_request("package_search", {"q": query, "rows": str(rows)})
    results: list[dict[str, Any]] = result.get("result", {}).get("results", [])
    return results


def download_resource(url: str, output_path: str) -> bool:
    req = Request(url, headers={"User-Agent": "SPASI-ETL/1.0"})
    try:
        with urlopen(req, timeout=60) as resp:
            data = resp.read()
        with open(output_path, "wb") as f:
            f.write(data)
        print(f"OK: {output_path} ({len(data) >> 10}KB)")
        return True
    except URLError as e:
        print(f"FAIL: {url} — {e}")
        return False


def export_catalog(datasets: list[dict[str, Any]]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, "ckan_catalog.csv")
    rows: list[dict[str, Any]] = []
    for ds in datasets:
        for res in ds.get("resources", []):
            rows.append(
                {
                    "dataset_id": ds["id"],
                    "dataset_name": ds["title"],
                    "dataset_notes": (ds.get("notes") or "")[:200],
                    "resource_id": res["id"],
                    "resource_name": res["name"],
                    "format": res.get("format", ""),
                    "url": res.get("url", ""),
                    "last_modified": res.get("last_modified", ""),
                }
            )
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"OK: Catalog → {path} ({len(rows)} resource)")


PRIORITY_RESOURCES: list[dict[str, str]] = [
    {"name": "data_desa", "pattern": "desa", "format": "csv"},
    {"name": "pdrb", "pattern": "pdrb", "format": "csv"},
    {"name": "pariwisata", "pattern": "pariwisata", "format": "csv"},
]


def download_priority(datasets: list[dict[str, Any]]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    for prio in PRIORITY_RESOURCES:
        for ds in datasets:
            for res in ds.get("resources", []):
                name = (res.get("name") or "").lower()
                fmt = (res.get("format") or "").lower()
                if prio["pattern"] in name and fmt == prio["format"]:
                    url = res.get("url", "")
                    if url:
                        ext = fmt if fmt == "csv" else "bin"
                        out = os.path.join(DATA_DIR, f"{prio['name']}.{ext}")
                        download_resource(url, out)


def main() -> None:
    print("Mencari dataset dari CKAN Kab. Serang...")
    datasets = search_datasets()
    print(f"Ditemukan: {len(datasets)} dataset")

    export_catalog(datasets)
    download_priority(datasets)

    print("\nSelesai. Dataset siap digunakan untuk ETL pipeline.")


if __name__ == "__main__":
    main()
