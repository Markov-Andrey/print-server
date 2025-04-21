import os
import shutil
from datetime import datetime, timedelta


def create_tmp_dir():
    now = datetime.now()
    date_dir = now.strftime("%Y-%m-%d")
    time_dir = now.strftime("%H-%M-%S")
    tmp_dir = os.path.join(os.getcwd(), 'tmp', date_dir, time_dir)
    os.makedirs(tmp_dir, exist_ok=True)
    return tmp_dir


def clean_old_tmp_dirs(days):
    TMP_DIR = os.path.join(os.getcwd(), 'tmp')
    CUTOFF_DATE = datetime.now() - timedelta(days=days)
    if not os.path.exists(TMP_DIR):
        return

    for date_folder in os.listdir(TMP_DIR):
        date_path = os.path.join(TMP_DIR, date_folder)
        if not os.path.isdir(date_path):
            continue

        try:
            folder_date = datetime.strptime(date_folder, "%Y-%m-%d")
        except ValueError:
            continue

        if folder_date < CUTOFF_DATE:
            shutil.rmtree(date_path)
