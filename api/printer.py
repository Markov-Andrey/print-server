import win32print
from fastapi import HTTPException


def get_printer_capabilities(printer_name: str):
    try:
        handle = win32print.OpenPrinter(printer_name)
        properties = win32print.GetPrinter(handle, 2)  # Получаем настройки принтера
        win32print.ClosePrinter(handle)

        devmode = properties["pDevMode"]
        if not devmode:
            raise HTTPException(status_code=500, detail="Failed to retrieve printer properties")

        # Просто возвращаем атрибуты devmode
        return {
            "Fields": dir(devmode),
            "Fields_values": {
                "Orientation": devmode.Orientation,
                "PaperSize": devmode.PaperSize,
                "PaperLength": devmode.PaperLength,
                "PaperWidth": devmode.PaperWidth,
                "Scale": devmode.Scale,
                "Copies": devmode.Copies,
                "DefaultSource": devmode.DefaultSource,
                "PrintQuality": devmode.PrintQuality,
                "Color": devmode.Color,
                "Duplex": devmode.Duplex,
                "YResolution": devmode.YResolution,
                "TTOption": devmode.TTOption,
                "Collate": devmode.Collate,
                "FormName": str(devmode.FormName),
                "BitsPerPel": devmode.BitsPerPel,
                "ICMMethod": devmode.ICMMethod,
                "ICMIntent": devmode.ICMIntent,
                "MediaType": devmode.MediaType,
                "DitherType": devmode.DitherType,
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
