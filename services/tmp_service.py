import os
import shutil
import logging
from datetime import datetime, timedelta

LOG_DIR = "Logs"
TMP_DIR = os.path.join(os.getcwd(), "tmp")


def create_tmp_dir():
    # Создаёт временную папку с путём tmp/YYYY-MM-DD/HH-MM-SS
    now = datetime.now()
    date_dir = now.strftime("%Y-%m-%d")
    time_dir = now.strftime("%H-%M-%S")
    tmp_dir = os.path.join(TMP_DIR, date_dir, time_dir)
    os.makedirs(tmp_dir, exist_ok=True)
    return tmp_dir


def clean_old_tmp_dirs(days: int):
    # Удаляет подпапки tmp/, старше указанного количества дней (по имени YYYY-MM-DD)
    cutoff_date = datetime.now() - timedelta(days=days)
    if not os.path.exists(TMP_DIR):
        return

    for date_folder in os.listdir(TMP_DIR):
        date_path = os.path.join(TMP_DIR, date_folder)
        if not os.path.isdir(date_path):
            continue

        try:
            folder_date = datetime.strptime(date_folder, "%Y-%m-%d")
            if folder_date < cutoff_date:
                shutil.rmtree(date_path)
                print(f"Deleted old tmp folder: {date_folder}")
        except ValueError:
            continue


def cleanup_old_logs(log_dir: str, days: int = 7):
    # Удаляет .log-файлы с именем в формате YYYY-MM-DD.log, старше указанного количества дней
    cutoff_date = datetime.now() - timedelta(days=days)
    if not os.path.exists(log_dir):
        return

    for filename in os.listdir(log_dir):
        name, ext = os.path.splitext(filename)
        if ext == ".log":
            try:
                file_date = datetime.strptime(name, "%Y-%m-%d")
                if file_date < cutoff_date:
                    os.remove(os.path.join(log_dir, filename))
                    print(f"Deleted old log file: {filename}")
            except ValueError:
                continue


def setup_logging():
    # Настраивает логирование в файл Logs/YYYY-MM-DD.log
    os.makedirs(LOG_DIR, exist_ok=True)

    today_str = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(LOG_DIR, f"{today_str}.log")

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    handler = logging.FileHandler(log_path, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
