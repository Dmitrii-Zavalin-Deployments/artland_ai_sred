from PIL import Image

# Load the original image
original_image = Image.open("background.jpg")

# Get dimensions
width, height = original_image.size

# Set scale factors
scale_factor_y = 10  # Adjust for vertical resizing (higher value increases height)
num_repeats_x = 10   # Adjust for horizontal duplication

# Scale the image vertically using bicubic interpolation
scaled_height = height * scale_factor_y
scaled_image = original_image.resize((width, scaled_height), Image.Resampling.BICUBIC)

# Create a new blank image for horizontal duplication
expanded_width = width * num_repeats_x
new_image = Image.new("RGB", (expanded_width, scaled_height))

# Paste the scaled image multiple times horizontally
for i in range(num_repeats_x):
    new_image.paste(scaled_image, (i * width, 0))

# Overwrite the original image file
new_image.save("background.jpg")
print("Image successfully expanded and replaced!")



