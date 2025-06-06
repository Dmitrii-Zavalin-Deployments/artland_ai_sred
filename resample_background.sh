#!/bin/bash

# Get the absolute path for the workspace (GitHub Actions sets this)
WORKSPACE_PATH="${GITHUB_WORKSPACE}"

# Folder containing the images
IMAGE_FOLDER="$WORKSPACE_PATH/book_compilation"

# Input filename
INPUT_FILE="$IMAGE_FOLDER/background.jpg"

# Check if background.jpg exists
if [[ ! -f "$INPUT_FILE" ]]; then
    echo "[ERROR] File '$INPUT_FILE' not found in '$IMAGE_FOLDER'!"
    exit 1
fi

echo "[INFO] Using ImageMagick to set DPI metadata to 350 for '$INPUT_FILE'."

# Use ImageMagick (modern syntax) to set the DPI metadata without resampling pixels.
# -set units PixelsPerInch ensures the density value is interpreted as DPI.
# The output file is specified as "$INPUT_FILE" to update it in place.
magick "$INPUT_FILE" -set units PixelsPerInch -density 350 "$INPUT_FILE"

# Ensure the command executed successfully
if [[ $? -ne 0 ]]; then
    echo "[ERROR] ImageMagick failed to update DPI metadata for '$INPUT_FILE'!"
    exit 1
fi

# Confirmation message
echo "[INFO] background.jpg's DPI metadata successfully updated to 350 inside '$IMAGE_FOLDER'."


