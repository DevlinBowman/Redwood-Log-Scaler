
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def extract_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    all_data = []
    for length, diameter_data in data.items():
        for diameter, taper_data in diameter_data.items():
            for taper, footage in taper_data.items():
                all_data.append({
                    'Length': int(length),
                    'Diameter': int(diameter),
                    'Taper': taper,
                    'Footage': footage
                })

    return pd.DataFrame(all_data)

def plot_data(df, jitter_amount=0.5):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    tapers = df['Taper'].unique()
    colors = plt.cm.jet(np.linspace(0, 1, len(tapers)))

    for idx, (taper, color) in enumerate(zip(tapers, colors)):
        taper_df = df[df['Taper'] == taper]

        # Apply jitter by adding a small random offset, scaled by the index to spread out each taper category
        jittered_length = taper_df['Length'] + (np.random.rand(len(taper_df)) - 0.5) * jitter_amount * idx
        jittered_diameter = taper_df['Diameter'] + (np.random.rand(len(taper_df)) - 0.5) * jitter_amount * idx

        ax.scatter(jittered_length, jittered_diameter, taper_df['Footage'], color=color, label=f'Taper {taper}', alpha=0.6, edgecolors='w')

    ax.set_title('Board Footage Distribution by Log Attributes')
    ax.set_xlabel('Length')
    ax.set_ylabel('Diameter')
    ax.set_zlabel('Board Footage')
    ax.legend(title='Taper Categories')
    plt.show()

# Main execution
# file_path = 'Utils/Scale_table_data.json'
# df = extract_data(file_path)
# plot_data(df)
