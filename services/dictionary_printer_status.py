import win32print

# https://learn.microsoft.com/en-us/windows/win32/printdocs/printer-info-2
printer_status_constants = {
    win32print.PRINTER_STATUS_BUSY: "BUSY",
    win32print.PRINTER_STATUS_DOOR_OPEN: "DOOR_OPEN",
    win32print.PRINTER_STATUS_ERROR: "ERROR",
    win32print.PRINTER_STATUS_INITIALIZING: "INITIALIZING",
    win32print.PRINTER_STATUS_IO_ACTIVE: "IO_ACTIVE",
    win32print.PRINTER_STATUS_MANUAL_FEED: "MANUAL_FEED",
    win32print.PRINTER_STATUS_NO_TONER: "NO_TONER",
    win32print.PRINTER_STATUS_NOT_AVAILABLE: "NOT_AVAILABLE",
    win32print.PRINTER_STATUS_OFFLINE: "OFFLINE",
    win32print.PRINTER_STATUS_OUT_OF_MEMORY: "OUT_OF_MEMORY",
    win32print.PRINTER_STATUS_OUTPUT_BIN_FULL: "OUTPUT_BIN_FULL",
    win32print.PRINTER_STATUS_PAGE_PUNT: "PAGE_PUNT",
    win32print.PRINTER_STATUS_PAPER_JAM: "PAPER_JAM",
    win32print.PRINTER_STATUS_PAPER_OUT: "PAPER_OUT",
    win32print.PRINTER_STATUS_PAPER_PROBLEM: "PAPER_PROBLEM",
    win32print.PRINTER_STATUS_PAUSED: "PAUSED",
    win32print.PRINTER_STATUS_PENDING_DELETION: "PENDING_DELETION",
    win32print.PRINTER_STATUS_POWER_SAVE: "POWER_SAVE",
    win32print.PRINTER_STATUS_PRINTING: "PRINTING",
    win32print.PRINTER_STATUS_PROCESSING: "PROCESSING",
    win32print.PRINTER_STATUS_SERVER_UNKNOWN: "SERVER_UNKNOWN",
    win32print.PRINTER_STATUS_TONER_LOW: "TONER_LOW",
    win32print.PRINTER_STATUS_USER_INTERVENTION: "USER_INTERVENTION",
    win32print.PRINTER_STATUS_WAITING: "WAITING",
    win32print.PRINTER_STATUS_WARMING_UP: "WARMING_UP",
}


def get_printer_status_by_hex(hex_value: int):
    # Получаем статус принтера по hex значению, учитывая множественные флаги
    status_list = []

    if hex_value == 0:
        status_list.append("ONLINE")

    for flag, name in printer_status_constants.items():
        if hex_value & flag:
            status_list.append(name)

    return status_list
