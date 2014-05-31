#!/usr/bin/env python
"""
SRR logging configuration utility module.
"""
import logging
import logging.handlers
import time
import sys

LOG_FILENAME = 'srr.log'
START_TIME = time.time()


class StartupTimeFormatter(logging.Formatter):
    converter = dt.datetime.fromtimestamp
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)
        return s


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
