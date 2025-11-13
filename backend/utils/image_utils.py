from PIL import Image

def convert_to_rgb(image_file):
    return Image.open(image_file).convert("RGB")
