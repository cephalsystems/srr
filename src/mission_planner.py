#!/usr/bin/env python
"""
The mission planner is the top-level autonomy for the rover.  
It is *THE* main outer loop for everything.
"""
import argparse
import thread
import yaml
import sys

import logging
import logging.handlers

from flask import Flask

LOG_FILENAME = 'srr.log'
mission = None


def setup_logging():
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - "
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


def main(args):
    """
    This is the main autonomy system for the rover.
    """
    logger = logging.getLogger('main')

    logger.info("Loading mission file '{0}'.".format(args.mission))
    with open(args.mission, 'rb') as mission_file:
        mission = yaml.load(mission_file)

    logger.info("Starting mission.")
    mission

    logger.info("Completed mission.")
    # TODO: shutdown stuff here?


app = Flask(__name__)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the SRR rover.')
    parser.add_argument('-m', '--mission', type=str, default='mission.yaml',
                        help='mission specification YAML file')
    args = parser.parse_args()

    setup_logging()
    thread.start_new_thread(main, args)
    app.run()
