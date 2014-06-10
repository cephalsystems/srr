#!/usr/bin/env python
import threading
import shapely.geometry
import logging
import run_vision
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
        return self.position.x, self.position.y, self.rotation

    @property
    def obstacles(self):
        """
        List of obstacles, specified as shapely.Point(x.y) tuples in the
        rover local frame in meters.
        """
        return []
    
    @property
    def targets(self):
        """
        List of potential targets, specified as (x,y) tuples in the rover
        local frame in meters.
        """
        return []

    @property
    def home(self):
        """
        Shapely point indicating the home platform position relative
        to the rover local frame in meters, or None if it is not detected.
        """
        return None

    @property
    def beacon(self):
        """
        Shapely point indicating the beacon position relative to the rover
        local frame in meters, or None if it is not detected.
        """
        return None

    def main(self):
        """
        Main execution function.  This is called from within a thread in
        the constructor.  The is_running flag is used to indicate when it
        should stop executing.
        """
        vision_system = run_vision.VisionRunner()
        vision_system.start_vision()
        while (self.is_running):
            vision_system.process_frame()
            # camera faces backwards
            camx = -1.0 * vision_system.scaled_pos[0]
            camy = -1.0 * vision_system.scaled_pos[1]

            # rover is forward of camera view pos
            fdist = 1.0 # m forward 
            roverx = camx - math.sin(vision_system.theta)*fdist
            rovery = camy + math.cos(vision_system.theta)*fdist
            
            self.position = shapely.geometry.Point(roverx, rovery)
            self.rotation = vision_system.theta
