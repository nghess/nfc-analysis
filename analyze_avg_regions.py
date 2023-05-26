import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# Create and visualize and image showing regions?
draw_contours = False
visualize = False
save_img = False

# Load img
def load_img(image_file):
    img = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
    img_bgr = 0 #cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img_bin = np.asarray(img)
    img_bin = (img_bin > np.mean(img_bin)).astype(np.uint8) * 255
    return img_bin, img_bgr, image_file

# Find regions
def get_regions(image_bin, upper_mean=True):
    assert len(image_bin.shape) < 3, "Image must be grayscale to extract regions"
    contours, h = cv2.findContours(image_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    r_count = len(contours)
    r_areas = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1:  # Area must be more than 3 contiguous pixels
            r_areas.append(area)

    if upper_mean:
        um_areas = [x for x in r_areas if x > np.mean(r_areas)]
        r_areas = um_areas

    um_area = round(np.mean(r_areas), 2)
    return r_count, um_area, contours

# Write to CSV
def write_csv(filename, r_c, m_r_a, img_file):
        f = open(filename, "a")
        f.write(f"\n{r_c}, {m_r_a}, {img_file}")

# Crawl and Execute
def collect_region_info(directory, csv_name, upper):
    i = 0
    path = f"E:/Git Repos/nfc-analysis/{directory}"
    os.chdir(path)

    for file in glob.glob("*.png"):
        image, image_bgr, image_file = load_img(file)
        region_count, mean_region_area, contours = get_regions(image, upper)
        write_csv(csv_name, region_count, mean_region_area, file)
        i += 1
        print(i)

# Write CSVs with region data
#collect_region_info("fractal", "fractal_region_counts.csv", upper=False)
collect_region_info("nf_ctrl_small", "nf_ctrl_region_counts.csv", upper=False)

# Optional visualization
if draw_contours:
    # Draw contours
    image_bgr = cv2.drawContours(image_bgr, contours, -1, (0, 0, 0), 1)
    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(image_bgr, center, radius, (0, 255, 0), 1)

if visualize:
    # Show an image
    assert draw_contours == True, 'draw_contours must be True'
    cv2.imshow('image', image_bgr)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()

if save_img:
    assert draw_contours == True, 'draw_contours must be True'
    # Save region image
    cv2.imwrite(f"regions_{image_file}")


