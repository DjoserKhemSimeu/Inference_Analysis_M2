
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('../Doc/g5k_edge.csv', delimiter=';')
df = pd.read_csv('../Doc/mem_density.csv', delimiter=';')
mem_data = df.set_index('name')['gCO2/GB'].to_dict()
mem_data_2 = df.set_index('name')['density'].to_dict()
xls = pd.ExcelFile('../Doc/Environmental-Footprint-ICs.xlsx')
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

memory_impacts_1 = []
processing_impacts_1 = []
hardware_names = []
hardware_fu = []

for i, name in enumerate(names):
    if name in hardware_dict:
        die_area_value = die_area[i]
        mem_name = mem_type[i]
        mem_size = mem[i]

        processing_impact_1 = np.mean([val * die_area_value * 0.01 for val in hardware_dict[name]])
        memory_impact_1 =(((mem_size * 8) / mem_data_2[mem_name]) * 0.01) * np.mean(hardware_dict[name])

        memory_impacts_1.append(memory_impact_1)
        processing_impacts_1.append(processing_impact_1)
        hardware_names.append(name)
        hardware_fu.append(fu[i])

total_impacts_1 = np.array(memory_impacts_1) + np.array(processing_impacts_1)
memory_percentages_1 = (np.array(memory_impacts_1) / total_impacts_1) * 100
processing_percentages_1 = (np.array(processing_impacts_1) / total_impacts_1) * 100

memory_impacts_2 = []
processing_impacts_2 = []

for i, name in enumerate(names):
    if name in hardware_dict:
        die_area_value = die_area[i]
        mem_name = mem_type[i]
        mem_size = mem[i]

        processing_impact_2 = np.mean([val * die_area_value * 0.01 for val in hardware_dict[name]])
        memory_impact_2 = (mem_size * mem_data[mem_name]) / 1000

        memory_impacts_2.append(memory_impact_2)
        processing_impacts_2.append(processing_impact_2)

total_impacts_2 = np.array(memory_impacts_2) + np.array(processing_impacts_2)
memory_percentages_2 = (np.array(memory_impacts_2) / total_impacts_2) * 100
processing_percentages_2 = (np.array(processing_impacts_2) / total_impacts_2) * 100

df_percentages_1 = pd.DataFrame({
    "Hardware": hardware_names,
    "Memory Impact (%)": memory_percentages_1,
    "Processing Impact (%)": processing_percentages_1,
    "FU": hardware_fu
})

df_percentages_2 = pd.DataFrame({
    "Hardware": hardware_names,
    "Memory Impact (%)": memory_percentages_2,
    "Processing Impact (%)": processing_percentages_2,
    "FU": hardware_fu
})

fu_order = ["Edge", "Gaming", "Desktop", "Large-scale"]

df_percentages_1['FU'] = pd.Categorical(df_percentages_1['FU'], categories=fu_order, ordered=True)
df_percentages_1 = df_percentages_1.sort_values('FU')

df_percentages_2['FU'] = pd.Categorical(df_percentages_2['FU'], categories=fu_order, ordered=True)
df_percentages_2 = df_percentages_2.sort_values('FU')

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 12), sharex=True)
bar_width = 0.5
index = np.arange(len(df_percentages_1))

bar1 = axes[0].bar(index, df_percentages_1["Memory Impact (%)"], bar_width, label='Memory chip Impact', color='skyblue')
bar2 = axes[0].bar(index, df_percentages_1["Processing Impact (%)"], bar_width, bottom=df_percentages_1["Memory Impact (%)"], label='Processing chip Impact', color='lightcoral')

current_x = 0
mids = [0,2.5,6.5,13]
for idx, fu_category in enumerate(fu_order):
    subset = df_percentages_1[df_percentages_1["FU"] == fu_category]
    unique_hardware = subset["Hardware"].unique()
    if idx<len(fu_order)-1:
        axes[0].axvline(x=current_x + len(unique_hardware) - 0.5, color='black', linestyle='--')
    axes[0].text(mids[idx], 100, fu_category, horizontalalignment='center', fontsize=14, color='black')
    current_x += len(unique_hardware)

axes[0].set_ylabel('Percentage of Impact', fontsize=16)
axes[0].set_title('Methodology°1 : Percentage Contribution of Memory and Processing Chips', fontsize=18)
axes[0].legend()

bar3 = axes[1].bar(index, df_percentages_2["Memory Impact (%)"], bar_width, label='Memory chip Impact', color='skyblue')
bar4 = axes[1].bar(index, df_percentages_2["Processing Impact (%)"], bar_width, bottom=df_percentages_2["Memory Impact (%)"], label='Processing chip Impact', color='lightcoral')

current_x = 0
for idx, fu_category in enumerate(fu_order):
    subset = df_percentages_2[df_percentages_2["FU"] == fu_category]
    unique_hardware = subset["Hardware"].unique()
    if idx<len(fu_order)-1:
        axes[1].axvline(x=current_x + len(unique_hardware) - 0.5, color='black', linestyle='--')
    #axes[1].text(mids[idx], 100, fu_category, horizontalalignment='center', fontsize=15, color='black')
    current_x += len(unique_hardware)

axes[1].set_xlabel('Hardware', fontsize=16)
axes[1].set_ylabel('Percentage of Impact', fontsize=16)
axes[1].set_title('Methodology°2: Percentage Contribution of Memory and Processing Chips', fontsize=18)


plt.xticks(index, df_percentages_1["Hardware"], rotation=45, fontsize=16)
plt.tight_layout()
plt.show()
