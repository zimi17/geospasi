# Analisis Potensi Pajak Restoran — Kecamatan Anyar

## Alur Analisis (QGIS Processing Model)

Model `deteksi_kesenjangan.model3` menjalankan langkah-langkah berikut:

### 1. Spatial Join

| Input | Layer |
|-------|-------|
| Titik | `restoran_lapangan` (dari PostGIS) |
| Poligon | `desa_anyar` (dari file atau PostGIS) |
| Operasi | `Join attributes by location (summary)` — hitung jumlah & total omzet per desa |

### 2. Gabung dengan Data Target

- Input: hasil spatial join + tabel `target_pad_desa` (kolom: `desa`, `target_pajak_restoran`)
- Operasi: `Join attributes by field value` — kunci: `desa`

### 3. Hitung Gap

Field kalkulasi:
```
gap_persen = ((target_pajak_restoran - total_omzet_estimasi) / target_pajak_restoran) * 100
```

### 4. Output

- Layer poligon desa dengan atribut: jumlah restoran, total omzet, target PAD, gap %
- Tabel statistik ringkasan

## Parameter Model

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| Target PAD per desa | Dari data Bapenda | Diisi manual atau dari CSV |
| Periode analisis | Bulanan | Bisa disesuaikan |
| Confidence threshold | "low" | Abaikan data dengan confidence "unparseable" |

## Cara Menggunakan

1. Buka QGIS
2. Processing → Models → Open Model → pilih file `.model3`
3. Pastikan koneksi PostGIS aktif (Browser Panel → PostgreSQL)
4. Klik Run, isi parameter jika diminta
5. Hasil akan muncul sebagai layer baru

## Catatan

- Model ini menggunakan data sintetis. Untuk produksi, ganti layer input dengan data asli dari PostGIS.
- Jika ada layer yang tidak ditemukan, periksa nama tabel di PostGIS.
- Gap positif = potensi pajak belum tergarap maksimal.
