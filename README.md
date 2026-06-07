# Geospasi

**Open-source geospatial research viewer.**

Static-first, GeoJSON-first, GitHub Pages friendly. Built for students, researchers, local governments, and communities who need a free geospatial data viewer.

| Directory | Purpose |
|---|---|
| `app/` | Core viewer — generic, zero region coupling |
| `examples/geoserang/` | Kab. Serang fiscal study — reference implementation |
| `scripts/` | Generic ETL utilities (GeoJSON simplification, OSM fetch) |

## Quick Start

```bash
# Open the demo
open app/index.html

# Or serve locally
python3 -m http.server -d app 8000
```

The demo loads sample data showing the core viewer features:
- Layer toggle (multiple layers active at once)
- Custom GeoJSON URL overlay
- Popup info on click
- Share URL with state

## Deploy Your Own Region

1. Copy `app/js/config.sample.js` → `app/js/config.js`
2. Define your layers (see sample config for structure)
3. Place GeoJSON files in `app/data/`
4. Deploy `app/` to any static host (GitHub Pages, Netlify, etc.)

## Examples

### GeoSERANG — Kab. Serang Fiscal Study

Full implementation with 46 GeoJSON layers across 7 thematic lens:
- Dasar, Tata Ruang, Risiko, Infrastruktur, Fisik, Ekonomi, Demografi

```bash
# Deploy GeoSERANG
cp examples/geoserang/config.js app/js/config.js
cp -r examples/geoserang/data/* app/data/
# Then deploy app/ to any static host
```

## Scripts

| Script | Function |
|---|---|
| `scripts/etl_utils.py` | Shared ETL functions (parse revenue, NPWP validation) |
| `scripts/simplify_web.py` | Simplify GeoJSON for web (round coords, filter props) |
| `scripts/fetch_osm.py` | Fetch POI data from OpenStreetMap Overpass API |
| `scripts/generate_lensa_data.py` | Join BPS CSV data with GeoJSON boundaries |

## Built With

- [MapLibre GL JS](https://maplibre.org) — Open-source map rendering
- Vanilla JS — No framework dependencies

## License

MIT
