import os
from fastapi import HTTPException
from wand.image import Image as WandImage
from PIL import Image, ImageOps
import win32print
import win32api
from wand.color import Color
from services.zpl_converter import convert_png_to_zpl


def print_datamatrix(printer, width, height):
    try:
        target_width_mm = width
        target_height_mm = height
        dpi = get_printer_dpi(printer)

        # Рабочие директории
        root_dir = os.getcwd()
        file_path = os.path.join(root_dir, 'datamatrix1.txt')
        tmp_png = os.path.join(root_dir, 'tmp', 'tmp1.png')

        # Чтение SVG
        with open(file_path, "r", encoding="utf-8") as file:
            svg_data = file.read()

        # Рендеринг изображения
        render_dpi = dpi * 4
        with WandImage(blob=svg_data.encode('utf-8'), format='svg', resolution=render_dpi) as img:
            img.format = 'png'
            img.compression = 'no'
            img.background_color = Color('white')
            img.alpha_channel = 'remove'
            img.save(filename=tmp_png)

        # Открываем изображение и изменяем размер с учетом параметров
        pil_img = Image.open(tmp_png)
        target_width_px = int(target_width_mm / 25.4 * dpi)
        target_height_px = int(target_height_mm / 25.4 * dpi)

        pil_img = ImageOps.contain(pil_img, (target_width_px, target_height_px), method=Image.LANCZOS)

        # Создаем финальное изображение
        final_width_px = target_width_px
        final_height_px = target_height_px

        final_img = Image.new("RGB", (final_width_px, final_height_px), "white")

        paste_x = (final_width_px - pil_img.width) // 2
        paste_y = (final_height_px - pil_img.height) // 2
        final_img.paste(pil_img, (paste_x, paste_y))

        # Сохраняем с нужным dpi
        final_img.save(tmp_png, dpi=(dpi, dpi))

        # Печать
        zpl = convert_png_to_zpl(tmp_png)
        send_zpl_to_printer(zpl, printer)

        return {"message": f"Этикетка {target_width_mm}x{target_height_mm} мм отправлена на принтер: {printer}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")


def get_printer_dpi(printer):
    handle = win32print.OpenPrinter(printer)
    try:
        properties = win32print.GetPrinter(handle, 2)
        devmode = properties["pDevMode"]
        dpi = devmode.PrintQuality
        return dpi
    finally:
        win32print.ClosePrinter(handle)


def send_zpl_to_printer(zpl, printer):
    hprinter = win32print.OpenPrinter(printer)
    try:
        win32print.StartDocPrinter(hprinter, 1, ("ZPL Label", None, "RAW"))
        win32print.StartPagePrinter(hprinter)
        win32print.WritePrinter(hprinter, zpl.encode('utf-8'))
        win32print.EndPagePrinter(hprinter)
        win32print.EndDocPrinter(hprinter)
    finally:
        win32print.ClosePrinter(hprinter)
