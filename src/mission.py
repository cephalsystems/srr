#!/usr/bin/env python
import argparse

import srr.util
import srr.planning

import logging
logger = logging.getLogger('mission')

from flask import Flask

mission_planner = None


# TODO: add Flask routes for KML stuff!

app = Flask(__name__)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the SRR rover.')
    parser.add_argument('-m', '--mission', type=str, default='mission.yaml',
                        help='mission specification YAML file')
    args = parser.parse_args()

    srr.util.setup_logging()
    mission_planner = planning.MissionPlanner(args)
    app.run()
