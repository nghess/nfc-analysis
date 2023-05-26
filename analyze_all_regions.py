import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import re


def process_image(image_path, dir_name):
    # Load the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Threshold the image to black and white
    _, thresh_img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create list to store data before it's added to df
    data = []

    # Extract fractal D from filename
    get_seed = r'^(\d+)_'
    get_fractal_d = r"_(\d+\.\d+)_"
    get_condition = r'(control|normal)'
    seed = re.search(get_seed, image_path).group(1)
    fractal_d = re.search(get_fractal_d, image_path).group(1)
    condition = re.search(get_condition, image_path).group(1)

    for cnt in contours:
        # Get the area of the contour
        area = cv2.contourArea(cnt)
        if area > 0:
            data.append({'filename': image_path, 'region_area': area, 'D': fractal_d, 'seed': seed, 'condition': dir_name})

    # Convert the list to a dataframe
    df = pd.DataFrame(data)

    return df

# Go through a directory and save dataframe as csv
directories = ['control_avg', 'control_upper', 'fractal']
total_df = pd.DataFrame()

for directory in directories:
    path = f"E:/Git Repos/nfc-analysis/{directory}"
    os.chdir(path)

    for file in glob.glob("*.png"):  # Just get first file to test
        data = process_image(file, directory)
        total_df = pd.concat([total_df, data], ignore_index=True)


total_df.to_csv('control_regions.csv', index=False)

