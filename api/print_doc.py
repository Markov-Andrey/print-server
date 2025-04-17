import os
import base64
from win32com import client
from services.tmp_service import create_tmp_dir


def print_doc(printer: str, filename: str, data: str):
    try:
        docx_data = base64.b64decode(data)
    except Exception as e:
        return {"message": f"Error decoding base64 data: {str(e)}"}

    word = None
    doc_to_print = None

    try:
        tmp_dir = create_tmp_dir()
        temp_filename = os.path.join(tmp_dir, f"{filename}.docx")

        with open(temp_filename, "wb") as temp_file:
            temp_file.write(docx_data)

        word = client.Dispatch("Word.Application")
        word.Visible = False
        word.ActivePrinter = printer
        doc_to_print = word.Documents.Open(os.path.abspath(temp_filename))

        doc_to_print.PrintOut(PrintToFile=False)

        return {"message": f"Doc {filename} print"}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

    finally:
        if doc_to_print:
            doc_to_print.Close()
        if word:
            word.Quit()
