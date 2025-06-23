import matplotlib.pyplot as plt
import numpy as np


bandwidth = 1.56e12  # en bytes par seconde
peak_performance = 19.49e12  # en FLOPS
computational_intensity = 1143.055074


operational_intensity = np.linspace(0.01, 10**5, 400)


bandwidth_limited_performance = bandwidth * operational_intensity


plt.figure(figsize=(10, 6))
plt.plot(operational_intensity, bandwidth_limited_performance, label='Bande passante mémoire', color='blue')
plt.hlines(peak_performance, min(operational_intensity), max(operational_intensity), label='Performance maximale', colors='red')
plt.vlines(computational_intensity,0,min(peak_performance,bandwidth*computational_intensity), label='expected model perf', colors = "green")


plt.xscale('log')
plt.yscale('log')
plt.xlabel('Intensité opérationnelle (FLOPs/byte)')
plt.ylabel('Performance (FLOPS)')
plt.title('Modèle Roofline pour Nvidia A100 SXM4 - 40G')
plt.legend()


plt.grid(True)
plt.show()