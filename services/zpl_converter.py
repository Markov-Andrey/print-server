from PIL import Image


def convert_png_to_zpl(filepath):
    with Image.open(filepath).convert('1') as img:  # конвертируем в черно-белый
        width, height = img.size
        bytes_per_row = (width + 7) // 8
        total_bytes = bytes_per_row * height
        hex_data = ""
        pixels = img.load()

        for y in range(height):
            byte = 0
            count = 0
            for x in range(width):
                # Важно: 0 = белый, 1 = чёрный
                bit = 0 if pixels[x, y] == 255 else 1  # Белый пиксель = 0, чёрный = 1
                byte = (byte << 1) | bit
                count += 1
                if count == 8:  # Если собралось 8 бит
                    hex_data += f"{byte:02X}"
                    byte = 0
                    count = 0

            if count > 0:  # Если остались недозаполненные биты
                byte = byte << (8 - count)  # Дополняем оставшиеся биты
                hex_data += f"{byte:02X}"

        zpl = f"~DGR:IMG.GRF,{total_bytes},{bytes_per_row},{hex_data}\n"
        zpl += "^XA\n"
        zpl += "^FO0,0^XGR:IMG.GRF,1,1^FS\n"
        zpl += "^XZ\n"

        return zpl
