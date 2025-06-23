import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import colors as mcolors

# Charger les données
data = pd.read_csv('g5k_edge.csv', delimiter=';')
df = pd.read_csv('mem_density.csv', delimiter=';')
mem_data = df.set_index('name')['gCO2/GB'].to_dict()
mem_data_2 = df.set_index('name')['density'].to_dict()
xls = pd.ExcelFile('Environmental-Footprint-ICs.xlsx')
df_gwp = xls.parse('GWP', header=3)
df_gwp = df_gwp.iloc[:, 1:]

names = data['names']
die_area = data['Die_area']
tdp = data['TDP']
gflops = data['GFLOPS']
price = data['price']
tech_node = data['Tech_node']
date = data['date']
mem = data['Memory']
mem_type = data['Mem_type']
foundry = data['foundry']
fu = data['FU']

hardware_dict = {name: [] for name in names}

df_gwp['iN\n[nm/mix]'] = pd.to_numeric(df_gwp['iN\n[nm/mix]'], errors='coerce')
df_gwp["Year"] = pd.to_numeric(df_gwp["Year"], errors='coerce')
df_gwp["Value"] = pd.to_numeric(df_gwp["Value"], errors='coerce')

for _, row in df_gwp.iterrows():
    category = row["Category"]
    value = row["Value"]

    if pd.isna(value):
        continue

    # Case 1: Category = Literature || Database
    if category in ["Literature", "Database"]:
        in_value = row['iN\n[nm/mix]']
        if not pd.isna(in_value):
            indices = data.index[data["Tech_node"] == in_value].tolist()
            for idx in indices:
                hardware_dict[names[idx]].append(value)

    # Case 2: Category = Industry || Roadmap
    elif category in ["Industry", "Roadmapping"]:
        year_value = row["Year"]
        author = row["Authors"]

        if not pd.isna(year_value):
            indices = data.index[data["date"] == year_value].tolist()

            # Case 2.1:  Category = Industry
            if category == "Industry":
                indices = [idx for idx in indices if data.loc[idx, "foundry"] == row["Authors"]]

            for idx in indices:
                hardware_dict[names[idx]].append(value)

# Créer une liste pour stocker toutes les valeurs d'impact environnemental
all_impact_values = []
hardware_names = []
hardware_fu = []

for i, name in enumerate(names):
    if name in hardware_dict:
        die_area_value = die_area[i]
        mem_name = mem_type[i]
        mem_size = mem[i]
        impact_values = [((val * die_area_value * 0.01) + ((mem_size * mem_data[mem_name]) / 1000))/((val * die_area_value*0.01)+((((mem_size*8)/mem_data_2[mem_name])*0.01)*val)) for val in hardware_dict[name]]

        all_impact_values.extend(impact_values)
        hardware_names.extend([name] * len(impact_values))
        hardware_fu.extend([fu[i]] * len(impact_values))

df_boxplot = pd.DataFrame({
    "Hardware": hardware_names,
    "Impact Environnemental": all_impact_values,
    "FU": hardware_fu
})

# Définir l'ordre des catégories FU
fu_order = ["Edge", "Gaming", "Desktop", "Large-scale"]

# Trier le DataFrame selon l'ordre des catégories FU
df_boxplot['FU'] = pd.Categorical(df_boxplot['FU'], categories=fu_order, ordered=True)
df_boxplot = df_boxplot.sort_values('FU')

# Créer le boxplot
plt.figure(figsize=(16, 10))
sns.boxplot(x="Hardware", y="Impact Environnemental", data=df_boxplot, palette="viridis")

# Ajouter des barres verticales en pointillé pour séparer les catégories
current_x = 0
mids = [0,1.5,5.5,12]
for idx,fu_category in enumerate(fu_order):
    subset = df_boxplot[df_boxplot["FU"] == fu_category]
    unique_hardware = subset["Hardware"].unique()
    plt.axvline(x=current_x + len(unique_hardware) - 0.5, color='black', linestyle='--')
    plt.text(mids[idx],1.2, fu_category, horizontalalignment='center', fontsize=15, color='black')
    current_x += len(unique_hardware)


plt.axhline(y=1, color='red', linestyle='-')
plt.ylabel('Ratio', fontsize=14)
plt.title('Ratio environmental impact Mem methodology°1 -> methodology°2', fontsize=16)
plt.xticks(rotation=90, fontsize=14)
plt.ylim(0,1.5)
plt.tight_layout()
plt.show()
