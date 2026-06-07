# Demo Checklist — Geospasi

Gunakan checklist ini untuk memverifikasi aplikasi Geospasi (atau
turunan seperti GeoSERANG) sebelum rilis.

## Persyaratan Dasar

- [ ] `app/index.html` terbuka tanpa error di Chrome/Firefox/Safari
- [ ] Tidak ada 404 untuk file statis (CSS, JS, GeoJSON, font)
- [ ] Mapbox GL / MapLibre inisialisasi tanpa error console
- [ ] Dark theme diterapkan konsisten
- [ ] Skip-link navigasi keyboard berfungsi

## Layer Dasar

- [ ] Minimal satu layer dasar (peta dasar) muncul saat app dimuat
- [ ] Base map dapat diganti (misal: OpenStreetMap, Satellite, Dark)
- [ ] Layer dasar tidak overlap dengan layer lain secara visual

## Lensa (Layer Groups)

- [ ] Tombol lensa muncul sesuai konfigurasi `LENSA`
- [ ] Klik lensa → layer muncul di peta
- [ ] Klik lensa lagi → layer hilang (toggle)
- [ ] Banyak lensa bisa aktif bersamaan (checkbox behavior)
- [ ] Tidak ada konflik render antar lensa yang aktif bersamaan

## Legend

- [ ] Legend muncul saat minimal satu lensa aktif
- [ ] Legend menampilkan semua lensa yang aktif beserta warnanya
- [ ] Legend hilang saat semua lensa non-aktif

## Custom GeoJSON Overlay

- [ ] Input URL tersedia di panel "Layer Kustom"
- [ ] URL GeoJSON valid → layer termuat di peta
- [ ] Checkbox toggle pada custom layer berfungsi
- [ ] Color picker mengubah warna custom layer
- [ ] Opacity slider mengubah transparansi
- [ ] Tombol zoom-to-layer (🔍) bekerja
- [ ] Tombol hapus (✕) menghapus layer
- [ ] URL GeoJSON invalid → pesan error (bukan crash)
- [ ] URL timeout → pesan error
- [ ] File >50MB ditolak dengan pesan jelas
- [ ] File >50.000 fitur ditolak
- [ ] Non-GeoJSON (HTML, XML) ditolak dengan pesan jelas

## URL State (Sharable)

- [ ] URL berubah saat lensa di-toggle
- [ ] URL menyertakan posisi peta (lat, lng, zoom)
- [ ] URL menyertakan data custom layer
- [ ] Buka URL yang disimpan → state peta sama persis
- [ ] Custom layer yang di-share via URL bisa dimuat ulang
- [ ] Tombol "Share" menyalin URL ke clipboard

## Pencarian (Search)

- [ ] Input search muncul di sidebar
- [ ] Mengetik memunculkan saran
- [ ] Pilih saran → peta fly-to lokasi
- [ ] Input kosong atau tidak cocok tidak menyebabkan error

## Mobile / Responsive

- [ ] Sidebar dapat ditutup/dibuka (hamburger menu atau toggle)
- [ ] Sidebar tidak menutupi peta secara permanen di layar sempit
- [ ] Kontrol peta (zoom, kompas) tetap terjangkau di mobile
- [ ] Legend tidak overflow di viewport sempit
- [ ] Tombol lensa tidak tumpang tindih di layar <480px

## Aksesibilitas (WCAG)

- [ ] Semua tombol memiliki `aria-label`
- [ ] Fokus keyboard terlihat (focus-visible)
- [ ] Kontras warna memadai (4.5:1 untuk teks normal)
- [ ] `prefers-reduced-motion` dihormati (animasi diminimalkan)

## Keamanan

- [ ] Custom URL tidak bisa akses `file://` atau `localhost`
- [ ] Custom URL tidak bisa inject script via JSONP
- [ ] Tidak ada eval atau dynamic script injection
- [ ] Hanya protokol HTTPS yang diizinkan untuk custom URL

---

*Last updated: 2026-06-07*
