#!/usr/bin/env python
"""
Launches and executes an SRR mission.
"""
import argparse
import srr.util
import srr.planning


if __name__ == "__main__":
    # Extract arguments from command line.
    parser = argparse.ArgumentParser(description='Run the SRR rover.')
    parser.add_argument('-m', '--mission', type=str, default='mission.yaml',
                        help='mission specification YAML file')
    parser.add_argument('-p', '--precached', action='store_true',
                        help='specify either level 1 or level 2')
    parser.add_argument('-s', '--sim', action='store_true',
                        help='simulate movement and perception')
    parser.add_argument('-v', '--vision', type=str,
                        help='perception simulation KML file')
    parser.add_argument('-c', '--console', action='store_true',
                        help='run as interactive console')
    parser.add_argument('-mp', '--motor-port', type=str, default=
                        '/dev/serial/by-path/pci-0000:00:14.0-usb-0:4:1.0',
                        help='serial port for drivetrain roboclaw')
    parser.add_argument('-sp', '--scoop-port', type=str, default=
                        '/dev/serial/by-path/pci-0000:04:00.0-usb-0:2:1.0',
                        help='serial port for scoop roboclaw')
    parser.add_argument('-bp', '--bagger-port', type=str, default=
                        '/dev/serial/by-path/pci-0000:04:00.0-usb-0:1:1.0',
                        help='serial port for bagger roboclaw')
    args = parser.parse_args()

    # Start logging and mission planner.
    srr.util.setup_logging()
    mission_planner = srr.planning.MissionPlanner(args)

    # Start web server to publish live feeds of rover activity.
    import srr.viewer
    srr.viewer.mission_planner = mission_planner
    srr.viewer.run()

    # Shut down mission planner if server is stopped.
    mission_planner.shutdown()
