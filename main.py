from fastapi import FastAPI

from fastapi.responses import Response
from api.printers import get_available_printers
from api.printer import get_printer_capabilities
from api.pillow import generate_collage
from api.print import handle_print_request
from api.print_datamatrix import print_datamatrix

app = FastAPI()


@app.get("/favicon.ico")
async def handle():
    return Response(status_code=204)  # Нет содержимого


@app.post("/print")
async def handle(file_name: str, printer_name: str, file_content_base64: str):
    return handle_print_request(file_name, printer_name, file_content_base64)


@app.get("/")
async def handle():
    return {"status": "Ok"}


@app.get("/printers")
async def handle():
    return {"printers": get_available_printers()}


@app.get("/printer")
async def handle():
    printer_name = "ZDesigner ZT411-300dpi ZPL"
    return get_printer_capabilities(printer_name)


@app.get("/print-datamatrix")
async def handle():
    return print_datamatrix()


@app.get("/pillow")
async def handle(grid: int = 3, gap: int = 10, border: str = "1,5,10"):
    return generate_collage(grid, gap, border)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
