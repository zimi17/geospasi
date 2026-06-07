export const LENSA = {
  dasar: {
    id: 'dasar',
    label: 'Dasar',
    icon: '🗺',
    color: '#94a3b8',
    layers: [
      { id: 'batas-desa', file: 'data/Batas_Kelurahan_Desa.geojson', type: 'line', paint: { 'line-color': '#64748b', 'line-width': 1 }, popup: ['nama','kecamatan'] },
      { id: 'batas-kecamatan', file: 'data/Batas_Kecamatan.geojson', type: 'line', paint: { 'line-color': '#475569', 'line-width': 2 }, popup: ['nama'] },
      { id: 'batas-kabupaten', file: 'data/Batas_Kabupaten_Kota.geojson', type: 'line', paint: { 'line-color': '#1e293b', 'line-width': 3 }, popup: ['nama'] },
    ]
  },
  'tata-ruang': {
    id: 'tata-ruang',
    label: 'Tata Ruang',
    icon: '🏗',
    color: '#22c55e',
    layers: [
      { id: 'pola-ruang', file: 'data/Pola_Ruang_Kabupaten_Serang.geojson', type: 'fill', paint: { 'fill-opacity': 0.5, 'fill-color': ['match', ['get', 'fungsi'], ['Lindung'], '#16a34a', ['Budidaya'], '#eab308', '#64748b'] }, popup: ['nama','fungsi'] },
      { id: 'pola-ruang-outline', file: 'data/Pola_Ruang_Kabupaten_Serang.geojson', type: 'line', paint: { 'line-color': '#166534', 'line-width': 0.5 }, popup: [] },
      { id: 'pariwisata', file: 'data/Rencana_Kawasan_Pariwisata.geojson', type: 'fill', paint: { 'fill-color': '#ec4899', 'fill-opacity': 0.4 }, popup: ['nama'] },
      { id: 'kawasan-hutan', file: 'data/Kawasan_Hutan_SK.geojson', type: 'fill', paint: { 'fill-color': '#15803d', 'fill-opacity': 0.4 }, popup: ['nama'] },
    ]
  },
  risiko: {
    id: 'risiko',
    label: 'Risiko',
    icon: '⚠',
    color: '#ef4444',
    layers: [
      { id: 'banjir', file: 'data/BAHAYA_BANJIR.geojson', type: 'fill', paint: { 'fill-opacity': 0.5, 'fill-color': ['match', ['get', 'tingkat'], ['Tinggi'], '#dc2626', ['Sedang'], '#f97316', ['Rendah'], '#fde047', '#64748b'] }, popup: ['tingkat'] },
      { id: 'banjir-bandang', file: 'data/BAHAYA_BANJIR_BANDANG.geojson', type: 'fill', paint: { 'fill-opacity': 0.5, 'fill-color': ['match', ['get', 'tingkat'], ['Tinggi'], '#dc2626', ['Sedang'], '#f97316', ['Rendah'], '#fde047', '#64748b'] }, popup: ['tingkat'] },
      { id: 'tanah-longsor', file: 'data/Bahaya_Tanah_Longsor.geojson', type: 'fill', paint: { 'fill-opacity': 0.5, 'fill-color': ['match', ['get', 'tingkat'], ['Tinggi'], '#dc2626', ['Sedang'], '#f97316', ['Rendah'], '#fde047', '#64748b'] }, popup: ['tingkat'] },
      { id: 'gempa', file: 'data/BAHAYA_GEMPA_BUMI.geojson', type: 'fill', paint: { 'fill-opacity': 0.4, 'fill-color': ['match', ['get', 'tingkat'], ['Tinggi'], '#dc2626', ['Sedang'], '#f97316', ['Rendah'], '#fde047', '#64748b'] }, popup: ['tingkat'] },
      { id: 'tsunami', file: 'data/Bahaya_Tsunami.geojson', type: 'fill', paint: { 'fill-opacity': 0.4, 'fill-color': ['match', ['get', 'tingkat'], ['Tinggi'], '#dc2626', ['Sedang'], '#f97316', ['Rendah'], '#fde047', '#64748b'] }, popup: ['tingkat'] },
      { id: 'lokasi-banjir', file: 'data/Lokasi_Banjir_2022.geojson', type: 'circle', paint: { 'circle-color': '#dc2626', 'circle-radius': 6, 'circle-opacity': 0.8 }, popup: ['kecamatan','desa'] },
      { id: 'rawan-bencana', file: 'data/Daerah_Rawan_Bencana.geojson', type: 'fill', paint: { 'fill-opacity': 0.3, 'fill-color': '#dc2626' }, popup: ['jenis','tingkat'] },
      { id: 'kebakaran', file: 'data/Bahaya_Kebakaran_Hutan.geojson', type: 'fill', paint: { 'fill-opacity': 0.4, 'fill-color': ['match', ['get', 'tingkat'], ['Tinggi'], '#dc2626', ['Sedang'], '#f97316', ['Rendah'], '#fde047', '#64748b'] }, popup: ['tingkat'] },
    ]
  },
  infra: {
    id: 'infra',
    label: 'Infrastruktur',
    icon: '🛣',
    color: '#f59e0b',
    layers: [
      { id: 'jalan-kab', file: 'data/Jalan_Kabupaten_Serang.geojson', type: 'line', paint: { 'line-color': '#f59e0b', 'line-width': 2 }, popup: ['nama','kondisi'] },
      { id: 'jalan-prov', file: 'data/Jalan_Provinsi_Banten.geojson', type: 'line', paint: { 'line-color': '#d97706', 'line-width': 2.5 }, popup: ['nama'] },
      { id: 'kondisi-jalan', file: 'data/KONDISI_JALAN_2025.geojson', type: 'line', paint: { 'line-color': ['match', ['get', 'kondisi'], ['Baik'], '#22c55e', ['Sedang'], '#f59e0b', ['Rusak'], '#ef4444', '#94a3b8'], 'line-width': 3 }, popup: ['nama','kondisi'] },
      { id: 'jembatan', file: 'data/JEMBATAN_PROVINSI_BANTEN_2024_UPDATE.geojson', type: 'circle', paint: { 'circle-color': '#f59e0b', 'circle-radius': 5 }, popup: ['nama','kondisi'] },
      { id: 'jaringan-jalan', file: 'data/Rencana_Jaringan_Jalan.geojson', type: 'line', paint: { 'line-color': '#fbbf24', 'line-width': 1.5, 'line-dasharray': [3,2] }, popup: ['nama'] },
    ]
  },
  fisik: {
    id: 'fisik',
    label: 'Fisik',
    icon: '⛰',
    color: '#8b5cf6',
    layers: [
      { id: 'kelerengan', file: 'data/Kelerengan.geojson', type: 'fill', paint: { 'fill-opacity': 0.5, 'fill-color': ['match', ['get', 'kelas'], ['Datar'], '#22c55e', ['Landai'], '#eab308', ['Curam'], '#f97316', ['Sangat Curam'], '#dc2626', '#64748b'] }, popup: ['kelas'] },
      { id: 'penggunaan-lahan', file: 'data/Penggunaan_Lahan.geojson', type: 'fill', paint: { 'fill-opacity': 0.4, 'fill-color': ['match', ['get', 'nama'], ['Hutan'], '#15803d', ['Sawah'], '#eab308', ['Permukiman'], '#a855f7', ['Industri'], '#dc2626', '#64748b'] }, popup: ['nama'] },
      { id: 'das', file: 'data/Daerah_Aliran_Sungai.geojson', type: 'fill', paint: { 'fill-color': '#0ea5e9', 'fill-opacity': 0.3 }, popup: ['nama'] },
      { id: 'kesesuaian-permukiman', file: 'data/Kesesuaian_Lahan_Permukiman.geojson', type: 'fill', paint: { 'fill-opacity': 0.5, 'fill-color': ['match', ['get', 'tingkat'], ['Sesuai'], '#22c55e', ['Kurang Sesuai'], '#eab308', ['Tidak Sesuai'], '#dc2626', '#64748b'] }, popup: ['tingkat'] },
    ]
  }
};

export const LEGENDA = {
  'tata-ruang': [
    { label: 'Kawasan Lindung', color: '#16a34a' },
    { label: 'Kawasan Budidaya', color: '#eab308' },
    { label: 'Kawasan Pariwisata', color: '#ec4899' },
    { label: 'Kawasan Hutan', color: '#15803d' },
  ],
  risiko: [
    { label: 'Tingkat Tinggi', color: '#dc2626' },
    { label: 'Tingkat Sedang', color: '#f97316' },
    { label: 'Tingkat Rendah', color: '#fde047' },
    { label: 'Lokasi Banjir', color: '#dc2626' },
  ],
  infra: [
    { label: 'Jalan Kabupaten', color: '#f59e0b' },
    { label: 'Jalan Provinsi', color: '#d97706' },
    { label: 'Jalan Baik', color: '#22c55e' },
    { label: 'Jalan Rusak', color: '#ef4444' },
    { label: 'Jembatan', color: '#f59e0b' },
  ],
  fisik: [
    { label: 'Datar', color: '#22c55e' },
    { label: 'Landai', color: '#eab308' },
    { label: 'Curam', color: '#f97316' },
    { label: 'Sangat Curam', color: '#dc2626' },
    { label: 'Sawah', color: '#eab308' },
    { label: 'Hutan', color: '#15803d' },
  ],
};
