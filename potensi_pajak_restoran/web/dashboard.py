"""
dashboard.py — Streamlit Dashboard SPASI

Menampilkan peta interaktif agregat pajak per desa
dengan filter, statistik, dan tabel data.

Penggunaan:
    streamlit run potensi_pajak_restoran/web/dashboard.py
"""

import os
import json
import urllib.request

import streamlit as st
import folium
from streamlit_folium import st_folium
from branca.colormap import LinearColormap

st.set_page_config(page_title="SPASI — Dashboard", layout="wide")

GEOJSON_URL = (
    "https://raw.githubusercontent.com/zimi17/geospasi/main/"
    "potensi_pajak_restoran/data/agregat_desa.geojson"
)

GEOJSON_LOCAL = os.path.join(
    os.path.dirname(__file__), "..", "data", "agregat_desa.geojson"
)


@st.cache_data
def load_data():
    try:
        with urllib.request.urlopen(GEOJSON_URL) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        with open(GEOJSON_LOCAL) as f:
            return json.load(f)


data = load_data()
features = data["features"]
props_list = [f["properties"] for f in features]

desa_names = [p["desa"] for p in props_list]
total_restoran = sum(p.get("jumlah_restoran", 0) for p in props_list)
total_terdaftar = sum(p.get("terdaftar", 0) for p in props_list)
total_tidak = sum(p.get("tidak_terdaftar", 0) for p in props_list)
total_omzet = sum(p.get("total_omzet", 0) for p in props_list)
rata_omzet = total_omzet / len(props_list) if props_list else 0

st.title("SPASI — Dashboard Analisis Pajak Restoran")
st.caption("Kecamatan Anyar, Kabupaten Serang | Data Sintetis — Fase Pilot")

# ---- Sidebar Filters ----
st.sidebar.header("Filter")
selected_desa = st.sidebar.multiselect("Desa", desa_names, default=desa_names)
min_omzet = st.sidebar.slider("Min. Total Omzet (Rp)", 0, int(total_omzet), 0, step=1_000_000)

filtered = [
    f for f in features
    if f["properties"]["desa"] in selected_desa
    and f["properties"].get("total_omzet", 0) >= min_omzet
]

# ---- Summary ----
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Desa", len(filtered))
col2.metric("Restoran", sum(p.get("jumlah_restoran", 0) for p in [f["properties"] for f in filtered]))
col3.metric("Terdaftar", sum(p.get("terdaftar", 0) for p in [f["properties"] for f in filtered]))
col4.metric("Total Omzet", f"Rp {sum(p.get('total_omzet', 0) for p in [f['properties'] for f in filtered]):,.0f}")
col5.metric("Rata-rata/Desa", f"Rp {rata_omzet:,.0f}")

# ---- Map ----
m = folium.Map(location=[-6.08, 105.93], zoom_start=13, tiles="OpenStreetMap")

cmap = LinearColormap(
    colors=["green", "yellow", "orange", "red"],
    vmin=0,
    vmax=max(p.get("total_omzet", 0) for p in props_list) or 1,
    caption="Total Omzet (Rp)",
)

for f in filtered:
    p = f["properties"]
    folium.GeoJson(
        f,
        style_function=lambda x, omzet=p["total_omzet"]: {
            "fillColor": cmap(omzet),
            "color": "white",
            "weight": 1,
            "fillOpacity": 0.7,
        },
        tooltip=f"{p['desa']} — {p.get('jumlah_restoran', 0)} restoran",
        popup=folium.Popup(
            f"<b>{p['desa']}</b><br>"
            f"Restoran: {p.get('jumlah_restoran', 0)}<br>"
            f"Terdaftar: {p.get('terdaftar', 0)}<br>"
            f"Tidak Terdaftar: {p.get('tidak_terdaftar', 0)}<br>"
            f"Total Omzet: Rp {p.get('total_omzet', 0):,.0f}<br>"
            f"Rata-rata: Rp {p.get('rata_omzet', 0):,.0f}",
            max_width=300,
        ),
    ).add_to(m)

cmap.add_to(m)
st_folium(m, height=500, width=None, key="map")

# ---- Data Table ----
st.subheader("Data Per Desa")
rows = []
for f in filtered:
    p = f["properties"]
    rows.append({
        "Desa": p["desa"],
        "Restoran": p.get("jumlah_restoran", 0),
        "Terdaftar": p.get("terdaftar", 0),
        "Tidak Terdaftar": p.get("tidak_terdaftar", 0),
        "Total Omzet": p.get("total_omzet", 0),
        "Rata-rata Omzet": p.get("rata_omzet", 0),
    })
st.dataframe(rows, column_config={
    "Total Omzet": st.column_config.NumberColumn(format="Rp %d"),
    "Rata-rata Omzet": st.column_config.NumberColumn(format="Rp %d"),
}, use_container_width=True)
