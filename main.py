import os
import re
import asyncio
import logging
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
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta

LOG_DIR = "Logs"


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


@app.get("/favicon.ico", response_class=Response)  # мини-костыль, чтобы не получать warning на сервере
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


def cleanup_old_logs(log_dir: str, days: int = 7):
    # Удаляет .log файлы с датой в имени, старше указанного количества дней
    cutoff_date = datetime.now() - timedelta(days=days)
    if not os.path.exists(log_dir):
        return

    for filename in os.listdir(log_dir):
        try:
            name, ext = os.path.splitext(filename)
            if ext == ".log":
                file_date = datetime.strptime(name, "%Y-%m-%d")
                if file_date < cutoff_date:
                    os.remove(os.path.join(log_dir, filename))
                    print(f"Deleted old log file: {filename}")
        except Exception:
            pass


def setup_logging():
    # Настраивает логирование в файл с именем по текущей дате
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    cleanup_old_logs(LOG_DIR, days=7)

    today_str = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(LOG_DIR, f"{today_str}.log")

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    handler = logging.FileHandler(log_path, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


if __name__ == "__main__":
    import uvicorn

    setup_logging()
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    logging.info(f"Starting server on {host}:{port}")

    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            log_config=None,
            log_level="info"
        )
    except Exception:
        logging.exception("Server crashed with exception")
