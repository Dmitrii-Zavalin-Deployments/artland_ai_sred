import os
import cv2
import numpy as np
import random
from glob import glob
from sklearn.cluster import KMeans
from PIL import Image

# Path to the folder containing images
IMAGE_FOLDER = "book_compilation"
OUTPUT_IMAGE = os.path.join(IMAGE_FOLDER, "background.jpg")

# Parameters for filtering dark colors
BRIGHTNESS_THRESHOLD = 50  # HSV V-channel threshold

def extract_colors_from_images(image_folder, num_colors=10):
    """Extracts dominant colors from images in the folder."""
    image_files = glob(os.path.join(image_folder, "*.jpg"))
    pixel_data = []

    for file in image_files:
        image = cv2.imread(file)
        if image is None:
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        reshaped_image = image.reshape(-1, 3)
        pixel_data.extend(reshaped_image)

    # Convert to NumPy array and use KMeans to find dominant colors
    pixel_data = np.array(pixel_data)
    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
    kmeans.fit(pixel_data)
    colors = kmeans.cluster_centers_.astype(int)

    # Filter out dark colors using HSV
    filtered_colors = []
    for color in colors:
        hsv = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_RGB2HSV)[0][0]
        if hsv[2] > BRIGHTNESS_THRESHOLD:  # V-channel brightness check
            filtered_colors.append(tuple(color))

    return filtered_colors

def create_gradient_background(colors, width=800, height=1200):
    """Generates a smooth gradient background using extracted light colors."""
    gradient = np.zeros((height, width, 3), dtype=np.uint8)

    for i in range(height):
        blend_factor = i / height
        color1 = np.array(colors[random.randint(0, len(colors)-1)])
        color2 = np.array(colors[random.randint(0, len(colors)-1)])
        mixed_color = (1 - blend_factor) * color1 + blend_factor * color2
        gradient[i, :] = mixed_color

    return gradient

def save_background(image_array, output_path):
    """Saves the generated background image."""
    background = Image.fromarray(image_array)
    background.save(output_path)

# Extract dominant colors from images
extracted_colors = extract_colors_from_images(IMAGE_FOLDER)

# If no colors extracted, set default light colors
if not extracted_colors:
    extracted_colors = [(255, 200, 220), (200, 220, 255), (220, 255, 200)]  # Light pastel tones

# Generate the background
background_array = create_gradient_background(extracted_colors)

# Save the background image
save_background(background_array, OUTPUT_IMAGE)

print(f"Background generated and saved as: {OUTPUT_IMAGE}")



