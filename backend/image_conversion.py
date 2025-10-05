from PIL import Image
from pillow_heif import register_heif_opener

# Enable HEIF/HEIC support
register_heif_opener()

def convert_any_to_png(input_path: str) -> Image.Image:
    """
    Converts an input image (any format supported by Pillow) to a PNG-compatible
    Image object in memory. Does not save to disk.
    Flask or upstream logic should validate the file extension.
    """
    with Image.open(input_path) as img:
        return img.convert("RGB") 