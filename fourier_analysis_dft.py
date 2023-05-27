import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import glob
import os
import re

def plot_dft(image_path):
    # Load image
    img = Image.open(image_path)

    # Convert image to grayscale
    gray_img = img.convert('L')

    # Convert the image to a NumPy array
    img_array = np.array(gray_img)

    # Perform the 1D Fourier Transform on each row of the image
    ft_img_rows = np.fft.fft(img, axis=1)

    # Calculate the power spectrum (absolute value squared)
    power_spectrum_rows = np.abs(ft_img_rows)**2

    # Average the power spectrum over all rows to get a 1D power spectrum
    power_spectrum_1D = np.mean(power_spectrum_rows, axis=0)

    slice = round(img.size[0]/2)
    plt.plot(power_spectrum_1D[1:slice], label=image_path)


def plot_trio(row, file_path):
    os.chdir(file_path)
    files = glob.glob('*.png') # Just get first file to test
    files = np.asarray(files).reshape([10,3])
    i = row
    for j in range(3):
        plot_dft(files[i][j])





# Initialize Plot
plt.figure(figsize=(10, 5))

# Plot Trio
path = f"E:/Git Repos/nfc-analysis/fourier_stimuli"

plot_trio(0, path)

# Shared Plot Attributes
plt.yscale('log')
#plt.xscale('log')
plt.title('Discreet Fourier Transform')
plt.xlabel('Cycles per 1024px')
plt.ylabel('Power')
plt.legend()
plt.show()
