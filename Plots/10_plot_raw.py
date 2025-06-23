import pandas as pd
import matplotlib.pyplot as plt
import glob

# Chemins vers les fichiers CSV
file_paths = glob.glob('A100x1_data/consommation_energie_single_A100x1_BS_1_QC_*_*.csv')
print(file_paths)
# Dictionnaire pour stocker les données par condition expérimentale
data_by_condition = {}

# Lire les fichiers et organiser les données par condition expérimentale
for file_path in file_paths:
    # Extraire la condition expérimentale du nom de fichier
    condition = file_path.split('_')[-2]

    # Lire le fichier CSV
    df = pd.read_csv(file_path)

    # Stocker les données dans le dictionnaire
    if condition not in data_by_condition:
        data_by_condition[condition] = []
    data_by_condition[condition].append(df)

# Tracer les graphiques
for condition, data_list in data_by_condition.items():
    plt.figure(figsize=(10, 6))
    for i, df in enumerate(data_list):
        plt.plot(df.iloc[:, 0], df.iloc[:, 1], label=f'Run {i+1}')

    plt.title(f'Condition expérimentale: QC {condition}')
    plt.xlabel('Temps')
    plt.ylabel('Puissance')
    plt.legend()
    plt.grid(True)
    plt.show()
