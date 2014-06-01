#!/usr/bin/env python
import math
import time
import threading
import roboclaw
import shapely.geometry
import logging
logger = logging.getLogger('navigation')

K_TURN = 50000
K_DRIVE = 50000
SPEED_LIMIT = 100000
ACCEL_LIMIT = 10000


def clamp(value, minimum, maximum):
    """
    Clamps the specified value between the given min and max values.
    """
    return max(minimum, min(value, maximum))


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

        # Connect to drivetrain Roboclaw.
        self.motors = roboclaw.Roboclaw(args.motor_port)

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

        # Divide the angle into 45 degree quadrants, reverse direction
        # each quadrant (to produce fake 'parallel' parking turns).
        if (abs(theta) > 3.0*math.pi/4.0):
            direction = -1
        elif (abs(theta) > math.pi/2.0):
            direction = 1
        elif (abs(theta) > math.pi/4.0):
            direction = -1
        else:
            direction = 1

        # Create speeds based on proportional heuristic.
        forward_speed = K_DRIVE * -math.log(theta / math.pi)  # Logarithmic
        turn_speed = K_TURN * (1.0 / (1.0 + math.exp(-2.0*theta)))  # Logistic

        # Combine turning and forward terms to get motor speed.
        v1 = direction * (forward_speed - turn_speed)
        v2 = direction * (forward_speed + turn_speed)

        # Limit velocities to reasonable range.
        v1 = clamp(v1, -SPEED_LIMIT, SPEED_LIMIT)
        v2 = clamp(v1, -SPEED_LIMIT, SPEED_LIMIT)
        self.motors.mixed_set_speed_accel(ACCEL_LIMIT, v1, v2)

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
