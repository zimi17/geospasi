/* SPASI — map.js */

const map = L.map("map").setView([-6.08, 105.93], 14);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; <a href='https://osm.org/copyright'>OSM</a>",
    maxZoom: 18,
}).addTo(map);

// Data agregat dari GitHub RAW CDN (unlimited bandwidth, gratis)
// Update: jalankan .github/workflows/export-agregat.yml
const DATA_URL =
  "https://raw.githubusercontent.com/zimi17/geospasi/main/potensi_pajak_restoran/data/agregat_desa.geojson";

// Fallback inline untuk development offline
const FALLBACK_DATA = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: { desa: "Anyar", jumlah_restoran: 8, terdaftar: 5, tidak_terdaftar: 3, total_omzet: 268000000 },
      geometry: { type: "Polygon", coordinates: [[[105.90,-6.05],[105.93,-6.05],[105.93,-6.08],[105.90,-6.08],[105.90,-6.05]]] }
    },
    {
      type: "Feature",
      properties: { desa: "Karyawan", jumlah_restoran: 4, terdaftar: 2, tidak_terdaftar: 2, total_omzet: 84000000 },
      geometry: { type: "Polygon", coordinates: [[[105.93,-6.05],[105.96,-6.05],[105.96,-6.08],[105.93,-6.08],[105.93,-6.05]]] }
    },
    {
      type: "Feature",
      properties: { desa: "Tambang Ayam", jumlah_restoran: 4, terdaftar: 3, tidak_terdaftar: 1, total_omzet: 193000000 },
      geometry: { type: "Polygon", coordinates: [[[105.90,-6.08],[105.93,-6.08],[105.93,-6.11],[105.90,-6.11],[105.90,-6.08]]] }
    },
    {
      type: "Feature",
      properties: { desa: "Cimanuk", jumlah_restoran: 4, terdaftar: 0, tidak_terdaftar: 4, total_omzet: 24500000 },
      geometry: { type: "Polygon", coordinates: [[[105.93,-6.08],[105.96,-6.08],[105.96,-6.11],[105.93,-6.11],[105.93,-6.08]]] }
    }
  ]
};

function getColor(omzet) {
  return omzet > 200000000 ? "#c0392b"
       : omzet > 100000000 ? "#e67e22"
       : omzet > 50000000  ? "#f1c40f"
       : "#27ae60";
}

function style(feature) {
  return {
    fillColor: getColor(feature.properties.total_omzet),
    weight: 2,
    opacity: 1,
    color: "white",
    fillOpacity: 0.7,
  };
}

function onEachFeature(feature, layer) {
  const p = feature.properties;
  layer.bindPopup(`
    <strong>${p.desa}</strong><br>
    Restoran: ${p.jumlah_restoran}<br>
    Terdaftar: ${p.terdaftar}<br>
    Belum terdaftar: <strong>${p.tidak_terdaftar}</strong><br>
    Estimasi omzet: Rp ${p.total_omzet.toLocaleString("id-ID")}
  `);
}

function render(data) {
  L.geoJson(data, { style, onEachFeature }).addTo(map);
  document.getElementById("summary").innerText =
    `${data.features.length} desa, terakhir diperbarui dari data lapangan.`;
}

// Ambil dari GitHub RAW, fallback ke inline
fetch(DATA_URL)
  .then(r => {
    if (!r.ok) throw new Error("Gagal fetch");
    return r.json();
  })
  .then(render)
  .catch(() => {
    console.warn("Gagal fetch dari GitHub RAW, pakai data fallback lokal");
    render(FALLBACK_DATA);
  });

// Legenda
const legend = L.control({ position: "bottomright" });
legend.onAdd = function () {
  const div = L.DomUtil.create("div", "info legend");
  const grades = [0, 25000000, 50000000, 100000000, 200000000];
  const labels = ["<b>Estimasi Omzet</b>"];
  for (let i = 0; i < grades.length; i++) {
    const from = grades[i];
    const to = grades[i + 1];
    labels.push(
      `<i style="background:${getColor(from + 1)};width:12px;height:12px;display:inline-block;margin-right:4px;"></i> ` +
      `Rp ${from.toLocaleString("id-ID")}${to ? " – Rp " + to.toLocaleString("id-ID") : "+"}`
    );
  }
  div.innerHTML = labels.join("<br>");
  return div;
};
legend.addTo(map);
