#!/bin/bash

# Input and temporary output filenames
INPUT_FILE="background.jpg"
TEMP_FILE="background_scaled.jpg"

# Use ImageMagick to resample the image to 350 DPI
magick "$INPUT_FILE" -resample 350 "$TEMP_FILE"

# Replace the original file with the scaled version
mv "$TEMP_FILE" "$INPUT_FILE"

# Confirmation message
echo "[INFO] background.jpg successfully resampled to 350 DPI."



