import win32print


def restart_print_job(printer: str, job_id: int):
    try:
        hPrinter = win32print.OpenPrinter(printer)
        win32print.SetJob(hPrinter, job_id, 0, None, win32print.JOB_CONTROL_RESTART)

        return {"status": "Job restarted successfully"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        if 'hPrinter' in locals():
            win32print.ClosePrinter(hPrinter)

