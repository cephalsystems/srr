#!/usr/bin/env python
"""
Collection wrapper script which controls the motion of the scoop and
collector, in conjunction with the navigation subsystem.
"""
import logging
logger = logging.getLogger('collection')


def scoop():
    """
    Perform a scooping action.
    """
    logger.info("SCOOPING")
    pass


def bag():
    """
    Perform a bagging action.
    """
    logger.info("BAGGING")
    pass
