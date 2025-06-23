import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
import seaborn as sns
from scipy.interpolate import interp1d

# Activer le style seaborn
sns.set(style="whitegrid")

# Chemins vers les fichiers
paths = {
    'v1.1': {
        'FULL': glob.glob('data_A100_v1.1/FULL/consommation_energie_single_A100_QC_*_*.csv'),
        'CI': glob.glob('data_A100_v1.1/CI/consommation_energie_single_A100_QC_*_*_ci.csv')
    },
    'v4.1': {
        'FULL': glob.glob('data_A100_v4.1/FULL/consommation_energie_single_A100_QC_*_*.csv'),
        'CI': glob.glob('data_A100_v4.1/CI/consommation_energie_single_A100_QC_*_*_ci.csv')
    }
}

def load_condition_data(version_paths, target_condition='256'):
    data_full, data_ci = [], []

    for file_path in version_paths['FULL']:
        if f'QC_{target_condition}_' in file_path:
            df = pd.read_csv(file_path)
            df = df[df.iloc[:, 1] >= 0]
            data_full.append(df)

    for file_path in version_paths['CI']:
        if f'QC_{target_condition}_' in file_path:
            df = pd.read_csv(file_path)
            df = df[df.iloc[:, 1] >= 0]
            data_ci.append(df)

    # Aligner le temps CI sur la fin de FULL
    for full_df, ci_df in zip(data_full, data_ci):
        time_shift = full_df.iloc[-1, 0] - ci_df.iloc[-1, 0]
        ci_df.iloc[:, 0] += time_shift

    return data_full, data_ci

# Charger les données pour QC 256
data_256 = {}
for version in paths:
    full_data, ci_data = load_condition_data(paths[version], target_condition='256')
    data_256[version] = {'FULL': full_data, 'CI': ci_data}

# Tracer les deux sous-graphiques
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Pour harmoniser l'axe Y
global_ymin, global_ymax = float('inf'), float('-inf')

for idx, (version, datasets) in enumerate(data_256.items()):
    ax = axes[idx]
    full_list = datasets['FULL']
    ci_list = datasets['CI']

    min_time = min(df.iloc[:, 0].min() for df in full_list)
    max_time = max(df.iloc[:, 0].max() for df in full_list)
    time_points = np.linspace(min_time, max_time, 100)

    interpolated_data = []
    for df in full_list:
        f = interp1d(df.iloc[:, 0], df.iloc[:, 1], kind='linear', fill_value="extrapolate")
        interpolated_data.append(f(time_points))
    interpolated_data = np.array(interpolated_data)
    interpolated_data[interpolated_data < 0] = 0

    # Format long pour seaborn boxplot
    df_long = pd.DataFrame({
        'Time': np.repeat(time_points.round(2).astype(str), interpolated_data.shape[0]),
        'Power': interpolated_data.T.flatten()
    })

    sns.boxplot(data=df_long, x='Time', y='Power', ax=ax, color='skyblue', fliersize=1)

    ticks_to_show = [i for i in range(0, len(time_points), 10)]
    ax.set_xticks(ticks_to_show)
    ax.set_xticklabels(df_long['Time'].unique()[ticks_to_show], rotation=45)

    # Moyenne et écart-type
    mean_power = interpolated_data.mean(axis=0)
    std_power = interpolated_data.std(axis=0)
    ax.plot(range(len(time_points)), mean_power, color='red', label='Mean', linewidth=1)
    ax.fill_between(range(len(time_points)),
                    mean_power - std_power,
                    mean_power + std_power,
                    color='red', alpha=0.2, label='± Standard deviation')

    # Ligne verticale pour début CI (pas de courbe bleue)
    if ci_list:
        ci_start_time = min(df.iloc[:, 0].min() for df in ci_list)
        idx_ci_start = np.searchsorted(time_points, ci_start_time)
        #ax.axvline(x=idx_ci_start, color='black', linestyle=':', linewidth=2,
                   #label='Début CI' if idx == 0 else None)

    ax.set_title(f'A100 {version} - QC 256')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Power (W)')

    # Mettre à jour les bornes Y globales
    global_ymin = min(global_ymin, interpolated_data.min())
    global_ymax = max(global_ymax, interpolated_data.max())

# Appliquer la même échelle Y aux deux graphes
for ax in axes:
    ax.set_ylim(global_ymin, global_ymax)

# Légende
axes[0].legend()

plt.tight_layout()
plt.show()
