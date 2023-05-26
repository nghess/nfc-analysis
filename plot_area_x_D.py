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

# Plot each D
def plot_points(df, category, condition, color_map):
    x = df['D']
    y = df['region_area']
    # Get unique names of categories
    unique = sorted_nicely(list(set(df[category])))
    cNorm = colors.Normalize(vmin=0, vmax=len(unique))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=color_map)
    for i in range(len(unique)):
        index = df['D'] == unique[i]
        plt.scatter(x[index], y[index], s=15, color=scalarMap.to_rgba(i), label=f"{condition} {unique[i]}", alpha=0.5)


def rand_jitter(arr):
    stdev = .01 * (max(arr) - min(arr))
    return arr + np.random.randn(len(arr)) * stdev

def jitter(x, y, s=20, c='b', marker='o', cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, verts=None, hold=None, **kwargs):
    return scatter(rand_jitter(x), rand_jitter(y), s=s, c=c, marker=marker, cmap=cmap, norm=norm, vmin=vmin, vmax=vmax, alpha=alpha, linewidths=linewidths, **kwargs)


#plt.xscale('log')
#plt.yscale('log')
plot_points(df_f, 'D', 'Fractal', 'hot')
plot_points(df_c, 'D', 'Control', 'cool')
plt.xlabel("Target Fractal Dimension")
plt.ylabel("Average Region Area")

plt.legend()
plt.show()
