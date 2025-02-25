import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text

# Charger les données
data = pd.read_csv('g5k_edge.csv', delimiter=';')

names = data['names']
die_area = data['Die_area']
tdp = data['TDP']
gflops = data['GFLOPS']
price = data['price']
tech_node = data['Tech_node']
date = data['date']
mem = data['Memory']
proc = (die_area*pow(10,6))/tech_node

norm_proc = (proc-proc.min())/(proc.max()-proc.min())
norm_mem = (mem-mem.min())/(mem.max()-mem.min())
manufacturing_impact = (norm_proc+norm_mem)/2
env = (((tdp-tdp.min())/(tdp.max()-tdp.min()))+manufacturing_impact)/2
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 7))

norm = plt.Normalize(vmin=date.min(), vmax=date.max())
cmap = plt.cm.viridis


sc1 = axes[0].scatter(tdp, manufacturing_impact, c=date, cmap=cmap, norm=norm)


coeffs1 = np.polyfit(tdp, manufacturing_impact, 2)
poly1 = np.poly1d(coeffs1)
x_range = np.linspace(min(tdp), max(tdp), 100)
axes[0].plot(x_range, poly1(x_range), color='red', linestyle='--', label="Quadratic regression")

texts = []
for i, name in enumerate(names):
    texts.append(axes[0].annotate(name, (tdp[i], manufacturing_impact[i]), fontsize=12, ha='right',
                                  arrowprops=dict(arrowstyle="->", lw=0.5, color='gray')))
adjust_text(texts, only_move={'points':'xy', 'text':'xy'}, max_move=(10,10), ax=axes[0])
axes[0].set_xlabel('TDP')
axes[0].set_ylabel('Manufacturing Impact estimation')
axes[0].set_title('TDP vs Manufacturing Impact')
axes[0].legend()


sc2 = axes[1].scatter(env, gflops, c=date, cmap=cmap, norm=norm)


coeffs2 = np.polyfit(env, gflops, 2)
poly2 = np.poly1d(coeffs2)
x_range = np.linspace(min(env), max(env), 100)
axes[1].plot(x_range, poly2(x_range), color='red', linestyle='--', label="Quadratic regression")

texts = []
for i, name in enumerate(names):
    texts.append(axes[1].annotate(name, (env[i], gflops[i]), fontsize=12, ha='right',
                                  arrowprops=dict(arrowstyle="->", lw=0.5, color='gray')))
adjust_text(texts, only_move={'points':'xy', 'text':'xy'}, max_move=(10,10), ax=axes[1])
axes[1].set_xlabel('Scale level')
axes[1].set_ylabel('GFLOPS(FP32)')
axes[1].set_yscale('log')
axes[1].set_title('Scale level level vs GFLOPS')
axes[1].legend()


cbar = fig.colorbar(sc1, ax=axes, orientation='vertical', fraction=0.015, pad=0.04)
cbar.set_label('Release year')

plt.show()
