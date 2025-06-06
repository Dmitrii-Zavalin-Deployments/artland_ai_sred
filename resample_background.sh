#!/bin/bash

# Get the absolute path for the workspace (GitHub Actions sets this)
WORKSPACE_PATH="${GITHUB_WORKSPACE}"

# Folder containing the images
IMAGE_FOLDER="$WORKSPACE_PATH/book_compilation"

# Input and temporary output filenames inside the folder
INPUT_FILE="$IMAGE_FOLDER/background.jpg"
TEMP_FILE="$IMAGE_FOLDER/background_scaled.jpg"

# Check if background.jpg exists
if [[ ! -f "$INPUT_FILE" ]]; then
    echo "[ERROR] File '$INPUT_FILE' not found in '$IMAGE_FOLDER'!"
    exit 1
fi

# Use ImageMagick to set the density to 350 DPI
convert "$INPUT_FILE" -density 350 "$TEMP_FILE"

# Ensure the temporary file was created successfully
if [[ ! -f "$TEMP_FILE" ]]; then
    echo "[ERROR] Converted image '$TEMP_FILE' not created!"
    exit 1
fi

# Replace the original file with the scaled version
mv "$TEMP_FILE" "$INPUT_FILE"

# Confirmation message
echo "[INFO] background.jpg successfully converted to 350 DPI inside '$IMAGE_FOLDER'."



