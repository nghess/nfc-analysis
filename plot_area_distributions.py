import re
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

# Import CSV's, strip spaces in column names.
df_f = pd.read_csv('fractal_region_counts.csv')
df_c = pd.read_csv('nf_ctrl_region_counts.csv')
df_f.columns = df_f.columns.str.strip()
df_c.columns = df_f.columns.str.strip()

def sorted_nicely( l ):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

# Extract target fractal dimension from filename
def extract_filename_info(df, colname, regex, newcol):
    newcol_data = []
    for index, row in df_f.iterrows():
        value = row[colname]
        match = re.search(regex, value)
        extracted_number = match.group(1)
        newcol_data.append(extracted_number)
    df[newcol] = newcol_data


# Extract D from filename and add to new column
regex = r"_(\d+\.\d+)_"
column_name = 'filename'
extract_filename_info(df_f, column_name, regex, 'D')
extract_filename_info(df_c, column_name, regex, 'D')

# Bin values and add to new column
def bin_column(df, column_name, n_bins, new_column_name):
    # Use pd.cut() to divide the column into n_bins and get the bin codes
    df[new_column_name], bins = pd.cut(df[column_name], n_bins, retbins=True, labels=False)
    # Compute midpoints of each bin
    bin_midpoints = (bins[:-1] + bins[1:]) / 2
    # Map bin codes to midpoints
    df[new_column_name] = df[new_column_name].map(lambda x: bin_midpoints[x])
    return df

df_f = bin_column(df_f, 'number', 5, 'binned_number')
df_c = bin_column(df_c, 'number', 5, 'binned_number')

# Plot each D
def plot_points(df, category, condition, color_map):
    x = df['region_area']
    y = df['binned_number']
    # Get unique names of categories
    unique = sorted_nicely(list(set(df[category])))
    cNorm = colors.Normalize(vmin=0, vmax=len(unique))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=color_map)
    for i in range(len(unique)):
        index = df['D'] == unique[i]
        plt.scatter(x[index], y[index], s=15, color=scalarMap.to_rgba(i), label=f"{condition} {unique[i]}", alpha=0.5)


plt.xscale('log')
#plt.yscale('log')
plot_points(df_f, 'D', 'Fractal', 'hot')
plot_points(df_c, 'D', 'Control', 'cool')
plt.xlabel("Target Fractal Dimension")
plt.ylabel("Average Region Area")

#plt.legend()
#plt.show()

print(df_f.head())
