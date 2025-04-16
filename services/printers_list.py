import win32print


def get_available_printers():
    printers = win32print.EnumPrinters(
        win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    )

    return [printer[2] for printer in printers]
