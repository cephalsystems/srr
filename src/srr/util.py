#!/usr/bin/env python
"""
SRR configuration utility module.
"""
import logging
import logging.handlers
import time
import sys

LOG_FILENAME = 'srr.log'
START_TIME = time.time()


def elapsed_time():
    """
    Simple helper function that returns elapsed time since startup.
    """
    global START_TIME
    return time.time() - START_TIME


class StartupTimeFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        global START_TIME
        return "{:03.3}".format(record.created.time() - START_TIME)


def setup_logging():
    formatter = logging.StartupTimeFormatter("%(asctime)s - "
                                             "%(name)s - "
                                             "%(levelname)s - "
                                             "%(message)s")
    root_logger = logging.getLogger()

    # Set up rolling log files for root logger.
    file_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                        backupCount=20)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Set up logging to stdout for root logger.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
