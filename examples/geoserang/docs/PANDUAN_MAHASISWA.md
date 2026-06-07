# 📘 SPASI — Panduan Mahasiswa: Mulai Skripsi dalam 7 Hari

## Apa itu SPASI?

SPASI (**S**istem **P**emetaan **A**nalisis **S**pasial **I**nformasi) adalah platform riset terbuka untuk analisis data spasial-ekonomi.

Kamu bisa membuat skripsi tentang:
- Pemetaan potensi pajak restoran/hotel
- Analisis kesenjangan PAD (Pendapatan Asli Daerah)
- Pola spasial usaha mikro di kecamatan
- Dan topik geospasial-ekonomi lainnya

## Yang Kamu Butuhkan

| Item | Keterangan |
|------|-----------|
| Laptop | Minimal RAM 4GB (kebanyakan laptop kampus cukup) |
| QGIS 3.28+ | Gratis, download di qgis.org |
| Python 3.10+ | Sudah terinstall di大部分 laptop |
| Akun GitHub | Gratis, daftar di github.com |
| Akun Supabase | Gratis, daftar di supabase.com |
| Semangat riset | Yang ini wajib ✅ |

## Langkah 7 Hari

### Hari 1: Clone & Coba
```bash
git clone https://github.com/zimi17/geospasi.git
cd spasi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Hari 2: Setup Database (30 menit)
1. Buka supabase.com → New project
2. Beri nama, simpan password database
3. Di SQL Editor, jalankan: `CREATE EXTENSION postgis;`
4. Copy-paste isi `shared/sql/rls_policies.sql` → Run
5. Salin `Connection String` dari Project Settings → Database
6. Isi ke `.env` (copy dari `.env.example`)

### Hari 3: Jalankan ETL
```bash
python potensi_pajak_restoran/etl/ingest_restoran.py \
  --csv potensi_pajak_restoran/data/restoran_anyar.csv \
  --dry-run
```
Kalau muncul tabel tanpa error, hapus `--dry-run` dan jalankan lagi.

### Hari 4: Buka QGIS
1. Buka QGIS
2. Tambah koneksi PostgreSQL: klik kanan PostgreSQL → New Connection
3. Isi credentials dari Supabase
4. Buka Processing → Models → Open → pilih `analysis/deteksi_kesenjangan.model3`
5. Klik Run

### Hari 5: Analisis & Interpretasi
- Lihat hasil spatial join: restoran mana yang di desa mana
- Lihat gap antara potensi dan realisasi
- Catat temuan untuk Bab 4 skripsimu

### Hari 6: Visualisasi Web
- Buka `potensi_pajak_restoran/web/index.html` di browser
- Atau lihat live di: https://zimi17.github.io/geospasi/

### Hari 7: Dokumentasi
- Catat semua langkah dan hasil
- Screenshoot peta untuk skripsi
- Tulis metodologi di Bab 3

## Struktur Folder untuk Skripsi

```
spasi/
├── potensi_pajak_restoran/   ← FOKUS DI SINI
│   ├── data/                 ← Data mentah & hasil olahan
│   ├── etl/                  ← Script ETL
│   ├── analysis/             ← Model QGIS
│   └── web/                  ← Peta publik
└── shared/                   ← Komponen bantuan
```

## Tips

- **Mulai dari data sintetis** dulu, ganti ke data asli setelah paham alurnya
- **Screenshot setiap layer QGIS** untuk dokumentasi skripsi
- **Tanya dosbing** kalau ada istilah teknis yang asing
- **Buat issue di GitHub** kalau nemu bug

## Kontak

Buka issue di https://github.com/zimi17/geospasi/issues

---

*SPASI dikembangkan oleh STIE Dwimulya untuk riset geospasial-ekonomi daerah.*
