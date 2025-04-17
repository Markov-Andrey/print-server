import os
from datetime import datetime


def create_tmp_dir():
    now = datetime.now()
    date_dir = now.strftime("%Y-%m-%d")
    time_dir = now.strftime("%H-%M-%S")
    tmp_dir = os.path.join(os.getcwd(), 'tmp', date_dir, time_dir)
    os.makedirs(tmp_dir, exist_ok=True)
    return tmp_dir
