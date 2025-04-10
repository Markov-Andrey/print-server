# pillow.py

from PIL import Image as PILImage
from fastapi import HTTPException


def generate_collage(grid: int, gap: int, border: str) -> dict:
    tmp = "tmp/tmp.png"
    tmp1 = "tmp/tmp1.png"
    array = [tmp, tmp1, tmp, tmp1, tmp, tmp1, tmp, tmp1, tmp, tmp1, tmp, tmp1, tmp, tmp1, tmp, tmp1, tmp, tmp1]

    try:
        border_values = list(map(int, border.strip().split(",")))
        match len(border_values):
            case 1:
                border_top = border_right = border_bottom = border_left = border_values[0]
            case 2:
                border_top, border_right = border_values
                border_bottom, border_left = border_values[0], border_values[1]
            case 3:
                border_top, border_right, border_bottom = border_values
                border_left = border_values[1]
            case 4:
                border_top, border_right, border_bottom, border_left = border_values
            case _:
                raise HTTPException(status_code=400, detail="border должен быть от 1 до 4 значений")

        original_img = PILImage.open(array[0])
        original_width, original_height = original_img.size

        num_images = len(array)
        num_rows = (num_images + grid - 1) // grid

        total_width = (original_width * grid) + (gap * (grid - 1)) + border_left + border_right
        total_height = (original_height * num_rows) + (gap * (num_rows - 1)) + border_top + border_bottom

        new_image = PILImage.new('RGB', (total_width, total_height), (255, 255, 255))

        for i, img_path in enumerate(array):
            img = PILImage.open(img_path)
            img = img.resize((original_width, original_height))
            row = i // grid
            col = i % grid
            x = border_left + col * (original_width + gap)
            y = border_top + row * (original_height + gap)
            new_image.paste(img, (x, y))

        new_image.save("tmp/result.png")
        return {"message": "Результат сохранен в tmp/result.png"}

    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
