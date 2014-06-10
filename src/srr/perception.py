#!/usr/bin/env python
import threading
import shapely.geometry
import logging
import run_vision
import math
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

        self.home = None
        self.targets = []

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
            # camera coordinates have y forward
            camx = -1.0 * vision_system.scaled_pos[1]
            camy =  1.0 * vision_system.scaled_pos[0]

            # rover is forward of camera view pos
            fdist = 1.0 # m forward 
            roverx = camx + math.cos(vision_system.theta)*fdist
            rovery = camy - math.sin(vision_system.theta)*fdist
            
            self.position = shapely.geometry.Point(roverx, rovery)
            self.rotation = vision_system.theta

            # home beacon
            if vision_system.platpos is not None:
                self.home = shapely.geometry.Point(vision_system.platpos[1],
                                                      -vision_system.platpos[0])

            if vision_system.objpoints is not None:
                pts = vision_system.objpoints
                npts = pts.shape[1]
                self.targets = []
                for i in range(npts):
                    curpt = shapely.geometry.Point(pts[1][i],
                                                    -pts[0][i])
                    self.targets.append(curpt)
