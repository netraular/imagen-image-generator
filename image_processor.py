# image_processor.py

import os
from PIL import Image
from datetime import datetime

def _make_white_transparent(img: Image.Image) -> Image.Image:
    """Converts all white pixels (255,255,255) to transparent."""
    img = img.convert("RGBA")
    pixel_data = img.getdata()
    
    new_pixel_data = []
    for item in pixel_data:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_pixel_data.append((255, 255, 255, 0))
        else:
            new_pixel_data.append(item)
            
    img.putdata(new_pixel_data)
    return img

def process_and_save_image(
    original_image: Image.Image,
    prompt: str,
    timestamp: str,
    config: object
) -> None:
    """
    Resizes, applies transparency if needed, and saves the original and final images.
    """
    # Create output directories if they don't exist
    os.makedirs(config.ORIGINAL_FOLDER, exist_ok=True)
    os.makedirs(config.FINAL_FOLDER, exist_ok=True)

    # --- Save the ORIGINAL image ---
    original_filename = f"original_{timestamp}_{config.GEN_WIDTH}x{config.GEN_HEIGHT}.png"
    original_filepath = os.path.join(config.ORIGINAL_FOLDER, original_filename)
    original_image.save(original_filepath)
    print(f"-> Original image saved to: '{original_filepath}'")

    # --- Process and save the FINAL image ---
    print(f"Resizing image to {config.FINAL_WIDTH}x{config.FINAL_HEIGHT} pixels...")
    final_image = original_image.resize(
        (config.FINAL_WIDTH, config.FINAL_HEIGHT),
        resample=Image.NEAREST 
    )
    
    # Apply transparency if "white background" is in the prompt
    if "white background" in prompt.lower():
        print("-> 'white background' detected. Applying transparency...")
        final_image = _make_white_transparent(final_image)

    # Save the final image
    final_filename = f"pixelart_{timestamp}_{config.FINAL_WIDTH}x{config.FINAL_HEIGHT}.png"
    final_filepath = os.path.join(config.FINAL_FOLDER, final_filename)
    final_image.save(final_filepath)
    print(f"-> Final image saved to: '{final_filepath}'")