import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from adjustText import adjust_text
from matplotlib import colors as mcolors


data = pd.read_csv('../Doc/g5k_edge.csv', delimiter=';')
df = pd.read_csv('../Doc/mem_density.csv', delimiter=';')
mem_data = df.set_index('name')['density'].to_dict()
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
mem_type = data ['Mem_type']
foundry = data['foundry']


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


hardware_means = []
hardware_tdp = []
hardware_names = []
hardware_errors = []
hardware_dates = []

for i, name in enumerate(names):
    if name in hardware_dict:
        die_area_value = die_area[i]
        mem_name = mem_type[i]
        mem_size = mem[i]
        impact_values = [(val * die_area_value*0.01)+((((mem_size*8)/mem_data[mem_name])*0.01)*val) for val in hardware_dict[name]]
        print(name,((mem_size*8)/mem_data[mem_name])*0.01)

        mean_value = np.mean(impact_values)
        std_dev = np.std(impact_values)


        hardware_means.append(mean_value)
        hardware_tdp.append(tdp[i])
        hardware_names.append(name)
        hardware_errors.append(std_dev)
        hardware_dates.append(date[i])


df_scatter = pd.DataFrame({
    "Hardware": hardware_names,
    "Mean Impact Environnemental": hardware_means,
    "TDP": hardware_tdp,
    "Error": hardware_errors,
    "Date": hardware_dates
})


norm = mcolors.Normalize(vmin=df_scatter["Date"].min(), vmax=df_scatter["Date"].max())


fig, ax = plt.subplots(figsize=(12, 8))


scatter = sns.scatterplot(x="TDP", y="Mean Impact Environnemental", data=df_scatter, ax=ax, hue="Date", palette='viridis', legend=None, s=100)


for i in range(len(df_scatter)):
    ax.errorbar(df_scatter["TDP"].iloc[i], df_scatter["Mean Impact Environnemental"].iloc[i],
                yerr=df_scatter["Error"].iloc[i], fmt='o', color='gray', alpha=0.5)


texts = []
for i, name in enumerate(df_scatter['Hardware'].unique()):
    mean_value = df_scatter[df_scatter['Hardware'] == name]["Mean Impact Environnemental"].mean()
    tdp_value = df_scatter[df_scatter['Hardware'] == name]["TDP"].iloc[0]
    texts.append(ax.annotate(f"{name}", (tdp_value, mean_value), fontsize=12, ha='center',
                              arrowprops=dict(arrowstyle="->", lw=0.5, color='gray')))


adjust_text(texts, only_move={'points': 'xy', 'text': 'xy'}, max_move=(10, 10), ax=ax)


sm = plt.cm.ScalarMappable(cmap="viridis", norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label('Years',fontsize=14)
cbar.set_ticks(np.unique(df_scatter["Date"]))


x = df_scatter["TDP"]
y = df_scatter["Mean Impact Environnemental"]


coeffs = np.polyfit(x, y, 2)
poly = np.poly1d(coeffs)





ax.set_xlabel('TDP',fontsize=14)
ax.set_ylabel('Manufacturing impact (kgCO2 eq)',fontsize=14)
ax.set_title('Manufacturing impact - TDP with confidence intervals',fontsize=16)



plt.tight_layout()

plt.show()
