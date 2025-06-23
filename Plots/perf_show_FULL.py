import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Constantes
EGM = 79.1  # gCO2/kWh
seven_years = 61320 * 3600  # nombre de secondes en 7 ans

# Impact conception v1.1
impact_conception_v11 = {
    'A100': [27.678700, 20.469933, 44.818200],
    'A40': [26.913520, 41.206800],
    'T4': [11.314983, 24.726000],
    '2080Ti': [11.645243, 30.199200],
    'QRTX8000': [24.965243, 43.519200],
    'Xavier': [12.847420, 21.460000]
}

# Impact conception v4.1
impact_conception_v41 = {
    'H100': [44.272180],
    'L40S': [33.643830],
    'Orin': [25.539700, 35.895500],
    'A100': [27.678700, 20.469933, 44.818200],
    'A40': [26.913520, 41.206800],
    'T4': [11.314983, 24.726000],
    '2080Ti': [11.645243, 30.199200],
    'QRTX8000': [24.965243, 43.519200]
}

# GPU list
gpus_v11 = ['A100', 'A40', 'T4', '2080Ti', 'QRTX8000', 'Xavier']
gpus_v41 = ['H100', 'L40S', 'Orin', 'A100']

# Mapping GPU to folder
gpu_folder_map_v11 = {
    'A100': 'data_A100_v1.1',
    'A40': 'data_A40_v1.1',
    'T4': 'data_T4_v1.1',
    '2080Ti': 'data_2080Ti_v1.1',
    'QRTX8000': 'data_QRTX8000_v1.1',
    'Xavier': 'data_xavier'
}

gpu_folder_map_v41 = {
    'H100': 'data_H100_v4.1',
    'L40S': 'data_L40S_v4.1',
    'Orin': 'data_orin',
    'A100': 'data_A100_v4.1',
}

# Fonction de calcul d'impact
def compute_impact_energy_mean_power(file_path, gpu_name, impact_conception):
    if not os.path.isfile(file_path):
        print(f"⚠️ Fichier non trouvé : {file_path}")
        return None
    data = pd.read_csv(file_path)
    timestamps = data['timestamp']
    mean_power = data['gpu_power']

    duration_sec = timestamps.iloc[-1] - timestamps.iloc[0]
    duration_hr = duration_sec / 3600

    energie_Wh = mean_power.mean() * duration_hr
    energie_kWh = energie_Wh / 1000

    co2_emissions = energie_kWh * EGM

    impact_total = [
        co2_emissions + ((duration_sec / seven_years) * val * 1000)
        for val in impact_conception[gpu_name]
    ]

    return np.mean(impact_total)

# Fonction d'agrégation des impacts
def gather_impacts(gpus, gpu_folder_map, impact_conception, version_label):
    results = []
    for gpu in gpus:
        folder = gpu_folder_map[gpu]
        for qc in [16, 32, 64, 128, 256]:
            file_path = os.path.join(folder, 'MEAN', 'FULL', f'mean_power_QC_{qc}.csv')
            impact = compute_impact_energy_mean_power(file_path, gpu, impact_conception)
            if impact is None:
                continue
            results.append({
                'QC': qc,
                'GPU': gpu,
                'Impact Environnemental Total (g)': impact,
                'Version': version_label
            })
    return pd.DataFrame(results)

# Charger les latences
latency_df = pd.read_csv('mlperf_summary.csv')

def assign_version(run_id):
    if 'v1.1' in run_id:
        return 'v1.1'
    elif 'v4.1' in run_id:
        return 'v4.1'
    return 'unknown'

latency_df['Version'] = latency_df['Run ID (log path)'].apply(assign_version)

gpu_name_map_latency = {
    'A100_v1.1_logs': 'A100',
    'A40_v1.1_logs': 'A40',
    'T4_v1.1_logs': 'T4',
    '2080Ti_v1.1_logs': '2080Ti',
    'QRTX8000_v1.1_logs': 'QRTX8000',
    'Xavier_v1.1_logs': 'Xavier',
    'H100_v4.1_logs': 'H100',
    'L40S_v4.1_logs': 'L40S',
    'Orin_v4.1_logs': 'Orin',
    'A100_v4.1_logs': 'A100',
}

latency_df['GPU'] = latency_df['Run ID (log path)'].map(gpu_name_map_latency)

latency_df = latency_df[['QC (min query count)', 'Max latency (ns)', 'GPU', 'Version']]
latency_df.rename(columns={'QC (min query count)': 'QC', 'Max latency (ns)': 'max_latency_ns'}, inplace=True)
latency_df['max_latency_ms'] = latency_df['max_latency_ns'] / 1e6
latency_df = latency_df.groupby(['GPU', 'QC', 'Version'], as_index=False).agg({'max_latency_ms': 'max'})

# Récupérer les impacts
df_v11 = gather_impacts(gpus_v11, gpu_folder_map_v11, impact_conception_v11, 'v1.1')
df_v41 = gather_impacts(gpus_v41, gpu_folder_map_v41, impact_conception_v41, 'v4.1')
df_merged = pd.concat([df_v11, df_v41], ignore_index=True)

# Fusionner avec latence (en gardant tous les impacts même si latence manquante)
df_final = pd.merge(df_merged, latency_df, on=['GPU', 'QC', 'Version'], how='left')

# Ajouter catégorie
categories = {
    'Xavier': 'Edge',
    'Orin': 'Edge',
    'H100': 'Large-scale',
    'A100': 'Large-scale',
    'A40': 'Large-scale',
    'T4': 'Desktop',
    '2080Ti': 'Gaming',
    'QRTX8000': 'Desktop',
    'L40S': 'Large-scale'
}
df_final['category'] = df_final['GPU'].map(categories)

# Affichage debug (facultatif)
print(df_final)

# Tracé
markers = {'Edge': 'o', 'Gaming': 's', 'Desktop': 'D', 'Large-scale': 'X'}
fig, axs = plt.subplots(2, 2, figsize=(14, 10), sharex=True)

# GWP v1.1
sns.lineplot(ax=axs[0, 0], data=df_final[df_final['Version'] == 'v1.1'],
             x='QC', y='Impact Environnemental Total (g)', hue='GPU',
             style='category', markers=markers, dashes=False)
axs[0, 0].set_title('GWP (g CO2 eq) - Version 1.1')
axs[0, 0].set_xlabel('Number of queries (QC)')
axs[0, 0].set_ylabel('Impact Environnemental Total (g)')
axs[0, 0].grid(True)

# Latence v1.1
sns.lineplot(ax=axs[1, 0], data=df_final[df_final['Version'] == 'v1.1'],
             x='QC', y='max_latency_ms', hue='GPU',
             style='category', markers=markers, dashes=False)
axs[1, 0].set_title('Max latency (ms) - Version 1.1')
axs[1, 0].set_xlabel('Number of queries (QC)')
axs[1, 0].set_ylabel('Max latency (ms)')
axs[1, 0].grid(True)

# GWP v4.1
sns.lineplot(ax=axs[0, 1], data=df_final[df_final['Version'] == 'v4.1'],
             x='QC', y='Impact Environnemental Total (g)', hue='GPU',
             style='category', markers=markers, dashes=False)
axs[0, 1].set_title('GWP (g CO2 eq) - Version 4.1')
axs[0, 1].set_xlabel('Number of queries (QC)')
axs[0, 1].set_ylabel('Impact Environnemental Total (g)')
axs[0, 1].grid(True)

# Latence v4.1
sns.lineplot(ax=axs[1, 1], data=df_final[df_final['Version'] == 'v4.1'],
             x='QC', y='max_latency_ms', hue='GPU',
             style='category', markers=markers, dashes=False)
axs[1, 1].set_title('Max latency (ms) - Version 4.1')
axs[1, 1].set_xlabel('Number of queries (QC)')
axs[1, 1].set_ylabel('Max latency (ms)')
axs[1, 1].grid(True)

plt.tight_layout()
plt.show()
