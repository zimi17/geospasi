# Working Paper — SPASI: Sistem Pemetaan Analisis Spasial Informasi

## untuk Deteksi Kesenjangan Pajak Daerah

**Penulis:** Tim Riset SPASI  
**Afiliasi:** [Universitas/Nama Institusi]  
**Status:** Draf Awal — Belum Dipublikasikan  
**Tanggal:** Juni 2026

---

## Abstrak

Kesenjangan antara potensi dan realisasi Pendapatan Asli Daerah (PAD) dari sektor pajak restoran dan hotel merupakan masalah klasik di banyak kabupaten/kota di Indonesia. Penelitian ini memperkenalkan **SPASI (Sistem Pemetaan Analisis Spasial Informasi)**, sebuah platform riset sumber terbuka (open-source) yang mengintegrasikan data survei lapangan, citra satelit, dan data OpenStreetMap untuk memetakan kesenjangan pajak secara spasial. Studi kasus dilakukan di Kecamatan Anyar, Kabupaten Serang, Banten.

**Kata Kunci:** pajak daerah, kesenjangan fiskal, sistem informasi geografis, open-source, Indonesia

---

## 1. Pendahuluan

### 1.1 Latar Belakang
Pajak restoran dan hotel menyumbang proporsi signifikan terhadap PAD kabupaten/kota di Indonesia. Namun, banyak wajib pajak potensial yang tidak terdaftar atau under-reporting omzet. Metode konvensional (inspeksi manual) tidak efisien untuk wilayah dengan ribuan titik usaha.

### 1.2 Rumusan Masalah
1. Seberapa besar kesenjangan antara potensi pajak restoran/hotel dengan realisasi PAD di Kecamatan Anyar?
2. Bagaimana pola spasial kesenjangan tersebut?
3. Faktor apa yang berkorelasi dengan tingkat kepatuhan wajib pajak?

### 1.3 Tujuan
1. Membangun platform pemetaan partisipatif untuk inventarisasi usaha
2. Menghitung estimasi kesenjangan pajak berbasis spasial
3. Menyediakan rekomendasi berbasis data untuk ekstensifikasi pajak

---

## 2. Metodologi

### 2.1 Arsitektur Sistem

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Survei Lapangan │ ──> │  ETL Pipeline    │ ──> │  Supabase/PostGIS│
│  (CSV + GPS)     │     │  (Python/pandas) │     │  (Cloud DB)      │
└──────────────────┘     └──────────────────┘     └────────┬─────────┘
                                                            │
                    ┌──────────────────┐                    │
                    │  GitHub RAW CDN  │ <──────────────────┘
                    │  (GeoJSON Publik)│
                    └────────┬─────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                              ▼
    ┌──────────────────┐          ┌──────────────────┐
    │  Leaflet.js Peta  │          │  QGIS Desktop    │
    │  (Frontend Publik)│          │  (Analisis)      │
    └──────────────────┘          └──────────────────┘
```

### 2.2 Alur Analisis
1. **Inventarisasi:** Data lapangan dikumpulkan melalui survei terstruktur
2. **Validasi:** Pengecekan NPWP, parse omzet, deteksi duplikat fuzzy
3. **Geocoding:** Titik koordinat dari GPS atau Nominatim
4. **Spatial Join:** Titik restoran di-overlay dengan batas desa
5. **Gap Analysis:** `gap_persen = (target_pad - omzet_estimasi) / target_pad × 100`
6. **Publikasi:** Data agregat (anonim) dipublikasikan via GitHub RAW CDN

### 2.3 Teknologi
| Komponen | Teknologi | Biaya |
|---|---|---|
| Database | Supabase (PostGIS) | Gratis (500 MB) |
| CDN Data Publik | GitHub RAW | Gratis (unlimited) |
| Frontend | Leaflet.js (static) | Gratis (GitHub Pages) |
| ETL | Python/pandas | Lokal |
| Analisis Spasial | QGIS 3.28+ | Gratis |
| Dashboard | Streamlit | Gratis (Community Cloud) |

---

## 3. Hasil Awal

### 3.1 Statistik Deskriptif
| Indikator | Nilai |
|---|---|
| Jumlah Desa | 4 |
| Total Restoran Terdeteksi | 20 |
| Terdaftar | 11 (55%) |
| Tidak Terdaftar | 9 (45%) |
| Total Omzet Estimasi | Rp 585,5 Juta |
| Rata-rata Omzet/ Restoran | Rp 29,3 Juta |

### 3.2 Temuan Awal
- **45% restoran tidak terdaftar** sebagai wajib pajak daerah
- Desa dengan tingkat kepatuhan tertinggi: Anyar (6/9 terdaftar)
- Desa dengan potensi terbesar: Tambang Ayam (Rp 193 Juta/bulan)
- Sebagian besar restoran tidak terdaftar adalah usaha kecil (warteg, depot)

---

## 4. Diskusi

### 4.1 Implikasi Kebijakan
1. Prioritas ekstensifikasi pada desa dengan gap tinggi
2. Simplifikasi registrasi NPWPD untuk usaha mikro
3. Pemetaan ulang berkala (6 bulan) untuk update data

### 4.2 Keterbatasan
1. Data sintetis (belum validasi lapangan sempurna)
2. Cakupan hanya 1 kecamatan (Anyar)
3. Omzet estimasi (self-report, belum di-cross-check)
4. Geocoding manual (belum automasi penuh)

---

## 5. Rencana Ke Depan

1. **Fase 2 (Q3 2026):** Input data real 50+ restoran, integrasi OSM
2. **Fase 3 (Q4 2026):** Ekspansi ke pajak hotel, dashboard real-time
3. **Fase 4 (Q1 2027):** Scaling ke kecamatan lain di Kab. Serang
4. **Publikasi:** Target submit ke jurnal nasional terakreditasi

---

## Referensi

1. Undang-Undang No. 28 Tahun 2009 tentang Pajak Daerah dan Retribusi Daerah
2. Peraturan Daerah Kab. Serang No. [X] Tahun [Y] tentang Pajak Restoran
3. BPS Kabupaten Serang (2025). Kecamatan Anyar dalam Angka
4. Goodchild, M.F. (2007). Citizens as sensors: the world of volunteered geography
5. OpenStreetMap contributors (2026). Planet dump retrieved from https://planet.osm.org
