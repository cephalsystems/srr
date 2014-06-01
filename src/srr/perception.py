#!/usr/bin/env python
import time
import threading
import shapely.geometry
import logging
logger = logging.getLogger('perception')


class Perceptor(object):
    """
    Perception wrapper object which provides object and obstacle detection
    information to other components.
    """
    def __init__(self, environment, args):
        # Get rover starting location from environment
        self.position = shapely.geometry.Point(environment.start[0],
                                               environment.start[1])
        self.rotation = environment.start[2]

        # Start main thread internally
        self.is_running = True
        self._thread = threading.Thread(target=self.main, name='perceptor')
        self._thread.start()

        logging.info("Perceptor initialized.")

    def shutdown(self):
        """
        Shuts down the main function for this object and waits for it
        to complete.
        """
        self.is_running = False
        self._thread.join()

        logging.info("Perceptor shutdown.")

    @property
    def pose(self):
        """
        Current (x,y,theta) pose of the rover, as best estimated by the
        odometry system in the global frame.
        """
        return self._position.x, self._position.y, self._rotation

    @property
    def obstacles(self):
        """
        List of obstacles, specified as shapely.Point(x.y) tuples in the
        rover local frame in meters.
        """
        return [shapely.geometry.Point(10, 10),
                shapely.geometry.Point(-10, 10)]

    @property
    def targets(self):
        """
        List of potential targets, specified as (x,y) tuples in the rover
        local frame in meters.
        """
        return [shapely.geometry.Point(5, 5)]

    def main(self):
        """
        Main execution function.  This is called from within a thread in
        the constructor.  The is_running flag is used to indicate when it
        should stop executing.
        """
        while (self.is_running):
            time.sleep(1)
