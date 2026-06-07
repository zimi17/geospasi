# Good First Issues

Issues berikut cocok untuk kontributor baru. Setiap item mencakup
estimasi effort, skill yang dibutuhkan, dan panduan memulai.

---

## 1. Improve Sample Datasets

**Effort:** Small (1-3 jam)  
**Skill:** Python, GeoJSON  
**Area:** `app/sample-data/`

Saat ini sample dataset hanya berisi 2 file sederhana. Tambahkan
variasi: polygon kompleks, multi-geometry, dataset dengan properties
bervariasi.

**Cara memulai:**
1. Baca `app/js/config.sample.js` untuk melihat struktur konfigurasi
2. Buat GeoJSON baru di `app/sample-data/`
3. Pastikan valid: `python3 -c "import json; json.load(open('file.geojson'))"`
4. Update `config.sample.js` jika perlu

---

## 2. Add New Example Region

**Effort:** Medium (3-8 jam)  
**Skill:** Python, data pipeline, GitHub Actions  
**Area:** `examples/`

Buat direktori `examples/kabupaten-bogor/` (atau daerah pilihan Anda)
dengan config dan dataset sendiri. Gunakan `examples/geoserang/`
sebagai referensi.

**Cara memulai:**
1. Copy struktur `examples/geoserang/`
2. Cari open data geospasial daerah di portal masing-masing
3. Jalankan `scripts/simplify_web.py` untuk optimasi
4. Update `.github/workflows/deploy-spasi-web.yml` jika perlu
5. Dokumentasikan di `examples/{nama-daerah}/README.md`

---

## 3. Improve Mobile Sidebar

**Effort:** Medium (3-6 jam)  
**Skill:** CSS, HTML, JavaScript  
**Area:** `app/css/style.css`, `app/index.html`, `app/js/app.js`

Sidebar saat ini bisa ditutup/dibuka tapi belum optimal di layar
sangat sempit (<360px). Beberapa peningkatan:

- Tombol lensa perlu scrolling horizontal jika terlalu banyak
- Legend jangan overflow
- Custom panel perlu ukuran yang proporsional

**Cara memulai:**
1. Buka Chrome DevTools → Device Toolbar → pilih iPhone SE (320px)
2. Identifikasi element yang rusak
3. Perbaiki di CSS dengan `@media (max-width: 480px)`
4. Test di beberapa ukuran layar

---

## 4. Add GeoJSON Validation Tests

**Effort:** Small (2-4 jam)  
**Skill:** Python, pytest  
**Area:** `scripts/`

Buat test untuk validasi GeoJSON yang digunakan:
- Struktur `FeatureCollection` valid
- Koordinat dalam range EPSG:4326
- Tidak ada properti sensitive
- File tidak corrupt

**Cara memulai:**
1. Baca `scripts/simplify_web.py` untuk memahami pipeline
2. Buat `scripts/test_geojson_validator.py`
3. Jalankan dengan `python3 -m pytest scripts/test_*.py`

---

## 5. Optimize Large GeoJSON Files

**Effort:** Medium (4-8 jam)  
**Skill:** Python, geospatial data  
**Area:** `examples/geoserang/data/`

Beberapa file GeoJSON di GeoSERANG >20MB. File ini bisa dioptimasi:
- Simplifikasi koordinat (tolerance lebih agresif)
- Filter properti yang tidak digunakan
- Split dataset besar menjadi beberapa file tematik

**Cara memulai:**
1. Jalankan `python3 scripts/report_geojson_size.py`
2. Pilih file kandidat (prioritas >20MB)
3. Baca `scripts/simplify_web.py` untuk opsi optimasi
4. Simplify dengan tolerance lebih tinggi, lalu bandingkan ukuran

---

## 6. Translate Documentation to English

**Effort:** Small (2-3 jam)  
**Skill:** Writing, English  
**Area:** `docs/`, `README.md`, `CONTRIBUTING.md`

Dokumentasi saat ini dalam Bahasa Indonesia. Agar proyek bisa
menjangkau audiens global, buat terjemahan Bahasa Inggris.

**Cara memulai:**
1. Copy `README.md` → `README.en.md`
2. Terjemahkan konten (pertahankan struktur markdown)
3. Update `CONTRIBUTING.md` dengan informasi lokasi file
4. Update `README.md` untuk menambahkan link ke versi Inggris

---

## 7. Add Accessibility Audit

**Effort:** Small (2-4 jam)  
**Skill:** WCAG, aXe, Lighthouse  
**Area:** `docs/`

Lakukan audit aksesibilitas menggunakan Lighthouse atau aXe,
kemudian dokumentasikan temuan dan rekomendasi.

**Cara memulai:**
1. Buka aplikasi di Chrome
2. DevTools → Lighthouse → Accessibility
3. Catat semua isu yang ditemukan
4. Buat `docs/accessibility-report.md`
5. Perbaiki isu yang mudah (prioritas: kritis → serius → sedang)

---

## 8. Add Dark Mode Toggle

**Effort:** Small (1-2 jam)  
**Skill:** CSS, JavaScript  
**Area:** `app/css/style.css`, `app/js/app.js`

Selain mengikuti preferensi sistem (`prefers-color-scheme`),
tambahkan toggle manual untuk dark/light mode.

**Cara memulai:**
1. Baca implementasi dark theme saat ini di `style.css`
2. Tambahkan CSS variables untuk light theme
3. Tambahkan toggle button di sidebar
4. Simpan preferensi ke `localStorage`

---

## 9. Display Layer Attribute Table

**Effort:** Medium (4-8 jam)  
**Skill:** JavaScript, MapLibre  
**Area:** `app/js/app.js`

Tambahkan panel yang menampilkan tabel atribut (properties) dari
layer aktif — mirip spreadsheet.

**Cara memulai:**
1. Baca `app/js/app.js` — pahami struktur data layer
2. Buat fungsi `buildAttributeTable(layerId)` yang query fitur
3. Tampilkan di panel baru atau modal
4. Tambahkan sorting dan filter sederhana

---

## 10. Create a New Lens Configuration

**Effort:** Small (1-3 jam)  
**Skill:** JSON/JavaScript  
**Area:** Konfigurasi lensa

Buat lensa baru menggunakan data yang sudah ada di repository.
Misal: lensa "Lingkungan" yang menggabungkan layer tutupan lahan,
DAS, dan kawasan hutan.

**Cara memulai:**
1. Baca `examples/geoserang/config.js` — pahami struktur `LENSA`
2. Identifikasi layer apa yang relevan dengan tema
3. Tambahkan entry baru di `LENSA`
4. Pastikan legend muncul dengan benar
