# Hugging Face API Image Generator

This is a simple Python script that uses the free Hugging Face Inference API to generate images from a text description (prompt). The script is designed to be modular and easy to customize.

## Features

-   **Text-to-Image Generation**: Creates complex images from a simple text prompt.
-   **External Configuration**: Securely loads the API token from a `.env` file and the prompt from `prompt.txt`.
-   **Customizable Model**: Allows for easily swapping out the Hugging Face model (default is `FLUX.1-dev`).
-   **Dual-Format Output**: Generates a high-resolution image (e.g., 256x256) and resizes it to a smaller pixel art format (e.g., 32x32).
-   **Organized File Output**: Saves the original and pixel art images into separate subfolders (`originals/` and `pixel_art/`).
-   **Automatic Transparency**: If the prompt contains the phrase "white background", the background of the final pixel art image will be made transparent.

## Requirements

-   Python 3.x
-   A [Hugging Face](https://huggingface.co/) account with an **Access Token** that has `write` permissions.
-   The following Python libraries:

```bash
pip install huggingface_hub python-dotenv Pillow
```

## Setup

1.  **Clone or download this project.**

2.  **Install the dependencies** using the command above.

3.  **Create a `.env` file** in the project root. This file will store your secret token. Add the following line, replacing `hf_...` with your actual token:
    ```
    HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```

4.  **Create a `prompt.txt` file** in the project root. This is where you will write the description of the image you want to generate. For example:
    ```txt
    8x8 pixel art simple minimalistic small straw bed. White background.
    ```

## How to Use

1.  Modify the `prompt.txt` file with your desired image description.
2.  Open a terminal in the project folder.
3.  Run the script:
    ```bash
    python generate_image.py
    ```
4.  Done! Check the `generated_images/` folder. You will find the high-resolution image in `originals/` and the pixel art version in `pixel_art/`.

## Customization

You can easily modify the script's behavior by editing the constants in the `# --- 0. Configuration ---` section of the `generate_image.py` file:

-   `MODEL_ID`: Change the Hugging Face model you want to use.
-   `GEN_WIDTH` / `GEN_HEIGHT`: Adjust the resolution of the original generated image (make sure it's compatible with the model).
-   `FINAL_WIDTH` / `FINAL_HEIGHT`: Change the final size of the pixel art image.

## Project Structure

```
my_project/
├── .env                # Stores your secret API token
├── prompt.txt          # This is where you write the image description
├── generate_image.py   # The main script
├── generated_images/   # Auto-created folder for the output
│   ├── originals/      # Stores the high-resolution images
│   └── pixel_art/      # Stores the resized (and transparent) images
└── README.md           # This file
```