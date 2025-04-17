import os
import base64
import win32print
import win32api
from services.tmp_service import create_tmp_dir


def print_pdf(printer: str, filename: str, data: str):
    try:
        pdf_data = base64.b64decode(data)
    except Exception as e:
        return {"message": f"Error decoding base64 data: {str(e)}"}

    try:
        tmp_dir = create_tmp_dir()
        temp_filename = os.path.join(tmp_dir, f"{filename}.pdf")

        with open(temp_filename, "wb") as temp_file:
            temp_file.write(pdf_data)

        win32print.SetDefaultPrinter(printer)
        win32api.ShellExecute(0, "print", temp_filename, None, ".", 0)

        return {"message": f"PDF {filename} sent to print"}

    except Exception as e:
        return {"message": f"Error: {str(e)}"}

