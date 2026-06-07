# Geospasi

**Open-source geospatial research viewer.** Statis, GeoJSON-first,
siap untuk GitHub Pages. Dibuat untuk akademisi, mahasiswa,
pemerintah daerah, dan komunitas yang membutuhkan viewer data
geospasial gratis tanpa ketergantungan backend.

---

## Project Positioning

Geospasi memiliki tiga lapisan identitas:

| Lapisan | Apa Itu | Contoh |
|---|---|---|
| **Geospasi Core** | Viewer geospasial statis generic. Zero coupling ke region atau dataset tertentu. Bisa digunakan siapa saja untuk daerah mana pun. | `app/` — cukup ganti `config.js` + data |
| **GeoSERANG** | Implementasi referensi untuk Kab. Serang, Banten. 46 layer, 7 lensa tematik. Bukti bahwa Geospasi Core bisa dipakai untuk studi fiskal dan tata ruang daerah nyata. | `examples/geoserang/` |
| **Research Platform** | Use case: platform penelitian geospasial untuk akademisi dan pemda. Satu aplikasi, 7 lensa berbeda — statis, murah, terbuka. | Live di https://zimi17.github.io/geospasi/ |

> **Geospasi Core** adalah *engine*-nya. **GeoSERANG** adalah
> *mobil* perdananya. **Research Platform** adalah *jalan* yang
> akan dilalui.

---

## Struktur Repository

| Direktori | Fungsi |
|---|---|
| `app/` | **Geospasi Core** — viewer generic, zero region coupling. Deploy ini ke GitHub Pages. |
| `examples/geoserang/` | **GeoSERANG** — studi fiskal Kab. Serang, 46 layer GeoJSON, 7 lensa. Referensi implementasi. |
| `examples/geoserang/scripts/` | ETL spesifik Serang (ingest GISTARU, ingest CKAN) |
| `examples/geoserang/data/` | GeoJSON + CSV untuk GeoSERANG (364MB, 46 file) |
| `scripts/` | Generic ETL utilities — GeoJSON simplification, OSM fetch, report |
| `docs/` | Dokumentasi — demo checklist, good first issues, open source preparation |
| `.github/` | CI/CD workflows, issue templates |

## Quick Start

```bash
# Buka demo (sample data included)
open app/index.html

# Atau serve lokal
python3 -m http.server -d app 8000
```

Demo menggunakan sample data bawaan `app/sample-data/`:
- Layer toggle independen (banyak lensa bisa aktif bersamaan)
- Custom GeoJSON URL overlay dengan color picker + opacity
- Popup informasi saat klik fitur
- Share URL dengan state peta + custom layer

## Deploy Your Own Region

1. Copy `app/js/config.sample.js` → `app/js/config.js`
2. Define layers + lensa di config (lihat struktur di sample)
3. Letakkan file GeoJSON di `app/data/`
4. Deploy `app/` ke static host (GitHub Pages, Netlify, dll)

## Live Demo: GeoSERANG

https://zimi17.github.io/geospasi/

GeoSERANG adalah implementasi referensi untuk Kab. Serang, Banten:
46 layer GeoJSON tersebar di 7 lensa tematik:

| Lensa | Layer |
|---|---|
| Dasar | Batas desa, kecamatan, kabupaten, Rupabumi |
| Tata Ruang | Pola ruang kabupaten, provinsi, kawasan strategis, bandara, pelabuhan |
| Risiko | Banjir, gempa, tsunami, longsor, kebakaran hutan, cuaca ekstrem, gunung api, kekeringan |
| Infrastruktur | Jalan kabupaten/provinsi, kondisi jalan, jembatan, kereta api |
| Fisik | Geologi, tanah, kelerengan, penggunaan lahan, DAS, garis pantai |
| Ekonomi | Peta choropleth pendapatan daerah per desa |
| Demografi | Peta choropleth kepadatan penduduk per desa |

## Scripts

| Script | Fungsi |
|---|---|
| `scripts/etl_utils.py` | Fungsi ETL shared (parse revenue, validasi NPWP) |
| `scripts/simplify_web.py` | Simplifikasi GeoJSON untuk web (round koordinat, filter props) |
| `scripts/fetch_osm.py` | Fetch POI dari OpenStreetMap Overpass API |
| `scripts/generate_lensa_data.py` | Gabung CSV BPS dengan batas GeoJSON |
| `scripts/report_geojson_size.py` | Audit ukuran file GeoJSON |

## Built With

- [MapLibre GL JS](https://maplibre.org) — Open-source map rendering
- Vanilla JS — zero framework dependency
- Python 3.14 — ETL + data pipeline

## Repository Stats

- **46** file GeoJSON (364MB simplified, 50 file 1.2GB raw ignored)
- **7** lensa tematik
- **1.315** desa terindeks (search)
- **96** total layer dari GISTARU GeoServer

## Lisensi

ISC

---

*Geospasi — geospasial terbuka untuk semua.*
