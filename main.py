from fastapi import FastAPI, Form
import win32print
import base64
import os
import win32com.client
from typing import List

from api.printer import get_printer_capabilities
from api.pillow import generate_collage
from api.print_datamatrix import print_datamatrix

app = FastAPI()


@app.get("/")
async def handle():
    return {"status": "Ok"}


@app.get("/printer")
async def handle():
    printer = "ZDesigner ZT411-300dpi ZPL"
    return get_printer_capabilities(printer)


@app.post("/print-datamatrix")
async def handle(
        printer: str = Form(...),
        width: int = Form(...),
        height: int = Form(...),
        data: List[str] = Form(...),
        grid: int = Form(1),
        gap: int = Form(0),
        padding_x: int = Form(0),  # left/right
        padding_y: int = Form(0),  # top/bottom
):
    return print_datamatrix(printer, width, height, data, grid, gap, padding_x, padding_y)


@app.post("/pillow")
async def handle(
        grid: int = Form(1),
        gap: int = Form(0),
        padding_x: int = Form(0),  # left/right
        padding_y: int = Form(0),  # top/bottom
):
    return generate_collage(grid, gap, padding_x, padding_y)


@app.get("/test_print_docx")
async def test_print_docx():
    file_path = "test.docx"
    printer_name = "ZDesigner ZT411-300dpi ZPL"

    # === Чтение и кодирование в base64 ===
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    # === Подготовка временного пути и удаление, если файл существует ===
    tmp_path = os.path.abspath("temp.docx")
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

    # === Декодирование обратно и сохранение как temp.docx ===
    with open(tmp_path, "wb") as f:
        f.write(base64.b64decode(encoded))

    # === Установка принтера и печать через Word ===
    default_printer = win32print.GetDefaultPrinter()
    win32print.SetDefaultPrinter(printer_name)

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(tmp_path)
    doc.PrintOut()
    doc.Close(False)
    word.Quit()

    # === Возврат принтера по умолчанию ===
    win32print.SetDefaultPrinter(default_printer)

    return {
        "status": "printed",
        "printer": printer_name,
        "original_file": file_path
    }


@app.get("/datamatrix")
async def handle():
    """Тестовый метод: построчная base64-кодировка"""
    input_file = "datamatrix1.txt"
    output_file = "datamatrix2.txt"

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(output_file, "w", encoding="utf-8") as file:
            for line in lines:
                clean_line = line.rstrip("\n\r")
                encoded = base64.b64encode(clean_line.encode("utf-8")).decode("utf-8")
                file.write(encoded + "\n")

        return {"message": f"{input_file} закодирован построчно в {output_file}"}

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
