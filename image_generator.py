# image_generator.py

from huggingface_hub import InferenceClient
from PIL import Image

def generate_image(client: InferenceClient, prompt: str, width: int, height: int) -> Image.Image | None:
    """
    Generates an image using the Hugging Face Inference API.
    Returns a PIL Image object on success, or None on failure.
    """
    print(f"Generating base image of {width}x{height} pixels... This may take a moment.")
    try:
        generated_image = client.text_to_image(
            prompt,
            width=width,
            height=height
        )
        return generated_image
    except Exception as e:
        print(f"An error occurred during image generation: {e}")
        return None