import os
from fastapi import HTTPException
from wand.image import Image as WandImage
from PIL import Image, ImageOps, ImageWin
import win32print
import win32ui
from wand.color import Color

def print_datamatrix():
    try:
        # Настройки
        target_width_mm = 40
        target_height_mm = 25
        dpi = 300

        # Конвертация в пиксели
        target_width_px = int(target_width_mm / 25.4 * dpi)
        target_height_px = int(target_height_mm / 25.4 * dpi)

        # Пути
        root_dir = os.getcwd()
        file_path = os.path.join(root_dir, 'datamatrix1.txt')
        tmp_png = os.path.join(root_dir, 'tmp', 'tmp1.png')

        # Чтение SVG
        with open(file_path, "r", encoding="utf-8") as file:
            svg_data = file.read()

        # Рендеринг SVG в PNG через wand
        render_dpi = dpi * 4
        with WandImage(blob=svg_data.encode('utf-8'), format='svg', resolution=render_dpi) as img:
            img.format = 'png'
            img.compression = 'no'
            img.background_color = Color('white')
            img.alpha_channel = 'remove'
            img.save(filename=tmp_png)

        # Открываем PNG и вписываем в нужный размер без искажения пропорций
        pil_img = Image.open(tmp_png)
        pil_img = ImageOps.contain(pil_img, (target_width_px, target_height_px), method=Image.LANCZOS)

        # Создаем финальный холст с белым фоном
        final_img = Image.new("RGB", (target_width_px, target_height_px), "white")
        paste_x = (target_width_px - pil_img.width) // 2
        paste_y = (target_height_px - pil_img.height) // 2
        final_img.paste(pil_img, (paste_x, paste_y))
        final_img.save(tmp_png, dpi=(dpi, dpi))  # Обновляем tmp_png

        # Прямая печать через GDI
        printer_name = "ZDesigner ZT411-300dpi ZPL"
        hprinter = win32print.OpenPrinter(printer_name)
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)

        # Начинаем печать
        hdc.StartDoc("DataMatrix Label")
        hdc.StartPage()

        # Загружаем финальное изображение
        img = Image.open(tmp_png)
        dib = ImageWin.Dib(img)

        # Отрисовка изображения в левом верхнем углу (можно сдвигать координаты)
        dib.draw(hdc.GetHandleOutput(), (0, 0, target_width_px, target_height_px))

        hdc.EndPage()
        hdc.EndDoc()
        hdc.DeleteDC()
        win32print.ClosePrinter(hprinter)

        return {"message": f"Этикетка {target_width_mm}x{target_height_mm} мм отправлена на принтер: {printer_name}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")
