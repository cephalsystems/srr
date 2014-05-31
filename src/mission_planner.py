#!/usr/bin/env python
"""
The mission planner is the top-level autonomy for the rover.  
It is *THE* main outer loop for everything.
"""
import argparse
import thread
import yaml
import time

import srr.logging
import logging

from flask import Flask

mission = None
environment = None
start_time = time.time()


def main(args):
    """
    This is the main autonomy system for the rover.
    """
    global mission
    global environment

    logger = logging.getLogger('main')

    logger.info("Loading mission file '{0}'.".format(args.mission))
    with open(args.mission, 'rb') as mission_file:
        mission_spec = yaml.safe_load(mission_file)
        mission = mission_spec.mission
        environment = mission_spec.environment

    logger.info("Starting mission.")
    for task in mission:
        print mission

    logger.info("Completed mission.")
    # TODO: shutdown stuff here?


app = Flask(__name__)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the SRR rover.')
    parser.add_argument('-m', '--mission', type=str, default='mission.yaml',
                        help='mission specification YAML file')
    args = parser.parse_args()

    srr.logging.setup_logging()
    thread.start_new_thread(main, args)
    app.run()
