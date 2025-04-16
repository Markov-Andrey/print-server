from PIL import Image as PILImage
from fastapi import HTTPException
import os


def generate_collage(grid: int, gap: int, padding_x: int, padding_y: int) -> dict:
    array = [
        "tmp/tmp0.png",
        "tmp/tmp.png",
        "tmp/tmp0.png",
        "tmp/tmp.png",
        "tmp/tmp0.png",
    ]
    box_size = 150

    try:
        os.makedirs("tmp", exist_ok=True)

        total_width = (box_size * grid) + (gap * (grid - 1)) + (padding_x * 2)
        total_height = box_size + (padding_y * 2)

        count = 0
        page = 0

        while count < len(array):
            images_on_page = array[count:count + grid]
            new_image = PILImage.new('RGB', (total_width, total_height), (255, 255, 255))

            for i, img_path in enumerate(images_on_page):
                img = PILImage.open(img_path)

                img_width, img_height = img.size
                aspect_ratio = img_width / img_height

                if aspect_ratio > 1:
                    new_width = box_size
                    new_height = int(box_size / aspect_ratio)
                else:
                    new_height = box_size
                    new_width = int(box_size * aspect_ratio)

                img = img.resize((new_width, new_height), PILImage.LANCZOS)

                x = padding_x + i * (box_size + gap)
                y = padding_y + (box_size - new_height) // 2

                new_image.paste(img, (x, y))

            result_path = f"tmp/result_{page}.png"
            new_image.save(result_path)
            page += 1
            count += grid

        return {"message": f"Сохранено {page} коллажей"}

    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
