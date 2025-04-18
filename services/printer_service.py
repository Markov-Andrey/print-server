import win32print
import subprocess
import os


def get_printer_dpi(printer):
    handle = win32print.OpenPrinter(printer)
    try:
        properties = win32print.GetPrinter(handle, 2)
        devmode = properties["pDevMode"]
        dpi = devmode.PrintQuality
        return dpi
    finally:
        win32print.ClosePrinter(handle)


def send_file_to_printer(tmp, printer):
    irfanview_path = os.path.join(os.getcwd(), "tools", "irfan_view", "i_view64.exe")
    cmd = f'"{irfanview_path}" "{tmp}" /print="{printer}" /silent /one'
    result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        raise RuntimeError(f"IrfanView error: {result.returncode}")
