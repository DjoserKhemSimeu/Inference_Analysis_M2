import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('Agg')

# Dossiers à analyser
gpu_dirs = [
    "data_2080Ti_v1.1_2",
    "data_A100_v1.1",
    "data_A40_v1.1",
    "data_T4_v1.1",
    "data_A100_v4.1",
    "data_H100_v4.1",
    "data_L40S_v4.1",
    "data_xavier_v1.1",
    "data_orin_v4.1"
]

# Conditions d'intérêt
conditions = ["64", "128", "256"]

# Séparation par version
gpus_v1_1 = [gpu for gpu in gpu_dirs if "v1.1" in gpu]
gpus_v4_1 = [gpu for gpu in gpu_dirs if "v4.1" in gpu]

# Fonction de chargement des données
def collect_mean_power(gpu_list):
    data_by_condition = {qc: {} for qc in conditions}
    for gpu in gpu_list:
        for qc in conditions:
            file_path = os.path.join(gpu, "MEAN", "FULL", f"mean_power_QC_{qc}.csv")
            if os.path.exists(file_path):
                df = pd.read_csv(file_path, header=None)
                df.columns = ['Time', 'Power']
                data_by_condition[qc][gpu] = df
    return data_by_condition

# Récupération des données
data_v1_1 = collect_mean_power(gpus_v1_1)
data_v4_1 = collect_mean_power(gpus_v4_1)

# Création des sous-graphes
fig, axes = plt.subplots(2, 3, figsize=(32, 16), sharey=True, constrained_layout=True)
axes = axes.flatten()

# Pour stocker les handles pour les légendes communes
handles_top, labels_top = [], []
handles_bottom, labels_bottom = [], []

# Affichage pour chaque condition
for col_idx, qc in enumerate(conditions):
    # Ligne 0 : v1.1
    print(qc)
    ax_top = axes[col_idx]
    ax_top.set_title(f"QC {qc} — v1.1")
    for gpu, df in data_v1_1[qc].items():
        label = gpu.replace("data_", "").replace("_", " ")
        if len(df) > 20:
            indices = np.linspace(0, len(df) - 1, 20, dtype=int)
            df_sampled = df.iloc[indices]
        else:
            df_sampled = df
        line, = ax_top.plot(df_sampled["Time"], df_sampled["Power"], label=label)
        if label not in labels_top:
            handles_top.append(line)
            labels_top.append(label)
    ax_top.set_xlabel("Temps (s)")
    ax_top.set_ylabel("Puissance (W)")

    # Ligne 1 : v4.1
    ax_bottom = axes[col_idx + 3]
    ax_bottom.set_title(f"QC {qc} — v4.1")
    for gpu, df in data_v4_1[qc].items():
        label = gpu.replace("data_", "").replace("_", " ")
        if len(df) > 20:
            indices = np.linspace(0, len(df) - 1, 20, dtype=int)
            df_sampled = df.iloc[indices]
        else:
            df_sampled = df
        line, = ax_bottom.plot(df_sampled["Time"], df_sampled["Power"], label=label)
        if label not in labels_bottom:
            handles_bottom.append(line)
            labels_bottom.append(label)
    ax_bottom.set_xlabel("Temps (s)")
    ax_bottom.set_ylabel("Puissance (W)")
    print("############################")

# Légende commune par ligne
axes[0].legend(handles_top, labels_top, loc='center left', bbox_to_anchor=(1.5, 1.15), ncol=3, fontsize=9, title="GPU v1.1")
axes[3].legend(handles_bottom, labels_bottom, loc='center left', bbox_to_anchor=(1.5, 1.15), ncol=3, fontsize=9, title="GPU v4.1")

# Mise en page finale
output_file = "plot_consommation_v1.1_v4.1.png"
plt.savefig(output_file, dpi=300)
print(f"Figure sauvegardée dans : {output_file}")
