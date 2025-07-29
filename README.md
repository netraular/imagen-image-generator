# Hugging Face API Image Generator

This project uses the Hugging Face Inference API to generate images from a text prompt and then processes them into pixel art assets. It features a powerful, AI-based background removal tool, an aspect-ratio-preserving framing step, and a dedicated script for automatic batch processing.

## Features

-   **Modular Codebase**: Logic is separated into configuration, generation, and processing modules.
-   **Text-to-Image Generation**: Creates an image from a text description in `prompt.txt`.
-   **AI-Powered Background Removal**: Automatically uses the `rembg` library to accurately remove backgrounds.
-   **Aspect Ratio Preservation**: After background removal, the object is framed within a square canvas, adding transparent padding as needed. This ensures the object is not stretched or distorted when resized.
-   **Centralized Configuration**: All key settings (model ID, image dimensions, folders) are in `config.py`.
-   **Secure API Key Handling**: Uses a `.env` file to keep your API token safe and private.
-   **Automatic Batch Processing**: Simply add images to the `batch_input/` folder and run a script to process them all automatically.
-   **Organized File Output**: Saves original and processed images into `generated_images/originals/` and `generated_images/pixel_art/`.

## Requirements

-   Python 3.x
-   A [Hugging Face](https://huggingface.co/) account with an **Access Token** (`write` permissions).
-   The required Python libraries.

## Setup

1.  **Clone or download this project.**

2.  **Install the dependencies** from the project's root directory:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The first time you use the background removal feature, it may need to download the AI model, which can take a moment.*

3.  **Create a `.env` file** in the project root. Add your Hugging Face token like this:
    ```
    HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```

4.  **Create a `prompt.txt` file** in the project root. This is where you write the description of the image to generate. For example:
    ```txt
    A magical glowing sword, pixel art, white background
    ```
5.  **Create a `batch_input` folder** in the project's root directory. This is where you will place images for processing.

## How to Use

### Usage 1: Generating a New Image

This workflow creates a brand new asset from a text prompt.

1.  Edit the `prompt.txt` file with your desired image description.
2.  (Optional) Adjust settings in `config.py` (model, dimensions, etc.).
3.  Run the main script from your terminal:
    ```bash
    python main.py
    ```
4.  The script will:
    -   Generate the image from your prompt.
    -   Save the original in `generated_images/originals/`.
    -   Remove the background, frame it, and resize it.
    -   Save the final version in `generated_images/pixel_art/`.

### Usage 2: Processing Existing Images in Batch

Use this to automatically process one or more of your own images.

1.  Place any images you want to process (e.g., `.png`, `.jpg`) into the `batch_input` folder.
2.  Run the image processor script from your terminal:
    ```bash
    python image_processor.py
    ```
3.  The script will automatically find and process every image in the `batch_input` folder using the standard pipeline (background removal, framing, and resizing).
4.  All processed images will be saved in the `generated_images/pixel_art/` folder.

## Customization

-   **`config.py`**: Change the `MODEL_ID`, `GEN_WIDTH`, `GEN_HEIGHT`, `FINAL_WIDTH`, or `FINAL_HEIGHT` to fit your needs. You can also change the name of the `BATCH_INPUT_FOLDER`.