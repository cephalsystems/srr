#!/usr/bin/env python
import math
import time
import threading
import roboclaw
import shapely.geometry
import shapely.affinity
import logging
logger = logging.getLogger('navigation')

# Potential field constants.
K_OBS = 1e2
K_TARGET = 1e2
MAX_DISTANCE = 10.0

# Driving constants.
K_TURN = 50000
K_DRIVE = 50000
SPEED_MIN = 20000
SPEED_MAX = 100000
ACCEL_MAX = 10000
WHEELBASE_WIDTH = 0.5

ORIGIN = shapely.geometry.Point(0, 0)


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

        # Set no current goal
        self.goal = None

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
        return self.position.x, self.position.y, self._rotation

    def stop(self):
        """
        Immediately stop the vehicle.
        """
        self.motors.mixed_forward(0.0)

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
        forces = []

        # Repelling force for obstacles.
        polar_obstacles = [to_polar(obstacle) for obstacle in obstacles]
        forces += [from_polar(-K_OBS*1.0/(obstacle_distance *
                                          obstacle_distance + 1e-6),
                              obstacle_angle)
                   for (obstacle_distance, obstacle_angle) in polar_obstacles]

        # Attractive force for the target.
        target_distance, target_angle = to_polar(target)
        target_distance = min(target_distance, MAX_DISTANCE)
        forces.append(from_polar(K_TARGET*1.0/(target_distance *
                                               target_distance + 1e-6),
                                 target_angle))

        # Compute goal from these forces.
        goal = ORIGIN
        for force in forces:
            goal = shapely.affinity.translate(goal, force.x, force.y)
        goal_distance, goal_angle = to_polar(goal)
        goal_distance = min(goal_distance, MAX_DISTANCE)
        return from_polar(goal_distance, goal_angle)

    def goto_home(self):
        """
        Go towards best guess of home position.
        """
        home = self.perceptor.home
        beacon = self.perceptor.beacon

        if home is not None:
            if ORIGIN.distance(home) < 1:
                return True
            else:
                self._goto_target(home)
        elif beacon is not None:
            self._goto_target(beacon)
            return False
        else:
            # TODO: figure out where starting locatiom was.
            start = ORIGIN
            self._goto_target(start)
            return False

    def _goto_target(self, point):
        """
        Internal function to drive directly to a target location.
        """
        obstacles = self.perceptor.obstacles

        beacon = self.perceptor.beacon
        if beacon is not None:
            obstacles.append(beacon)

        self.goal = self._compute_safe_target(point, obstacles)
        distance, theta = to_polar(self.goal)

        # Create speeds based on proportional heuristic.
        forward_speed = K_DRIVE * math.cos(theta) * distance
        turn_speed = K_TURN * (1.0 / (1.0 + math.exp(-2.0*theta)))  # Logistic

        # Combine turning and forward terms to get motor speed.
        v1 = forward_speed - turn_speed
        v2 = forward_speed + turn_speed

        # Limit velocities to reasonable range.
        v1 = clamp(v1, -SPEED_MAX, SPEED_MAX)
        v2 = clamp(v1, -SPEED_MAX, SPEED_MAX)
        self.motors.mixed_set_speed_accel(ACCEL_MAX, v1, v2)

    def main(self):
        """
        Main execution function.  This is called from within a thread in
        the constructor.  The is_running flag is used to indicate when it
        should stop executing.
        """
        while (self.is_running):
            time.sleep(1)
            pass
