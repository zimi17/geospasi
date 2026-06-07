# Codex untuk Open Source Preparation — Geospasi

Dokumen ini menjelaskan kesiapan Geospasi sebagai proyek open
source publik, ditujukan untuk review internal dan potential sponsor.

---

## 1. Role Maintainer

| Aspek | Detail |
|---|---|
| **Maintainer** | @zimi17 (arsyad azimi) |
| **Afiliasi** | Independen / akademisi |
| **Motivasi** | Open data geospasial untuk perencanaan daerah |
| **Komitmen** | Update minimal 1x minggu (issue triage, PR review, rilis) |
| **Risiko** | Single point of failure — perlu吸引 kontributor aktif |

**Mitigasi:** Dokumentasi kontribusi lengkap, good first issues
tertandai, issue template memandu pelapor.

---

## 2. Why Repository Qualifies

- **100% open source** — ISC license, tanpa dependency proprietary
- **Reproducible** — static files, no build step required
- **Portable** — bisa jalan dari file:// hingga GitHub Pages
- **Self-contained** — semua data GeoJSON dalam repo (kecuali raw 1.2GB di .gitignore)
- **Minimal stack** — pure HTML/CSS/JS + Python ETL (opsional)
- **Real use case** — GeoSERANG adalah implementasi konkret untuk Kab. Serang
- **Bahasa Indonesia** — memberdayakan akademisi lokal non-Inggris

---

## 3. Planned API Credits Usage

| Layanan | Tujuan | Estimasi Biaya | Sumber |
|---|---|---|---|
| GitHub Actions | CI/CD deploy | Gratis (2000 min/bulan) | GitHub Free |
| GitHub Pages | Hosting | Gratis (1GB) | GitHub Free |
| GitHub RAW CDN | GeoJSON delivery | Gratis | GitHub Free |
| Supabase REST API | Query data (masa depan) | Gratis tier | Supabase Free |
| MapTiler/MapLibre | Tile render | Gratis (self-hosted) | Open source |

**Komitmen:** Tidak akan ada layanan berbayar untuk fungsi inti.
Semua fitur harus berjalan dengan biaya \$0.

---

## 4. Public Benefit

- **Pemerintah daerah** — visualisasi RTRW tanpa GIS berbayar
- **Akademisi** — data geospasial siap pakai untuk penelitian
- **Mahasiswa** — belajar GIS dengan dataset nyata dan aplikasi terbuka
- **Masyarakat sipil** — transparansi tata ruang dan risiko bencana
- **Developer** — referensi implementasi MapLibre + GeoJSON statis

**Dampak langsung:** Satu portal bisa menghemat ±Rp 50-200 juta
biaya lisensi GIS per tahun per daerah.

---

## 5. Maintenance Workflow

### Mingguan
- Triage issue baru (label, priority, assign)
- Review open PR
- Cek GitHub Actions health

### Bulanan
- Rilis minor (fitur baru small)
- Update sample data jika ada
- Audit ukuran repository

### Per Kuartal
- Rilis mayor (fitur baru besar, breaking changes jika perlu)
- Audit dependency keamanan
- Evaluasi roadmap

### Ad-hoc
- Security issue: response <24 jam
- Bug kritis: fix dalam 1 minggu
- Dataset request: validasi sumber, tambah jika open

---

## 6. Release Strategy

| Versi | Target | Isi |
|---|---|---|
| v0.1 (current) | Stabilisasi | Struktur repo, CI/CD, dokumentasi, hardening |
| v0.2 | Fitur inti | File upload, opacity control, layer reorder |
| v0.3 | Ekosistem | Contoh daerah baru, API query, PMTiles |
| v1.0 | GA | Feature complete, aksesibilitas AAA, i18n |

---

## 7. Kontribusi

Lihat `CONTRIBUTING.md` untuk panduan detail.

**Prasyarat minimal kontributor:**
- Bisa menjalankan Python 3.13+
- Bisa menggunakan git
- Memahami GitHub Flow (fork → branch → PR)

**Tidak diperlukan:**
- Framework JavaScript (React/Vue)
- DevOps / Docker
- Kartu kredit
- Izin atasan
