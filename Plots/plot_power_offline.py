import pandas as pd
import matplotlib.pyplot as plt

# Charger les données depuis les fichiers CSV
data_A100 = pd.read_csv('data/consommation_energie_A100x1_offline_BS_8.csv')
data_A100_BS_16 = pd.read_csv('data/consommation_energie_A100x1_offline_BS_16.csv')
data_A100_BS_32 = pd.read_csv('data/consommation_energie_A100x1_offline_BS_32.csv')
data_jetson = pd.read_csv('data/consommation_energie_jetson_offline_BS_8.csv')
data_jetson_BS_16 = pd.read_csv('data/consommation_energie_jetson_offline_BS_16.csv')
data_jetson_BS_32 = pd.read_csv('data/consommation_energie_jetson_offline_BS_32.csv')
# Supposons que les colonnes soient nommées 'timestamp' et 'gpu_power'
# Remplacez 'timestamp' et 'gpu_power' par les noms réels de vos colonnes si nécessaire
temps_A100_BS_16 = data_A100_BS_16['timestamp']
energie_A100_W_BS_16 = data_A100_BS_16['gpu_power']

temps_A100_BS_32 = data_A100_BS_32['timestamp']
energie_A100_W_BS_32 = data_A100_BS_32['gpu_power']

temps_A100 = data_A100['timestamp']
energie_A100_W = data_A100['gpu_power']

temps_jetson = data_jetson['timestamp']
energie_jetson_mW = data_jetson['gpu_power']/1000

temps_jetson_BS_16 = data_jetson_BS_16['timestamp']
energie_jetson_mW_BS_16 = data_jetson_BS_16['gpu_power']/1000

temps_jetson_BS_32 = data_jetson_BS_32['timestamp']
energie_jetson_mW_BS_32 = data_jetson_BS_32['gpu_power']/1000
# Tracer les données
plt.figure(figsize=(10, 6))
plt.plot(temps_A100, energie_A100_W, linestyle='-', color='blue', label='A100_BS_8')
plt.plot(temps_A100_BS_16, energie_A100_W_BS_16, linestyle='-', color='green', label='A100_BS_16')
plt.plot(temps_A100_BS_32, energie_A100_W_BS_32, linestyle='-', color='purple', label='A100_BS_32')
plt.plot(temps_jetson, energie_jetson_mW, linestyle='-', color='red', label='Jetson_BS_8')
plt.plot(temps_jetson_BS_16, energie_jetson_mW_BS_16, linestyle='-', color='orange', label='Jetson_BS_16')
plt.plot(temps_jetson_BS_32, energie_jetson_mW_BS_32, linestyle='-', color='grey', label='Jetson_BS_32')
plt.title('Instantaneous power required by GPUs-Offline')
plt.xlabel('Time (s)')
plt.ylabel('Power (W)')
plt.grid(True)
plt.legend()
plt.show()
