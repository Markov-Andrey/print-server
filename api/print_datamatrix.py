import os
from fastapi import HTTPException
from wand.image import Image as WandImage
from PIL import Image, ImageOps
import win32print
import base64
import subprocess
from wand.color import Color
from services.printers_list import get_available_printers


def print_datamatrix(printer: str, width: int, height: int, data: list[str], grid: int, gap: int, padding_x: int,
                     padding_y: int):
    if printer not in get_available_printers():
        raise HTTPException(status_code=400, detail="Error: Printer not found")

    try:
        dpi = get_printer_dpi(printer)
        render_dpi = dpi * 4
        tmp_dir = os.path.join(os.getcwd(), 'tmp')
        os.makedirs(tmp_dir, exist_ok=True)

        num_images = (len(data) + grid - 1) // grid

        gap_px = int(gap / 25.4 * dpi)
        padding_x_px = int(padding_x / 25.4 * dpi)
        padding_y_px = int(padding_y / 25.4 * dpi)

        final_img_width_px = int(width / 25.4 * dpi)
        final_img_height_px = int(height / 25.4 * dpi)

        # Доступная область после вычета отступов
        content_width_px = final_img_width_px - 2 * padding_x_px
        content_height_px = final_img_height_px - 2 * padding_y_px

        element_width_px = (content_width_px - (grid - 1) * gap_px) // grid
        element_height_px = content_height_px

        for img_idx in range(num_images):
            start_idx = img_idx * grid
            end_idx = min((img_idx + 1) * grid, len(data))
            group_data = data[start_idx:end_idx]

            final_img = Image.new("RGB", (final_img_width_px, final_img_height_px), "white")

            for idx, base64_svg in enumerate(group_data):
                svg_data = base64.b64decode(base64_svg).decode('utf-8')
                tmp_png = os.path.join(tmp_dir, f'tmp_{img_idx}_{idx}.png')

                with WandImage(blob=svg_data.encode('utf-8'), format='svg', resolution=render_dpi) as img:
                    img.format = 'png'
                    img.compression = 'no'
                    img.background_color = Color('white')
                    img.alpha_channel = 'remove'
                    img.save(filename=tmp_png)

                pil_img = Image.open(tmp_png)
                pil_img = ImageOps.contain(pil_img, (element_width_px, element_height_px), method=Image.LANCZOS)

                # Учитываем padding при позиционировании
                paste_x = padding_x_px + idx * (element_width_px + gap_px)
                paste_y = padding_y_px + (element_height_px - pil_img.height) // 2

                final_img.paste(pil_img, (paste_x, paste_y))

            tmp_png_final = os.path.join(tmp_dir, f'tmp_final_{img_idx}.png')
            final_img.save(tmp_png_final, dpi=(dpi, dpi))

            # zpl = convert_png_to_zpl(tmp_png_final)
            # send_zpl_to_printer(zpl, printer)
            send_png_to_printer(tmp_png_final, printer)

        return {"message": f"Printed {len(data)} labels ({width}x{height}mm) to printer: {printer}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


def get_printer_dpi(printer):
    handle = win32print.OpenPrinter(printer)
    try:
        properties = win32print.GetPrinter(handle, 2)
        devmode = properties["pDevMode"]
        dpi = devmode.PrintQuality
        return dpi
    finally:
        win32print.ClosePrinter(handle)


def send_png_to_printer(tmp_png, printer):
    irfanview_path = os.path.join(os.getcwd(), "tools", "irfan_view", "i_view64.exe")
    cmd = f'"{irfanview_path}" "{tmp_png}" /print="{printer}" /silent /one'
    result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        raise RuntimeError(f"IrfanView error: {result.returncode}")
