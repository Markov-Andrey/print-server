from fastapi import FastAPI, Form
import win32print
import base64
import os
import win32com.client

from api.printers import get_available_printers
from api.printer import get_printer_capabilities
from api.pillow import generate_collage
from api.print import handle_print_request
from api.print_datamatrix import print_datamatrix

app = FastAPI()


@app.post("/print")
async def handle(file_name: str, printer_name: str, file_content_base64: str):
    return handle_print_request(file_name, printer_name, file_content_base64)


@app.get("/")
async def handle():
    return {"status": "Ok"}


@app.get("/printers")
async def handle():
    """Возвращает список доступных принтеров в системе."""
    return get_available_printers()


@app.get("/printer")
async def handle():
    printer = "ZDesigner ZT411-300dpi ZPL"
    return get_printer_capabilities(printer)


@app.post("/print-datamatrix")
async def handle(
        printer: str = Form(...),
        width: str = Form(...),
        height: str = Form(...)
):
    return print_datamatrix(printer, width, height)


@app.post("/pillow")
async def handle(
        grid: int = Form(1),
        gap: int = Form(0),
        border: int = Form(0)
):
    return generate_collage(grid, gap, border)


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
