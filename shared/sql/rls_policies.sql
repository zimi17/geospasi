-- RLS Policies untuk GeoSERANG
-- Jalankan di Supabase SQL Editor setelah enable RLS di tabel

-- 1. Tabel restoran_lapangan
CREATE TABLE IF NOT EXISTS restoran_lapangan (
    id SERIAL PRIMARY KEY,
    nama_usaha TEXT,
    pemilik TEXT,
    alamat TEXT,
    desa TEXT,
    kecamatan TEXT DEFAULT 'Anyar',
    npwp TEXT,
    omzet_bulanan NUMERIC,
    kategori TEXT,
    status TEXT,
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    geocode_confidence TEXT,
    omzet_confidence TEXT,
    npwp_valid BOOLEAN,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE restoran_lapangan ENABLE ROW LEVEL SECURITY;

-- Publik bisa SELECT (anon key)
CREATE POLICY select_restoran_publik ON restoran_lapangan
    FOR SELECT
    USING (true);

-- Hanya service role bisa INSERT/UPDATE/DELETE
CREATE POLICY insert_restoran_service ON restoran_lapangan
    FOR INSERT
    WITH CHECK (auth.role() = 'service_role');

CREATE POLICY update_restoran_service ON restoran_lapangan
    FOR UPDATE
    USING (auth.role() = 'service_role');

CREATE POLICY delete_restoran_service ON restoran_lapangan
    FOR DELETE
    USING (auth.role() = 'service_role');

-- 2. View agregat per desa (untuk peta publik)
CREATE OR REPLACE VIEW agregat_pajak_per_desa AS
SELECT
    desa,
    COUNT(*) AS jumlah_restoran,
    COUNT(*) FILTER (WHERE status = 'terdaftar') AS terdaftar,
    COUNT(*) FILTER (WHERE status = 'tidak_terdaftar') AS tidak_terdaftar,
    SUM(omzet_bulanan) AS total_omzet_estimasi,
    AVG(omzet_bulanan) AS rata_omzet
FROM restoran_lapangan
WHERE omzet_bulanan IS NOT NULL
GROUP BY desa;
