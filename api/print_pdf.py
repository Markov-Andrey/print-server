import os
import base64
from services.tmp_service import create_tmp_dir
from services.printer_service import send_file_to_printer


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

        send_file_to_printer(temp_filename, printer)

        return {"message": f"{filename} print"}

    except Exception as e:
        return {"message": f"Error: {str(e)}"}