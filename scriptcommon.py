import os
import sys
import logging

def _log_path(log_file_name):
    dir_path = '/var/log' if os.geteuid() == 0 else '.'
    return os.path.join(dir_path, log_file_name)

def init_logging(log_file_name, debug=False):
    logging.basicConfig(filename=_log_path(log_file_name), level=logging.INFO)

    if os.path.exists('debug') or debug:
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)
