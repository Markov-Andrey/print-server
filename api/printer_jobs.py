# printer_jobs.py

import win32print
from services.dictionary_job_status import get_printer_jobs_by_hex


def get_printer_jobs(printer_name: str):
    jobs_info = []

    try:
        hPrinter = win32print.OpenPrinter(printer_name)
        jobs = win32print.EnumJobs(hPrinter, 0, 100, 1)

        for job in jobs:
            jobs_info.append({
                "job_id": job["JobId"],
                "document": job["pDocument"],
                "status": get_printer_jobs_by_hex(job["Status"]),
                "owner": job["pUserName"],
                "pages_printed": job["PagesPrinted"],
                "total_pages": job["TotalPages"],
                "time_submitted": job["Submitted"],
            })

    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'hPrinter' in locals():
            win32print.ClosePrinter(hPrinter)

    return jobs_info
