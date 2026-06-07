/* SPASI — map.js */

const map = L.map("map").setView([-6.08, 105.93], 14);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; <a href='https://osm.org/copyright'>OSM</a>",
    maxZoom: 18,
}).addTo(map);

// Sample data (GeoJSON inline — dalam produksi ambil dari Supabase)
const desaSamples = {
    type: "FeatureCollection",
    features: [
        {
            type: "Feature",
            properties: { desa: "Anyar", jumlah: 8, estimasi_potensi: 268000000, terdaftar: 5, tidak_terdaftar: 3 },
            geometry: { type: "Polygon", coordinates: [[[105.90,-6.05],[105.93,-6.05],[105.93,-6.08],[105.90,-6.08],[105.90,-6.05]]] }
        },
        {
            type: "Feature",
            properties: { desa: "Karyawan", jumlah: 4, estimasi_potensi: 84000000, terdaftar: 2, tidak_terdaftar: 2 },
            geometry: { type: "Polygon", coordinates: [[[105.93,-6.05],[105.96,-6.05],[105.96,-6.08],[105.93,-6.08],[105.93,-6.05]]] }
        },
        {
            type: "Feature",
            properties: { desa: "Tambang Ayam", jumlah: 4, estimasi_potensi: 193000000, terdaftar: 3, tidak_terdaftar: 1 },
            geometry: { type: "Polygon", coordinates: [[[105.90,-6.08],[105.93,-6.08],[105.93,-6.11],[105.90,-6.11],[105.90,-6.08]]] }
        },
        {
            type: "Feature",
            properties: { desa: "Cimanuk", jumlah: 4, estimasi_potensi: 24500000, terdaftar: 0, tidak_terdaftar: 4 },
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
        fillColor: getColor(feature.properties.estimasi_potensi),
        weight: 2,
        opacity: 1,
        color: "white",
        fillOpacity: 0.7,
    };
}

function onEachFeature(feature, layer) {
    const p = feature.properties;
    const gapBanyak = p.tidak_terdaftar;
    layer.bindPopup(`
        <strong>${p.desa}</strong><br>
        Restoran: ${p.jumlah}<br>
        Terdaftar: ${p.terdaftar}<br>
        Belum terdaftar: <strong>${p.tidak_terdaftar}</strong><br>
        Estimasi potensi: Rp ${p.estimasi_potensi.toLocaleString("id-ID")}
    `);
}

L.geoJson(desaSamples, { style, onEachFeature }).addTo(map);

document.getElementById("summary").innerText = "4 desa, 20 restoran.";

// Legenda
const legend = L.control({ position: "bottomright" });
legend.onAdd = function () {
    const div = L.DomUtil.create("div", "info legend");
    const grades = [0, 25000000, 50000000, 100000000, 200000000];
    const labels = ["<b>Estimasi Potensi</b>"];
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
