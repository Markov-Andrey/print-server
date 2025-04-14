import win32print


def get_available_printers():
    printers = win32print.EnumPrinters(
        win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    )

    printer_list = []
    for printer in printers:
        printer_name = printer[2]
        handle = win32print.OpenPrinter(printer_name)
        try:
            info = win32print.GetPrinter(handle, 2)  # level 2 = detailed info
            status_code = info['Status']
            status_str = parse_printer_status(status_code)
        finally:
            win32print.ClosePrinter(handle)

        printer_list.append({
            "name": printer_name,
            "status": status_str
        })

    return printer_list


def parse_printer_status(status):
    if status == 0:
        return "Online"

    status_flags = {
        0x00000001: "Paused",
        0x00000002: "Error",
        0x00000004: "Pending Deletion",
        0x00000008: "Paper Jam",
        0x00000010: "Paper Out",
        0x00000020: "Manual Feed",
        0x00000040: "Paper Problem",
        0x00000080: "Offline",
        0x00000100: "IO Active",
        0x00000200: "Busy",
        0x00000400: "Printing",
        0x00000800: "Output Bin Full",
        0x00001000: "Not Available",
        0x00002000: "Waiting",
        0x00004000: "Processing",
        0x00008000: "Initializing",
        0x00010000: "Warming Up",
        0x00020000: "Toner Low",
        0x00040000: "No Toner",
        0x00080000: "Page Punt",
        0x00100000: "User Intervention Required",
        0x00200000: "Out of Memory",
        0x00400000: "Door Open",
        0x00800000: "Server Unknown",
        0x01000000: "Power Save",
    }

    readable = [name for code, name in status_flags.items() if status & code]
    return ", ".join(readable) if readable else f"Unknown (code: {status})"
