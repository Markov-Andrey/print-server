import os
import asyncio
from fastapi import FastAPI, Form, Request, HTTPException, status, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from starlette.responses import FileResponse
from dotenv import load_dotenv
from api.print_svg import print_svg
from api.print_doc import print_doc
from api.print_file import print_file
from services.tmp_service import clean_old_tmp_dirs
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async def periodic_cleaning():
        while True:
            try:
                clean_old_tmp_dirs(30)
            except Exception as e:
                print(f"[TMP CLEAN ERROR]: {e}")
            await asyncio.sleep(86400)

    task = asyncio.create_task(periodic_cleaning())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)
load_dotenv()
APP_KEY = os.getenv("APP_KEY")
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


def token_validation(request: Request):
    token = request.headers.get("X-Token")
    if token != APP_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token does not match or is missing.")
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
        data: list = Form(...),
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
