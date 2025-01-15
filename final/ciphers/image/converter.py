from PIL import Image
import sys
import subprocess
import os


if len(sys.argv) != 4:
    print("Usage: converter.py image1.bmp output text.txt")
    sys.exit(1)

subprocess.run(['./image'] + sys.argv[1:])
bmp_image = Image.open(sys.argv[2])
os.remove(sys.argv[2])
bmp_image.save(sys.argv[2] + ".png", format='PNG')

