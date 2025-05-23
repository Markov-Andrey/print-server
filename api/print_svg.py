import os
from fastapi import FastAPI, HTTPException, Form
from typing import List
from services.printer_service import get_printer_dpi, send_file_to_printer, get_default_printer
from services.tmp_service import create_tmp_dir
import base64
from wand.image import Image as WandImage
from PIL import Image, ImageOps
from wand.color import Color

app = FastAPI()


@app.post("/print-svg")
async def handle(
        printer: str = Form(None),
        width: int = Form(...),
        height: int = Form(...),
        data: list = Form(...),
        grid: int = Form(1),
        gap: int = Form(0),
        padding_x: int = Form(0),
        padding_y: int = Form(0),
):
    if not printer:
        printer = get_default_printer()

    return print_svg(printer, width, height, data, grid, gap, padding_x, padding_y)


def mm_to_px(value, dpi):
    return int(value / 25.4 * dpi)


def print_svg(printer: str, width: int, height: int, data: list, grid: int, gap: int, padding_x: int,
              padding_y: int):
    if not printer:
        printer = get_default_printer()

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

        tmp_dir = create_tmp_dir()

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

            tmp_page_path = os.path.join(tmp_dir, f'tmp_page_{img_idx}.png')
            final_img.save(tmp_page_path, dpi=(dpi, dpi))
            send_file_to_printer(tmp_page_path, printer)

        return {"message": f"Printed {len(data)} labels ({width}x{height}mm) to printer: {printer}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
