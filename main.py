from fastapi import FastAPI, Form

from typing import List
from api.print_datamatrix import print_datamatrix

app = FastAPI()


@app.get("/")
async def handle():
    return {"status_server": "Ok"}


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
