# api/printer.py

from fastapi import HTTPException
from wand.image import Image as WandImage
import win32print


def print_datamatrix():
    try:
        with open("datamatrix1.txt", "r", encoding="utf-8") as file:
            svg_data = file.read()

        # Конвертация SVG → PNG
        tmp_png = "tmp1.png"
        with WandImage(blob=svg_data.encode('utf-8'), format='svg') as img:
            img.resize(int(10 * 37.795), int(10 * 37.795))  # 5x5 см в пикселях
            img.format = 'png'
            img.save(filename=tmp_png)

        # Отправка на печать
        printer_name = "ZDesigner ZT411-300dpi ZPL"
        if printer_name not in [p[2] for p in win32print.EnumPrinters(2)]:
            raise HTTPException(status_code=400, detail="Принтер не найден")

        # win32api.ShellExecute(
        #     0,
        #     "printto",
        #     tmp_png,
        #     f'"{printer_name}"',
        #     ".",
        #     0
        # )

        return {"message": f"Этикетка 5x5 см отправлена на принтер: {printer_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")
