from PIL import Image as PILImage
from fastapi import HTTPException


def generate_collage(grid: int, gap: int, border: int) -> dict:
    tmp = "tmp/tmp.png"
    tmp1 = "tmp/tmp0.png"
    array = [tmp, tmp1, tmp, tmp1]
    box_size = 150

    try:
        num_images = len(array)
        num_rows = (num_images + grid - 1) // grid

        total_width = (box_size * grid) + (gap * (grid - 1)) + (border * 2)
        total_height = (box_size * num_rows) + (gap * (num_rows - 1)) + (border * 2)

        new_image = PILImage.new('RGB', (total_width, total_height), (255, 255, 255))

        for i, img_path in enumerate(array):
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

            row = i // grid
            col = i % grid
            x = border + col * (box_size + gap)
            y = border + row * (box_size + gap)

            new_image.paste(img, (x, y))

        new_image.save("tmp/result.png")
        return {"message": "Результат сохранен в tmp/result.png"}

    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
