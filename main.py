# main.py

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from datetime import datetime

# Import our own modules
import config
import image_generator
import image_processor

def run():
    """Main function to run the image generation and processing pipeline."""
    # --- 1. Load Configuration ---
    print("Loading configuration...")
    load_dotenv()
    api_token = os.getenv("HF_TOKEN")
    if not api_token:
        print("Hugging Face token not found. Make sure your .env file is set up correctly.")
        return

    try:
        with open("prompt.txt", "r", encoding="utf-8") as f:
            prompt = f.read().strip()
        print(f"Prompt loaded: '{prompt}'")
    except FileNotFoundError:
        print("'prompt.txt' file not found. Please create it and add your prompt.")
        return

    # --- 2. Set up API Client ---
    print(f"Using model: {config.MODEL_ID}")
    client = InferenceClient(model=config.MODEL_ID, token=api_token)

    # --- 3. Generate Image ---
    base_image = image_generator.generate_image(
        client,
        prompt,
        config.GEN_WIDTH,
        config.GEN_HEIGHT
    )

    # --- 4. Process and Save Image ---
    if base_image:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_processor.process_and_save_image(base_image, prompt, timestamp, config)
        print("\nProcess completed successfully!")
    else:
        print("\nProcess failed. No image was generated.")


if __name__ == "__main__":
    run()