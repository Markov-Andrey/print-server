# utils.py

import win32print
import win32api
from api.printers import get_available_printers


def print_pdf(input_pdf, printer_name):
    available_printers = get_available_printers()
    if printer_name not in available_printers:
        raise ValueError("Unknown printer")

    win32print.SetDefaultPrinter(printer_name)

    handle = win32print.OpenPrinter(printer_name, {"DesiredAccess": win32print.PRINTER_ALL_ACCESS})
    win32api.ShellExecute(2, 'print', input_pdf, '.', '/manualstoprint', 0)
    win32print.ClosePrinter(handle)