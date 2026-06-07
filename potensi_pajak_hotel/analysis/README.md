# Analisis Pajak Hotel — Kec. Anyar

## Data
- `hotel_sintetis.csv`: 8 hotel sintetis (6 terdaftar, 2 tidak terdaftar)
- Sumber data real: Dinas Pariwisata / Bapenda Kab. Serang

## Metode
1. **Okupansi vs Target** — Bandingkan okupansi aktual dengan proyeksi Bapenda
2. **Estimasi Omzet** — `jumlah_kamar × tarif_rata × okupansi_persen × 30`
3. **Kesenjangan** — `target_pad - omzet_estimasi`

## Output
- Peta sebaran hotel (terdaftar vs tidak terdaftar)
- Tabel kesenjangan per desa
