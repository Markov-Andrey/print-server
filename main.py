import base64

from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List

from api.print_datamatrix import print_svg
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_documentation():
    with open(os.path.join("static", "docs.html"), encoding="utf-8") as f:
        return f.read()


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
