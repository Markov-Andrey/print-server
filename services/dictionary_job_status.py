import win32print

# https://learn.microsoft.com/en-us/windows/win32/printdocs/job-info-1
printer_jobs_constants = {
    win32print.JOB_STATUS_BLOCKED_DEVQ: "JOB_STATUS_BLOCKED_DEVQ",
    win32print.JOB_STATUS_COMPLETE: "JOB_STATUS_COMPLETE",
    win32print.JOB_STATUS_DELETED: "JOB_STATUS_DELETED",
    win32print.JOB_STATUS_DELETING: "JOB_STATUS_DELETING",
    win32print.JOB_STATUS_ERROR: "JOB_STATUS_ERROR",
    win32print.JOB_STATUS_OFFLINE: "JOB_STATUS_OFFLINE",
    win32print.JOB_STATUS_PAPEROUT: "JOB_STATUS_PAPEROUT",
    win32print.JOB_STATUS_PAUSED: "JOB_STATUS_PAUSED",
    win32print.JOB_STATUS_PRINTED: "JOB_STATUS_PRINTED",
    win32print.JOB_STATUS_PRINTING: "JOB_STATUS_PRINTING",
    win32print.JOB_STATUS_RESTART: "JOB_STATUS_RESTART",
    win32print.JOB_STATUS_SPOOLING: "JOB_STATUS_SPOOLING",
    win32print.JOB_STATUS_USER_INTERVENTION: "JOB_STATUS_USER_INTERVENTION",
}


def get_printer_jobs_by_hex(hex_value: int):
    """Получаем статус задания по hex значению, проверяя все флаги и возвращаем массив."""
    statuses = []

    for flag_value, status_name in printer_jobs_constants.items():
        if hex_value & flag_value:
            statuses.append(status_name)

    return statuses
