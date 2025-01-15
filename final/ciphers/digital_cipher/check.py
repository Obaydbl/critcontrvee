import freetype
import numpy as np
from math import ceil, floor

face = freetype.Face("dseg14.ttf")
face.set_char_size(int(0.6*48*64))

with open('bitmaps.txt', 'w') as file:
    with open('sizes.txt', 'w') as file2:
        with open('offsets.txt', 'w') as file3:
            file2.write("uint8_t sizes[94][2] = {")
            file3.write("uint8_t offsets[94][2] = {")
            for i in range(33, 127, 1):
                face.load_char(chr(i))
                units_per_em = face.units_per_EM
                lsb_pixels = face.glyph.metrics.horiBearingX * face.size.x_ppem * 0.6 / units_per_em
                tsb_pixles = face.glyph.metrics.horiBearingY * face.size.x_ppem * 0.6 / units_per_em
                if i in [88, 89, 120, 121]:
                    lsb_pixels -=1
                    tsb_pixles +=0
                elif i == 44:
                    lsb_pixels -=1
                    tsb_pixles +=1

                bitmap = face.glyph.bitmap
                bitmap_array = (np.array(bitmap.buffer, dtype=np.uint8).reshape(bitmap.rows, bitmap.width)).tolist()
                file.write("uint8_t _" + str(i) + "[" + str(bitmap.rows) + "][" + str(bitmap.width) + "] = " + str(bitmap_array).replace('[', '{').replace(']', '}') + ';' + '\n' + '\n')
                file2.write(", {" + str(bitmap.rows) + ", " + str(bitmap.width) + "}")
                file3.write(", {" + str(round(tsb_pixles)) + ", " + str(round(lsb_pixels)) + "}")

            file2.write("};")
            file3.write("};")


with open('pointers.txt', 'w') as file:
    file.write("uint8_t* ptr[94];\n")
    for i in range(33, 127, 1):
        file.write("ptr["+ str(i - 33)+ "] = _" + str(i) + "[0];" + "\n")





