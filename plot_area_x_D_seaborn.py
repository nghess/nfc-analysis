import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
import matplotlib.cm as cm

# Import CSV's, strip spaces in column names.
df_f = pd.read_csv('fractal_region_counts.csv')
df_c = pd.read_csv('upper_nf_ctrl_region_counts.csv')
df_f.columns = df_f.columns.str.strip()
df_c.columns = df_c.columns.str.strip()

def sorted_nicely(l):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

# Extract target fractal dimension from filename
def extract_filename_info(df, colname, regex, newcol):
    newcol_data = []
    for index, row in df.iterrows():
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

# Add a column to differentiate between df_f and df_c
df_f['dataset'] = 'Fractal'
df_c['dataset'] = 'Upper Mean Control'

# Concatenate the two dataframes
df_combined = pd.concat([df_f, df_c])

# Generate a colormap using 'hot' and 'cool'
color_map = cm.get_cmap('hot')
fractal_color = mcolors.to_rgb(color_map(0.5))
color_map = cm.get_cmap('cool')
control_color = mcolors.to_rgb(color_map(0.5))
palette = {'Fractal': fractal_color, 'Upper Mean Control': control_color}

# Plot combined data
plt.figure(figsize=(8, 6))
sns.stripplot(data=df_combined, x='D', y='region_area', hue='dataset', jitter=True, palette=palette, alpha=0.5)
plt.xlabel("Target Fractal Dimension")
plt.ylabel("Average Region Area")
plt.title("Comparison of Fractal and Control Stimuli - Average Region Size")
plt.yscale('log')
plt.legend()
plt.show()
