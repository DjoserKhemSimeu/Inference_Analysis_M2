import pandas as pd
import matplotlib.pyplot as plt

# Charger les données depuis les fichiers CSV
data_A100 = pd.read_csv('data/consommation_energie_A100x1_server_BS_16_QPS_360.csv')
data_A100_BS_24_QPS_360 = pd.read_csv('data/consommation_energie_A100x1_server_BS_24_QPS_360.csv')
data_A100_BS_8_QPS_360 = pd.read_csv('data/consommation_energie_A100x1_server_BS_8_QPS_360.csv')
data_A100_BS_16_QPS_720 = pd.read_csv('data/consommation_energie_A100x1_server_BS_16_QPS_720.csv')
data_jetson = pd.read_csv('data/consommation_energie_jetson_server_BS_16_QPS_360.csv')
data_jetson_BS_8_QPS_360 = pd.read_csv('data/consommation_energie_jetson_server_BS_8_QPS_360.csv')
data_jetson_BS_24_QPS_360 = pd.read_csv('data/consommation_energie_jetson_server_BS_24_QPS_360.csv')
data_jetson_BS_16_QPS_720 = pd.read_csv('data/consommation_energie_jetson_server_BS_16_QPS_720.csv')


# Supposons que les colonnes soient nommées 'timestamp' et 'gpu_power'
# Remplacez 'timestamp' et 'gpu_power' par les noms réels de vos colonnes si nécessaire
temps_A100 = data_A100['timestamp']
energie_A100_W = data_A100['gpu_power']

temps_A100_BS_16_QPS_720 = data_A100_BS_16_QPS_720['timestamp']
energie_A100_W_BS_16_QPS_720 = data_A100_BS_16_QPS_720['gpu_power']

temps_A100_BS_24_QPS_360 = data_A100_BS_24_QPS_360['timestamp']
energie_A100_W_BS_24_QPS_360 = data_A100_BS_24_QPS_360['gpu_power']

temps_A100_BS_8_QPS_360 = data_A100_BS_8_QPS_360['timestamp']
energie_A100_W_BS_8_QPS_360 = data_A100_BS_8_QPS_360['gpu_power']

temps_jetson = data_jetson['timestamp']
energie_jetson_mW = data_jetson['gpu_power']/1000

temps_jetson_BS_8_QPS_360 = data_jetson_BS_8_QPS_360['timestamp']
energie_jetson_mW_BS_8_QPS_360 = data_jetson_BS_8_QPS_360['gpu_power']/1000

temps_jetson_BS_24_QPS_360 = data_jetson_BS_24_QPS_360['timestamp']
energie_jetson_mW_BS_24_QPS_360 = data_jetson_BS_24_QPS_360['gpu_power']/1000

temps_jetson_BS_16_QPS_720 = data_jetson_BS_16_QPS_720['timestamp']
energie_jetson_mW_BS_16_QPS_720 = data_jetson_BS_16_QPS_720['gpu_power']/1000

# Tracer les données
plt.figure(figsize=(10, 6))
plt.plot(temps_A100, energie_A100_W, linestyle='-', color='blue', label='A100_BS_16_QPS_360')
plt.plot(temps_A100_BS_16_QPS_720, energie_A100_W_BS_16_QPS_720, linestyle='-', color='purple', label='A100_BS_16_QPS_720')
plt.plot(temps_A100_BS_24_QPS_360, energie_A100_W_BS_24_QPS_360, linestyle='-', color='green', label='A100_BS_24_QPS_360')
plt.plot(temps_A100_BS_8_QPS_360, energie_A100_W_BS_8_QPS_360, linestyle='-', color='skyblue', label='A100_BS_8_QPS_360')
plt.plot(temps_jetson, energie_jetson_mW, linestyle='-', color='red', label='Jetson_BS_16_QPS_360')
plt.plot(temps_jetson_BS_8_QPS_360, energie_jetson_mW_BS_8_QPS_360, linestyle='-', color='orange', label='Jetson_BS_8_QPS_360')
plt.plot(temps_jetson_BS_24_QPS_360, energie_jetson_mW_BS_24_QPS_360, linestyle='-', color='grey', label='Jetson_BS_24_QPS_360')
plt.plot(temps_jetson_BS_16_QPS_720, energie_jetson_mW_BS_16_QPS_720, linestyle='-', color='purple', label='Jetson_BS_16_QPS_720')
plt.title(' Instantenous power required by GPUs-Server')
plt.xlabel('Time (s)')
plt.ylabel('Power (W)')
plt.grid(True)
plt.legend()
plt.show()
