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
env = (((tdp-tdp.min())/(tdp.max()-tdp.min()))+((die_area-die_area.min())/(die_area.max()-die_area.min())))/2
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 7))
print(env)
norm = plt.Normalize(vmin=price.min(), vmax=price.max())
cmap = plt.cm.viridis


sc1 = axes[0].scatter(tdp, die_area, c=price, cmap=cmap, norm=norm)


coeffs1 = np.polyfit(tdp, die_area, 2)
poly1 = np.poly1d(coeffs1)
x_range = np.linspace(min(tdp), max(tdp), 100)
axes[0].plot(x_range, poly1(x_range), color='red', linestyle='--', label="Quadratic regression")

texts = []
for i, name in enumerate(names):
    texts.append(axes[0].annotate(name, (tdp[i], die_area[i]), fontsize=12, ha='right',
                                  arrowprops=dict(arrowstyle="->", lw=0.5, color='gray')))
adjust_text(texts, only_move={'points':'xy', 'text':'xy'}, max_move=(10,10), ax=axes[0])
axes[0].set_xlabel('TDP')
axes[0].set_ylabel('Die Area')
axes[0].set_title('TDP vs Die Area')
axes[0].legend()


sc2 = axes[1].scatter(env, gflops, c=price, cmap=cmap, norm=norm)


coeffs2 = np.polyfit(env, gflops, 2)
poly2 = np.poly1d(coeffs2)
x_range = np.linspace(min(env), max(env), 100)
axes[1].plot(x_range, poly2(x_range), color='red', linestyle='--', label="Quadratic regression")

texts = []
for i, name in enumerate(names):
    texts.append(axes[1].annotate(name, (env[i], gflops[i]), fontsize=12, ha='right',
                                  arrowprops=dict(arrowstyle="->", lw=0.5, color='gray')))
adjust_text(texts, only_move={'points':'xy', 'text':'xy'}, max_move=(10,10), ax=axes[1])
axes[1].set_xlabel('Edge level ((TDP_norm+Die_norm)/2)')
axes[1].set_ylabel('GFLOPS(FP32)')
axes[1].set_title('Edge level vs GFLOPS')
axes[1].legend()


cbar = fig.colorbar(sc1, ax=axes, orientation='vertical', fraction=0.015, pad=0.04)
cbar.set_label('Price')

plt.show()
