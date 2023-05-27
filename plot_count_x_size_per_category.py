import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress

df = pd.read_csv('all_regions.csv')

# Calculate the average and standard deviation of region_area per 'D' and 'condition'
avg_region_area = df.groupby(['D', 'condition'])['region_area'].mean()
print(avg_region_area)
# Calculate the number of regions and their standard deviation per 'D' and 'condition'
df_counts = df.groupby(['D', 'condition', 'seed']).size().reset_index(name='counts')
std_devs = df_counts.groupby(['D', 'condition'])['counts'].std()
avg_counts = df_counts.groupby(['D', 'condition'])['counts'].mean()

# Create a new dataframe for plotting
plot_df = pd.DataFrame({
    '1/Avg_Region_Area': 1 / avg_region_area,
    'Avg_Num_Regions': avg_counts,
    'Avg_Num_Regions_std': std_devs
})

# Reset the index
plot_df = plot_df.reset_index()
plt.figure(figsize=(10, 6))

# Set up color palette with seaborn
palette = iter(sns.color_palette('icefire', n_colors=len(plot_df['condition'].unique())))

for condition in plot_df['condition'].unique():
    color = next(palette)
    df_subset = plot_df[plot_df['condition'] == condition]
    plt.errorbar(df_subset['1/Avg_Region_Area'], df_subset['Avg_Num_Regions'],
                 yerr=df_subset['Avg_Num_Regions_std'],
                 label=condition, fmt='o', capsize=5, color=color, ecolor=color, alpha=1, errorevery=1)
    slope, intercept, r_value, p_value, std_err = linregress(df_subset['1/Avg_Region_Area'], df_subset['Avg_Num_Regions'])
    x_range = np.linspace(df_subset['1/Avg_Region_Area'].min(), df_subset['1/Avg_Region_Area'].max(), 100)
    plt.plot(x_range, intercept + slope * x_range, alpha=0.75, color=color)

plt.rc('axes', labelsize=200)
plt.xlabel("1 / Size")
plt.ylabel("Count")

plt.title('Average Region Count vs 1 / Region Size')
plt.legend()
plt.show()
