import win32print

# https://learn.microsoft.com/en-us/windows/win32/printdocs/job-info-1
printer_jobs_constants = {
    win32print.JOB_STATUS_BLOCKED_DEVQ: "BLOCKED_DEVQ",
    win32print.JOB_STATUS_COMPLETE: "COMPLETE",
    win32print.JOB_STATUS_DELETED: "DELETED",
    win32print.JOB_STATUS_DELETING: "DELETING",
    win32print.JOB_STATUS_ERROR: "ERROR",
    win32print.JOB_STATUS_OFFLINE: "OFFLINE",
    win32print.JOB_STATUS_PAPEROUT: "PAPEROUT",
    win32print.JOB_STATUS_PAUSED: "PAUSED",
    win32print.JOB_STATUS_PRINTED: "PRINTED",
    win32print.JOB_STATUS_PRINTING: "PRINTING",
    win32print.JOB_STATUS_RESTART: "RESTART",
    win32print.JOB_STATUS_SPOOLING: "SPOOLING",
    win32print.JOB_STATUS_USER_INTERVENTION: "USER_INTERVENTION",
}


def get_printer_jobs_by_hex(hex_value: int):
    # Получаем статус задания по hex значению, проверяя все флаги и возвращаем массив
    statuses = []

    if hex_value == 0:
        statuses.append("PENDING")

    for flag_value, status_name in printer_jobs_constants.items():
        if hex_value & flag_value:
            statuses.append(status_name)

    return statuses
