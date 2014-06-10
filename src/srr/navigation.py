#!/usr/bin/env python
import math
import time
import threading
import roboclaw
import shapely.geometry
import shapely.affinity
import srr.util
import logging
logger = logging.getLogger('navigation')

# Potential field constants.
K_OBS = 1.0
K_TARGET = 1.0
MAX_DISTANCE = 10.0

# Driving constants.
K_TURN = 1.0
K_DRIVE = 50000
SPEED_MIN = 10000
SPEED_MAX = 80000
ACCEL_MAX = 40000
WHEELBASE_WIDTH = 0.350
TICKS_PER_METER = 66000.0

ORIGIN = shapely.geometry.Point(0, 0)
DISTANCE_THRESHOLD = 0.5


def signum(value):
    """
    Separates value into sign and magnitude.
    """
    if (value > 0.0):
        return (1.0, value)
    elif (value < 0.0):
        return (-1.0, -value)
    else:
        return (0.0, 0.0)


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
        self._position = shapely.geometry.Point(environment.start[0],
                                                environment.start[1])
        self._rotation = environment.start[2]

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
    def position(self):
        return self.perceptor.position

    @property
    def rotation(self):
        return self.perceptor.rotation
        
    @property
    def pose(self):
        """
        Current (x,y,theta) pose of the rover, as best estimated by the
        odometry system in the global frame.
        """
        return self.position.x, self.position.y, self.rotation

    def stop(self):
        """
        Immediately stop the vehicle.
        """
        self.motors.mixed_forward(0.0)

    def spiral(self, start_time):
        """
        Drives the vehicle in a progressively widening spiral.
        """
        logger.info("SPIRAL: {0}".format(time.time() - start_time))
        t = time.time() - start_time
        self.goto_angle((math.pi/2)/math.exp(t/180.0))

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

    def goto_goal(self, goal):
        """
        Navigate toward a point in the global frame.  This considers
        the global direction and the distance to the target.
        """
        logger.info("GOTO_GOAL: {0}".format(goal))
        task_distance = self.position.distance(goal)
        if task_distance < DISTANCE_THRESHOLD:
            # I could stop here, but that might stall the rover,
            # so I'm just going to let it run.
            return True

        # If we are not near the waypoint or inside the bounds,
        # try to get there.
        target = srr.util.to_local((self.position, self.rotation), goal)
        self.goto_target(target)
        return False

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
            start = ORIGIN
            self.goto_goal(start)
            return False

    def _goto_target(self, point, obstacle_home=True):
        """
        Internal function to drive directly to a target location.
        """
        obstacles = self.perceptor.obstacles

        beacon = self.perceptor.beacon
        if beacon is not None:
            obstacles.append(beacon)

        home = self.perceptor.home
        if home is not None and obstacle_home:
            obstacles.append(home)

        self.goal = self._compute_safe_target(point, obstacles)
        distance, theta = to_polar(self.goal)
        print (point.x, point.y)
        print '->'
        print (distance, theta)

        # Create speeds based on proportional heuristic.
        forward_speed = K_DRIVE * math.cos(theta) * distance
        turn_speed = K_TURN * theta * (forward_speed + 10000)


        # Combine turning and forward terms to get motor speed.
        v1 = forward_speed - turn_speed
        v2 = forward_speed + turn_speed

        # Limit velocities to reasonable range.
        v1 = clamp(v1, -SPEED_MAX, SPEED_MAX)
        v2 = clamp(v2, -SPEED_MAX, SPEED_MAX)

        print '='
        print (v1, v2)
        
        self.motors.mixed_set_speed_accel(ACCEL_MAX, v1, v2)

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

    def angle(self, angle):
        """
        Rotates in place towards specified angle.
        """
        (sign, angle_magnitude) = signum(angle)
        tick_distance = angle_magnitude * WHEELBASE_WIDTH * TICKS_PER_METER

        self.motors.mixed_set_speed_accel_distance(
            20000,
            -sign*20000, tick_distance,
            sign*20000, tick_distance
            )
        # TODO: do I need to wait here?

    def drive(self, distance):
        """
        Drives directly forward by the specified distance.
        Waits until complete.
        """
        # Compute direction and distance to travel in encoder ticks.
        sign = 1.0
        if distance < 0:
            sign = -1.0
            distance *= -1.0
        tick_distance = distance * TICKS_PER_METER

        # Start movement.
        self.motors.mixed_set_speed_accel_distance(
            ACCEL_MAX,
            sign*SPEED_MAX, tick_distance,
            sign*SPEED_MAX, tick_distance)

        # Loop to monitor distance traveled so far.
        timeout = time.time() + (tick_distance / 40000.0)
        start_distance = self.motors.m1_encoder[0]
        while time.time() < timeout:
            try:
                time.sleep(0.1)
                if self.motors.m1_encoder[0] - start_distance >= tick_distance:
                    logger.info("Completed traverse of {0}m.".format(distance))
                    break
            except ValueError:
                logger.info("Wireless pause.  Waiting for resume.")
                tick_distance -= start_distance
                start_distance = 0

                while not self.motors.is_connected:
                    time.sleep(0.5)
                timeout = time.time() + (tick_distance / 40000.0)
                logger.info("Resuming drive.")

        # Stop motion after timeout or completion.
        logger.info("Stopping angle turn.")
        self.motors.mixed_set_speed_accel(ACCEL_MAX, 0, 0)

    def main(self):
        """
        Main execution function.  This is called from within a thread in
        the constructor.  The is_running flag is used to indicate when it
        should stop executing.
        """
        last_encoders = None
        time.sleep(1)

        while (self.is_running):
            try:
                time.sleep(0.01)
                curr_encoder_m1 = self.motors.m1_encoder[0]
                curr_encoder_m2 = self.motors.m2_encoder[0]

                if last_encoders is not None:
                    # Get distances traveled by each wheel.
                    distance_m1 = (curr_encoder_m1 - last_encoders[0]) \
                        * TICKS_PER_METER
                    distance_m2 = (curr_encoder_m2 - last_encoders[1]) \
                        * TICKS_PER_METER

                    # Avoid numerical singularity w/ divide-by-zero.
                    if distance_m2 == distance_m1:
                        distance_m2 += 1e-6

                    # Compute radius of curvature and angle.
                    dTheta = (distance_m2 - distance_m1) / WHEELBASE_WIDTH
                    dR = WHEELBASE_WIDTH * (distance_m2 + distance_m1) \
                        / 2.0 * (distance_m2 - distance_m1)
                    rotation_center = shapely.geometry.Point(
                        -math.sin(self.rotation) * dR,
                        math.cos(self.rotation) * dR
                        )

                    # Integrate with existing pose estimate.
                    self._rotation += dTheta
                    self._position = shapely.affinity.rotate(
                        self._position, dTheta,
                        origin=rotation_center, use_radians=True)

                last_encoders = (curr_encoder_m1, curr_encoder_m2)

            except ValueError:
                last_encoders = (0, 0)
