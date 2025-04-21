from services.tmp_service import clean_old_tmp_dirs

if __name__ == "__main__":
    # cleaning old directories
    # 0 3 * * * /usr/bin/python3 /path/to/clean.py
    clean_old_tmp_dirs(30)
