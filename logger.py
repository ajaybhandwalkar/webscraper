import logging
import os
import sys


def init_logger():
    log_level = os.getenv('LOGLEVEL', 'DEBUG').upper()
    console_format_str = '%(asctime)s %(levelname)s - %(message)s'
    formatter = logging.Formatter(console_format_str)
    log = logging.getLogger(__name__)
    if not log.hasHandlers():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        log.addHandler(console_handler)
        log.setLevel(log_level)
    return log
