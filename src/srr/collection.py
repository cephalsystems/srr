#!/usr/bin/env python
import time
import logging
logger = logging.getLogger('collection')


class Collector(object):
    """
    Collection wrapper object which controls the motion of the scoop and
    collector, in conjunction with the navigation and perception subsystems.
    """
    def __init__(self, navigator, perceptor):
        self.navigator = navigator
        self.perceptor = perceptor

        logging.info("Collector initialized.")

    def shutdown(self):
        """
        Shuts down the main function for this object and waits for it
        to complete.
        """
        logging.info("Collector shutdown.")

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
