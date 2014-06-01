#!/usr/bin/env python
"""
Launches and executes an SRR mission.
"""
import argparse
import flask
import srr.util
import srr.planning

mission_planner = None

# TODO: add Flask routes for KML stuff!

if __name__ == "__main__":
    # Extract arguments from command line.
    parser = argparse.ArgumentParser(description='Run the SRR rover.')
    parser.add_argument('-m', '--mission', type=str, default='mission.yaml',
                        help='mission specification YAML file')
    parser.add_argument('-s', '--sim', action='store_true',
                        help='simulate movement and perception')
    parser.add_argument('-v', '--vision', type=str,
                        help='perception simulation KML file')
    args = parser.parse_args()

    # Start logging and mission planner.
    srr.util.setup_logging()
    mission_planner = srr.planning.MissionPlanner(args)

    # Start web server to publish live feeds of rover activity.
    app = flask.Flask(__name__)
    app.run()

    # Shut down mission planner if server is stopped.
    mission_planner.shutdown()
