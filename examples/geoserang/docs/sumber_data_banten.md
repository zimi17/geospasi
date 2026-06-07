# Daftar Sumber Data Terbuka — Provinsi Banten & Kabupaten Serang

**Pembaruan:** Juni 2026  
**Tujuan:** Dokumentasi hasil audit Fase 1 Open Data Pemerintah untuk riset SPASI  
**Fokus:** Kecamatan Anyar, Kabupaten Serang (pajak restoran & hotel)

---

## 1. Open Data Kabupaten Serang

**URL:** https://opendata.serangkab.go.id  
**Platform:** CKAN 2.9  
**Lisensi:** ODC-BY (mayoritas), CC-BY  
**API:** `https://opendata.serangkab.go.id/en_AU/api/3/action/`  
**Total Dataset:** 4.203 dataset  
**Total Organisasi:** 50+ OPD  
**Format Data:** CSV (4.091), XLSX (92), JPEG (6)

### Dataset Terkait SPASI

| Dataset | OPD | Tipe Data | Granularitas | Ukuran | Relevansi |
|---------|-----|-----------|-------------|--------|-----------|
| Pendapatan Pajak Daerah & Retribusi Daerah | BAPENDA | Agregat Tahunan | Kabupaten | 128 byte, 2 baris (2021-2022) | PAD baseline |
| Pertumbuhan Ekonomi (PDRB) | DKPP | Agregat Tahunan | Kabupaten | 236 byte, 3 baris (2020-2022) | Konteks ekonomi |
| Data BPS Pariwisata, Transportasi & Komunikasi | BPS | Detail per Desa | **Desa** | 21 KB, 326 baris | **Hotel & penginapan per desa!** |
| Data BPS Kecamatan | BPS | Multi-sektor | **Kecamatan** | 11 KB, 29 kecamatan | Demografi, pendidikan, cuaca |
| Data Desa | DPMD | Daftar desa + koordinat | **Desa** | 26 KB, 326 baris | Validasi desa, kode Kemendagri |
| Jasa Boga Rumah Makan/Restoran | Dinkes | Agregat | Kabupaten | 875 byte | Kesehatan restoran |
| Dokumen Ketetapan Pajak Daerah | BAPENDA | Agregat | Kabupaten | 663 byte | Metadata jumlah SKP |
| Pelaku Ekonomi Kreatif 17 Subsektor | Disporapar | Agregat | Kabupaten | 727 byte | Kreatif (kuliner) |
| Kawasan Strategis Pariwisata | Disporapar | Agregat | Kabupaten | 1.1 KB | Pariwisata |

### Dataset Pajak BAPENDA (20 dataset)

Seluruh dataset BAPENDA bersifat **agregat jumlah dokumen/laporan**, bukan data transaksional:
- Dokumen Ketetapan Pajak Daerah
- Laporan Pengembangan Pajak Daerah
- Layanan dan Konsultasi Pajak Daerah
- Dokumen Rencana Pengelolaan Pajak Daerah
- Laporan Pendataan Objek Pajak Daerah
- Sarana Prasarana Pengelolaan Pajak Daerah
- Objek Pajak yang Disesuaikan NJOP
- Dokumen Keberatan Pajak Daerah
- *Dan 12 dataset agregat lainnya*

### Temuan Penting — Data BPS Pariwisata (Hotel per Desa!)

Dataset `list data Kab Serang - BPS - Pariwisata, Transportasi dan Komunikasi.csv` berisi data **jumlah hotel dan penginapan per desa** untuk seluruh Kab. Serang.

**Kecamatan Anyar — Detail Hotel & Penginapan:**

| Desa | Hotel | Penginapan | Menara Telpon | Operator |
|------|-------|-----------|---------------|----------|
| Anyar | 2 | 3 | 5 | 5 |
| Bandulu | **5** | **10** | 1 | 5 |
| Bunihara | **7** | **8** | 0 | 4 |
| Tambang Ayam | 2 | 6 | 2 | 5 |
| Sindang Mandi | 0 | 0 | 1 | 3 |
| Cikoneng | 0 | 0 | 2 | 5 |
| Tanjung Manis | 0 | 0 | 1 | 5 |
| Kosambironyok | 0 | 0 | 2 | 4 |
| Banjarsari | 0 | 0 | 0 | 4 |
| Mekarsari | 0 | 0 | 0 | 4 |
| Sindangkarya | 0 | 0 | 1 | 4 |
| Grogol Indah | 0 | 0 | 2 | 4 |
| **Total** | **16** | **27** | **17** | — |

Dataset ini juga mencakup 29 kecamatan lain — sangat berguna untuk **analisis spasial kesenjangan pajak hotel**.

### Data PDRB Kab. Serang

| Tahun | PDRB Berlaku (Mlyr Rp) | PDRB Konstan (Mlyr Rp) | Pertumbuhan Ekonomi |
|-------|----------------------|----------------------|-------------------|
| 2020 | 76.198 | 53.056 | -1,4% |
| 2021 | 80.464 | 54.993 | 3,65% |
| 2022 | 87.983 | 57.607 | 5,04% |

### Data Desa (Daftar 326 Desa)

Semua 326 desa di Kab. Serang dengan kode Kemendagri, nama kecamatan, dan koordinat (centroid). **12 desa untuk Kec. Anyar** dengan kode `36.04.30.xxxx`.

---

## 2. GISTARU Banten (GIS Tata Ruang)

**URL:** https://gistaru.bantenprov.go.id  
**Pengelola:** Dinas PUPR Provinsi Banten  
**Dataset Tersedia:** 24 dataset, 196 layer, 64 metadata

### Layer Tersedia

| Kategori | Layer | Kegunaan SPASI |
|----------|-------|----------------|
| **RTRW Provinsi** | Pola Ruang, Struktur Ruang, Kawasan Strategis | Zonasi tata ruang untuk lokasi usaha |
| **RTRW Kab. Serang** | RTRW Kabupaten Serang | Batas administratif, peruntukan lahan |
| **Tematik Provinsi** | Bahaya & Risiko, Fisik Lingkungan | Risiko wilayah |
| **LP2B/KP2B** | Lahan Pertanian Pangan Berkelanjutan | Tutupan lahan |
| **Bina Marga** | Kondisi Jalan 2025 | Aksesibilitas usaha |
| **Peta Dasar** | Garis Pantai, **Batas Administrasi** | **Batas desa resmi!** |

### Regulasi Terkait

- **PERDA RTRW Provinsi Banten 2023-2043** (PDF tersedia)
- PERDA Kab. Serang No. 1/2018 tentang Bangunan Gedung
- PERDA Kab. Serang No. 3/2017 tentang Infrastruktur Jalan
- PERDA RTRW Kabupaten tetangga tersedia untuk Lebak, Pandeglang, Tangerang, dll.

### Akses Data Spasial

Melalui peta interaktif di https://gistaru.bantenprov.go.id/map dengan layer:
- Basemap: Citra Satelit, BIG, OSM
- Query layer, filter atribut
- Upload KMZ untuk overlay

> **Catatan:** Belum ditemukan API/service WMS/WFS. Data mungkin perlu diunduh manual dari peta interaktif.

---

## 3. BPS Kabupaten Serang

**URL:** https://serangkab.bps.go.id  
**Platform:** Next.js (client-side rendering)  
**Status:** Memblokir akses programatik (403)

### Publikasi Relevan

| Publikasi | Periode | Katalog | Relevansi |
|-----------|---------|---------|-----------|
| **Kecamatan Anyar Dalam Angka 2024** | 2024 | 1102001.3604200 | **Data desa: penduduk, ekonomi, usaha** |
| Kabupaten Serang Dalam Angka | 2024 | — | Konteks kabupaten |
| PDRB Kecamatan Anyar | — | — | Potensi ekonomi |

Data BPS juga tersedia melalui Open Data Kab. Serang (CKAN) dalam format CSV yang lebih mudah diakses.

### WebAPI BPS

**URL:** https://webapi.bps.go.id  
Untuk akses data BPS nasional dan kabupaten secara terprogram (perlu API key).

---

## 4. Ina-Geoportal BIG (Badan Informasi Geospasial)

**URL:** https://tanahair.indonesia.go.id  
**Platform:** SPA JavaScript  
**Status:** Membutuhkan browser untuk rendering

### Data Tersedia (via portal)

- **Batas Desa & Kecamatan** — data batas wilayah paling resmi
- RBI (Rupa Bumi Indonesia) — peta dasar skala 1:25.000
- Citra satelit resolusi tinggi
- Toponimi (nama tempat)

### Akses

Perlu diakses via browser (Selenium/Playwright). Data SHP/GeoJSON dapat diunduh per wilayah.

---

## 5. Satu Data Banten

**URL:** https://satudata.bantenprov.go.id  
**Status:** Beranda bisa diakses, halaman `/dataset` mengembalikan 404  
**Catatan:** Portal milik Pemerintah Provinsi Banten, terintegrasi dengan Satu Data Indonesia.

---

## 6. Satu Data Kab. Serang

**URL:** https://satudata.serangkab.go.id  
**Status:** Transport error — mungkin site down atau memblokir  
Diduga merupakan portal internal yang tidak bisa diakses publik.

---

## 7. Website Kab. Serang (Dokumen)

**URL:** https://serangkab.go.id  
**Halaman:** `/dokumen` — menyediakan APBD, LKIP, Perbup, Perda  
**Format:** PDF  
**Relevansi:** Data APBD untuk membandingkan target vs realisasi PAD

---

## 8. OpenStreetMap (GeoFabrik / Overpass)

**URL:** https://download.geofabrik.de/asia/indonesia.html  
**Script:** `shared/scripts/fetch_osm.py` (menggunakan Overpass API)

### Data Banten dari OSM

| Kategori | Tag | Kegunaan |
|----------|-----|----------|
| Restoran | `amenity=restaurant` | POI restoran potensial |
| Kafe | `amenity=cafe` | POI kafe |
| Hotel | `tourism=hotel` | POI hotel |
| Supermarket | `shop=supermarket` | Usaha besar |

OSM menyediakan data **titik lokasi** (POI) yang bisa dibandingkan dengan data Pemda untuk analisis kesenjangan.

---

## 9. Portal Data Kota/Kabupaten Lain (Pembanding)

Dari hasil pencarian web, portal open data untuk kota/kabupaten sekitar:

| Portal | URL | Status |
|--------|-----|--------|
| Open Data Kota Serang | *(perlu dicari)* | — |
| Open Data Kota Cilegon | *(perlu dicari)* | — |
| Open Data Kota Tangerang | *(perlu dicari)* | — |
| Open Data Kab. Tangerang | *(perlu dicari)* | — |

---

## Ringkasan & Prioritas

### Data Tersedia (Bisa Langsung Dipakai)

| Prioritas | Data | Sumber | Format | Granularitas |
|-----------|------|--------|--------|-------------|
| **P1** | Hotel & Penginapan per Desa | BPS via CKAN Kab. Serang | CSV | **Desa** ✅ |
| **P1** | Daftar Desa + Koordinat | DPMD via CKAN | CSV | **Desa** ✅ |
| **P2** | PDRB Kab. Serang | CKAN | CSV | Kabupaten |
| **P2** | Demografi per Kecamatan | BPS via CKAN | CSV | Kecamatan |
| **P2** | Batas Administrasi | GISTARU Banten | SHP/GeoJSON | Provinsi/Kab |
| **P3** | RTRW (Pola Ruang) | GISTARU Banten | WebGIS | Kabupaten |
| **P3** | Kec. Anyar Dalam Angka | BPS Website | PDF | Kecamatan |

### Data Perlu Diunduh Manual

| Prioritas | Data | Sumber | Metode |
|-----------|------|--------|--------|
| **P1** | Batas Desa Resmi | Ina-Geoportal BIG | Browser → download SHP |
| **P1** | POI Restoran/Hotel | OpenStreetMap | `fetch_osm.py` (Overpass) |
| **P2** | Podes (Potensi Desa) | BPS Website | Manual download PDF |
| **P3** | Citra Satelit | Ina-Geoportal BIG | Browser |
| **P3** | Kondisi Jalan | GISTARU Banten | Peta interaktif |

### Data Tidak Tersedia (Perlu Survei)

| Data | Alasan | Alternatif |
|------|--------|-----------|
| Omzet restoran per usaha | Data sensitif, tidak dipublikasikan | Survei lapangan / estimasi |
| Omzet hotel per usaha | Data sensitif, tidak dipublikasikan | Survei lapangan / estimasi |
| Jumlah wajib pajak restoran per desa | Data internal BAPENDA | Permohonan informasi publik |
| Realisasi PAD per desa | Tidak dipublikasi sedetail itu | Agregat kabupaten di CKAN |

---

## Lampiran: Query CKAN API

```python
import requests

BASE = "https://opendata.serangkab.go.id/en_AU/api/3/action"

# Cari dataset
r = requests.get(f"{BASE}/package_search", params={
    "q": "pajak", "rows": 10
})

# Detail dataset
r = requests.get(f"{BASE}/package_show", params={
    "id": "pendapatan"
})

# Organisasi
r = requests.get(f"{BASE}/organization_list")

# List dataset per organisasi
r = requests.get(f"{BASE}/package_search", params={
    "fq": "organization:bappeda-serangkab"
})
```

### Catatan Teknis

- Semua dataset ODC-BY/CC-BY bisa digunakan bebas dengan atribusi
- BPS Website (serangkab.bps.go.id) memblokir akses programatik (403) — gunakan CKAN API sebagai alternatif
- GISTARU dan BIG memerlukan browser untuk mengakses peta interaktif
- Data agregat (jumlah dokumen) dari BAPENDA tidak berguna untuk analisis kesenjangan pajak — hanya metadata kegiatan
- **Data paling berharga**: BPS Pariwisata (hotel per desa), Data Desa (koordinat), dan GISTARU (batas administrasi)
