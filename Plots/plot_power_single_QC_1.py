import pandas as pd
import matplotlib.pyplot as plt

# Charger les données depuis les fichiers CSV
data_A100_BS_1_QC_16 = pd.read_csv('data/consommation_energie_A100x1_single_BS_1_QC_16.csv')
data_A100_BS_1_QC_32 = pd.read_csv('data/consommation_energie_A100x1_single_BS_1_QC_32.csv')
data_A100_BS_1_QC_64 = pd.read_csv('data/consommation_energie_A100x1_single_BS_1_QC_64.csv')
data_A100_BS_1_QC_128 = pd.read_csv('data/consommation_energie_A100x1_single_BS_1_QC_128.csv')
data_A100_BS_1_QC_256 = pd.read_csv('data/consommation_energie_A100x1_single_BS_1_QC_256.csv')

data_orin_BS_1_QC_16 = pd.read_csv('data_orin/FULL/consommation_energie_single_orin_QC_16_1.csv')
data_orin_BS_1_QC_32 = pd.read_csv('data_orin/FULL/consommation_energie_single_orin_QC_32_1.csv')
data_orin_BS_1_QC_64 = pd.read_csv('data_orin/FULL/consommation_energie_single_orin_QC_64_1.csv')
data_orin_BS_1_QC_128 = pd.read_csv('data_orin/FULL/consommation_energie_single_orin_QC_128_1.csv')
data_orin_BS_1_QC_256 = pd.read_csv('data_orin/FULL/consommation_energie_single_orin_QC_256_1.csv')

data_jetson_BS_1_QC_128 = pd.read_csv('data/consommation_energie_jetson_single_BS_1_QC_128.csv')
data_jetson_BS_1_QC_64 = pd.read_csv('data/consommation_energie_jetson_single_BS_1_QC_64.csv')
data_jetson_BS_1_QC_256 = pd.read_csv('data/consommation_energie_jetson_single_BS_1_QC_256.csv')
data_jetson_BS_1_QC_32 = pd.read_csv('data/consommation_energie_jetson_single_BS_1_QC_32.csv')
data_jetson_BS_1_QC_16 = pd.read_csv('data/consommation_energie_jetson_single_BS_1_QC_16.csv')

# Charger les données pour T4 et A40
data_T4_BS_1_QC_16 = pd.read_csv('data/consommation_energie_T4x1_single_BS_1_QC_16.csv')
data_T4_BS_1_QC_32 = pd.read_csv('data/consommation_energie_T4x1_single_BS_1_QC_32.csv')
data_T4_BS_1_QC_64 = pd.read_csv('data/consommation_energie_T4x1_single_BS_1_QC_64.csv')
data_T4_BS_1_QC_128 = pd.read_csv('data/consommation_energie_T4x1_single_BS_1_QC_128.csv')
data_T4_BS_1_QC_256 = pd.read_csv('data/consommation_energie_T4x1_single_BS_1_QC_256.csv')

data_A40_BS_1_QC_16 = pd.read_csv('data/consommation_energie_A40x1_single_BS_1_QC_16.csv')
data_A40_BS_1_QC_32 = pd.read_csv('data/consommation_energie_A40x1_single_BS_1_QC_32.csv')
data_A40_BS_1_QC_64 = pd.read_csv('data/consommation_energie_A40x1_single_BS_1_QC_64.csv')
data_A40_BS_1_QC_128 = pd.read_csv('data/consommation_energie_A40x1_single_BS_1_QC_128.csv')
data_A40_BS_1_QC_256 = pd.read_csv('data/consommation_energie_A40x1_single_BS_1_QC_256.csv')

# Charger les données pour 2080Ti
data_2080Ti_BS_1_QC_16 = pd.read_csv('data/consommation_energie_2080Tix1_BS_1_QC_16.csv')
data_2080Ti_BS_1_QC_32 = pd.read_csv('data/consommation_energie_2080Tix1_BS_1_QC_32.csv')
data_2080Ti_BS_1_QC_64 = pd.read_csv('data/consommation_energie_2080Tix1_BS_1_QC_64.csv')
data_2080Ti_BS_1_QC_128 = pd.read_csv('data/consommation_energie_2080Tix1_BS_1_QC_128.csv')
data_2080Ti_BS_1_QC_256 = pd.read_csv('data/consommation_energie_2080Tix1_BS_1_QC_256.csv')

# Charger les données pour Quadro RTX 8000x1
data_Quadro_RTX_8000x1_BS_1_QC_16 = pd.read_csv('data/consommation_energie_Quadro_RTX_8000x1_single_BS_1_QC_16.csv')
data_Quadro_RTX_8000x1_BS_1_QC_32 = pd.read_csv('data/consommation_energie_Quadro_RTX_8000x1_single_BS_1_QC_32.csv')
data_Quadro_RTX_8000x1_BS_1_QC_64 = pd.read_csv('data/consommation_energie_Quadro_RTX_8000x1_single_BS_1_QC_64.csv')
data_Quadro_RTX_8000x1_BS_1_QC_128 = pd.read_csv('data/consommation_energie_Quadro_RTX_8000x1_single_BS_1_QC_128.csv')
data_Quadro_RTX_8000x1_BS_1_QC_256 = pd.read_csv('data/consommation_energie_Quadro_RTX_8000x1_single_BS_1_QC_256.csv')

# Charger les données pour A5000x1
data_A5000x1_BS_1_QC_16 = pd.read_csv('data/consommation_energie_A5000x1_single_BS_1_QC_16.csv')
data_A5000x1_BS_1_QC_32 = pd.read_csv('data/consommation_energie_A5000x1_single_BS_1_QC_32.csv')
data_A5000x1_BS_1_QC_64 = pd.read_csv('data/consommation_energie_A5000x1_single_BS_1_QC_64.csv')
data_A5000x1_BS_1_QC_128 = pd.read_csv('data/consommation_energie_A5000x1_single_BS_1_QC_128.csv')
data_A5000x1_BS_1_QC_256 = pd.read_csv('data/consommation_energie_A5000x1_single_BS_1_QC_256.csv')

# Créer un dictionnaire pour stocker les données de chaque GPU
gpu_data = {
    'A100': {
        '16': (data_A100_BS_1_QC_16['timestamp'], data_A100_BS_1_QC_16['gpu_power']),
        '32': (data_A100_BS_1_QC_32['timestamp'], data_A100_BS_1_QC_32['gpu_power']),
        '64': (data_A100_BS_1_QC_64['timestamp'], data_A100_BS_1_QC_64['gpu_power']),
        '128': (data_A100_BS_1_QC_128['timestamp'], data_A100_BS_1_QC_128['gpu_power']),
        '256': (data_A100_BS_1_QC_256['timestamp'], data_A100_BS_1_QC_256['gpu_power'])
    },
    'Jetson AGX Xavier': {
        '16': (data_jetson_BS_1_QC_16['timestamp'], data_jetson_BS_1_QC_16['gpu_power'] / 1000),
        '32': (data_jetson_BS_1_QC_32['timestamp'], data_jetson_BS_1_QC_32['gpu_power'] / 1000),
        '64': (data_jetson_BS_1_QC_64['timestamp'], data_jetson_BS_1_QC_64['gpu_power'] / 1000),
        '128': (data_jetson_BS_1_QC_128['timestamp'], data_jetson_BS_1_QC_128['gpu_power'] / 1000),
        '256': (data_jetson_BS_1_QC_256['timestamp'], data_jetson_BS_1_QC_256['gpu_power'] / 1000)
    },
    'Orin': {
        '16': (data_orin_BS_1_QC_16['timestamp'], data_orin_BS_1_QC_16['gpu_power'] / 1000),
        '32': (data_orin_BS_1_QC_32['timestamp'], data_orin_BS_1_QC_32['gpu_power'] / 1000),
        '64': (data_orin_BS_1_QC_64['timestamp'], data_orin_BS_1_QC_64['gpu_power'] / 1000),
        '128': (data_orin_BS_1_QC_128['timestamp'], data_orin_BS_1_QC_128['gpu_power'] / 1000),
        '256': (data_orin_BS_1_QC_256['timestamp'], data_orin_BS_1_QC_256['gpu_power'] / 1000)
    },
    'T4': {
        '16': (data_T4_BS_1_QC_16['timestamp'], data_T4_BS_1_QC_16['gpu_power']),
        '32': (data_T4_BS_1_QC_32['timestamp'], data_T4_BS_1_QC_32['gpu_power']),
        '64': (data_T4_BS_1_QC_64['timestamp'], data_T4_BS_1_QC_64['gpu_power']),
        '128': (data_T4_BS_1_QC_128['timestamp'], data_T4_BS_1_QC_128['gpu_power']),
        '256': (data_T4_BS_1_QC_256['timestamp'], data_T4_BS_1_QC_256['gpu_power'])
    },
    'A40': {
        '16': (data_A40_BS_1_QC_16['timestamp'], data_A40_BS_1_QC_16['gpu_power']),
        '32': (data_A40_BS_1_QC_32['timestamp'], data_A40_BS_1_QC_32['gpu_power']),
        '64': (data_A40_BS_1_QC_64['timestamp'], data_A40_BS_1_QC_64['gpu_power']),
        '128': (data_A40_BS_1_QC_128['timestamp'], data_A40_BS_1_QC_128['gpu_power']),
        '256': (data_A40_BS_1_QC_256['timestamp'], data_A40_BS_1_QC_256['gpu_power'])
    },
    '2080Ti': {
        '16': (data_2080Ti_BS_1_QC_16['timestamp'], data_2080Ti_BS_1_QC_16['gpu_power']),
        '32': (data_2080Ti_BS_1_QC_32['timestamp'], data_2080Ti_BS_1_QC_32['gpu_power']),
        '64': (data_2080Ti_BS_1_QC_64['timestamp'], data_2080Ti_BS_1_QC_64['gpu_power']),
        '128': (data_2080Ti_BS_1_QC_128['timestamp'], data_2080Ti_BS_1_QC_128['gpu_power']),
        '256': (data_2080Ti_BS_1_QC_256['timestamp'], data_2080Ti_BS_1_QC_256['gpu_power'])
    },
    'Quadro RTX 8000x1': {
        '16': (data_Quadro_RTX_8000x1_BS_1_QC_16['timestamp'], data_Quadro_RTX_8000x1_BS_1_QC_16['gpu_power']),
        '32': (data_Quadro_RTX_8000x1_BS_1_QC_32['timestamp'], data_Quadro_RTX_8000x1_BS_1_QC_32['gpu_power']),
        '64': (data_Quadro_RTX_8000x1_BS_1_QC_64['timestamp'], data_Quadro_RTX_8000x1_BS_1_QC_64['gpu_power']),
        '128': (data_Quadro_RTX_8000x1_BS_1_QC_128['timestamp'], data_Quadro_RTX_8000x1_BS_1_QC_128['gpu_power']),
        '256': (data_Quadro_RTX_8000x1_BS_1_QC_256['timestamp'], data_Quadro_RTX_8000x1_BS_1_QC_256['gpu_power'])
    },
    'A5000x1': {
        '16': (data_A5000x1_BS_1_QC_16['timestamp'], data_A5000x1_BS_1_QC_16['gpu_power']),
        '32': (data_A5000x1_BS_1_QC_32['timestamp'], data_A5000x1_BS_1_QC_32['gpu_power']),
        '64': (data_A5000x1_BS_1_QC_64['timestamp'], data_A5000x1_BS_1_QC_64['gpu_power']),
        '128': (data_A5000x1_BS_1_QC_128['timestamp'], data_A5000x1_BS_1_QC_128['gpu_power']),
        '256': (data_A5000x1_BS_1_QC_256['timestamp'], data_A5000x1_BS_1_QC_256['gpu_power'])
    }
}

# Couleurs pour chaque GPU
gpu_colors = {
    'A100': 'blue',
    'Orin': 'gray',
    'Jetson AGX Xavier': 'darkorange',
    'T4': 'red',
    'A40': 'green',
    '2080Ti': 'purple',
    'Quadro RTX 8000x1': 'violet',
    'A5000x1': 'brown'
}

# Créer une figure avec cinq sous-graphiques (3 en haut et 2 en bas)
fig, axs = plt.subplots(3, 2, figsize=(10, 10))

# Aplatir le tableau de sous-graphiques pour faciliter l'itération
axs = axs.flatten()

# Liste pour stocker les lignes tracées pour la légende
lines = []

# Tracer les données pour chaque QC dans un sous-graphique différent
for i, qc in enumerate(['16', '32', '64', '128', '256']):
    for gpu in gpu_data:
        timestamp, power = gpu_data[gpu][qc]
        line, = axs[i].plot(timestamp, power, color=gpu_colors[gpu], label=f'{gpu}')
        if i == 0:  # Ajouter seulement les lignes du premier sous-graphique à la légende
            lines.append(line)

    axs[i].set_title(f'Instantaneous power required by GPUs - Single-stream (QC={qc})')
    axs[i].set_xlabel('Time (s)')
    axs[i].set_ylabel('Power (W)')
    axs[i].grid(True)

# Supprimer le dernier sous-graphique inutilisé
fig.delaxes(axs[-1])

# Créer une légende unique pour tous les sous-graphiques à la place du sous-graphique manquant
legend_ax = fig.add_subplot(3, 2, 6)
legend_ax.axis('off')  # Désactiver les axes pour la légende
legend_ax.legend(handles=lines, loc='center', title='GPU Legend')

plt.tight_layout()
plt.show()
