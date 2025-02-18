import matplotlib.pyplot as plt
import numpy as np


bandwidth = 1.56e12  # en bytes par seconde
peak_performance = 19.49e12  # en FLOPS
computational_intensity = 285.764


operational_intensity = np.linspace(0.01, 10**5, 400)


bandwidth_limited_performance = bandwidth * operational_intensity

bandwidth_jetson = 136.5e9  # en bytes par seconde
peak_performance_jetson = 1.41e12  # en FLOPS

bandwidth_limited_performance_jetson = bandwidth_jetson * operational_intensity


fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 11))

# Nvidia A100
axes[0].plot(operational_intensity, bandwidth_limited_performance, label='Bandwith limitation', color='blue')
axes[0].hlines(peak_performance, min(operational_intensity), max(operational_intensity), label='Peak performance', colors='red')
axes[0].vlines(computational_intensity, 0, min(peak_performance, bandwidth * computational_intensity), label='Expected inference performance', colors='green')
axes[0].set_xscale('log')
axes[0].set_yscale('log')
axes[0].set_xlabel('Operational Intensity (FLOPs/byte)')
axes[0].set_ylabel('Performance (FLOPS)')
axes[0].set_title('Roofline model - Nvidia A100 SXM4 - 40G')
axes[0].fill_betweenx([0, min(peak_performance, bandwidth * computational_intensity)],
                      computational_intensity, max(operational_intensity), color='green', alpha=0.3, hatch='/',label="StarCoder region")
axes[0].legend()
axes[0].grid(True)

axes[0].annotate(f'{min(peak_performance, bandwidth * computational_intensity):.2e} FLOPS',
             xy=(computational_intensity, min(peak_performance, bandwidth * computational_intensity)),
             xytext=(1e3, 1e14),
             arrowprops=dict(facecolor='black', arrowstyle='->'),
             fontsize=18)

# Nvidia Jetson
axes[1].plot(operational_intensity, bandwidth_limited_performance_jetson, label='Bandwith limitation', color='blue')
axes[1].hlines(peak_performance_jetson, min(operational_intensity), max(operational_intensity), label='Peak performance ', colors='red')
axes[1].vlines(computational_intensity, 0, min(peak_performance_jetson, bandwidth_jetson * computational_intensity), label='Expected inference performance', colors='green')
axes[1].set_xscale('log')
axes[1].set_yscale('log')
axes[1].set_xlabel('Operational Intensity (FLOPs/byte)')
axes[1].set_ylabel('Performance (FLOPS)')
axes[1].set_title('Roofline model - Nvidia Jetson AMX Xavier - 32G')
axes[1].fill_betweenx([0, min(peak_performance_jetson, bandwidth_jetson * computational_intensity)],
                      computational_intensity, max(operational_intensity), color='green', alpha=0.3, hatch='/',label="StarCoder region")
axes[1].legend()
axes[1].grid(True)

axes[1].annotate(f'{min(peak_performance_jetson, bandwidth_jetson * computational_intensity):.2e} FLOPS',
             xy=(computational_intensity, min(peak_performance_jetson, bandwidth_jetson * computational_intensity)),
             xytext=(1e3, 1e10),
             arrowprops=dict(facecolor='black', arrowstyle='->'),
             fontsize=18)
x_min = min(operational_intensity)
x_max = max(operational_intensity)
y_min = min(min(bandwidth_limited_performance), min(bandwidth_limited_performance_jetson))
y_max = max(max(bandwidth_limited_performance), max(bandwidth_limited_performance_jetson), peak_performance, peak_performance_jetson)

axes[0].set_xlim([x_min, x_max])
axes[0].set_ylim([y_min, y_max])
axes[1].set_xlim([x_min, x_max])
axes[1].set_ylim([y_min, y_max])
plt.tight_layout()
plt.show()
