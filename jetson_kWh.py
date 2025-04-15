import pandas as pd

# Charger les données depuis le fichier CSV
data = pd.read_csv('data/consommation_energie_jetson.csv')

EGM=12#gCO2/kWh
timestamp = data['timestamp']
gpu_power = data['gpu_power']


moyenne_gpu_power_mW = gpu_power.mean()


dernier_timestamp = timestamp.iloc[-1]


duree_heures = dernier_timestamp / 3600


moyenne_gpu_power_kW = moyenne_gpu_power_mW / 1000000


energie_totale_kWh = moyenne_gpu_power_kW * duree_heures

Co2_emissions = energie_totale_kWh * EGM

print(f"Moyenne de la consommation GPU (mW): {moyenne_gpu_power_mW}")
print(f"Durée totale (heures): {duree_heures}")
print(f"Énergie totale consommée (kWh): {energie_totale_kWh}")
print(f"émission équivalent CO2 (g): {Co2_emissions}")
