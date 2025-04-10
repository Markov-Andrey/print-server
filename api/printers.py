import win32print


def get_available_printers():
    """Возвращает список доступных принтеров в системе."""
    return [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
