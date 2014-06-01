#!/usr/bin/env python
import math
import time
import threading
import roboclaw
import shapely.geometry
import logging
logger = logging.getLogger('navigation')

# Potential field constants.
K_OBS = 10.0
K_TARGET = 1.0
MAX_DISTANCE = 10.0

# Driving constants.
K_TURN = 50000
K_DRIVE = 50000
SPEED_LIMIT = 100000
ACCEL_LIMIT = 10000

ORIGIN = shapely.geometry.Point


def clamp(value, minimum, maximum):
    """
    Clamps the specified value between the given min and max values.
    """
    return max(minimum, min(value, maximum))


def to_polar(point):
    """
    Converts a shapely Point to a (distance, angle) tuple.
    """
    return ORIGIN.distance(point), math.atan2(point.y, point.x)


def from_polar(distance, angle):
    return shapely.geometry.Point(distance * math.cos(angle),
                                  distance * math.sin(angle))


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
        point = shapely.geometry.Point(1000 * math.cos(theta),
                                       1000 * math.sin(theta))
        self._goto_target(point)

    def goto_target(self, point):
        """
        Navigate toward a point in the local frame.  This considers
        the local direction and the distance to the target.
        """
        logger.info("GOTO_TGT: {0}".format(point))
        self._goto_target(point)

    def _compute_safe_target(self, target, obstacles):
        """
        Computes new vector target using quadratic potential fields to
        avoid obstacles.
        """
        polar_obstacles = [to_polar(obstacle) for obstacle in obstacles]
        forces = [from_polar(-K_OBS*distance*distance, angle)
                  for (distance, angle) in polar_obstacles]

        # Attractive force for the target.
        polar_target = to_polar(target)
        polar_target[0] = max(polar_target[0], MAX_DISTANCE)
        forces.append(from_polar(K_TARGET*polar_target[0]*polar_target[0],
                                 polar_target[1]))

        # Compute goal from these forces.
        goal = ORIGIN
        for force in forces:
            goal = goal + force
        polar_goal = to_polar(goal)
        return from_polar(math.sqrt(polar_goal[0]), polar_goal[1])

    def _goto_target(self, point):
        """
        Internal function to drive directly to a target location.
        """
        goal = self._compute_field(point, self.perceptor.obstacles)
        distance, theta = to_polar(goal)

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
        forward_speed = K_DRIVE * math.cos(theta) * distance
        turn_speed = K_TURN * (1.0 / (1.0 + math.exp(-2.0*theta)))  # Logistic

        # Combine turning and forward terms to get motor speed.
        v1 = direction * (forward_speed - turn_speed)
        v2 = direction * (forward_speed + turn_speed)

        # Limit velocities to reasonable range.
        v1 = clamp(v1, -SPEED_LIMIT, SPEED_LIMIT)
        v2 = clamp(v1, -SPEED_LIMIT, SPEED_LIMIT)
        self.motors.mixed_set_speed_accel(ACCEL_LIMIT, v1, v2)

    def main(self):
        """
        Main execution function.  This is called from within a thread in
        the constructor.  The is_running flag is used to indicate when it
        should stop executing.
        """
        while (self.is_running):
            time.sleep(1)
            pass
