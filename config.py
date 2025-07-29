# config.py

import os

# --- File and Folder Paths ---
BASE_OUTPUT_FOLDER = "generated_images"
ORIGINAL_FOLDER = os.path.join(BASE_OUTPUT_FOLDER, "originals")
FINAL_FOLDER = os.path.join(BASE_OUTPUT_FOLDER, "pixel_art")
BATCH_INPUT_FOLDER = "batch_input" # New folder for automatic processing

# --- Model Configuration ---
MODEL_ID = "black-forest-labs/FLUX.1-dev"

# --- Image Dimensions ---
# Dimensions for the initial generation
GEN_WIDTH = 256
GEN_HEIGHT = 256

# Final desired dimensions for the pixel art asset
FINAL_WIDTH = 32
FINAL_HEIGHT = 32