import os
import pandas as pd
import matplotlib.pyplot as plt

# === Paramètres ===
base_path = "."
qc_list = [16, 32, 64, 128, 256]
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
        "data_xavier"
    ],
    "v4.1": [
        "data_A100_v4.1",
        "data_H100_v4.1",
        "data_L40S_v4.1",
        "data_orin"
    ]
}

# === Génération des graphes pour chaque QC ===
for qc in qc_list:
    for version, gpu_dirs in versions.items():
        plt.figure(figsize=(12, 6))
        for gpu_dir in gpu_dirs:
            mean_file = os.path.join(base_path, gpu_dir, "MEAN", "CI", f"mean_power_QC_{qc}.csv")
            if not os.path.exists(mean_file):
                print(f"❌ Fichier manquant : {mean_file}")
                continue

            df = pd.read_csv(mean_file)
            label = gpu_dir.replace("data_", "").replace("_v", " v").replace("_", "-")
            plt.plot(df['timestamp'], df['gpu_power'], label=label)

        plt.title(f"CI - Consommation Moyenne GPU (Version {version}) - QC={qc}")
        plt.xlabel("Temps (s)")
        plt.ylabel("Puissance GPU (W)")
        plt.legend(loc='upper right', fontsize='small')
        plt.grid(True)
        plt.tight_layout()

        output_path = os.path.join(output_dir, f"version_{version}_CI_QC_{qc}.png")
        plt.savefig(output_path)
        plt.close()
        print(f"✅ Graphique sauvegardé : {output_path}")
