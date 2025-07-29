# image_processor.py

import os
from PIL import Image
from datetime import datetime
from collections import deque

# Importamos config para usar las dimensiones y rutas
import config

def _make_background_transparent_flood_fill(img: Image.Image, threshold: int = 60, seed_pos: tuple = (0, 0)) -> Image.Image:
    """
    Usa un algoritmo de relleno por inundación (flood fill) para hacer transparente el fondo.

    Este método es mucho más preciso porque solo elimina los píxeles que están conectados
    a un punto de partida (la semilla) y tienen un color similar. Esto evita que se eliminen
    partes blancas o claras del objeto principal.

    Args:
        img: La imagen de entrada de PIL.
        threshold: Tolerancia de color para considerar un píxel como parte del fondo.
        seed_pos: La coordenada (x, y) desde donde empezar a "inundar" el fondo.
                  Por defecto es (0,0), la esquina superior izquierda.

    Returns:
        Una nueva imagen de PIL con el fondo transparente.
    """
    img = img.convert("RGBA")
    pixel_data = img.load()
    width, height = img.size

    # Color del píxel de partida (semilla)
    seed_color = pixel_data[seed_pos]
    
    # Cola para el algoritmo de relleno (Breadth-First Search)
    q = deque([seed_pos])
    
    # Conjunto para llevar registro de los píxeles ya visitados
    visited = set([seed_pos])

    while q:
        x, y = q.popleft()

        # Comprobar si el color del píxel actual está dentro del umbral del color semilla
        current_color = pixel_data[x, y]
        color_diff = sum(abs(current_color[i] - seed_color[i]) for i in range(3))

        if color_diff <= threshold:
            # Si es similar, lo hacemos transparente y añadimos sus vecinos a la cola
            pixel_data[x, y] = (255, 255, 255, 0) # Lo hacemos transparente

            # Explorar vecinos (arriba, abajo, izquierda, derecha)
            for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                    q.append((nx, ny))
                    visited.add((nx, ny))
    
    return img

# --- Mantenemos la función original por si acaso, pero ya no la usaremos en el modo interactivo ---
def process_and_save_image(
    original_image: Image.Image,
    prompt: str,
    timestamp: str,
    config: object
) -> None:
    # ... (El código de esta función no necesita cambios, ya que usa su propia lógica de prompt)
    os.makedirs(config.ORIGINAL_FOLDER, exist_ok=True)
    os.makedirs(config.FINAL_FOLDER, exist_ok=True)
    original_filename = f"original_{timestamp}_{config.GEN_WIDTH}x{config.GEN_HEIGHT}.png"
    original_filepath = os.path.join(config.ORIGINAL_FOLDER, original_filename)
    original_image.save(original_filepath)
    print(f"-> Original image saved to: '{original_filepath}'")
    final_image = original_image.resize(
        (config.FINAL_WIDTH, config.FINAL_HEIGHT),
        resample=Image.NEAREST
    )
    if "white background" in prompt.lower():
        print("-> 'white background' detected. Applying smart transparency...")
        # Podríamos actualizar esto para que también use el método nuevo
        final_image = _make_background_transparent_flood_fill(final_image)
    final_filename = f"pixelart_{timestamp}_{config.FINAL_WIDTH}x{config.FINAL_HEIGHT}.png"
    final_filepath = os.path.join(config.FINAL_FOLDER, final_filename)
    final_image.save(final_filepath)
    print(f"-> Final image saved to: '{final_filepath}'")


# --- Ejecución Independiente e Interactiva (ACTUALIZADA) ---

def run_interactive_mode():
    """
    Ejecuta un menú interactivo en la consola para procesar una imagen existente.
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

    apply_transparency = False
    while True:
        choice = input("> Apply SMART transparency to remove the background? (y/n): ").lower().strip()
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

    # --- ORDEN DE OPERACIONES CORREGIDO ---
    # Paso 1: Aplicar transparencia PRIMERO, sobre la imagen de alta resolución
    if apply_transparency:
        print("Applying SMART transparency (flood fill) on the original image...")
        image_to_process = _make_background_transparent_flood_fill(image_to_process)

    # Paso 2: Escalar DESPUÉS, una vez que el fondo ya está eliminado
    print(f"Resizing image to {config.FINAL_WIDTH}x{config.FINAL_HEIGHT} pixels...")
    final_image = image_to_process.resize(
        (config.FINAL_WIDTH, config.FINAL_HEIGHT),
        resample=Image.NEAREST
    )
    # --- FIN DEL CAMBIO ---

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_filename = f"pixelart_{timestamp}_{config.FINAL_WIDTH}x{config.FINAL_HEIGHT}.png"
    
    os.makedirs(config.FINAL_FOLDER, exist_ok=True)
    final_filepath = os.path.join(config.FINAL_FOLDER, final_filename)
    
    final_image.save(final_filepath)
    print(f"\n✅ Processing complete!")
    print(f"-> Final image saved to: '{final_filepath}'")

if __name__ == "__main__":
    run_interactive_mode()