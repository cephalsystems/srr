#!/usr/bin/env python
"""
SRR configuration utility module.
"""
import logging
import logging.handlers
import collections
import time
import sys
import shapely.geometry

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
    formatter = StartupTimeFormatter("%(asctime)s - "
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


class Task(object):
    def __init__(self, task_name, task_yaml, environment):
        self.name = task_name
        if not task_yaml.bounds and not task_yaml.location:
            raise ValueError("Location and bounds not specified for "
                             "task '{0}'".format(task_name))

        if task_yaml.bounds:
            self.bounds = shapely.geometry.Polygon(task_yaml.bounds)
        if task_yaml.location:
            self.location = shapely.geometry.Point(task_yaml.location)

        if not self.location:
            self.location = self.bounds.centroid
        if not self.bounds:
            self.bounds = self.location

        self.is_forced = task_yaml.is_forced
        self.timeout = task_yaml.timeout
        self.environment = environment

    @property
    def kml():
        pass


def parse_environment(environment_yaml):
    """
    Parse raw YAML environment.
    """
    environment = {}
    environment.origin = environment_yaml.origin
    environment.start = environment_yaml.start
    environment.bounds = shapely.geom.Polygon(environment.bounds,
                                              environment.obstacles)


def parse_mission(mission_yaml, environment):
    """
    Parse raw YAML mission.
    """
    return collections.OrderedDict(Task(name, task_yaml, environment)
                                   for (name, task_yaml) in mission_yaml)
