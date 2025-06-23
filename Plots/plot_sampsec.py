import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Chemin vers le fichier CSV
file_path = 'data/sample_per_sec.csv'

# Lecture du fichier CSV
df = pd.read_csv(file_path, delimiter=';')
print(df)

# Configuration du style de seaborn
sns.set(style="whitegrid")

# Palette de couleurs personnalisée
color_palette = {
    "Edge": "green",
    "Gaming": "yellow",
    "Desktop": "orange",
    "Large-scale": "red"
}

# Création du barplot avec la palette personnalisée
plt.figure(figsize=(10, 6))
barplot = sns.barplot(x='Sampsec', y='GPU', hue='Cat', data=df, palette=color_palette, dodge=False)

# Ajout des valeurs sur les barres en utilisant les données du DataFrame
for idx, row in df.iterrows():
    sampsec_value = row['Sampsec']
    annotation_text = f"{sampsec_value:.2f}".rstrip('0').rstrip('.')

    # Positionnement de l'annotation
    if sampsec_value < 100:
        xytext = (40, 0)  # Déplace l'annotation légèrement vers la droite pour les petites valeurs
    else:
        xytext = (-5, 0)  # Déplace l'annotation légèrement vers la gauche pour les grandes valeurs

    # Ajout de l'annotation
    barplot.annotate(annotation_text,
                     xy=(sampsec_value, idx),
                     ha='left' if sampsec_value < 1 else 'right', va='center',
                     xytext=xytext,
                     textcoords='offset points')

# Configuration des titres et des labels
plt.title('Testing results in Offline setting with the BERT model', fontsize=16)
plt.xlabel('Samples per second', fontsize=14)
plt.ylabel('GPUs', fontsize=14)

# Ajout de la légende
plt.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')

# Affichage du plot
plt.tight_layout()
plt.show()
