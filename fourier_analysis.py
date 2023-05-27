import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns

def plot_image_fft(image_path):
    # Load image
    img = Image.open(image_path)

    # Convert image to grayscale
    gray_img = img.convert('L')

    # Convert the image to a NumPy array
    img_array = np.array(gray_img)

    # Perform the 2D Fourier Transform and shift the zero frequency component to the center
    ft_img = np.fft.fft2(img_array)
    ft_img_shifted = np.fft.fftshift(ft_img)

    # Calculate the magnitude spectrum
    magnitude_spectrum = 20*np.log1p(np.abs(ft_img_shifted))

    # Flatten the magnitude spectrum to a 1D array
    magnitude_spectrum_1D = magnitude_spectrum.flatten()

    # Create histogram using plt.hist

    plt.hist(magnitude_spectrum_1D, bins=100, alpha=0.7, label=image_path)

# Initialize Plot
plt.figure(figsize=(10, 5))

# Call the function with an image
plot_image_fft("1.3_fractal.png")
plot_image_fft("1.3_control_avg.png")
plot_image_fft("1.3_control_upr.png")

# Share Plot Attributes
plt.title('Power Spectra')
plt.xlabel('Frequency')
plt.ylabel('Power')
plt.legend()
plt.show()
