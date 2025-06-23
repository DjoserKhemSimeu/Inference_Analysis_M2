import os
import pandas as pd
import matplotlib.pyplot as plt

# === Paramètres ===
base_path = "."
qc_list = [16,32,64, 128, 256]
output_dir = "comparaison_versions"
os.makedirs(output_dir, exist_ok=True)

# === Regroupement par version ===
versions = {
    "v1.1": [
        "data_2080Ti_v1.1",
        "data_QRTX6000_v1.1",
        "data_QRTX8000_v1.1",
        "data_A100_v1.1",
        "data_A40_v1.1",
        "data_T4_v1.1",
        "data_xavier_v1.1"
    ],
    "v4.1": [
        "data_A100_v4.1",
        "data_H100_v4.1",
        "data_L40S_v4.1",
        "data_orin_v4.1"
    ]
}

# === Création de la figure globale ===
fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(18, 10), sharex=False, sharey=False)
qc_to_col = {qc: i for i, qc in enumerate(qc_list)}
version_to_row = {"v1.1": 0, "v4.1": 1}

# Stockage des handles pour légende par ligne
row_legends = {row: {} for row in version_to_row.values()}

# Stockage des valeurs min/max par ligne
row_power_min = {row: float('inf') for row in version_to_row.values()}
row_power_max = {row: float('-inf') for row in version_to_row.values()}

# === Lecture et tracé ===
for version, gpu_dirs in versions.items():
    for qc in qc_list:
        row = version_to_row[version]
        col = qc_to_col[qc]
        ax = axes[row, col]

        for gpu_dir in gpu_dirs:
            mean_file = os.path.join(base_path, gpu_dir, "MEAN", "FULL", f"mean_power_QC_{qc}.csv")
            if not os.path.exists(mean_file):
                print(f"❌ Fichier manquant : {mean_file}")
                continue

            df = pd.read_csv(mean_file)

            # Mise à jour des bornes Y
            row_power_min[row] = min(row_power_min[row], df['gpu_power'].min())
            row_power_max[row] = max(row_power_max[row], df['gpu_power'].max())

            # Nettoyage du label
            clean_label = gpu_dir.replace("data_", "").replace("_v1.1", "").replace("_v4.1", "")

            if "xavier" in clean_label.lower():
                clean_label = "AGX Xavier"
            elif "orin" in clean_label.lower():
                clean_label = "AGX Orin"
            else:
                clean_label = clean_label.replace("_", "-")
            line, = ax.plot(df['timestamp'], df['gpu_power'], label=clean_label)

            if clean_label not in row_legends[row]:
                row_legends[row][clean_label] = line

        ax.set_title(f"{version} - QC={qc}")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("GPU Power (W)")
        ax.grid(True)

# === Uniformisation de l’échelle Y par ligne ===
for row in range(2):
    y_min = row_power_min[row]
    y_max = row_power_max[row]
    for col in range(5):
        axes[row, col].set_ylim(y_min, y_max)

# === Légendes à droite de chaque ligne ===
for row in range(2):
    handles = list(row_legends[row].values())
    labels = list(row_legends[row].keys())
    axes[row, -1].legend(
        handles,
        labels,
        loc='center left',
        bbox_to_anchor=(1.05, 0.5),
        fontsize='small',
        borderaxespad=0.
    )

plt.tight_layout(rect=[0, 0, 0.93, 1])
output_path = os.path.join(output_dir, "grille_comparaison_FULL_QC_16_32_64_128_256.pdf")
plt.savefig(output_path)
plt.close()
print(f"✅ Grille sauvegardée avec échelle Y homogène par ligne : {output_path}")
