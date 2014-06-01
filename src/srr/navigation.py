#!/usr/bin/env python
import math
import time
import threading
import shapely.geometry
import logging
logger = logging.getLogger('navigation')


class Navigator(object):
    """
    Navigation wrapper object which controls the motion of the rover as
    it is given targets in the environment.
    """
    def __init__(self, environment, perceptor, args):
        # Store reference to the perception system.
        self.perceptor = perceptor

        # Get rover starting location from environment.
        self.position = shapely.geometry.Point(environment.start[0],
                                               environment.start[1])
        self.rotation = environment.start[2]

        # Start main thread internally.
        self.is_running = True
        self._thread = threading.Thread(target=self.main, name='navigator')
        self._thread.start()

        logging.info("Navigator initialized.")

    def shutdown(self):
        """
        Shuts down the main function for this object and waits for it
        to complete.
        """
        self.is_running = False
        self._thread.join()

        logging.info("Navigator shutdown.")

    @property
    def pose(self):
        """
        Current (x,y,theta) pose of the rover, as best estimated by the
        odometry system in the global frame.
        """
        return self._position.x, self._position.y, self._rotation

    def goto_angle(self, theta):
        """
        Navigate toward a specified angle in the local frame.
        """
        logger.info("GOTO_ANG: {0}".format(theta))
        pass

    def goto_target(self, point):
        """
        Navigate toward a point in the local frame.  This only considers
        the local direction and not the distance to the target.
        """
        logger.info("GOTO_VEC: {0}".format(point))
        self.goto_angle(math.atan2(point.y, point.x))

    def main(self):
        """
        Main execution function.  This is called from within a thread in
        the constructor.  The is_running flag is used to indicate when it
        should stop executing.
        """
        while (self.is_running):
            time.sleep(1)
            pass
