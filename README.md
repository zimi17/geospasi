# GeoSERANG

**Sistem Informasi Geografis Analisis Fiskal-Ekonomi Kabupaten Serang**

Platform riset terbuka untuk memetakan potensi PAD (Pendapatan Asli Daerah) berbasis data spasial. Pilot: *Fiscal Leakage Auditor* pajak restoran/hotel di Kecamatan Anyar.

---

## Visi

Membangun layer analisis fiskal-ekonomi di atas infrastruktur SDI (Sistem Data Infrastruktur) dan OpenStreetMap Kabupaten Serang. Target 24 bulan: +10% PAD sektor restoran/hotel, 15 riset terapan oleh akademisi Untirta.

---

## Tech Stack (Ringan — Tanpa Docker)

| Komponen | Pilihan | Alasan |
|----------|---------|--------|
| Database | Supabase (PostGIS) | Cloud gratis, koneksi dari mana saja, RLS keamanan bawaan |
| Analisis Spasial | QGIS 3.28+ | Processing Model, gratis, standar SDI Indonesia |
| ETL & Validasi | Python (GeoPandas, Pandas) | Ringan, cocok RAM 4GB, dokumentasi luas |
| Frontend Publik | Leaflet.js + HTML statis | Zero build step, hosting gratis di GitHub Pages |
| Version Control | GitHub | Monorepo, kontribusi via pull request |
| Geocoding | Nominatim (gratis) + validasi manual | Tanpa API key, cocok data skala kecil |

---

## Peta Folder 5 Menit

| Saya ingin... | Buka folder ini |
|---------------|-----------------|
| Melihat atau menambah data restoran | `potensi_pajak_restoran/data/` |
| Menjalankan script ETL | `potensi_pajak_restoran/etl/` |
| Membuka template analisis di QGIS | `potensi_pajak_restoran/analysis/` |
| Melihat peta interaktif hasil analisis | `potensi_pajak_restoran/web/` |
| Mengambil komponen reusable | `shared/` |
| Dokumentasi tambahan | `docs/` |

### Struktur Lengkap

```
geoserang/
├── potensi_pajak_restoran/        # Modul pilot: pajak restoran Anyar
│   ├── data/                      # CSV & GeoJSON sampel (<500 KB)
│   ├── etl/                       # Script ETL Python
│   ├── analysis/                  # QGIS model & catatan analisis
│   └── web/                       # Frontend Leaflet.js
├── shared/                        # Komponen reusable
│   ├── sql/                       # Skema DB, RLS policies
│   ├── scripts/                   # Utilitas (pembuat data sintetis)
│   └── assets/                    # Logo, ikon, style QGIS
├── docs/                          # Dokumentasi tambahan
├── README.md                      # ← kamu di sini
├── CONTRIBUTING.md
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Prasyarat

- **Python** 3.10+
- **PostgreSQL + PostGIS** (atau akun Supabase gratis — [daftar di sini](https://supabase.com))
- **QGIS** 3.28+ (unduh [di sini](https://qgis.org))
- **RAM** minimal 4GB (telah diuji di laptop 4GB)
- **Git** (unduh [di sini](https://git-scm.com))

---

## Panduan Instalasi

### 1. Clone Repo

```bash
git clone https://github.com/<username>/geoserang.git
cd geoserang
```

### 2. Buat Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
# atau
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Setup Database (Supabase)

**a.** Buat akun gratis di [supabase.com](https://supabase.com)

**b.** Buat project baru, catat:
- Project URL
- Anon key (publik)
- Service key (rahasia)
- Database connection string

**c.** Aktifkan ekstensi PostGIS:
- Buka Supabase Dashboard → SQL Editor
- Jalankan: `CREATE EXTENSION IF NOT EXISTS postgis;`

**d.** Aktifkan Row Level Security (RLS) dan jalankan policies:

```bash
# Buka Supabase Dashboard → SQL Editor
# Copy-paste isi shared/sql/rls_policies.sql
# Klik RUN
```

**e.** Isi file `.env` (copy dari `.env.example`):

```bash
cp .env.example .env
# Edit .env dengan credentials dari Supabase
```

### 5. Generate Data Sintetis

```bash
python shared/scripts/generate_synthetic_data.py
```

### 6. Jalankan ETL

```bash
cd potensi_pajak_restoran
python etl/ingest_restoran.py --csv data/restoran_anyar.csv --dry-run

# Jika sudah siap, jalankan tanpa --dry-run:
python etl/ingest_restoran.py --csv data/restoran_anyar.csv
```

### 7. Buka QGIS Model

Buka QGIS → Processing Toolbox → Models → Open Model → pilih `analysis/deteksi_kesenjangan.model3`

### 8. Lihat Peta Web

Buka `potensi_pajak_restoran/web/index.html` di browser, atau deploy ke GitHub Pages:

```bash
# Settings → Pages → Source: main → folder: /potensi_pajak_restoran/web
```

---

## Roadmap 90 Hari

| Fase | Kegiatan | Durasi | Output |
|------|----------|--------|--------|
| **0** | Setup infrastruktur & data sintetis | 2 minggu | PostGIS siap, ETL jalan, model QGIS template |
| **1** | Input data nyata (50 restoran) | 2 minggu | Dataset valid, geocode, confidence score |
| **2** | Validasi model gap fiskal | 3 minggu | Hasil gap per desa, laporan riset draft |
| **3** | Finalisasi model + QGIS automation | 4 minggu | `.model3` final, batch processing script |
| **4** | Publikasi peta cerita | 2 minggu | Leaflet storymap, artikel GitHub Pages |

---

## Keamanan Data

| Jenis Data | Akses | Lokasi |
|------------|-------|--------|
| Kode & model | Publik (AGPLv3) | GitHub |
| Data sintetis | Publik | `data/` di repo |
| Data agregat per desa | Publik (anon key RLS) | Supabase schema `public` |
| Data mentah (nama, NPWP, omzet) | Peneliti terdaftar | Supabase schema `restricted` |

**Data mentah tidak pernah masuk Git.** Hanya data sintetis dan agregat yang dipublikasikan.

---

## Kontribusi

Kami menyambut kontribusi dari akademisi, mahasiswa, dan komunitas GIS. Baca [CONTRIBUTING.md](CONTRIBUTING.md) untuk panduan memulai.

**Pertanyaan?** Buat issue di GitHub atau hubungi maintainer.

---

## Lisensi

Kode: AGPLv3. Data sintetis: CC0 (domain publik). Data riset: tunduk pada perjanjian dengan Pemkab Serang.
