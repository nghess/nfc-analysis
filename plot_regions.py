import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df_f = pd.read_csv('fractal_region_counts.csv')
df_c = pd.read_csv('nf_ctrl_region_counts.csv')
df_f.columns = df_f.columns.str.strip()
df_c.columns = df_f.columns.str.strip()

print(df_f.min())

plt.xscale('log')
plt.yscale('log')

plt.xlabel("Average Region Area")
plt.ylabel("Region Count")

plt.scatter(y=df_f['number'], x=df_f['region_area'], s=1, alpha=0.5, label='fractal')
plt.scatter(y=df_c['number'], x=df_c['region_area'], s=1, alpha=0.5, label='control')
plt.legend()
plt.show()
