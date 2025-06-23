import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Définir l'émission de CO2 par kWh
EGM = 79.1  # gCO2/kWh
seven_years = 61320  # nombre d'heures en 7 ans

# Impacts de conception (données fournies)
impact_conception = {
    'NVIDIA-AGX-Xavier': [13.716, 5.103420289346586],
    'NVIDIA-A100': [19.0787, 36.2182, 11.86993300846043]
}

# Liste des valeurs de BS
bs_values = [8, 16, 32]

# Liste pour stocker les résultats
results = []
runtime_results = []

# Boucle sur les valeurs de BS
for bs in bs_values:
    # Charger les données pour chaque BS
    data_A100 = pd.read_csv(f'data/consommation_energie_A100x1_offline_BS_{bs}.csv')
    data_jetson = pd.read_csv(f'data/consommation_energie_jetson_offline_BS_{bs}.csv')

    # Calculer les valeurs pour l'A100
    timestamp_A100 = data_A100['timestamp']
    gpu_power_A100 = data_A100['gpu_power']
    moyenne_gpu_power_A100_W = gpu_power_A100.mean()
    dernier_timestamp_A100 = timestamp_A100.iloc[-1]
    duree_heures_A100 = dernier_timestamp_A100 / 3600
    moyenne_gpu_power_A100_kW = moyenne_gpu_power_A100_W / 1000
    energie_totale_A100_kWh = moyenne_gpu_power_A100_kW * duree_heures_A100
    Co2_emissions_A100 = energie_totale_A100_kWh * EGM
    impact_total_A100_values = [Co2_emissions_A100 + ((duree_heures_A100 / seven_years) * value * 1000) for value in impact_conception['NVIDIA-A100']]

    # Calculer les valeurs pour le Jetson (AGX Xavier)
    timestamp_jetson = data_jetson['timestamp']
    gpu_power_jetson = data_jetson['gpu_power']
    moyenne_gpu_power_jetson_mW = gpu_power_jetson.mean()
    dernier_timestamp_jetson = timestamp_jetson.iloc[-1]
    duree_heures_jetson = dernier_timestamp_jetson / 3600
    moyenne_gpu_power_jetson_kW = moyenne_gpu_power_jetson_mW / 1_000_000
    energie_totale_jetson_kWh = moyenne_gpu_power_jetson_kW * duree_heures_jetson
    Co2_emissions_jetson = energie_totale_jetson_kWh * EGM
    impact_total_jetson_values = [Co2_emissions_jetson + ((duree_heures_jetson / seven_years) * value * 1000) for value in impact_conception['NVIDIA-AGX-Xavier']]

    # Ajouter les résultats à la liste
    results.append({
        'BS': bs,
        'GPU': 'NVIDIA-A100',
        'Impact Environnemental Total (g)': np.mean(impact_total_A100_values)
    })
    results.append({
        'BS': bs,
        'GPU': 'NVIDIA-AGX-Xavier',
        'Impact Environnemental Total (g)': np.mean(impact_total_jetson_values)
    })

    # Ajouter les résultats de runtime à la liste
    runtime_results.append({
        'BS': bs,
        'GPU': 'NVIDIA-A100',
        'Runtime (heures)': duree_heures_A100
    })
    runtime_results.append({
        'BS': bs,
        'GPU': 'NVIDIA-AGX-Xavier',
        'Runtime (heures)': duree_heures_jetson
    })

# Créer des DataFrames consolidés
df_results = pd.DataFrame(results)
df_runtime_results = pd.DataFrame(runtime_results)

# Tracer les graphiques
plt.figure(figsize=(6, 12))

# Graphique de l'impact environnemental
plt.subplot(2, 1, 1)
sns.lineplot(data=df_results, x='BS', y='Impact Environnemental Total (g)', hue='GPU', marker='o')
plt.title('Impact Environnemental des GPU en fonction de la taille du batch (BS)')
plt.xlabel('Taille du batch (BS)')
plt.ylabel('Impact Environnemental Total (g)')
plt.grid(True)

# Graphique du runtime
plt.subplot(2, 1, 2)
sns.lineplot(data=df_runtime_results, x='BS', y='Runtime (heures)', hue='GPU', marker='o')
plt.title('Runtime des GPU en fonction de la taille du batch (BS)')
plt.xlabel('Taille du batch (BS)')
plt.ylabel('Runtime (heures)')
plt.grid(True)

plt.tight_layout()
plt.show()
