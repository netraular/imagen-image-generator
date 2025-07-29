# Hugging Face API Image Generator

This project uses the Hugging Face Inference API to generate images from a text prompt and then processes them into pixel art assets. It features a powerful, AI-based background removal tool and an interactive mode for reprocessing existing images.

## Features

-   **Modular Codebase**: Logic is separated into configuration, generation, and processing modules.
-   **Text-to-Image Generation**: Creates an image from a text description in `prompt.txt`.
-   **AI-Powered Background Removal**: Automatically uses the `rembg` library to accurately remove backgrounds from all generated images by identifying the main subject.
-   **Centralized Configuration**: All key settings (model ID, image dimensions) are in `config.py`.
-   **Secure API Key Handling**: Uses a `.env` file to keep your API token safe and private.
-   **Interactive Reprocessing**: Run the `image_processor.py` script to choose from a list of existing images and re-apply processing settings, saving you from re-generating images.
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

## How to Use

This project has two main uses: generating a new image, or reprocessing an existing one.

### Usage 1: Generating a New Image

This is the main workflow for creating a brand new asset. AI background removal is applied automatically.

1.  Edit the `prompt.txt` file with your desired image description.
2.  (Optional) Adjust settings in `config.py` (model, dimensions, etc.).
3.  Run the main script from your terminal:
    ```bash
    python main.py
    ```
4.  The script will generate the image, automatically remove the background, resize it, and save both the original and final versions in the `generated_images/` folder.

### Usage 2: Reprocessing an Existing Image

Use this to re-apply scaling or transparency to an image you've already generated, without calling the API again.

1.  Run the image processor script **without any arguments**:
    ```bash
    python image_processor.py
    ```
2.  The script will list all images in the `generated_images/originals/` folder.
3.  Enter the number corresponding to the image you want to process.
4.  You will be asked if you want to apply AI background removal. Answer `y` (yes) or `n` (no).
5.  The new processed image will be saved in the `generated_images/pixel_art/` folder.

## Customization

-   **`config.py`**: Change the `MODEL_ID`, `GEN_WIDTH`, `GEN_HEIGHT`, `FINAL_WIDTH`, or `FINAL_HEIGHT` to fit your needs.