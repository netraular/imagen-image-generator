# generate_image.py

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from PIL import Image
from datetime import datetime

def make_white_transparent(img):
    """
    Takes a PIL image and converts all white pixels (255,255,255) to transparent.
    Returns a new image with the changes applied.
    """
    # Convert the image to RGBA if it isn't already (to support the Alpha/transparency channel)
    img = img.convert("RGBA")
    
    pixel_data = img.getdata()
    
    new_pixel_data = []
    for item in pixel_data:
        # If the pixel is white (R,G,B are 255), change it to a transparent pixel
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_pixel_data.append((255, 255, 255, 0)) # The last value (0) means full transparency
        else:
            new_pixel_data.append(item) # Otherwise, keep the original pixel
            
    img.putdata(new_pixel_data)
    return img

# --- 0. Configuration ---
BASE_OUTPUT_FOLDER = "generated_images"
ORIGINAL_FOLDER = os.path.join(BASE_OUTPUT_FOLDER, "originals")
FINAL_FOLDER = os.path.join(BASE_OUTPUT_FOLDER, "pixel_art")

MODEL_ID = "black-forest-labs/FLUX.1-dev"

# Generation dimensions (discovered to work with FLUX.1-dev)
GEN_WIDTH = 256
GEN_HEIGHT = 256

# Final desired dimensions for the asset
FINAL_WIDTH = 32
FINAL_HEIGHT = 32

# --- 1. Load Configuration ---
print("Loading configuration...")
load_dotenv()
api_token = os.getenv("HF_TOKEN")
if not api_token:
    raise ValueError("Hugging Face token not found. Make sure your .env file is set up correctly.")

try:
    with open("prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read().strip()
    print(f"Prompt loaded: '{prompt}'")
except FileNotFoundError:
    raise FileNotFoundError("'prompt.txt' file not found. Please create it in the same folder as the script.")

# --- 2. Set up API Client ---
print(f"Using model: {MODEL_ID}")
client = InferenceClient(model=MODELO_ID, token=api_token)

# --- 3. Generate Image ---
print(f"Generating base image of {GEN_WIDTH}x{GEN_HEIGHT} pixels... This may take a moment.")

try:
    generated_image = client.text_to_image(
        prompt,
        width=GEN_WIDTH,
        height=GEN_HEIGHT
    )

    # --- 4. Save and Process Images ---
    os.makedirs(ORIGINAL_FOLDER, exist_ok=True)
    os.makedirs(FINAL_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save the ORIGINAL image
    original_filename = f"original_{timestamp}_{GEN_WIDTH}x{GEN_HEIGHT}.png"
    original_filepath = os.path.join(ORIGINAL_FOLDER, original_filename)
    generated_image.save(original_filepath)
    print(f"-> Original image saved to: '{original_filepath}'")

    # Resize the final image
    print(f"Resizing image to {FINAL_WIDTH}x{FINAL_HEIGHT} pixels...")
    final_image = generated_image.resize(
        (FINAL_WIDTH, FINAL_HEIGHT),
        resample=Image.NEAREST 
    )
    
    # --- KEY CHANGE: Transparency Logic ---
    # Check if the prompt asks for a white background (case-insensitive)
    if "white background" in prompt.lower():
        print("-> 'white background' detected in prompt. Applying transparency...")
        final_image = make_white_transparent(final_image)

    # Save the FINAL (and possibly transparent) image
    final_filename = f"pixelart_{timestamp}_{FINAL_WIDTH}x{FINAL_HEIGHT}.png"
    final_filepath = os.path.join(FINAL_FOLDER, final_filename)
    final_image.save(final_filepath)
    print(f"-> Final image saved to: '{final_filepath}'")
    
    print("\nProcess completed successfully!")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Possible causes: The model may be loading (this can take several minutes on the first run), the service is busy, or the resolution is not supported.")