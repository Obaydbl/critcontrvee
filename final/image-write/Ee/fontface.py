import freetype
import numpy


face = freetype.Face("hwriting2.ttf")
face.set_char_size(48*64)

width, height = bitmap.width, bitmap.rows

pixel_data = np.array
