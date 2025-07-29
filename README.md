# Hugging Face API Image Generator

This project provides a modular set of Python scripts that use the Hugging Face Inference API to generate images from a text description (prompt). The code is organized for readability, maintainability, and ease of customization.

## Features

-   **Modular Codebase**: The logic is separated into distinct files for configuration, image generation, and image processing (resizing, transparency).
-   **Text-to-Image Generation**: Creates complex images from a simple text prompt.
-   **Centralized Configuration**: All key settings (model ID, image dimensions) are managed in a single `config.py` file.
-   **Secure API Key Handling**: Loads the Hugging Face token securely from a `.env` file, keeping it out of the source code.
-   **Dual-Format Output**: Generates a high-resolution image and resizes it to a smaller pixel art format (e.g., 32x32).
-   **Organized File Output**: Saves the original and pixel art images into separate, auto-generated subfolders (`originals/` and `pixel_art/`).
-   **Automatic Transparency**: If the prompt contains the phrase "white background", the background of the final pixel art image is automatically made transparent.

## Requirements

-   Python 3.x
-   A [Hugging Face](https://huggingface.co/) account with an **Access Token** that has `write` permissions.
-   The required Python libraries, which can be installed from `requirements.txt`.

## Setup

1.  **Clone or download this project.**

2.  **Install the dependencies** by running the following command in your terminal from the project's root directory:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file** in the project root. This file will store your secret token. Add the following line, replacing `hf_...` with your actual token:
    ```
    HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```

4.  **Create a `prompt.txt` file** in the project root. This is where you will write the description of the image you want to generate. For example:
    ```txt
    A beautiful pixel art sword, magical, glowing, on a white background
    ```

## How to Use

1.  Modify the `prompt.txt` file with your desired image description.
2.  (Optional) Adjust any settings in the `config.py` file if you wish to use a different model or image size.
3.  Open a terminal in the project folder.
4.  Run the main script:
    ```bash
    python main.py
    ```
5.  Done! Check the `generated_images/` folder. You will find the high-resolution image in `originals/` and the final pixel art version in `pixel_art/`.

## Customization

You can easily modify the script's behavior by editing the **`config.py`** file.

-   `MODEL_ID`: Change the Hugging Face model you want to use.
-   `GEN_WIDTH` / `GEN_HEIGHT`: Adjust the resolution of the original generated image (make sure it's compatible with the model).
-   `FINAL_WIDTH` / `FINAL_HEIGHT`: Change the final size of the pixel art image.
-   `ORIGINAL_FOLDER` / `FINAL_FOLDER`: Change the names of the output directories.

## Project Structure

```
image_generation_project/
│
├── .env                  # Your secret API token (not committed to Git)
├── prompt.txt            # The input prompt for the image
├── requirements.txt      # Lists project dependencies for pip
│
├── config.py             # All configuration variables (model, dimensions)
├── image_generator.py    # Handles communication with the Hugging Face API
├── image_processor.py    # Handles resizing, transparency, and saving files
├── main.py               # The main script to run the entire process
│
├── generated_images/     # Auto-created folder for all output
│   ├── originals/        # Stores the original high-resolution images
│   └── pixel_art/        # Stores the final, processed pixel art images
│
└── README.md             # This file
```