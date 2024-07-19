from PIL import Image
import os
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

console = Console()

def check_image_requirements(image_path):
    results = []
    try:
        with Image.open(image_path) as img:
            # Check dimensions
            width, height = img.size
            if width == height:
                if 600 <= width <= 1200:
                    results.append((True, "The image dimensions are within the acceptable range (600 x 600 to 1200 x 1200 pixels)."))
                else:
                    results.append((False, "The image dimensions are not within the acceptable range (600 x 600 to 1200 x 1200 pixels)."))
            else:
                results.append((False, "The image dimensions must be in a square aspect ratio (equal width and height)."))

            # Check color mode
            if img.mode == 'RGB':
                results.append((True, "The image is in color (24 bits per pixel) in sRGB color space."))
            else:
                results.append((False, "The image must be in color (24 bits per pixel) in sRGB color space."))

            # Check file format
            if img.format == 'JPEG':
                results.append((True, "The image is in JPEG file format."))
            else:
                results.append((False, "The image must be in JPEG file format."))

            # Check file size
            file_size_kb = os.path.getsize(image_path) / 1024
            if file_size_kb <= 240:
                results.append((True, f"The image file size is {file_size_kb:.2f} kB, which is within the acceptable limit of 240 kB."))
            else:
                results.append((False, f"The image file size is {file_size_kb:.2f} kB, which exceeds the acceptable limit of 240 kB."))

            # Check compression ratio
            if file_size_kb <= (width * height * 3) / (20 * 1024):
                results.append((True, "The image compression ratio is within the acceptable limit of 20:1."))
            else:
                results.append((False, "The image compression ratio exceeds the acceptable limit of 20:1."))

    except Exception as e:
        results.append((False, f"An error occurred: {e}"))

    return results

def display_results(results):
    for is_valid, message in results:
        if is_valid:
            text = Text("✔ ", style="bold green") + Text(message)
        else:
            text = Text("✘ ", style="bold red") + Text(message)
        
        console.print(Panel(text, expand=False))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        console.print("[bold red]Usage: python check_image.py <image_path>[/bold red]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    results = check_image_requirements(image_path)
    display_results(results)
