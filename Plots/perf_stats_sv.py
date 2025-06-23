import os
import csv
import re

# Liste des dossiers racines à analyser
gpu_dirs = [
    "A100_v1.1_logs",
    "A100_v4.1_logs",
    "H100_v4.1_logs",
    "QRTX6000_v1.1_logs",
    "2080Ti_v1.1_logs",
    "A40_v1.1_logs",
    "QRTX8000_v1.1_logs",
    "T4_v1.1_logs",
    "L40S_v4.1_logs",
    "Orin_v4.1_logs",
    "Xavier_v1.1_logs"
]

# Nom du fichier CSV de sortie
output_csv = "mlperf_summary.csv"

# En-tête du CSV
header = ["Run ID (log path)", "QC (min query count)", "Max latency (ns)", "QPS w/ loadgen overhead", "QPS w/o loadgen overhead"]

# Fonction pour extraire les données depuis un fichier summary
def parse_summary(file_path, run_id):
    with open(file_path, 'r') as f:
        content = f.read()

    try:
        min_query_count = re.search(r"min_query_count\s*:\s*(\d+)", content).group(1)
        max_latency = re.search(r"Max latency \(ns\)\s*:\s*(\d+)", content).group(1)
        qps_with_ovh = re.search(r"QPS w/ loadgen overhead\s*:\s*([\d\.]+)", content).group(1)
        qps_wo_ovh = re.search(r"QPS w/o loadgen overhead\s*:\s*([\d\.]+)", content).group(1)
        return [run_id, min_query_count, max_latency, qps_with_ovh, qps_wo_ovh]
    except AttributeError:
        print(f"⚠️  Données manquantes dans {file_path}")
        return None

# Liste pour les résultats
results = []

# Parcours de tous les dossiers GPU
for gpu_dir in gpu_dirs:
    for dirpath, _, filenames in os.walk(gpu_dir):
        for file in filenames:
            if file == "mlperf_log_summary.txt":
                full_path = os.path.join(dirpath, file)
                # Extrait un identifiant de test lisible basé sur le chemin relatif
                run_id = os.path.dirname(full_path)
                row = parse_summary(full_path, gpu_dir)
                if row:
                    results.append(row)

# Écriture du CSV
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(results)

print(f"✅ Fichier CSV généré : {output_csv}")
