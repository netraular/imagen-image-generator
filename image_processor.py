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


# --- Interactive Standalone Execution (MODIFIED) ---

def run_interactive_mode():
    """
    Runs a simplified interactive console menu to re-process an existing image.
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

    selected_index = -1
    while True:
        try:
            choice = input(f"\nEnter the number of the image (1-{len(image_files)}): ")
            selected_index = int(choice) - 1
            if 0 <= selected_index < len(image_files):
                break
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    selected_filename = image_files[selected_index]
    input_path = os.path.join(config.ORIGINAL_FOLDER, selected_filename)
    print(f"\n> You selected: '{selected_filename}'")

    # --- Simplified yes/no prompt ---
    apply_processing = False
    while True:
        # Updated prompt to be more accurate
        choice = input("> Apply background removal and square framing (preserves aspect ratio)? (y/n): ").lower().strip()
        if choice in ['y', 'yes']:
            apply_processing = True
            break
        elif choice in ['n', 'no']:
            apply_processing = False
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    print("\nStarting processing...")
    try:
        image_to_process = Image.open(input_path)
    except Exception as e:
        print(f"Error: Could not open or read image file. Reason: {e}")
        return

    # Step 1: Apply transparency and framing if requested
    if apply_processing:
        image_to_process = remove_background(image_to_process)
        image_to_process = crop_and_pad_to_square(image_to_process)
    else:
        print("Skipping background removal and framing.")

    # Step 2: Resize AFTER optional processing has been applied
    print(f"Resizing image to {config.FINAL_WIDTH}x{config.FINAL_HEIGHT} pixels...")
    final_image = image_to_process.resize(
        (config.FINAL_WIDTH, config.FINAL_HEIGHT),
        resample=Image.NEAREST
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_filename = f"pixelart_{timestamp}_{config.FINAL_WIDTH}x{config.FINAL_HEIGHT}.png"
    
    os.makedirs(config.FINAL_FOLDER, exist_ok=True)
    final_filepath = os.path.join(config.FINAL_FOLDER, final_filename)
    
    final_image.save(final_filepath)
    print(f"\n✅ Processing complete!")
    print(f"-> Final image saved to: '{final_filepath}'")

if __name__ == "__main__":
    run_interactive_mode()