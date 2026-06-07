from __future__ import annotations

import argparse
import json
import sys
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

import pandas as pd

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def build_query(
    bbox: tuple[float, float, float, float],
    amenity_types: list[str] | None = None,
) -> str:
    if amenity_types is None:
        amenity_types = ["restaurant", "cafe"]
    tags = " ".join(f'nwr["amenity"="{t}"]' for t in amenity_types)
    tags += ' nwr["shop"="supermarket"]'
    south, west, north, east = bbox
    return (
        f"[out:json][timeout:30];\n"
        f"  (\n"
        f"    {tags}({south},{west},{north},{east});\n"
        f"  );\n"
        f"out center tags;\n"
    )


def fetch_osm(
    bbox: tuple[float, float, float, float],
    amenity_types: list[str] | None = None,
) -> pd.DataFrame:
    query = build_query(bbox, amenity_types)
    data = json.dumps({"data": query}).encode()
    req = Request(
        OVERPASS_URL,
        data=data,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"},
    )

    try:
        with urlopen(req, timeout=60) as resp:
            result: dict[str, Any] = json.loads(resp.read().decode())
    except URLError as e:
        print(f"ERROR: Gagal fetch Overpass API ({e})")
        sys.exit(1)

    records: list[dict[str, Any]] = []
    for el in result.get("elements", []):
        tags: dict[str, str] = el.get("tags", {})
        if el["type"] == "node":
            lat, lon = el.get("lat"), el.get("lon")
        else:
            lat = el.get("center", {}).get("lat")
            lon = el.get("center", {}).get("lon")
        if lat is None or lon is None:
            continue

        if tags.get("amenity") == "restaurant":
            kategori = "restoran"
        elif tags.get("amenity") == "cafe":
            kategori = "kafe"
        elif tags.get("shop") == "supermarket":
            kategori = "supermarket"
        else:
            continue

        name = tags.get("name") or tags.get("name:id") or ""
        pemilik = tags.get("operator") or ""
        parts = []
        for key in [
            "addr:housenumber",
            "addr:street",
            "addr:subdistrict",
            "addr:district",
            "addr:city",
        ]:
            v = tags.get(key, "")
            if v:
                parts.append(v)
        alamat = ", ".join(parts) if parts else ""

        records.append(
            {
                "nama_usaha": name,
                "pemilik": pemilik,
                "alamat": alamat,
                "lat": round(float(lat), 6),
                "lon": round(float(lon), 6),
                "kategori": kategori,
                "sumber_data": "osm",
            }
        )

    return pd.DataFrame(records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch data dari OpenStreetMap")
    parser.add_argument(
        "--bbox",
        nargs=4,
        type=float,
        default=[-6.15, 105.80, -5.95, 106.00],
        metavar=("SOUTH", "WEST", "NORTH", "EAST"),
        help="Bounding box (south west north east)",
    )
    parser.add_argument("--output", default=None, help="Path output CSV")
    parser.add_argument("--print", action="store_true", help="Print hasil ke stdout")
    args = parser.parse_args()

    bbox = tuple(args.bbox)
    df = fetch_osm(bbox)
    print(f"OK: {len(df)} titik dari OSM")

    if args.output:
        df.to_csv(args.output, index=False)
        print(f"OK: Disimpan ke {args.output}")

    if args.print or not args.output:
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()
