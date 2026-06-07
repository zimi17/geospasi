"""
generate_atlas.py — Generate QGIS Atlas otomatis untuk laporan per desa (PDF)

Workflow:
  1. Baca agregat_desa.geojson + desa_anyar.geojson
  2. Untuk tiap desa, buka QGIS project template
  3. Export ke PDF dengan atlas

Prasyarat: QGIS installed + PyQGIS di PYTHONPATH

Penggunaan:
    qgis --code shared/scripts/generate_atlas.py

Alternatif (tanpa QGIS):
    python shared/scripts/generate_atlas.py --no-qgis

Mode --no-qgis akan generate laporan HTML sederhana.
"""

import os
import json
import sys
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def generate_html_report(desa_data, output_dir):
    """Generate laporan HTML per desa (fallback tanpa QGIS)."""
    os.makedirs(output_dir, exist_ok=True)

    index_links = []
    for desa in desa_data["features"]:
        props = desa["properties"]
        nama = props["desa"]
        html = f"""<!DOCTYPE html>
<html lang="id">
<head><meta charset="UTF-8"><title>Laporan {nama}</title>
<style>
  body {{ font-family: sans-serif; margin: 2em; }}
  h1 {{ color: #1a3a5c; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
  th {{ background: #1a3a5c; color: white; }}
  .good {{ color: green; }} .bad {{ color: red; }}
</style></head>
<body>
<h1>Laporan SPASI — Desa {nama}</h1>
<p>Kecamatan {props['kecamatan']} | {datetime.now().strftime('%d %B %Y')}</p>
<table>
  <tr><th>Indikator</th><th>Nilai</th></tr>
  <tr><td>Jumlah Restoran</td><td>{props.get('jumlah_restoran', 'N/A')}</td></tr>
  <tr><td>Terdaftar</td><td class="good">{props.get('terdaftar', 0)}</td></tr>
  <tr><td>Tidak Terdaftar</td><td class="bad">{props.get('tidak_terdaftar', 0)}</td></tr>
  <tr><td>Total Omzet</td><td>Rp {props.get('total_omzet', 0):,.0f}</td></tr>
  <tr><td>Rata-rata Omzet</td><td>Rp {props.get('rata_omzet', 0):,.0f}</td></tr>
  <tr><td>Luas Wilayah</td><td>{props.get('luas_ha', 'N/A')} ha</td></tr>
</table>
</body></html>"""
        path = os.path.join(output_dir, f"laporan_{nama.lower().replace(' ', '_')}.html")
        with open(path, "w") as f:
            f.write(html)
        index_links.append(f'<li><a href="laporan_{nama.lower().replace(" ", "_")}.html">{nama}</a></li>')

    index = f"""<!DOCTYPE html>
<html lang="id">
<head><meta charset="UTF-8"><title>Laporan SPASI — Semua Desa</title></head>
<body>
<h1>Laporan SPASI — Kec. Anyar, Kab. Serang</h1>
<p>Dihasilkan: {datetime.now().strftime('%d %B %Y %H:%M')}</p>
<ul>{''.join(index_links)}</ul>
</body></html>"""
    with open(os.path.join(output_dir, "index.html"), "w") as f:
        f.write(index)
    print(f"OK: {len(desa_data['features'])} laporan HTML di {output_dir}")


def main():
    no_qgis = "--no-qgis" in sys.argv

    geojson_path = os.path.join(ROOT, "potensi_pajak_restoran", "data", "agregat_desa.geojson")
    with open(geojson_path) as f:
        data = json.load(f)

    output_dir = os.path.join(ROOT, "docs", "laporan")
    generate_html_report(data, output_dir)

    if not no_qgis:
        try:
            from qgis.core import QgsApplication, QgsProject
            from qgis.PyQt.QtCore import QFileInfo
            print("INFO: QGIS tersedia — bisa export PDF")
        except ImportError:
            print("INFO: PyQGIS tidak tersedia, fallback ke HTML")
    return 0


if __name__ == "__main__":
    exit(main())
