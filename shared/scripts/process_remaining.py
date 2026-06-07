"""Process remaining GeoJSON files for web data."""
import json
from pathlib import Path

SRC = Path("shared/data/spasial")
DST = Path("web/data")
DST.mkdir(parents=True, exist_ok=True)

# Max size to process (50MB)
MAX_BYTES = 50_000_000

processed = 0
skipped_big = 0

for f in sorted(SRC.glob("*.geojson")):
    dst = DST / f.name

    if dst.exists() and dst.stat().st_size > 1000:
        continue

    size = f.stat().st_size
    if size > MAX_BYTES:
        print(f"  SKIP (besar): {f.stem} ({size//1024//1024}MB)")
        skipped_big += 1
        continue

    print(f"  PROSES: {f.stem} ({size//1024}KB)...", end=" ")

    try:
        with open(f) as fh:
            data = json.load(fh)

        features = data.get("features", [])
        for feat in features:
            g = feat.get("geometry")
            if g and g.get("coordinates"):
                def rc(v, d=5):
                    if isinstance(v, (int, float)):
                        return round(float(v), d)
                    if isinstance(v, list):
                        return [rc(x, d) for x in v]
                    return v
                g["coordinates"] = rc(g["coordinates"])

            props = feat.get("properties", {})
            feat["properties"] = dict(list(props.items())[:4])

        data["features"] = features
        with open(dst, "w") as fh:
            json.dump(data, fh, ensure_ascii=False)

        new_size = dst.stat().st_size
        print(f"{new_size//1024}KB ({new_size*100//size}%)")
        processed += 1
    except Exception as e:
        print(f"ERROR: {e}")

print(f"\nDone: {processed} OK, {skipped_big} skipped (besar)")
