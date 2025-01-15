import freetype
import numpy as np

face = freetype.Face("hwriting2.ttf")
face.set_char_size(int(0.25 * 48*64))


with open('bitmaps2.txt', 'w') as file:
    with open('sizes2.txt', 'w') as file2:
        file2.write("uint8_t sizes[94][2] = {")
        for i in range(33, 127, 1):
            face.load_char(chr(i))
            bitmap = face.glyph.bitmap
            bitmap_array = (np.array(bitmap.buffer, dtype=np.uint8).reshape(bitmap.rows, bitmap.width)).tolist()
            file.write("uint8_t _" + str(i) + "[" + str(bitmap.rows) + "][" + str(bitmap.width) + "] = " + str(bitmap_array).replace('[', '{').replace(']', '}') + ';' + '\n' + '\n')
            file2.write(", {" + str(bitmap.rows) + ", " + str(bitmap.width) + "}")

        file2.write("};")

with open('pointers2.txt', 'w') as file:
    file.write("uint8_t* ptr[94];\n")
    for i in range(33, 127, 1):
        file.write("ptr["+ str(i - 33)+ "] = _" + str(i) + "[0];" + "\n")





