# Importing Required Modules
from rembg import remove
from PIL import Image

img = Image.open("notepaper.png")


img.save("notepaper.jpeg", "JPEG", quality=85)
