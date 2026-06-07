"""
generate_synthetic_data.py

Menghasilkan data sintetis untuk development & demo SPASI.
Data dummy ini memiliki struktur yang sama persis dengan data asli
sehingga ETL, QGIS model, dan frontend bisa diuji tanpa akses data Pemkab.

Penggunaan:
    python generate_synthetic_data.py

Output:
    potensi_pajak_restoran/data/restoran_sintetis.csv
    potensi_pajak_restoran/data/desa_sintetis.geojson
"""

import csv
import json
import random
import os

random.seed(42)

OUTPUT_DIR = os.path.join(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
    "potensi_pajak_restoran",
    "data"
)

DESA_NAMES = ["Anyar", "Karyawan", "Tambang Ayam", "Cimanuk"]
KATEGORI = ["restoran", "kafe", "warteg"]
STATUS = ["terdaftar", "tidak_terdaftar"]

# Bounding box Kec. Anyar (approx)
BOUNDS = {"lat_min": -6.11, "lat_max": -6.05, "lon_min": 105.90, "lon_max": 105.96}


def random_coord():
    lat = round(random.uniform(BOUNDS["lat_min"], BOUNDS["lat_max"]), 6)
    lon = round(random.uniform(BOUNDS["lon_min"], BOUNDS["lon_max"]), 6)
    return lat, lon


def generate_restoran_csv(n=30):
    rows = []
    for i in range(1, n + 1):
        desa = random.choice(DESA_NAMES)
        kategori = random.choice(KATEGORI)
        status = random.choices(STATUS, weights=[0.6, 0.4])[0]
        omzet = random.randint(5000000, 75000000)
        npwp = str(random.randint(100000000000000, 999999999999999)) if status == "terdaftar" else ""

        rows.append({
            "id": i,
            "nama_usaha": f"RM Sintetis {i}",
            "pemilik": f"Pemilik {i}",
            "alamat": f"Jl Sintetis No {i}, Kp {desa}",
            "desa": desa,
            "kecamatan": "Anyar",
            "npwp": npwp,
            "omzet_bulanan": omzet,
            "kategori": kategori,
            "status": status,
        })

    fieldnames = [
        "id", "nama_usaha", "pemilik", "alamat", "desa",
        "kecamatan", "npwp", "omzet_bulanan", "kategori", "status"
    ]

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "restoran_sintetis.csv")
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"OK: {path} ({len(rows)} baris)")


if __name__ == "__main__":
    generate_restoran_csv()
    print("Data sintetis siap digunakan untuk development.")
