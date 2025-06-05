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
NUM_COLORS_PER_IMAGE = 5   # Reduced number of clusters per image for efficiency

# Global set for storing unique colors across all images
unique_colors = set()

def extract_colors_from_image(image_path):
    """Extracts dominant colors from a single image."""
    print(f"[INFO] Processing image: {image_path}")  # Log start

    image = cv2.imread(image_path)
    if image is None:
        print(f"[WARNING] Could not read image: {image_path}")
        return []

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    reshaped_image = image.reshape(-1, 3)

    # Use KMeans to find dominant colors
    kmeans = KMeans(n_clusters=NUM_COLORS_PER_IMAGE, random_state=42, n_init=10)
    kmeans.fit(reshaped_image)
    colors = kmeans.cluster_centers_.astype(int)

    # Filter out dark colors using HSV
    filtered_colors = set()
    for color in colors:
        hsv = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_RGB2HSV)[0][0]
        if hsv[2] > BRIGHTNESS_THRESHOLD:  # V-channel brightness check
            filtered_colors.add(tuple(color))  # Store as tuple for uniqueness

    print(f"[INFO] Colors extracted from {image_path}: {filtered_colors}")

    return filtered_colors

def process_images(image_folder):
    """Loops through images, extracts colors, and accumulates unique colors."""
    image_files = glob(os.path.join(image_folder, "*.jpg"))
    
    if not image_files:
        print("[ERROR] No .jpg images found in the folder!")
        return

    for image_path in image_files:
        extracted_colors = extract_colors_from_image(image_path)
        unique_colors.update(extracted_colors)  # Add new unique colors
    
        # Log the updated unique color set after each image
        print(f"[INFO] Updated unique color set: {unique_colors}")

def create_gradient_background(colors, width=800, height=1200):
    """Generates a smooth gradient background using extracted light colors."""
    gradient = np.zeros((height, width, 3), dtype=np.uint8)

    for i in range(height):
        blend_factor = i / height
        color1 = np.array(random.choice(list(colors)))  # Convert set to list
        color2 = np.array(random.choice(list(colors)))
        mixed_color = (1 - blend_factor) * color1 + blend_factor * color2
        gradient[i, :] = mixed_color

    return gradient

def save_background(image_array, output_path):
    """Saves the generated background image."""
    background = Image.fromarray(image_array)
    background.save(output_path)

# Process images sequentially, accumulating colors
process_images(IMAGE_FOLDER)

# If no colors extracted, set default light colors
if not unique_colors:
    unique_colors = {(255, 200, 220), (200, 220, 255), (220, 255, 200)}  # Light pastel tones

# Generate the background
background_array = create_gradient_background(unique_colors)

# Save the background image
save_background(background_array, OUTPUT_IMAGE)

print(f"[INFO] Background generated and saved as: {OUTPUT_IMAGE}")



