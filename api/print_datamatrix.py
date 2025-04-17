import os
from fastapi import HTTPException
from wand.image import Image as WandImage
from PIL import Image, ImageOps
import win32print
import base64
import subprocess
from wand.color import Color
from services.printers_list import get_available_printers


def mm_to_px(value, dpi):
    return int(value / 25.4 * dpi)


def get_printer_dpi(printer):
    handle = win32print.OpenPrinter(printer)
    try:
        properties = win32print.GetPrinter(handle, 2)
        devmode = properties["pDevMode"]
        dpi = devmode.PrintQuality
        return dpi
    finally:
        win32print.ClosePrinter(handle)


def print_datamatrix(printer: str, width: int, height: int, data: list[str], grid: int, gap: int, padding_x: int,
                     padding_y: int):
    if printer not in get_available_printers():
        raise HTTPException(status_code=400, detail="Error: Printer not found")

    try:
        dpi = get_printer_dpi(printer)
        gap_px = mm_to_px(gap, dpi)
        pad_x = mm_to_px(padding_x, dpi)
        pad_y = mm_to_px(padding_y, dpi)
        img_w = mm_to_px(width, dpi)
        img_h = mm_to_px(height, dpi)
        content_w = img_w - 2 * pad_x
        content_h = img_h - 2 * pad_y
        elem_w = (content_w - (grid - 1) * gap_px) // grid
        elem_h = content_h

        tmp_dir = os.path.join(os.getcwd(), 'tmp')
        os.makedirs(tmp_dir, exist_ok=True)

        for img_idx in range((len(data) + grid - 1) // grid):
            final_img = Image.new("RGB", (img_w, img_h), "white")
            offset_x = pad_x + (content_w - (grid * elem_w + (grid - 1) * gap_px)) // 2
            group = data[img_idx * grid: (img_idx + 1) * grid]

            for idx, base64_svg in enumerate(group):
                svg_data = base64.b64decode(base64_svg).decode()
                tmp_png = os.path.join(tmp_dir, f'tmp_{img_idx}_{idx}.png')

                with WandImage(blob=svg_data.encode(), format='svg', resolution=dpi) as img:
                    img.format = 'png'
                    img.compression = 'no'
                    img.background_color = Color('white')
                    img.alpha_channel = 'remove'
                    img.save(filename=tmp_png)

                pil_img = ImageOps.contain(Image.open(tmp_png), (elem_w, elem_h), method=Image.LANCZOS)
                x = offset_x + idx * (elem_w + gap_px) + (elem_w - pil_img.width) // 2
                y = pad_y + (elem_h - pil_img.height) // 2
                final_img.paste(pil_img, (x, y))

            final_img_path = os.path.join(tmp_dir, f'tmp_final_{img_idx}.png')
            final_img.save(final_img_path, dpi=(dpi, dpi))
            # send_png_to_printer(final_img_path, printer)

        return {"message": f"Printed {len(data)} labels ({width}x{height}mm) to printer: {printer}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


def send_png_to_printer(tmp_png, printer):
    irfanview_path = os.path.join(os.getcwd(), "tools", "irfan_view", "i_view64.exe")
    cmd = f'"{irfanview_path}" "{tmp_png}" /print="{printer}" /silent /one'
    result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        raise RuntimeError(f"IrfanView error: {result.returncode}")
