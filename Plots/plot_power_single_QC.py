import pandas as pd
import matplotlib.pyplot as plt

# Charger les données depuis les fichiers CSV
#data_A100_BS_1_EL_31__ = pd.read_csv('data/consommation_energie_A100x1_single_BS_1_EL_31__.csv')
#data_A100_BS_4_EL_31__ = pd.read_csv('data/consommation_energie_A100x1_single_BS_4_EL_31__.csv')
#data_A100_BS_1_EL_15__ = pd.read_csv('data/consommation_energie_A100x1_single_BS_1_EL_15__.csv')
#data_A100_BS_1_EL_17_ = pd.read_csv('data/consommation_energie_A100x1_single_BS_1_EL_1.7__.csv')
#data_A100_BS_4_EL_17_ = pd.read_csv('data/consommation_energie_A100x1_single_BS_4_EL_1.7__.csv')
#data_A100_BS_1_EL_31__2 = pd.read_csv('data/consommation_energie_A100x1_single_BS_1_EL_31__2.csv')
data_A100_BS_32_QC_16 = pd.read_csv('data/consommation_energie_A100x1_single_BS_32_QC_16.csv')
data_A100_BS_32_QC_32 = pd.read_csv('data/consommation_energie_A100x1_single_BS_32_QC_32.csv')
data_A100_BS_32_QC_64 = pd.read_csv('data/consommation_energie_A100x1_single_BS_32_QC_64.csv')
data_A100_BS_32_QC_128 = pd.read_csv('data/consommation_energie_A100x1_single_BS_32_QC_128.csv')
data_A100_BS_32_QC_256 = pd.read_csv('data/consommation_energie_A100x1_single_BS_32_QC_256.csv')




#data_jetson_BS_1_EL_31__ = pd.read_csv('data/consommation_energie_jetson_single_BS_1_EL_31__.csv')
#data_jetson_BS_8_EL_31__ = pd.read_csv('data/consommation_energie_jetson_single_BS_8_EL_31__.csv')
#data_jetson_BS_4_EL_31__ = pd.read_csv('data/consommation_energie_jetson_single_BS_4_EL_31__.csv')
data_jetson_BS_32_QC_128 = pd.read_csv('data/consommation_energie_jetson_single_BS_32_QC_128.csv')
data_jetson_BS_32_QC_64 = pd.read_csv('data/consommation_energie_jetson_single_BS_32_QC_64.csv')
data_jetson_BS_32_QC_256 = pd.read_csv('data/consommation_energie_jetson_single_BS_32_QC_256.csv')
data_jetson_BS_32_QC_32 = pd.read_csv('data/consommation_energie_jetson_single_BS_32_QC_32.csv')
data_jetson_BS_32_QC_16 = pd.read_csv('data/consommation_energie_jetson_single_BS_32_QC_16.csv')

# Supposons que les colonnes soient nommées 'timestamp' et 'gpu_power'
# Remplacez 'timestamp' et 'gpu_power' par les noms réels de vos colonnes si nécessaire
#temps_A100_BS_1_EL_31__ = data_A100_BS_1_EL_31__['timestamp']
#energie_A100_W_BS_1_EL_31__ = data_A100_BS_1_EL_31__['gpu_power']

# temps_A100_BS_4_EL_31__ = data_A100_BS_4_EL_31__['timestamp']
# energie_A100_W_BS_4_EL_31__ = data_A100_BS_4_EL_31__['gpu_power']

# temps_A100_BS_1_EL_15__ = data_A100_BS_1_EL_15__['timestamp']
# energie_A100_W_BS_1_EL_15__ = data_A100_BS_1_EL_15__['gpu_power']

# temps_A100_BS_1_EL_17_ = data_A100_BS_1_EL_17_['timestamp']
# energie_A100_W_BS_1_EL_17_ = data_A100_BS_1_EL_17_['gpu_power']

# temps_A100_BS_4_EL_17_ = data_A100_BS_4_EL_17_['timestamp']
# energie_A100_W_BS_4_EL_17_ = data_A100_BS_4_EL_17_['gpu_power']

# temps_A100_BS_1_EL_31__2 = data_A100_BS_1_EL_31__2['timestamp']
# energie_A100_W_BS_1_EL_31__2 = data_A100_BS_1_EL_31__2['gpu_power']

# temps_A100_BS_8_EL_31__ = data_A100_BS_8_EL_31__['timestamp']
# energie_A100_W_BS_8_EL_31__ = data_A100_BS_8_EL_31__['gpu_power']

temps_A100_BS_32_QC_16 = data_A100_BS_32_QC_16['timestamp']
energie_A100_W_BS_32_QC_16 = data_A100_BS_32_QC_16['gpu_power']


temps_A100_BS_32_QC_32 = data_A100_BS_32_QC_32['timestamp']
energie_A100_W_BS_32_QC_32 = data_A100_BS_32_QC_32['gpu_power']

temps_A100_BS_32_QC_64 = data_A100_BS_32_QC_64['timestamp']
energie_A100_W_BS_32_QC_64 = data_A100_BS_32_QC_64['gpu_power']

temps_A100_BS_32_QC_128 = data_A100_BS_32_QC_128['timestamp']
energie_A100_W_BS_32_QC_128 = data_A100_BS_32_QC_128['gpu_power']

temps_A100_BS_32_QC_256 = data_A100_BS_32_QC_256['timestamp']
energie_A100_W_BS_32_QC_256 = data_A100_BS_32_QC_256['gpu_power']
# temps_jetson_BS_1_EL_31__ = data_jetson_BS_1_EL_31__['timestamp']
# energie_jetson_mW_BS_1_EL_31__ = data_jetson_BS_1_EL_31__['gpu_power']/1000

# temps_jetson_BS_8_EL_31__ = data_jetson_BS_8_EL_31__['timestamp']
# energie_jetson_mW_BS_8_EL_31__ = data_jetson_BS_8_EL_31__['gpu_power']/1000

# temps_jetson_BS_4_EL_31__ = data_jetson_BS_4_EL_31__['timestamp']
# energie_jetson_mW_BS_4_EL_31__ = data_jetson_BS_4_EL_31__['gpu_power']/1000

temps_jetson_BS_32_QC_128 = data_jetson_BS_32_QC_128['timestamp']
energie_jetson_mW_BS_32_QC_128 = data_jetson_BS_32_QC_128['gpu_power']/1000

temps_jetson_BS_32_QC_64 = data_jetson_BS_32_QC_64['timestamp']
energie_jetson_mW_BS_32_QC_64 = data_jetson_BS_32_QC_64['gpu_power']/1000

temps_jetson_BS_32_QC_32 = data_jetson_BS_32_QC_32['timestamp']
energie_jetson_mW_BS_32_QC_32 = data_jetson_BS_32_QC_32['gpu_power']/1000

temps_jetson_BS_32_QC_16 = data_jetson_BS_32_QC_16['timestamp']
energie_jetson_mW_BS_32_QC_16 = data_jetson_BS_32_QC_16['gpu_power']/1000

temps_jetson_BS_32_QC_256 = data_jetson_BS_32_QC_256['timestamp']
energie_jetson_mW_BS_32_QC_256 = data_jetson_BS_32_QC_256['gpu_power']/1000

# Tracer les données
plt.figure(figsize=(10, 6))
#plt.plot(temps_A100_BS_1_EL_31__, energie_A100_W_BS_1_EL_31__, linestyle='-', color='blue', label='A100_BS_1_EL_31__')
#plt.plot(temps_A100_BS_1_EL_15__, energie_A100_W_BS_1_EL_15__, linestyle='-', color='skyblue', label='A100_BS_1_EL_15__')
#plt.plot(temps_A100_BS_1_EL_17_, energie_A100_W_BS_1_EL_17_, linestyle='-', color='cyan', label='A100_BS_1_EL_17_')
#plt.plot(temps_A100_BS_4_EL_17_, energie_A100_W_BS_4_EL_17_, linestyle='-', color='grey', label='A100_BS_4_EL_17_')
#plt.plot(temps_A100_BS_4_EL_31__, energie_A100_W_BS_4_EL_31__, linestyle='-', color='orange', label='A100_BS_4_EL_31__')
plt.plot(temps_A100_BS_32_QC_16, energie_A100_W_BS_32_QC_16, linestyle='-', color='pink', label='A100_BS_32_QC_16')
plt.plot(temps_A100_BS_32_QC_32, energie_A100_W_BS_32_QC_32, linestyle='-', color='purple', label='A100_BS_32_QC_32')
plt.plot(temps_A100_BS_32_QC_64, energie_A100_W_BS_32_QC_64, linestyle='-', color='green', label='A100_BS_32_QC_64')
plt.plot(temps_A100_BS_32_QC_128, energie_A100_W_BS_32_QC_128, linestyle='-', color='blue', label='A100_BS_32_QC_128')
plt.plot(temps_A100_BS_32_QC_256, energie_A100_W_BS_32_QC_256, linestyle='-', color='orange', label='A100_BS_32_QC_256')
#plt.plot(temps_A100_BS_1_EL_31__2, energie_A100_W_BS_1_EL_31__2, linestyle='-', color='skyblue', label='A100_BS_1_EL_31__2')
#plt.plot(temps_A100_BS_8_EL_31__, energie_A100_W_BS_8_EL_31__, linestyle='-', color='green', label='A100_BS_8_EL_31__')
# plt.plot(temps_jetson_BS_1_EL_31__, energie_jetson_mW_BS_1_EL_31__, linestyle='-', color='red', label='Jetson_BS_1_EL_31__') 
# plt.plot(temps_jetson_BS_8_EL_31__, energie_jetson_mW_BS_8_EL_31__, linestyle='-', color='yellow', label='Jetson_BS_8_EL_31__')
# plt.plot(temps_jetson_BS_4_EL_31__, energie_jetson_mW_BS_4_EL_31__, linestyle='-', color='black', label='Jetson_BS_4_EL_31__')
plt.plot(temps_jetson_BS_32_QC_128, energie_jetson_mW_BS_32_QC_128, linestyle='-', color='blue', label='Jetson_BS_32_QC_128')
plt.plot(temps_jetson_BS_32_QC_64, energie_jetson_mW_BS_32_QC_64, linestyle='-', color='green', label='Jetson_BS_32_QC_64')
plt.plot(temps_jetson_BS_32_QC_32, energie_jetson_mW_BS_32_QC_32, linestyle='-', color='purple', label='Jetson_BS_32_QC_32')
plt.plot(temps_jetson_BS_32_QC_16, energie_jetson_mW_BS_32_QC_16, linestyle='-', color='pink', label='Jetson_BS_32_QC_16')
plt.plot(temps_jetson_BS_32_QC_256, energie_jetson_mW_BS_32_QC_256, linestyle='-', color='orange', label='Jetson_BS_32_QC_256')
plt.title('Instantaneous power required by GPUs-Single-stream')
plt.xlabel('Time (s)')
plt.ylabel('Power (W)')
plt.grid(True)
plt.legend()
plt.show()
