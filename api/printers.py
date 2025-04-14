import win32print
from services.dictionary_printer_status import get_printer_status_by_hex


def get_available_printers():
    printers = win32print.EnumPrinters(
        win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    )

    printer_list = []
    for printer in printers:
        name = printer[2]
        try:
            handle = win32print.OpenPrinter(name)
            status = win32print.GetPrinter(handle, 2)['Status']
            win32print.ClosePrinter(handle)
        except Exception as e:
            status = -1

        printer_list.append({
            "name": name,
            "status": get_printer_status_by_hex(status),
        })

    return printer_list
