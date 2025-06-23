import os
import numpy as np
import pandas as pd
from glob import glob

# === Paramètres ===
base_dir = "data_orin"
phases = ["FULL", "CI"]
qcs = [16, 32, 64, 128, 256]
runs = list(range(1, 11))  # 1 à 10

# === Dossier de sortie ===
mean_dir = os.path.join(base_dir, "MEAN")
os.makedirs(mean_dir, exist_ok=True)

for phase in phases:
    phase_dir = os.path.join(base_dir, phase)
    phase_mean_dir = os.path.join(mean_dir, phase)
    os.makedirs(phase_mean_dir, exist_ok=True)

    for qc in qcs:
        pattern = f"consommation_energie_single_orin_QC_{qc}_*_ci.csv" if phase == "CI" else f"consommation_energie_single_orin_QC_{qc}_*.csv"
        files = sorted(glob(os.path.join(phase_dir, pattern)))
        files = [f for f in files if not f.endswith("_ci.csv") or phase == "CI"]

        if len(files) != 10:
            print(f"⚠️  {len(files)} fichiers trouvés pour QC={qc}, phase={phase}. Attendu: 10.")
            continue

        dfs = []
        for f in files:
            df = pd.read_csv(f)
            df = df.dropna()
            dfs.append(df)

        # Interpolation sur base de timestamps communs
        min_time = max(df['timestamp'].min() for df in dfs)
        max_time = min(df['timestamp'].max() for df in dfs)
        common_timestamps = np.linspace(min_time, max_time, 1000)  # 1000 points réguliers

        interpolated = []
        for df in dfs:
            interp_power = np.interp(common_timestamps, df['timestamp'], df['gpu_power'])
            interpolated.append(interp_power)

        mean_power = np.mean(interpolated, axis=0)
        mean_df = pd.DataFrame({
            'timestamp': common_timestamps,
            'gpu_power': mean_power/1000
        })

        output_filename = f"mean_power_QC_{qc}.csv"
        output_path = os.path.join(phase_mean_dir, output_filename)
        mean_df.to_csv(output_path, index=False)
        print(f"✅ Fichier moyen enregistré : {output_path}")
