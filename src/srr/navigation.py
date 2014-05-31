#!/usr/bin/env python
"""
Navigation wrapper script which controls the motion of the rover as it
is given targets in the environment.
"""
import logging
logger = logging.getLogger('navigation')


def location():
    """
    Current location of the rover, as best estimated by the odometry
    system in the global frame.

    @return (x,y,theta), with x, y in meters and theta is in radians
    """
    return (0, 0, 0)


def goto_waypoint(x, y):
    """
    Navigate toward a distant waypoint in the global frame, using
    local obstacle avoidance if necessary.
    """
    logger.info("GOTO_WPT: {0}".format((x, y)))
    pass


def goto_angle(theta):
    """
    Navigate toward a specified angle in the local frame.
    """
    logger.info("GOTO_ANG: {0}".format(theta))
    pass


def goto_vector(x, y):
    """
    Navigate toward a vector in the local frame.  This only considers
    the local angle and not the length of the vector.
    """
    logger.info("GOTO_VEC: {0}".format((x, y)))
    pass


def main(args):
    """
    Main launch function.  This is called from within a thread in
    the launching script.
    """
    pass
