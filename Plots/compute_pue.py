import pandas as pd
import numpy as np
import os
import re
from glob import glob

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
    return np.trapz(df[power_col]/1000, df['timestamp'])/3_600_000

# Récupération des fichiers
dir_full = "FULL"
dir_pue = "PUE"

files_full = glob(os.path.join(dir_full, "*.csv"))
files_pue = glob(os.path.join(dir_pue, "*.csv"))

# Organisation par groupe QC (QC_16, QC_32, ...)
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
        gpu_energy = compute_energy(full_file)
        total_energy = compute_energy(pue_file)
        if gpu_energy > 0:
            pue = total_energy / gpu_energy
            pue_values.append(pue)
    if pue_values:
        pue_results[qc_group] = {
            "mean_pue": np.mean(pue_values),
            "std_pue": np.std(pue_values),
            "nb_runs": len(pue_values)
        }

# Affichage et sauvegarde
df_pue = pd.DataFrame.from_dict(pue_results, orient="index")
df_pue.index.name = "QC_condition"
df_pue = df_pue.sort_index()
print(df_pue)
df_pue.to_csv("../Doc/pue_resume_par_QC.csv")
