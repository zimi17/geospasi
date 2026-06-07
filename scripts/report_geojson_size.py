from __future__ import annotations

import json
import os

DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "examples", "geoserang", "data")
)


def main() -> None:
    if not os.path.isdir(DATA_DIR):
        print(f"ERROR: {DATA_DIR} tidak ditemukan")
        return

    files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith(".geojson"))
    if not files:
        print("Tidak ada file GeoJSON.")
        return

    rows: list[dict[str, object]] = []
    for fname in files:
        path = os.path.join(DATA_DIR, fname)
        size_mb = os.path.getsize(path) / (1024 * 1024)
        with open(path) as f:
            data = json.load(f)
        features = len(data.get("features", []))
        props_count = 0
        for feat in data["features"]:
            p = feat.get("properties", {})
            props_count += len(p)
        avg_props = round(props_count / features, 1) if features else 0
        rows.append(
            {
                "file": fname,
                "size_mb": round(size_mb, 1),
                "features": features,
                "avg_props": avg_props,
            }
        )

    # sort by size desc
    rows.sort(key=lambda r: r["size_mb"], reverse=True)

    print(f"{'File':<50} {'Size (MB)':<12} {'Features':<12} {'Avg Props':<10}")
    print("-" * 84)
    total_mb = 0
    for r in rows:
        print(f"{r['file']:<50} {r['size_mb']:<12} {r['features']:<12} {r['avg_props']:<10}")
        total_mb += r["size_mb"]
    print("-" * 84)
    print(f"{'TOTAL':<50} {round(total_mb, 1):<12} {sum(r['features'] for r in rows):<12}")

    print("\n=== TOP 10 TERBESAR ===")
    for r in rows[:10]:
        print(f"  {r['file']:<50} {r['size_mb']}MB  ({r['features']} fitur)")

    over_20mb = [r for r in rows if r["size_mb"] > 20]
    if over_20mb:
        print(f"\n=== KANDIDAT OPTIMASI (>20MB, {len(over_20mb)} file) ===")
        for r in over_20mb:
            print(f"  {r['file']:<50} {r['size_mb']}MB — {r['features']} fitur")


if __name__ == "__main__":
    main()
