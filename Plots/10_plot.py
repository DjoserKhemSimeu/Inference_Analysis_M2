import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
import seaborn as sns
from scipy.interpolate import interp1d

file_paths = glob.glob('A100x1_data/consommation_energie_single_A100x1_BS_1_QC_*_*.csv')
data_by_condition = {}
def extract_condition_num(path):
    # Si les fichiers sont comme '..._QC_16_1.csv' → on prend l'avant-dernier morceau
    return int(path.split('_')[-2])

# Trier les chemins FULL et CI selon la condition numérique
file_paths = sorted(file_paths, key=extract_condition_num)
for file_path in file_paths:
    condition = file_path.split('_')[-2]
    df = pd.read_csv(file_path)
    data_by_condition.setdefault(condition, []).append(df)

fig, axes = plt.subplots(3, 2, figsize=(10, 12))
axes = axes.flatten()

for idx, (condition, data_list) in enumerate(data_by_condition.items()):
    ax = axes[idx]

    min_time = min(df.iloc[:, 0].min() for df in data_list)
    max_time = max(df.iloc[:, 0].max() for df in data_list)
    time_points = np.linspace(min_time, max_time, 100)

    interpolated_data = []
    for df in data_list:
        f = interp1d(df.iloc[:, 0], df.iloc[:, 1], kind='linear', fill_value="extrapolate")
        interpolated_data.append(f(time_points))
    interpolated_data = np.array(interpolated_data)

    df_long = pd.DataFrame({
        'Time': np.repeat(time_points.round(2).astype(str), interpolated_data.shape[0]),
        'Power': interpolated_data.T.flatten()
    })

    sns.boxplot(data=df_long, x='Time', y='Power', ax=ax, color='skyblue', fliersize=1)

    # Afficher un tick sur 10 (pour éviter surcharge)
    ticks_to_show = [i for i in range(0, len(time_points), 10)]
    ax.set_xticks(ticks_to_show)
    ax.set_xticklabels(df_long['Time'].unique()[ticks_to_show], rotation=45)

    mean_power = interpolated_data.mean(axis=0)
    std_power = interpolated_data.std(axis=0)

    ax.plot(range(len(time_points)), mean_power, color='red', label='Moyenne', linewidth=1)
    ax.fill_between(range(len(time_points)),
                    mean_power - std_power,
                    mean_power + std_power,
                    color='red',
                    alpha=0.2,
                    label='± Écart-type')

    ax.set_title(f'Condition expérimentale: QC {condition}')
    ax.set_xlabel('Temps (s)')
    ax.set_ylabel('Puissance (W)')

axes[5].axis('off')
handles, labels = axes[0].get_legend_handles_labels()

# Ajouter une légende globale en bas à droite de la figure
fig.legend(handles, labels, loc='lower right', fontsize=20)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.show()
