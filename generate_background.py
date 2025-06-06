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

# Global list to store extracted colors
unique_colors = []

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

    # Filter and store light colors
    filtered_colors = []
    for color in colors:
        hsv = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_RGB2HSV)[0][0]
        if hsv[2] > BRIGHTNESS_THRESHOLD:  # V-channel brightness check
            filtered_colors.append(color.tolist())

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
        unique_colors.extend(extracted_colors)  # Add new extracted colors

    # Log the updated unique color list
    print(f"[INFO] Updated unique color list: {unique_colors}")

def group_colors_by_hue_and_lightness(colors):
    """Groups colors by hue and lightness similarity for smoother transitions."""
    if not colors:
        return colors

    # Convert to HSV for better grouping by hue and brightness
    colors_hsv = [cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_RGB2HSV)[0][0] for color in colors]

    # Sort colors by Hue and Lightness (V channel)
    colors_sorted = [color for _, _, color in sorted(zip([hsv[0] for hsv in colors_hsv], [hsv[2] for hsv in colors_hsv], colors))]

    return colors_sorted

def create_smoother_gradient_background(colors, width=800, height=1200):
    """Generates a **highly blended, grouped-color gradient background**."""
    gradient = np.zeros((height, width, 3), dtype=np.uint8)

    colors = group_colors_by_hue_and_lightness(colors)  # Group colors by hue and lightness before blending

    for i in range(height):
        blend_factor = np.sin((i / height) * np.pi)  # Sin wave for dynamic blending
        color1 = np.array(random.choice(colors))
        color2 = np.array(random.choice(colors))
        color3 = np.array(random.choice(colors))  # Additional refined blending

        mixed_color = (
            (1 - blend_factor) * color1 +
            (blend_factor * 0.4) * color2 +
            (blend_factor * 0.6) * color3
        )

        # Introduce subtle variations to reduce abrupt shifts
        noise_intensity = random.randint(-10, 10)
        mixed_color = np.clip(mixed_color + noise_intensity, 0, 255)

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
    unique_colors = [[255, 200, 220], [200, 220, 255], [220, 255, 200]]  # Light pastel tones

# Generate the **grouped and smoother** background
background_array = create_smoother_gradient_background(unique_colors)

# Save the background image
save_background(background_array, OUTPUT_IMAGE)

print(f"[INFO] Background generated with **stronger blending, color harmony, and shading variations** and saved as: {OUTPUT_IMAGE}")



