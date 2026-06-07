# GeoSERANG — Kabupaten Serang Fiscal Study

Example implementation of Geospasi for Kab. Serang, Banten.

**7 Thematic Lensa — 46 GeoJSON Layers — 364MB Data**

| Lensa | Layers | Source |
|---|---|---|
| Dasar | 3 (desa, kecamatan, kabupaten boundaries) | GISTARU |
| Tata Ruang | 4 (pola ruang, pariwisata, hutan) | GISTARU |
| Risiko | 8 (banjir, gempa, tsunami, longsor, dll) | GISTARU/BNPB |
| Infrastruktur | 5 (jalan, jembatan, jaringan) | GISTARU/PUPR |
| Fisik | 4 (kelerengan, lahan, DAS) | GISTARU |
| Ekonomi | 1 (hotel per desa choropleth) | BPS |
| Demografi | 1 (penduduk per kecamatan) | BPS |

## Deploy

```bash
cp config.js ../../app/js/config.js
cp -r data/* ../../app/data/
# Then deploy app/ to GitHub Pages
```

## Data Sources

- GISTARU Banten — GeoServer WFS (webgis_sipr workspace)
- CKAN Kab. Serang — opendata.serangkab.go.id
- BPS — serangkab.bps.go.id
- OpenStreetMap — Overpass API

## Scripts

| Script | Purpose |
|---|---|
| `scripts/ingest_gistaru.py` | Download WFS layers from GISTARU |
| `scripts/ingest_ckan.py` | Scrape CKAN catalog |
| `scripts/generate_synthetic_data.py` | Generate demo data |
| `studi/potensi_pajak_restoran/etl/ingest_restoran.py` | Restoran ETL pipeline |
| `studi/potensi_pajak_hotel/etl/ingest_hotel.py` | Hotel ETL pipeline |

See `docs/` for detailed data source documentation.
