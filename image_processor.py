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

def process_and_save_image(
    original_image: Image.Image,
    prompt: str,
    timestamp: str,
    config: object
) -> None:
    """
    Processes a newly generated image: saves the original, removes the background,
    resizes it, and saves the final version.
    This function is used by the main generation pipeline.
    """
    os.makedirs(config.ORIGINAL_FOLDER, exist_ok=True)
    os.makedirs(config.FINAL_FOLDER, exist_ok=True)

    # --- Save the original high-resolution image first ---
    original_filename = f"original_{timestamp}_{config.GEN_WIDTH}x{config.GEN_HEIGHT}.png"
    original_filepath = os.path.join(config.ORIGINAL_FOLDER, original_filename)
    original_image.save(original_filepath)
    print(f"-> Original image saved to: '{original_filepath}'")

    # --- Automatically apply AI background removal ---
    # No conditional checks needed, we always apply the best method.
    processed_image = remove_background(original_image)

    # --- Resize to final pixel art dimensions ---
    final_image = processed_image.resize(
        (config.FINAL_WIDTH, config.FINAL_HEIGHT),
        resample=Image.NEAREST
    )

    # --- Save the final processed image ---
    final_filename = f"pixelart_{timestamp}_{config.FINAL_WIDTH}x{config.FINAL_HEIGHT}.png"
    final_filepath = os.path.join(config.FINAL_FOLDER, final_filename)
    final_image.save(final_filepath)
    print(f"-> Final image saved to: '{final_filepath}'")


# --- Interactive Standalone Execution (SIMPLIFIED) ---

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
    apply_transparency = False
    while True:
        choice = input("> Apply AI background removal? (y/n): ").lower().strip()
        if choice in ['y', 'yes']:
            apply_transparency = True
            break
        elif choice in ['n', 'no']:
            apply_transparency = False
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    print("\nStarting processing...")
    try:
        image_to_process = Image.open(input_path)
    except Exception as e:
        print(f"Error: Could not open or read image file. Reason: {e}")
        return

    # Step 1: Apply AI transparency if requested
    if apply_transparency:
        image_to_process = remove_background(image_to_process)
    else:
        print("Skipping background removal.")

    # Step 2: Resize AFTER transparency has been applied
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