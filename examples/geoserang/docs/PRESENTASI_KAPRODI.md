# SPASI
## Sistem Pemetaan Analisis Spasial Informasi
### Platform Riset Geospasial-Ekonomi untuk STIE Dwimulya

---

## Slide 1: Masalah

**Skripsi mahasiswa Manajemen & Akuntansi:**
- ❌ Didominasi metode kuantitatif klasik (regresi, SPSS)
- ❌ Data sekunder dari BPS yang sudah publikasi tahun lalu
- ❌ Output: tabel dan angka — sulit divisualisasikan

**Padahal kebutuhan mitra (Pemkab Serang):**
- Analisis spasial pajak & PAD
- Peta potensi ekonomi per desa
- Data real-time, bukan tahun lalu

**Akibat:**
- Skripsi tidak relevan dengan kebutuhan daerah
- Nilai riset rendah, tidak bisa dipakai Pemkab
- Peluang hibah dan publikasi hilang

---

## Slide 2: Solusi — SPASI

**S**istem **P**emetaan **A**nalisis **S**pasial **I**nformasi

Platform riset terbuka yang memungkinkan mahasiswa:
1. **Memetakan** data ekonomi (pajak, PAD, usaha) ke peta digital
2. **Menganalisis** pola spasial dengan QGIS & Python
3. **Mempublikasikan** hasil sebagai peta interaktif di web
4. **Berkontribusi** ke riset yang langsung dipakai Pemkab

**Target pilot:** Kecamatan Anyar, Kabupaten Serang

---

## Slide 3: Kenapa SPASI Berbeda?

| Aspek | Skripsi Biasa | Skripsi + SPASI |
|-------|--------------|-----------------|
| Data | BPS tahun lalu | Data lapangan real + OpenStreetMap |
| Alat | SPSS / Excel | QGIS + Python (open source) |
| Output | Tabel + PDF | Tabel + Peta interaktif + Web |
| Relevansi | Teoritis | Langsung untuk kebijakan daerah |
| Skill baru | — | GIS, Python, geospasial analytics |

**Mahasiswa lulus dengan portfolio, bukan cuma nilai.**

---

## Slide 4: Tech Stack — Ringan, Gratis, Tanpa Docker

| Komponen | Tools | Biaya |
|----------|-------|-------|
| Database | Supabase (PostGIS) | Gratis 500MB |
| Analisis | QGIS 3.28+ | Gratis |
| ETL | Python + GeoPandas | Gratis |
| Web | Leaflet.js + GitHub Pages | Gratis |
| Version Control | GitHub | Gratis |

**Berjalan di laptop RAM 4GB** — laptop mahasiswa biasa.

---

## Slide 5: Roadmap 90 Hari

| Fase | Kegiatan | Output |
|------|----------|--------|
| **Minggu 1-2** | Setup infrastruktur, data sintetis | ETL + QGIS model siap |
| **Minggu 3-4** | Input data real 50 restoran Anyar | Dataset valid |
| **Minggu 5-8** | Analisis gap fiskal per desa | Hasil gap, draft laporan |
| **Minggu 9-12** | Publikasi peta cerita + working paper | Storymap live, artikel |

**Target 12 minggu → 1 skripsi pilot + 1 publikasi.**

---

## Slide 6: Manfaat untuk Prodi

**Untuk Manajemen:**
- Topik skripsi: analisis potensi PAD, pemetaan UMKM, rantai pasok
- Hubungan dengan Bappelitbangda & Bapenda

**Untuk Akuntansi:**
- Topik skripsi: audit fiskal spasial, ketaatan pajak per wilayah
- Data real dari Dispenda, bukan simulasi

**Untuk Semua:**
- Opening peluang hibah riset (DRTPM, Kemendikbud)
- Publikasi bersama di Jurnal Ilmiah
- MoU dengan Pemkab Serang

---

## Slide 7: Dukungan yang Dibutuhkan

| Dari Kaprodi | Dukungan |
|-------------|----------|
| Izin | 1-2 mahasiswa pilot dibebaskan mata kuliah tertentu untuk riset lapangan |
| Sosialisasi | Pengenalan SPASI di kelas seminar proposal |
| Kurikulum | Spark: mata kuliah analisis data spasial ekonomi |
| Dana | Hibah internal untuk riset dosen pendamping |

---

## Slide 8: Ukuran Kesuksesan

| Metrik | Target 12 bulan |
|--------|----------------|
| Mahasiswa skripsi berbasis SPASI | 5 mahasiswa |
| Artikel ilmiah terbit | 2 artikel |
| Data Pemkab yang terpetakan | 5 kecamatan |
| MoU aktif dengan Pemkab | 1 MoU |
| Repeat rate (mahasiswa lanjut S2) | Terbangun minat riset spasial |

---

## Slide 9: Mulai dari Mana?

**Sekarang:**
- ✅ Repo GitHub sudah live: https://github.com/zimi17/geospasi
- ✅ Template ETL, database, QGIS model sudah jadi
- ✅ Data sintetis Anyar siap pakai

**Yang perlu:**
- 1-2 mahasiswa pemberani sebagai pilot
- 1 dosen pendamping yang tertarik GIS
- Persetujuan Kaprodi

**Biaya awal: Rp 0** (semua open source & free tier)

---

## Slide 10: Ajakan

**SPASI bukan aplikasi komersial.**
**SPASI adalah ekosistem riset.**

Mahasiswa lulus dengan skripsi yang:
- ✅ Ada peta-nya (bukan cuma tabel)
- ✅ Datanya real (bukan simulasi)
- ✅ Dipakai Pemkab (bukan cuma perpus)
- ✅ Bisa jadi portfolio (GIS analyst)

**"Satu mahasiswa yang lulus dengan SPASI lebih berharga dari seribu fitur yang tidak ada yang pakai."**

### 👉 Bersedia jadi prodi percontohan?

---

## Lampiran: Link Penting

- Repo GitHub: https://github.com/zimi17/geospasi
- Panduan Mahasiswa: `docs/PANDUAN_MAHASISWA.md`
- Dokumentasi teknis: `docs/adr/ADR-001.md`
- Contoh peta web: (https://zimi17.github.io/geospasi/ — setelah Actions selesai)

**Kontak:** [Nama] — [Email/HP]
