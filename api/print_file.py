import os
import base64
from services.tmp_service import create_tmp_dir
from services.printer_service import send_file_to_printer


def print_file(format: str, printer: str, filename: str, data: str):
    PRINTABLE_FORMATS = [
        "JPG", "JPEG", "PNG", "BMP", "GIF", "TIF", "TIFF", "WEBP", "HEIC", "AVIF",
        "PDF", "SVG", "ICO", "PSD", "DJVU", "TXT", "EPS", "PS", "AI"
    ]

    format = format.upper()
    if format not in PRINTABLE_FORMATS:
        return {"message": f"Format {format} not supported!"}

    try:
        file_data = base64.b64decode(data)
    except Exception as e:
        return {"message": f"Error decoding base64 data: {str(e)}"}

    try:
        tmp_dir = create_tmp_dir()
        safe_filename = os.path.basename(filename)
        temp_filename = os.path.join(tmp_dir, f"{safe_filename}.{format.lower()}")

        with open(temp_filename, "wb") as temp_file:
            temp_file.write(file_data)

        send_file_to_printer(temp_filename, printer)

        return {"message": f"{safe_filename} отправлен на печать"}

    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}
