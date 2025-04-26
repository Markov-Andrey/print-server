from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response
from fastapi import Request, HTTPException, status, Depends
from typing import List
from starlette.responses import FileResponse
from api.print_svg import print_svg
from api.print_doc import print_doc
from api.print_file import print_file
import os
import base64
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
APP_KEY = os.getenv("APP_KEY")

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


def token_validation(request: Request):
    token = request.headers.get("X-Token")
    if token != APP_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not match or is missing.",
        )
    return token


@app.get("/", response_class=FileResponse)
async def serve_documentation():
    return FileResponse(path=os.path.join(static_dir, "docs.html"), media_type='text/html')


@app.get("/favicon.ico", response_class=Response)
async def favicon():
    return Response(status_code=204)


@app.post("/print-svg")
async def handle(
        token: str = Depends(token_validation),
        printer: str = Form(None),
        width: int = Form(...),
        height: int = Form(...),
        data: List[str] = Form(...),
        grid: int = Form(1),
        gap: int = Form(0),
        padding_x: int = Form(0),
        padding_y: int = Form(0),
):
    return print_svg(printer, width, height, data, grid, gap, padding_x, padding_y)


@app.post("/print-doc")
async def handle(
        token: str = Depends(token_validation),
        printer: str = Form(None),
        filename: str = Form(...),
        data: str = Form(...),
):
    return print_doc(printer, filename, data)


@app.post("/print-file")
async def handle(
        token: str = Depends(token_validation),
        format: str = Form(...),
        printer: str = Form(None),
        filename: str = Form(...),
        data: str = Form(...),
):
    return print_file(printer, format, filename, data)


@app.get("/test")
async def handle():
    try:
        file_path = os.path.join(os.getcwd(), "test.avif")
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

    uvicorn.run(app, host="127.0.0.1", port=8000)
