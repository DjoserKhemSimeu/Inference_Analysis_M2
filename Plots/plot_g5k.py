import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text


data = pd.read_csv('../Doc/g5k_edge.csv', delimiter=';')

names = data['names']
die_area = data['Die_area']
tdp = data['TDP']
gflops = data['GFLOPS']
price = data['price']
tech_node = data['Tech_node']
c_i=data['Compute_capability']
date = data['date']
mem = data['Memory']
proc = (die_area*pow(10,6))/tech_node

norm_proc = (proc-proc.min())/(proc.max()-proc.min())
norm_mem = (mem-mem.min())/(mem.max()-mem.min())
manufacturing_impact = (norm_proc+norm_mem)/2
env = (((tdp-tdp.min())/(tdp.max()-tdp.min()))+manufacturing_impact)/2


fig, ax = plt.subplots(figsize=(10, 7))

norm = plt.Normalize(vmin=date.min(), vmax=date.max())
cmap = plt.cm.viridis

sc = ax.scatter(tdp, c_i, c=date, cmap=cmap, norm=norm)


coeffs = np.polyfit(tdp, c_i, 2)
poly = np.poly1d(coeffs)
x_range = np.linspace(min(tdp), max(tdp), 100)
ax.plot(x_range, poly(x_range), color='red', linestyle='--', label="Quadratic regression")


texts = []
for i, name in enumerate(names):
    texts.append(ax.annotate(name, (tdp[i], c_i[i]), fontsize=12, ha='right',
                             arrowprops=dict(arrowstyle="->", lw=0.5, color='gray')))
adjust_text(texts, only_move={'points': 'xy', 'text': 'xy'}, max_move=(10, 10), ax=ax)

ax.set_xlabel('TDP')
ax.set_ylabel('Compute capability')

ax.set_title('TDP vs GFLOPS')
ax.legend()


cbar = fig.colorbar(sc, ax=ax, orientation='vertical', fraction=0.02, pad=0.04)
cbar.set_label('Release year')

plt.show()
