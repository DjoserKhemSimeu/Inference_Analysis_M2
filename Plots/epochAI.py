import requests
import io
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
import plotly.express as px

# 1. Load the Epoch AI dataset
url = "https://epoch.ai/data/ai_supercomputers.csv"
r = requests.get(url)
r.raise_for_status()
df = pd.read_csv(io.StringIO(r.text))

# 2. Clean and rename
df = df.rename(columns={
    'First Operational Date': 'release_date',
    '32-bit OP/s': 'performance_32flops',
    'Chip type (primary)': 'hardware_type'
})
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['performance_32flops'] = pd.to_numeric(df['performance_32flops'], errors='coerce')
df = df.dropna(subset=['release_date', 'performance_32flops', 'hardware_type'])
df = df[df['release_date'].dt.year >= 2019]

# 3. Group rare hardware types (<5 occurrences) as "Other"
type_counts = df['hardware_type'].value_counts()
common_types = type_counts[type_counts >= 5].index
df['hardware_type_grouped'] = df['hardware_type'].apply(
    lambda x: x if x in common_types else 'Other'
)

# 4. Sort types by frequency (not alphabetically)
grouped_counts = df['hardware_type_grouped'].value_counts()
sorted_types = list(grouped_counts.index)

# 5. Use a high-contrast qualitative color palette
palette = px.colors.qualitative.Alphabet  # 26 visually distinct colors
palette = palette[:len(sorted_types)]  # Trim to number of categories
color_map = {htype: palette[i] for i, htype in enumerate(sorted_types)}
df['color'] = df['hardware_type_grouped'].map(color_map)

# 6. Create the scatter plot
plt.figure(figsize=(15, 8))
plt.scatter(
    df['release_date'],
    df['performance_32flops'],
    c=df['color'],
    alpha=0.85,
    edgecolor='black',
    linewidth=0.4
)

# 7. Add legend
legend_elements = [
    Line2D([0], [0], marker='o', color='w',
           label=f"{label} ({grouped_counts[label]})",
           markerfacecolor=color_map[label],
           markeredgecolor='black',
           markersize=8)
    for label in sorted_types
]
plt.legend(handles=legend_elements, title="Hardware Type (≥5 entries)",
           bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)

# 8. Format axes and title
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.yscale('log')
plt.xlabel("Operational Date")
plt.ylabel("Performance (32-bit FLOPS, log scale)")
plt.title("AI Supercomputer Performance Over Time (Epoch AI)")
plt.grid(True, which="both", ls="--", alpha=0.5)

# 9. Layout and save
plt.tight_layout()
plt.savefig("epoch_ai_colored_plot.pdf")
plt.show()
print("Plot saved as epoch_ai_colored_plot.pdf")
