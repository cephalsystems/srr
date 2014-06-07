#!/usr/bin/env python
import time
import logging
logger = logging.getLogger('collection')


class Collector(object):
    """
    Collection wrapper object which controls the motion of the scoop and
    collector, in conjunction with the navigation and perception subsystems.
    """
    def __init__(self, navigator, perceptor, args):
        self.navigator = navigator
        self.perceptor = perceptor

        logger.info("Collector initialized.")

    def shutdown(self):
        """
        Shuts down the main function for this object and waits for it
        to complete.
        """
        logger.info("Collector shutdown.")

    def scoop(self):
        """
        Perform a scooping action.
        """
        logger.info("SCOOPING")
        time.sleep(2)

    def bag(self):
        """
        Perform a bagging action.
        """
        logger.info("BAGGING")
        time.sleep(2)

    def home(self):
        """
        Attempts to drive onto the home platform if we are really close.
        """
        logger.info("HOMING")
        time.sleep(10)
        # TODO: fill this in!!
        # While < 15 deg angle, drive forward (before ramp)

        # If we never hit a ramp, drive backwards and exit.

        # After ramp, drive until we are flat again

        # If we never flattened, drive backwards and exit.
