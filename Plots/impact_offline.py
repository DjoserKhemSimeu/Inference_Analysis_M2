import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données depuis les fichiers CSV
data_A100 = pd.read_csv('data/consommation_energie_A100x1.csv')
data_jetson = pd.read_csv('data/consommation_energie_jetson.csv')

# Définir l'émission de CO2 par kWh
EGM = 79.1  # gCO2/kWh
four_years = 35040  # nombre d'heures en 4 ans

# Calculer les valeurs pour l'A100
timestamp_A100 = data_A100['timestamp']
gpu_power_A100 = data_A100['gpu_power']

moyenne_gpu_power_A100_W = gpu_power_A100.mean()
dernier_timestamp_A100 = timestamp_A100.iloc[-1]
duree_heures_A100 = dernier_timestamp_A100 / 3600
moyenne_gpu_power_A100_kW = moyenne_gpu_power_A100_W / 1000
energie_totale_A100_kWh = moyenne_gpu_power_A100_kW * duree_heures_A100
Co2_emissions_A100 = energie_totale_A100_kWh * EGM

# Calculer les valeurs pour le Jetson (AGX Xavier)
timestamp_jetson = data_jetson['timestamp']
gpu_power_jetson = data_jetson['gpu_power']

moyenne_gpu_power_jetson_mW = gpu_power_jetson.mean()
dernier_timestamp_jetson = timestamp_jetson.iloc[-1]
duree_heures_jetson = dernier_timestamp_jetson / 3600
moyenne_gpu_power_jetson_kW = moyenne_gpu_power_jetson_mW / 1_000_000
energie_totale_jetson_kWh = moyenne_gpu_power_jetson_kW * duree_heures_jetson
Co2_emissions_jetson = energie_totale_jetson_kWh * EGM

# Impacts de conception (données fournies)
impact_conception = {
    'NVIDIA-AGX-Xavier': [13.716, 5.103420289346586],
    'NVIDIA-A100': [19.0787, 36.2182, 11.86993300846043]
}

# Calculer l'impact environnemental total pour chaque valeur individuelle
impact_total_A100_values = [Co2_emissions_A100 + ((duree_heures_A100 / four_years) * value * 1000) for value in impact_conception['NVIDIA-A100']]
impact_total_jetson_values = [Co2_emissions_jetson + ((duree_heures_jetson / four_years) * value * 1000) for value in impact_conception['NVIDIA-AGX-Xavier']]

# Afficher les résultats
print("A100:")
print(f"Moyenne de la consommation GPU (W): {moyenne_gpu_power_A100_W}")
print(f"Durée totale (heures): {duree_heures_A100}")
print(f"Énergie totale consommée (kWh): {energie_totale_A100_kWh}")
print(f"Émission équivalent CO2 inference (g): {Co2_emissions_A100}")
print(f"Émission équivalent CO2 manufacturing (g): {np.mean(impact_total_A100_values-Co2_emissions_A100)}")
print(f"Impact environnemental total (g): {np.mean(impact_total_A100_values)}")

print("\nJetson (AGX Xavier):")
print(f"Moyenne de la consommation GPU (mW): {moyenne_gpu_power_jetson_mW}")
print(f"Durée totale (heures): {duree_heures_jetson}")
print(f"Énergie totale consommée (kWh): {energie_totale_jetson_kWh}")
print(f"Émission équivalent CO2 inference (g): {Co2_emissions_jetson}")
print(f"Émission équivalent CO2 manufacturing (g): {np.mean(impact_total_jetson_values-Co2_emissions_jetson)}")
print(f"Impact environnemental total (g): {np.mean(impact_total_jetson_values)}")

# Créer un DataFrame pour le boxplot en utilisant les impacts environnementaux totaux
data_boxplot = {
    'GPU': ['NVIDIA-AGX-Xavier'] * len(impact_total_jetson_values) + ['NVIDIA-A100'] * len(impact_total_A100_values),
    'Impact Environnemental Total (g)': impact_total_jetson_values + impact_total_A100_values
}
df_boxplot = pd.DataFrame(data_boxplot)

# Créer un DataFrame pour le bar plot des pourcentages de contribution
data_barplot = {
    'GPU': ['NVIDIA-AGX-Xavier', 'NVIDIA-A100'],
    'Impact Conception (%)': [
        np.mean((np.array(impact_total_jetson_values) - Co2_emissions_jetson) / np.array(impact_total_jetson_values)) * 100,
        np.mean((np.array(impact_total_A100_values) - Co2_emissions_A100) / np.array(impact_total_A100_values)) * 100
    ],
    'Impact Inference (%)': [
        100 - np.mean((np.array(impact_total_jetson_values) - Co2_emissions_jetson) / np.array(impact_total_jetson_values)) * 100,
        100 - np.mean((np.array(impact_total_A100_values) - Co2_emissions_A100) / np.array(impact_total_A100_values)) * 100
    ]
}
df_barplot = pd.DataFrame(data_barplot)

# Afficher les graphiques
plt.figure(figsize=(10, 12))

# Boxplot
plt.subplot(2, 1, 1)
sns.boxplot(x='GPU', y='Impact Environnemental Total (g)', data=df_boxplot)
plt.title('Impact Environnemental Global des GPU')

# Barplot
plt.subplot(2, 1, 2)
df_barplot.set_index('GPU').plot(kind='bar', stacked=True, ax=plt.gca())
plt.title('Pourcentages de Contribution de l\'Impact Environnemental')
plt.ylabel('Pourcentage (%)')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
