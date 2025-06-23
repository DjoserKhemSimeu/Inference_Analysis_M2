import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Définir l'émission de CO2 par kWh
EGM = 79.1  # gCO2/kWh
seven_years = 61320  # nombre d'heures en 7 ans

# Impacts de conception (données fournies)
impact_conception = {
    'NVIDIA-AGX-Xavier': [12.847420, 21.460000],
    'NVIDIA-A100': [27.678700, 20.469933, 44.818200],
    'NVIDIA-A40': [26.913520, 41.206800],
    'NVIDIA-Tesla-T4': [11.314983, 24.726000],
    'NVIDIA-RTX-2080-Ti': [11.645243, 30.199200],
    'NVIDIA-A5000': [18.273520, 32.566800],
    'NVIDIA-Quadro-RTX-8000': [20.0, 35.0]  # Exemple de valeurs pour le Quadro RTX 8000, à remplacer par les vraies données
}

# Liste des valeurs de BS
qc_values = [16, 32, 64, 128, 256]

# Liste pour stocker les résultats
results = []

# Boucle sur les valeurs de BS
for qc in qc_values:
    # Charger les données pour chaque BS
    data_A100 = pd.read_csv(f'data/consommation_energie_A100x1_single_BS_1_QC_{qc}.csv')
    data_A40 = pd.read_csv(f'data/consommation_energie_A40x1_single_BS_1_QC_{qc}.csv')
    data_T4 = pd.read_csv(f'data/consommation_energie_T4x1_single_BS_1_QC_{qc}.csv')
    data_jetson = pd.read_csv(f'data/consommation_energie_jetson_single_BS_1_QC_{qc}.csv')
    data_2080Ti = pd.read_csv(f'data/consommation_energie_2080Tix1_single_BS_1_QC_{qc}.csv')
    data_A5000 = pd.read_csv(f'data/consommation_energie_A5000x1_single_BS_1_QC_{qc}.csv')
    data_Quadro_RTX_8000 = pd.read_csv(f'data/consommation_energie_Quadro_RTX_8000x1_single_BS_1_QC_{qc}.csv')  # Charger les données pour le Quadro RTX 8000

    # Calculer les valeurs pour l'A100
    timestamp_A100 = data_A100['timestamp']
    gpu_power_A100 = data_A100['gpu_power']
    moyenne_gpu_power_A100_W = gpu_power_A100.mean()
    dernier_timestamp_A100 = timestamp_A100.iloc[-1]
    duree_heures_A100 = dernier_timestamp_A100/3600
    moyenne_gpu_power_A100_kW = moyenne_gpu_power_A100_W / 1000
    energie_totale_A100_kWh = moyenne_gpu_power_A100_kW * duree_heures_A100
    Co2_emissions_A100 = energie_totale_A100_kWh * EGM
    impact_total_A100_values = [Co2_emissions_A100 + ((duree_heures_A100 / seven_years) * value * 1000) for value in impact_conception['NVIDIA-A100']]

    # Calculer les valeurs pour l'A40
    timestamp_A40 = data_A40['timestamp']
    gpu_power_A40 = data_A40['gpu_power']
    area_A40=np.trapz(gpu_power_A40,timestamp_A40)

    moyenne_gpu_power_A40_W = gpu_power_A40.mean()
    dernier_timestamp_A40 = timestamp_A40.iloc[-1]
    duree_heures_A40 = dernier_timestamp_A40/3600
    moyenne_gpu_power_A40_kW = moyenne_gpu_power_A40_W / 1000
    print(area_A40)
    energie_totale_A40_kWh = moyenne_gpu_power_A40_kW *duree_heures_A40
    Co2_emissions_A40 = energie_totale_A40_kWh * EGM
    impact_total_A40_values = [Co2_emissions_A40 + ((duree_heures_A40 / seven_years) * value * 1000) for value in impact_conception['NVIDIA-A40']]

    # Calculer les valeurs pour le T4
    timestamp_T4 = data_T4['timestamp']
    gpu_power_T4 = data_T4['gpu_power']
    moyenne_gpu_power_T4_W = gpu_power_T4.mean()
    dernier_timestamp_T4 = timestamp_T4.iloc[-1]
    duree_heures_T4 = dernier_timestamp_T4/3600
    moyenne_gpu_power_T4_kW = moyenne_gpu_power_T4_W / 1000
    energie_totale_T4_kWh = moyenne_gpu_power_T4_kW * duree_heures_T4
    Co2_emissions_T4 = energie_totale_T4_kWh * EGM
    impact_total_T4_values = [Co2_emissions_T4 + ((duree_heures_T4 / seven_years) * value * 1000) for value in impact_conception['NVIDIA-Tesla-T4']]

    # Calculer les valeurs pour le Jetson (AGX Xavier)
    timestamp_jetson = data_jetson['timestamp']
    gpu_power_jetson = data_jetson['gpu_power']
    moyenne_gpu_power_jetson_mW = gpu_power_jetson.mean()
    dernier_timestamp_jetson = timestamp_jetson.iloc[-1]
    duree_heures_jetson = dernier_timestamp_jetson/3600
    moyenne_gpu_power_jetson_kW = moyenne_gpu_power_jetson_mW / 1_000_000
    energie_totale_jetson_kWh = moyenne_gpu_power_jetson_kW * duree_heures_jetson
    Co2_emissions_jetson = energie_totale_jetson_kWh * EGM
    impact_total_jetson_values = [Co2_emissions_jetson + ((duree_heures_jetson / seven_years) * value * 1000) for value in impact_conception['NVIDIA-AGX-Xavier']]

    # Calculer les valeurs pour la 2080Ti
    timestamp_2080Ti = data_2080Ti['timestamp']
    gpu_power_2080Ti = data_2080Ti['gpu_power']
    moyenne_gpu_power_2080Ti_W = gpu_power_2080Ti.mean()
    dernier_timestamp_2080Ti = timestamp_2080Ti.iloc[-1]
    duree_heures_2080Ti = dernier_timestamp_2080Ti/3600
    moyenne_gpu_power_2080Ti_kW = moyenne_gpu_power_2080Ti_W / 1000
    energie_totale_2080Ti_kWh = moyenne_gpu_power_2080Ti_kW * duree_heures_2080Ti
    Co2_emissions_2080Ti = energie_totale_2080Ti_kWh * EGM
    impact_total_2080Ti_values = [Co2_emissions_2080Ti + ((duree_heures_2080Ti / seven_years) * value * 1000) for value in impact_conception['NVIDIA-RTX-2080-Ti']]

    # Calculer les valeurs pour la A5000
    timestamp_A5000 = data_A5000['timestamp']
    gpu_power_A5000 = data_A5000['gpu_power']
    moyenne_gpu_power_A5000_W = gpu_power_A5000.mean()
    dernier_timestamp_A5000 = timestamp_A5000.iloc[-1]
    duree_heures_A5000 = dernier_timestamp_A5000/3600
    moyenne_gpu_power_A5000_kW = moyenne_gpu_power_A5000_W / 1000
    energie_totale_A5000_kWh = moyenne_gpu_power_A5000_kW * duree_heures_A5000
    Co2_emissions_A5000 = energie_totale_A5000_kWh * EGM
    impact_total_A5000_values = [Co2_emissions_A5000 + ((duree_heures_A5000 / seven_years) * value * 1000) for value in impact_conception['NVIDIA-A5000']]

    # Calculer les valeurs pour le Quadro RTX 8000
    timestamp_Quadro_RTX_8000 = data_Quadro_RTX_8000['timestamp']
    gpu_power_Quadro_RTX_8000 = data_Quadro_RTX_8000['gpu_power']
    moyenne_gpu_power_Quadro_RTX_8000_W = gpu_power_Quadro_RTX_8000.mean()
    dernier_timestamp_Quadro_RTX_8000 = timestamp_Quadro_RTX_8000.iloc[-1]
    duree_heures_Quadro_RTX_8000 = dernier_timestamp_Quadro_RTX_8000/3600
    moyenne_gpu_power_Quadro_RTX_8000_kW = moyenne_gpu_power_Quadro_RTX_8000_W / 1000
    energie_totale_Quadro_RTX_8000_kWh = moyenne_gpu_power_Quadro_RTX_8000_kW * duree_heures_Quadro_RTX_8000
    Co2_emissions_Quadro_RTX_8000 = energie_totale_Quadro_RTX_8000_kWh * EGM
    impact_total_Quadro_RTX_8000_values = [Co2_emissions_Quadro_RTX_8000 + ((duree_heures_Quadro_RTX_8000 / seven_years) * value * 1000) for value in impact_conception['NVIDIA-Quadro-RTX-8000']]
    # Ajouter les résultats à la liste
    results.append({
        'QC': qc,
        'GPU': 'NVIDIA-A100',
        'Impact Environnemental Total (g)': np.mean(impact_total_A100_values),
        'category': 'Large-scale'
    })
    results.append({
        'QC': qc,
        'GPU': 'NVIDIA-AGX-Xavier',
        'Impact Environnemental Total (g)': np.mean(impact_total_jetson_values),
        'category': 'Edge'
    })
    results.append({
        'QC': qc,
        'GPU': 'NVIDIA-A40',
        'Impact Environnemental Total (g)': np.mean(impact_total_A40_values),
        'category': 'Large-scale'
    })
    results.append({
        'QC': qc,
        'GPU': 'NVIDIA-Tesla-T4',
        'Impact Environnemental Total (g)': np.mean(impact_total_T4_values),
        'category': 'Desktop'
    })
    results.append({
        'QC': qc,
        'GPU': 'NVIDIA-RTX-2080-Ti',
        'Impact Environnemental Total (g)': np.mean(impact_total_2080Ti_values),
        'category': 'Gaming'
    })
    results.append({
        'QC': qc,
        'GPU': 'NVIDIA-A5000',
        'Impact Environnemental Total (g)': np.mean(impact_total_A5000_values),
        'category': 'Desktop'
    })
    results.append({
        'QC': qc,
        'GPU': 'NVIDIA-Quadro-RTX-8000',
        'Impact Environnemental Total (g)': np.mean(impact_total_Quadro_RTX_8000_values),
        'category': 'Desktop'
    })

# Créer un DataFrame consolidé pour l'impact environnemental
df_results = pd.DataFrame(results)

# Charger les données de latence
latency_data = pd.read_csv('data/latency_single.csv', delimiter=';')

# Ajouter une colonne 'category' à latency_data
latency_data['category'] = latency_data['GPU'].map({
    'NVIDIA-A100': 'Large-scale',
    'NVIDIA-AGX-Xavier': 'Edge',
    'NVIDIA-A40': 'Large-scale',
    'NVIDIA-Tesla-T4': 'Desktop',
    'NVIDIA-RTX-2080-Ti': 'Gaming',
    'NVIDIA-A5000': 'Desktop',
    'NVIDIA-Quadro-RTX-8000': 'Desktop'
})

#print(latency_data)
#print(df_results)

# Définir les formes des points en fonction de la catégorie
markers = {'Edge': 'o', 'Gaming': 's', 'Desktop': 'D', 'Large-scale': 'X'}

# Tracer les graphiques
plt.figure(figsize=(6, 12))

# Graphique de l'impact environnemental
plt.subplot(2, 1, 1)
sns.lineplot(data=df_results, x='QC', y='Impact Environnemental Total (g)', hue='GPU', style='category', markers=markers, dashes=False)
plt.title('Global warming potential of the inference in function of the number of queries')
plt.xlabel('Number of queries')
plt.ylabel('GWP (g CO2 eq)')
plt.grid(True)

# Graphique de la latence
plt.subplot(2, 1, 2)
sns.lineplot(data=latency_data, x='QC', y='latency(ms)', hue='GPU', style='category', markers=markers, dashes=False)
plt.title('90th percentile query latency in function of the number of queries')
plt.xlabel('Number of queries')
plt.ylabel('query latency (ms)')
plt.grid(True)

plt.tight_layout()
plt.show()
