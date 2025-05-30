import pandas as pd
import numpy as np
import os
import re
from glob import glob
import matplotlib.pyplot as plt

def extract_qc_group(filename):
    match = re.search(r'QC_(\d+)_\d+', filename)
    return f"QC_{match.group(1)}" if match else None

def compute_energy(file_path):
    df = pd.read_csv(file_path)
    if "gpu_power" in df.columns:
        power_col = "gpu_power"
    elif "total_power" in df.columns:
        power_col = "total_power"
    else:
        raise ValueError(f"Colonne de puissance introuvable dans {file_path}")
    return np.trapz(df[power_col], df['timestamp'])

# Dossiers
dir_full = "FULL"
dir_pue = "PUE"

# Lister fichiers
files_full = glob(os.path.join(dir_full, "*.csv"))
files_pue = glob(os.path.join(dir_pue, "*.csv"))

# Regrouper par QC
data_by_qc = {}

for f_full in files_full:
    basename = os.path.basename(f_full)
    qc_group = extract_qc_group(basename)
    if not qc_group:
        continue
    matching_pue = f_full.replace("FULL", "PUE").replace(".csv", "_pue.csv")
    if not os.path.exists(matching_pue):
        continue
    if qc_group not in data_by_qc:
        data_by_qc[qc_group] = []
    data_by_qc[qc_group].append((f_full, matching_pue))

# Calcul des PUE
pue_results = {}

for qc_group, file_pairs in data_by_qc.items():
    pue_values = []
    for full_file, pue_file in file_pairs:
        try:
            gpu_energy = compute_energy(full_file)
            total_energy = compute_energy(pue_file)
            if gpu_energy > 0:
                pue = total_energy / gpu_energy
                pue_values.append(pue)
        except Exception as e:
            print(f"Erreur sur {full_file} / {pue_file} : {e}")
    if pue_values:
        pue_results[qc_group] = {
            "mean_pue": np.mean(pue_values),
            "std_pue": np.std(pue_values),
            "nb_runs": len(pue_values)
        }

# Résumé sous forme de DataFrame
df_pue = pd.DataFrame.from_dict(pue_results, orient="index")
df_pue.index.name = "QC_condition"
df_pue = df_pue.sort_index()
df_pue.to_csv("pue_resume_par_QC.csv")
print(df_pue)

# 📊 Graphe : barre avec erreur
plt.figure(figsize=(8, 5))
x_labels = [int(label.split('_')[1]) for label in df_pue.index]
mean_values = df_pue["mean_pue"].values
std_values = df_pue["std_pue"].values

plt.bar(x_labels, mean_values, yerr=std_values, capsize=5, color='skyblue', edgecolor='black')
plt.xlabel("Nombre de requêtes concurrentes (QC)")
plt.ylabel("PUE moyen")
plt.title("PUE moyen par condition QC (10 runs)")
plt.grid(True, axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("pue_par_condition_QC.png")
plt.show()
