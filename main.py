from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response
from typing import List
from api.print_svg import print_svg
from api.print_doc import print_doc
from services.printer_service import get_available_printers
import os
import base64

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_documentation():
    with open(os.path.join("static", "docs.html"), encoding="utf-8") as f:
        return f.read()


@app.get("/favicon.ico", response_class=Response)
async def favicon():
    return Response(status_code=204)


@app.post("/print-svg")
async def handle(
        printer: str = Form(...),
        width: int = Form(...),
        height: int = Form(...),
        data: List[str] = Form(...),
        grid: int = Form(1),
        gap: int = Form(0),
        padding_x: int = Form(0),
        padding_y: int = Form(0),
):
    return print_svg(printer, width, height, data, grid, gap, padding_x, padding_y)


@app.get("/printers")
async def handle():
    return {"printers": get_available_printers()}


@app.post("/print-doc")
async def handle(
        printer: str = Form(...),
        filename: str = Form(...),
        data: str = Form(...),
):
    return print_doc(printer, filename, data)


@app.get("/test")
async def handle():
    try:
        file_path = os.path.join(os.getcwd(), "test.docx")
        if not os.path.exists(file_path):
            return {"message": "File not found"}
        with open(file_path, "rb") as file:
            file_data = file.read()
        encoded_data = base64.b64encode(file_data).decode("utf-8")
        return {"file_base64": encoded_data}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
