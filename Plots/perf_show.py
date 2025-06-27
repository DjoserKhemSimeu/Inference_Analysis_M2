import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import LogLocator, FormatStrFormatter
from matplotlib.backends.backend_pdf import PdfPages


PUE = 1.5
# Paramètres globaux
EGM = 79.1  # gCO2/kWh
seven_years = 61320 * 3600

# Impact fabrication
impact_conception_v11 = {
    'A100_v1': [27.678700, 20.469933, 44.818200],
    'A40': [26.913520, 41.206800],
    'T4': [11.314983, 24.726000],
    '2080Ti': [11.645243, 30.199200],
    'QRTX8000': [24.965243, 43.519200],
    'QRTX6000': [16.325243,34.879200],
    'Xavier': [8.207420, 16.82]
}
impact_conception_v41 = {
    'H100': [44.272180],
    'L40S': [33.643830],
    'Orin': [25.539700, 35.895500],
    'A100_v4': [27.678700, 20.469933, 44.818200],
    'A40': [26.913520, 41.206800],
    'T4': [11.314983, 24.726000],
    '2080Ti': [11.645243, 30.199200],
    'QRTX8000': [24.965243, 43.519200]
}

gpus_v11 = ['A100_v1', 'A40', 'T4', '2080Ti', 'QRTX8000','QRTX6000', 'Xavier']
gpus_v41 = ['H100', 'L40S', 'Orin', 'A100_v4']

gpu_folder_map_v11 = {
    'A100_v1': '../Data/data_A100_v1.1',
    'A40': '../Data/data_A40_v1.1',
    'T4': '../Data/data_T4_v1.1',
    '2080Ti': '../Data/data_2080Ti_v1.1',
    'QRTX8000': '../Data/data_QRTX8000_v1.1',
    'QRTX6000': '../Data/data_QRTX6000_v1.1',
    'Xavier': '../Data/data_xavier_v1.1'
}
gpu_folder_map_v41 = {
    'H100': '../Data/data_H100_v4.1',
    'L40S': '../Data/data_L40S_v4.1',
    'Orin': '../Data/data_orin_v4.1',
    'A100_v4': '../Data/data_A100_v4.1'
}

def compute_impact_energy_all_powers(file_path, gpu_name, impact_conception):
    if not os.path.isfile(file_path):
        return None
    data = pd.read_csv(file_path)
    timestamps = data['timestamp']
    mean_power = data['gpu_power']
    duration_sec = timestamps.iloc[-1] - timestamps.iloc[0]
    duration_hr = duration_sec / 3600
    energie_Wh = mean_power.mean() * duration_hr
    energie_kWh = energie_Wh / 1000

    large_scale_gpus = ['A100_v1','A100_v4', 'A40', 'H100', 'L40S']
    if gpu_name in large_scale_gpus:
        energie_kWh *= PUE

    co2 = energie_kWh * EGM
    return [(co2 + ((duration_sec / seven_years) * v * 1000))*1000 for v in impact_conception[gpu_name]]

def gather_impacts_expanded(gpus, folder_map, impact_conception, version_label):
    results = []
    for gpu in gpus:
        folder = folder_map[gpu]
        for qc in [16, 32, 64, 128, 256]:
            file_path = os.path.join(folder, 'MEAN', 'FULL', f'mean_power_QC_{qc}.csv')
            impacts = compute_impact_energy_all_powers(file_path, gpu, impact_conception)
            if impacts is None:
                continue
            for impact in impacts:
                results.append({
                    'QC': qc,
                    'GPU': gpu,
                    'GWP (mg CO2 eq)': impact,
                    'Version': version_label
                })
    return pd.DataFrame(results)

# Chargement latence
latency_df = pd.read_csv('../Doc/mlperf_summary.csv')
latency_df['Version'] = latency_df['Run ID (log path)'].apply(
    lambda x: 'v1.1' if 'v1.1' in x else 'v4.1' if 'v4.1' in x else 'unknown'
)
gpu_name_map = {
    'A100_v1.1_logs': 'A100_v1', 'A40_v1.1_logs': 'A40', 'T4_v1.1_logs': 'T4',
    '2080Ti_v1.1_logs': '2080Ti', 'QRTX8000_v1.1_logs': 'QRTX8000', 'QRTX6000_v1.1_logs': 'QRTX6000', 'Xavier_v1.1_logs': 'Xavier',
    'H100_v4.1_logs': 'H100', 'L40S_v4.1_logs': 'L40S', 'Orin_v4.1_logs': 'Orin',
    'A100_v4.1_logs': 'A100_v4'
}
latency_df['GPU'] = latency_df['Run ID (log path)'].map(gpu_name_map)
latency_df = latency_df[['QC (min query count)', 'Max latency (ns)', 'GPU', 'Version']]
latency_df.rename(columns={'QC (min query count)': 'QC', 'Max latency (ns)': 'max_latency_ns'}, inplace=True)
latency_df['max_latency_ms'] = latency_df['max_latency_ns'] / 1e6

# Fusion impact
df_v11 = gather_impacts_expanded(gpus_v11, gpu_folder_map_v11, impact_conception_v11, 'v1.1')
df_v41 = gather_impacts_expanded(gpus_v41, gpu_folder_map_v41, impact_conception_v41, 'v4.1')
df_merged = pd.concat([df_v11, df_v41], ignore_index=True)
df_final = pd.merge(df_merged, latency_df, on=['GPU', 'QC', 'Version'], how='left')

# Catégories et markers
categories = {
    'Xavier': 'Edge', 'Orin': 'Edge',
    'H100': 'Large-scale', 'A100_v1': 'Large-scale','A100_v4': 'Large-scale', 'A40': 'Large-scale', 'L40S': 'Large-scale',
    'T4': 'Desktop', 'QRTX8000': 'Desktop','QRTX6000': 'Desktop',
    '2080Ti': 'Gaming'
}
df_final['category'] = df_final['GPU'].map(categories)
markers = {'Edge': 'o', 'Gaming': 's', 'Desktop': 'D', 'Large-scale': 'X'}
# Exclure 'QC' et 'GPU' des colonnes numériques à moyenner
numeric_columns = [
    col for col in df_final.select_dtypes(include=['float64', 'int64']).columns
    if col not in ['QC', 'GPU']
]

# Calcul des moyennes pour chaque couple (QC, GPU)
temp = df_final.groupby(['QC', 'GPU'])[numeric_columns].mean().reset_index()
print(temp)
# Sauvegarde du DataFrame dans un fichier CSV
temp.to_csv('../Doc/gwp+latency_results.csv', index=False)
# --- Fonction pour tracer les lignes médianes GPU ---
def plot_median_lines(ax, df_plot, value_col):
    gpus = df_plot['GPU'].unique()
    qc_order = sorted(df_plot['QC'].unique())
    x_pos = range(len(qc_order))
    qc_to_x = dict(zip(qc_order, x_pos))
    medians = df_plot.groupby(['GPU', 'QC'])[value_col].median().reset_index()
    for gpu in gpus:
        data_gpu = medians[medians['GPU'] == gpu]
        x_vals = data_gpu['QC'].map(qc_to_x)
        y_vals = data_gpu[value_col]
        ax.plot(x_vals, y_vals, linestyle='--', linewidth=1.5)
    ax.set_xticks(list(x_pos))
    ax.set_xticklabels(qc_order)

# Sauvegarde des graphiques GWP (ligne du haut)
with PdfPages('../images/gwp_graphs.pdf') as pdf:
    fig_gwp, axs_gwp = plt.subplots(1, 2, figsize=(14, 5), sharex=True)

    # GWP v1.1
    sns.boxplot(ax=axs_gwp[0], data=df_final[df_final['Version'] == 'v1.1'],
                x='QC', y='GWP (mg CO2 eq)', hue='GPU')
    plot_median_lines(axs_gwp[0], df_final[df_final['Version'] == 'v1.1'],'GWP (mg CO2 eq)')
    axs_gwp[0].set_title('GWP (g CO2 eq) - Version 1.1')
    axs_gwp[0].set_xlabel('Number of queries (QC)')
    axs_gwp[0].set_ylabel('GWP (mg CO2 eq)')
    axs_gwp[0].legend(loc='center left', bbox_to_anchor=(1.0, 0.5),fontsize=12)
    axs_gwp[0].grid(True)

    # GWP v4.1
    sns.boxplot(ax=axs_gwp[1], data=df_final[df_final['Version'] == 'v4.1'],
                x='QC', y='GWP (mg CO2 eq)', hue='GPU')
    plot_median_lines(axs_gwp[1], df_final[df_final['Version'] == 'v4.1'], 'GWP (mg CO2 eq)')
    axs_gwp[1].set_title('GWP (g CO2 eq) - Version 4.1')
    axs_gwp[1].set_xlabel('Number of queries (QC)')
    axs_gwp[1].set_ylabel('GWP (mg CO2 eq)')
    axs_gwp[1].legend(loc='center left', bbox_to_anchor=(1.0, 0.5),fontsize=12)
    axs_gwp[1].grid(True)

    fig_gwp.tight_layout()
    pdf.savefig(fig_gwp)
    plt.close(fig_gwp)

# Sauvegarde des graphiques latence (ligne du bas)
with PdfPages('../images/latency_graphs.pdf') as pdf:
    fig_latency, axs_latency = plt.subplots(1, 2, figsize=(14, 5), sharex=True)

    # Latence v1.1
    sns.boxplot(ax=axs_latency[0], data=df_final[df_final['Version'] == 'v1.1'],
                x='QC', y='max_latency_ms', hue='GPU')
    plot_median_lines(axs_latency[0], df_final[df_final['Version'] == 'v1.1'], 'max_latency_ms')
    axs_latency[0].set_title('Max latency (ms) - Version 1.1')
    axs_latency[0].set_xlabel('Number of queries (QC)')
    axs_latency[0].set_ylabel('Max latency (ms)')
    axs_latency[0].set_yscale("log")
    axs_latency[0].yaxis.set_major_locator(LogLocator(base=10.0, subs='all', numticks=5))
    axs_latency[0].yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    axs_latency[0].legend(loc='center left', bbox_to_anchor=(1.0, 0.5),fontsize=12)
    axs_latency[0].grid(True)

    # Latence v4.1
    sns.boxplot(ax=axs_latency[1], data=df_final[df_final['Version'] == 'v4.1'],
                x='QC', y='max_latency_ms', hue='GPU')
    plot_median_lines(axs_latency[1], df_final[df_final['Version'] == 'v4.1'], 'max_latency_ms')
    axs_latency[1].set_title('Max latency (ms) - Version 4.1')
    axs_latency[1].set_xlabel('Number of queries (QC)')
    axs_latency[1].set_ylabel('Max latency (ms)')
    axs_latency[1].set_yscale("log")
    axs_latency[1].yaxis.set_major_locator(LogLocator(base=10.0, subs='all', numticks=5))
    axs_latency[1].yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    axs_latency[1].legend(loc='center left', bbox_to_anchor=(1.0, 0.5),fontsize=12)
    axs_latency[1].grid(True)

    fig_latency.tight_layout()
    pdf.savefig(fig_latency)
    plt.close(fig_latency)
