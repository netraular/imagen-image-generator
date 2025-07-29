# image_processor.py

import os
from PIL import Image
from datetime import datetime
import rembg

# Import config to use dimensions and paths
import config

def remove_background(img: Image.Image) -> Image.Image:
    """
    Uses the 'rembg' library to remove the background using a pre-trained AI model.

    This is the primary method for background removal due to its high accuracy
    with both simple and complex backgrounds.

    Args:
        img: The input PIL Image.

    Returns:
        A new PIL Image with the background removed.
    """
    print("Applying AI background removal... This might take a moment.")
    # The rembg.remove function handles all the complexity.
    return rembg.remove(img)

def crop_and_pad_to_square(img: Image.Image) -> Image.Image:
    """
    Crops an image to its content, then pads it with transparency to make it square.

    This preserves the original aspect ratio of the object by creating a square
    canvas based on the object's longest side and centering the object within it.

    Args:
        img: The input PIL Image, expected to have an alpha channel.

    Returns:
        A new, square PIL Image with the original content centered.
    """
    # Ensure the image has an alpha channel
    img = img.convert("RGBA")

    # Get the bounding box of the non-alpha part of the image
    bbox = img.getbbox()

    if not bbox:
        # If the image is completely transparent, return it as is
        print("Warning: Image is fully transparent. Skipping crop and pad.")
        return img

    # Crop the image to the content
    cropped_img = img.crop(bbox)

    # Determine the longest side of the cropped content
    width, height = cropped_img.size
    max_side = max(width, height)

    # Create a new square canvas with a transparent background
    print(f"Framing content in a new {max_side}x{max_side} square canvas...")
    square_canvas = Image.new("RGBA", (max_side, max_side), (0, 0, 0, 0))

    # Calculate the position to paste the cropped image to center it
    paste_x = (max_side - width) // 2
    paste_y = (max_side - height) // 2

    # Paste the cropped image onto the square canvas
    square_canvas.paste(cropped_img, (paste_x, paste_y))

    return square_canvas


def process_and_save_image(
    original_image: Image.Image,
    prompt: str,
    timestamp: str,
    config: object
) -> None:
    """
    Processes a newly generated image: saves the original, removes the background,
    frames it in a square, resizes it, and saves the final version.
    This function is used by the main generation pipeline.
    """
    os.makedirs(config.ORIGINAL_FOLDER, exist_ok=True)
    os.makedirs(config.FINAL_FOLDER, exist_ok=True)

    # --- Save the original high-resolution image first ---
    original_filename = f"original_{timestamp}_{config.GEN_WIDTH}x{config.GEN_HEIGHT}.png"
    original_filepath = os.path.join(config.ORIGINAL_FOLDER, original_filename)
    original_image.save(original_filepath)
    print(f"-> Original image saved to: '{original_filepath}'")

    # --- Step 1: Automatically apply AI background removal ---
    processed_image = remove_background(original_image)

    # --- Step 2: Crop and pad to a square to preserve aspect ratio ---
    processed_image = crop_and_pad_to_square(processed_image)

    # --- Step 3: Resize to final pixel art dimensions ---
    print(f"Resizing image to {config.FINAL_WIDTH}x{config.FINAL_HEIGHT} pixels...")
    final_image = processed_image.resize(
        (config.FINAL_WIDTH, config.FINAL_HEIGHT),
        resample=Image.NEAREST
    )

    # --- Step 4: Save the final processed image ---
    final_filename = f"pixelart_{timestamp}_{config.FINAL_WIDTH}x{config.FINAL_HEIGHT}.png"
    final_filepath = os.path.join(config.FINAL_FOLDER, final_filename)
    final_image.save(final_filepath)
    print(f"-> Final image saved to: '{final_filepath}'")


# --- BATCH PROCESSING MODE ---

def run_batch_mode():
    """
    Automatically processes all images found in the BATCH_INPUT_FOLDER.
    This mode is non-interactive. It applies the full processing pipeline
    (background removal, framing, resizing) to each image.
    """
    print("--- Batch Processing Mode ---")

    if not os.path.isdir(config.BATCH_INPUT_FOLDER):
        print(f"Error: The batch input folder '{config.BATCH_INPUT_FOLDER}' was not found.")
        print("Please create it and add images to process.")
        return

    print(f"Searching for images in '{config.BATCH_INPUT_FOLDER}'...")
    try:
        image_files = sorted([
            f for f in os.listdir(config.BATCH_INPUT_FOLDER)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))
        ])
    except FileNotFoundError:
        print(f"Error: The batch input folder was not found at '{config.BATCH_INPUT_FOLDER}'")
        return

    if not image_files:
        print(f"No images found in '{config.BATCH_INPUT_FOLDER}'. Nothing to do.")
        return

    print(f"Found {len(image_files)} image(s) to process.")
    os.makedirs(config.FINAL_FOLDER, exist_ok=True)

    for filename in image_files:
        print(f"\n--- Processing '{filename}' ---")
        input_path = os.path.join(config.BATCH_INPUT_FOLDER, filename)
        
        try:
            image_to_process = Image.open(input_path)
            
            # Step 1: Apply background removal
            processed_image = remove_background(image_to_process)
            
            # Step 2: Crop and pad to a square
            processed_image = crop_and_pad_to_square(processed_image)

            # Step 3: Resize to final dimensions
            print(f"Resizing image to {config.FINAL_WIDTH}x{config.FINAL_HEIGHT} pixels...")
            final_image = processed_image.resize(
                (config.FINAL_WIDTH, config.FINAL_HEIGHT),
                resample=Image.NEAREST
            )

            # Step 4: Save the final image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(filename)[0]
            final_filename = f"pixelart_{base_name}_{timestamp}_{config.FINAL_WIDTH}x{config.FINAL_HEIGHT}.png"
            final_filepath = os.path.join(config.FINAL_FOLDER, final_filename)
            
            final_image.save(final_filepath)
            print(f"-> Final image saved to: '{final_filepath}'")

        except Exception as e:
            print(f"Error: Could not process '{filename}'. Reason: {e}")
            continue

    print("\n✅ Batch processing complete!")


# The interactive mode function is kept in case it's needed by other modules
# in the future, but it is no longer called when this script is run directly.
def run_interactive_mode():
    """
    Runs an interactive console menu to re-process an existing image
    from the 'originals' folder.
    """
    print("--- Image Processor Interactive Mode ---")
    if not os.path.isdir(config.ORIGINAL_FOLDER):
        print(f"Error: The originals folder was not found at '{config.ORIGINAL_FOLDER}'")
        return

    try:
        image_files = sorted([f for f in os.listdir(config.ORIGINAL_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))])
    except FileNotFoundError:
        print(f"Error: The folder '{config.ORIGINAL_FOLDER}' does not exist.")
        return

    if not image_files:
        print(f"No images found in '{config.ORIGINAL_FOLDER}'.")
        return

    print("\nPlease select an image to process from the list below:")
    for i, filename in enumerate(image_files, 1):
        print(f"  {i}: {filename}")

    # ... [rest of the function is unchanged but will not be called] ...


if __name__ == "__main__":
    # When this script is executed, it will always run in batch mode.
    run_batch_mode()