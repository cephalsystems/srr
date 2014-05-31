#!/usr/bin/env python
"""
Perception wrapper script which provides object and obstacle detection
information to other components.
"""
import shapely.geom
import logging
logger = logging.getLogger('perception')


def pose():
    """
    Current pose of the rover, as best estimated by the perception
    system in the global frame.

    @return (x,y,theta), with x, y in meters and theta is in radians
    """
    return (0, 0, 0)


def location():
    """
    Current location of the rover, as best estimated by the perception
    system in the global frame.

    @return shapely.Point(x,y) in meters.
    """
    return shapely.geom.Point(pose()[0:2])


def obstacles():
    """
    List of obstacles, specified as shapely.Point(x.y) tuples in the
    rover local frame in meters.
    """
    return [shapely.geom.Point(10, 10),
            shapely.geom.Point(-10, 10)]


def targets():
    """
    List of potential targets, specified as (x,y) tuples in the rover
    local frame in meters.
    """
    return [shapely.Point(5, 5)]


def main(args):
    """
    Main launch function.  This is called from within a thread in
    the launching script.
    """
    pass
