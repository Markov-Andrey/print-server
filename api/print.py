# printer.py

import os
import base64
from fastapi import HTTPException
from utils import get_available_printers, print_pdf


def handle_print_request(file_name: str, printer_name: str, file_content_base64: str) -> dict:
    # Проверка принтера
    if printer_name not in get_available_printers():
        raise HTTPException(status_code=400, detail="Printer not found")

    # Проверка формата файла
    if not file_name.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Декодирование base64
    try:
        file_content = base64.b64decode(file_content_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 content")

    # Создание временного файла
    temp_file_path = os.path.join("temp_files", file_name)
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)

    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_content)

    if not os.path.isfile(temp_file_path):
        raise HTTPException(status_code=400, detail="File could not be saved")

    # Печать файла
    try:
        print_pdf(temp_file_path, printer_name)
        return {"message": f"File {file_name} sent to printer {printer_name}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="An error occurred during printing")
