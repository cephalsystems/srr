#!/usr/bin/env python
"""
SRR configuration utility module.
"""
import logging
import logging.handlers
import time
import math
import sys
import shapely.geometry
import shapely.affinity

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
        return "{:03.3}".format(record.created - START_TIME)


def setup_logging():
    formatter = StartupTimeFormatter("%(asctime)s - "
                                     "%(name)s - "
                                     "%(levelname)s - "
                                     "%(message)s")
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Set up rolling log files for root logger.
    file_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                        backupCount=20)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Set up logging to stdout for root logger.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


class Task(object):
    def __init__(self, task_name, task_yaml, environment):
        self.name = task_name
        if 'bounds' in task_yaml:
            self.bounds = shapely.geometry.Polygon(task_yaml['bounds'])
        if 'location' in task_yaml:
            self.location = shapely.geometry.Point(task_yaml['location'])

        if 'bounds' not in task_yaml and 'location' not in task_yaml:
            raise ValueError("Location and bounds not specified for "
                             "task '{0}'".format(task_name))
        elif 'location' not in task_yaml:
            self.location = self.bounds.centroid
        elif 'bounds' not in task_yaml:
            self.bounds = self.location

        self.is_forced = ('is_forced' in task_yaml) and task_yaml['is_forced']
        self.timeout = task_yaml['timeout']
        self.environment = environment

    @property
    def kml():
        pass


class Environment(object):
    def __init__(self, origin, start, bounds, obstacles):
        self.origin = origin
        self.start = start
        self.bounds = shapely.geometry.Polygon(bounds, obstacles)

    @property
    def kml():
        pass


def parse_environment(environment_yaml):
    """
    Parse raw YAML environment.
    """
    bounds = [tuple(coords) for coords in environment_yaml['bounds']]
    obstacles = [[tuple(coords) for coords in obstacle]
                 for (name, obstacle) in
                 environment_yaml['obstacles'].iteritems()]

    return Environment(environment_yaml['origin'],
                       environment_yaml['start'],
                       bounds,
                       obstacles)


def parse_mission(mission_yaml, environment):
    """
    Parse raw YAML mission.
    """
    return [Task(name, task_yaml, environment)
            for (name, task_yaml) in mission_yaml.iteritems()]


def local_to_global(origin, point, theta):
    """
    Converts from a local frame in meters into a global frame in lon/lat.

    @param origin (lon, lat, heading)
    @param point shapely.geometry.Point()
    @return (longitude, latitude) in WGS84
    """
    # Create local transformation frame.
    import utm
    ox, oy, zone, hemi = utm.from_latlon(origin[0], origin[1])
    origin_utm = shapely.geometry.Point(ox, oy)
    origin_theta = math.pi - origin[2]

    # Translate and rotate point to origin.
    point += origin_utm
    point = shapely.affinity.rotate(point, origin_theta, origin=origin_utm)
    heading = theta + origin_theta

    # Return transformed point.
    lat, lon = utm.to_latlon(point.x, point.y, zone, hemi)
    return lon, lat, heading
