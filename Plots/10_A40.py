import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
import seaborn as sns
from scipy.interpolate import interp1d
import os

# Chemins vers les fichiers CSV
file_paths = glob.glob('data_A40_v1.1/FULL/consommation_energie_single_A40_QC_*_*.csv')
ci_paths = glob.glob('data_A40_v1.1/CI/consommation_energie_single_A40_QC_*_*_ci.csv')

def extract_condition_num(path):
    return int(path.split('_')[-2])

# Trier les chemins FULL et CI selon la condition numérique
file_paths = sorted(file_paths, key=extract_condition_num)
ci_paths = sorted(ci_paths, key=extract_condition_num)

# Dictionnaires pour stocker les données par condition
data_by_condition = {}
ci_data_by_condition = {}

# Charger et nettoyer les données FULL
for file_path in file_paths:
    condition = file_path.split('_')[-2]
    df = pd.read_csv(file_path)
    df = df[df.iloc[:, 1] >= 0]  # Supprimer les valeurs négatives
    data_by_condition.setdefault(condition, []).append(df)

# Charger et nettoyer les données CI
for file_path in ci_paths:
    condition = file_path.split('_')[-3]
    df = pd.read_csv(file_path)
    df = df[df.iloc[:, 1] >= 0]
    ci_data_by_condition.setdefault(condition, []).append(df)

# Ajuster les temps CI pour s'aligner sur les FULL
for condition in data_by_condition:
    if condition in ci_data_by_condition:
        for other_df, ci_df in zip(data_by_condition[condition], ci_data_by_condition[condition]):
            time_diff = other_df.iloc[-1, 0] - ci_df.iloc[-1, 0]
            ci_df.iloc[:, 0] += time_diff

# Préparer les sauvegardes
results_mean_full = {}
results_mean_ci = {}
time_points_by_condition = {}

# Tracer les graphiques
fig, axes = plt.subplots(3, 2, figsize=(10, 12))
axes = axes.flatten()
sorted_conditions = sorted(data_by_condition.keys(), key=lambda x: int(x))

for idx, (condition, data_list) in enumerate(data_by_condition.items()):
    ax = axes[idx]

    min_time = min(df.iloc[:, 0].min() for df in data_list)
    max_time = max(df.iloc[:, 0].max() for df in data_list)
    time_points = np.linspace(min_time, max_time, 100)
    time_points_by_condition[condition] = time_points  # Enregistrer pour l'export

    # Interpolation des données FULL
    interpolated_data = []
    for df in data_list:
        f = interp1d(df.iloc[:, 0], df.iloc[:, 1], kind='linear', fill_value="extrapolate")
        interpolated_data.append(f(time_points))

    interpolated_data = np.array(interpolated_data)
    interpolated_data[interpolated_data < 0] = 0

    # Format long pour boxplot
    df_long = pd.DataFrame({
        'Time': np.repeat(np.round(time_points, 2).astype(str), interpolated_data.shape[0]),
        'Power': interpolated_data.T.flatten()
    })

    sns.boxplot(data=df_long, x='Time', y='Power', ax=ax, color='skyblue', fliersize=1)

    ticks_to_show = [i for i in range(0, len(time_points), 10)]
    ax.set_xticks(ticks_to_show)
    ax.set_xticklabels(df_long['Time'].unique()[ticks_to_show], rotation=45)

    mean_power = interpolated_data.mean(axis=0)
    std_power = interpolated_data.std(axis=0)

    ax.plot(range(len(time_points)), mean_power, color='red', label='Moyenne FULL', linewidth=1)
    ax.fill_between(range(len(time_points)),
                    mean_power - std_power,
                    mean_power + std_power,
                    color='red', alpha=0.2, label='± Écart-type')

    results_mean_full[condition] = mean_power  # Enregistrer pour export

    # Phase CI
    if condition in ci_data_by_condition:
        ci_list = ci_data_by_condition[condition]
        ci_interp = []
        ci_start_time = min(df.iloc[:, 0].min() for df in ci_list)

        for df in ci_list:
            f_ci = interp1d(df.iloc[:, 0], df.iloc[:, 1], kind='linear', fill_value="extrapolate")
            ci_interp.append(f_ci(time_points))

        ci_interp = np.array(ci_interp)
        ci_interp[ci_interp < 0] = 0

        mean_ci = ci_interp.mean(axis=0)
        results_mean_ci[condition] = mean_ci  # Enregistrer pour export

        idx_ci_start = np.searchsorted(time_points, ci_start_time)
        #ax.plot(range(idx_ci_start, len(time_points)), mean_ci[idx_ci_start:], color='blue', label='Moyenne CI', linewidth=1)
        #ax.axvline(x=idx_ci_start, color='black', linestyle=':', linewidth=2,
                   #label='Début CI' if idx == 0 else None)

    ax.set_title(f'A40 v1.1 : QC {condition}',fontsize=10)
    ax.set_xlabel('Time (s)',fontsize=9)
    ax.set_ylabel('Power (W)',fontsize=9)

# Supprimer le dernier axe vide
axes[5].axis('off')

# Légende globale
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower right', fontsize=12)
plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.show()

# === Sauvegarde des fichiers CSV par condition ===
os.makedirs("mean_A40_QC", exist_ok=True)

# Export des moyennes FULL
for condition, mean_power in results_mean_full.items():
    df_full = pd.DataFrame({
        'timestamp': time_points_by_condition[condition],
        'gpu_power': mean_power
    })
    df_full.to_csv(f"mean_A40_QC/moyenne_FULL_QC_{condition}.csv", index=False)

# Export des moyennes CI
for condition, mean_ci in results_mean_ci.items():
    df_ci = pd.DataFrame({
        'timestamp': time_points_by_condition[condition],
        'gpu_power': mean_ci
    })
    df_ci.to_csv(f"mean_A40_QC/moyenne_CI_QC_{condition}.csv", index=False)
