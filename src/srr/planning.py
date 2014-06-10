#!/usr/bin/env python
import threading
import yaml
import time
import math
import shapely.geometry

import srr.util
import srr.navigation
import srr.perception
import srr.collection

import logging
logger = logging.getLogger('mission')


class MissionPlanner(object):

    """
    The mission planner is the top-level autonomy for the rover.
    It is *THE* main outer loop for everything.
    """
    DISTANCE_THRESHOLD = 2

    def __init__(self, args):
        """
        Starts up the mission planner for the rover, instantiating the
        underlying navigation, perception, and collection subsystems.
        """
        self.task = None

        logger.info("Loading mission '{0}'.".format(args.mission))
        with open(args.mission, 'rb') as mission_file:
            mission_spec = yaml.safe_load(mission_file)
            self.environment = srr.util.parse_environment(
                mission_spec['environment'])
            self.mission = srr.util.parse_mission(mission_spec['mission'],
                                                  self.environment)

        logger.info("Starting up subsystems.")
        self.perceptor = srr.perception.Perceptor(self.environment,
                                                  args)
        self.navigator = srr.navigation.Navigator(self.environment,
                                                  self.perceptor,
                                                  args)
        self.collector = srr.collection.Collector(self.navigator,
                                                  self.perceptor,
                                                  args)

        self.is_running = True
        self._thread = threading.Thread(target=self.main,
                                        args=[args], name='planner')
        self._thread.start()

    def shutdown(self):
        """
        Shuts down the main function for this object and waits for it
        to complete.
        """
        self.is_running = False
        self._thread.join()

        logging.info("Navigator shutdown.")

    def main(self, args):
        """
        Main planning loop.  This dequeues tasks from the mission and
        attempts to execute each one until it completes or a timeout
        is reached.
        """
        if args.console:
            import IPython
            IPython.embed()
        elif args.precached:
            self.mission1()
        else:
            self.mission2()

        self.perceptor.shutdown()
        self.navigator.shutdown()
        self.collector.shutdown()
        logger.info("Shutdown complete.")

    def mission1(self):
        """
        Attempts to retrieve the precached sample!
        """
        logger.info("Precached sample mission started.")
        self.collector.home_scoop()

        # Drive straight to the sample.
        timeout = time.time() + 300.0  # 5 minute timeout.
        while time.time() < timeout:
            time.sleep(0.01)
            if not self.is_running:
                logger.info("Mission aborted.")
                return

#            self.navigator.goto_goal(0.0, 86.56)  # Position of precached sampl
            self.navigator.goto_goal(0.0, 5.0)  # testing code

        # Try to find the sample by spiraling.
        while True:
            time.sleep(0.01)
            if not self.is_running:
                logger.info("Mission aborted.")
                return

            targets = self.perceptor.targets
            if len(targets) > 0:
                # If we see a target try to get it!
                logger.info("Diverting to target of opportunity!")
                distances = [srr.navigation.to_polar(target)[0]
                             for target in targets]
                min_distance = min(distances)
                min_target = targets[distances.index(min_distance)]

                if min_distance > MissionPlanner.DISTANCE_THRESHOLD:
                    self.navigator.goto_target(min_target)
                elif abs(min_target[1]) > 0.1:
                    self.navigator.angle(min_target[1])
                else:
                    self.collector.collect()
                    break
            else:
                # If we don't see anything, just spiral around.
                self.navigator.spiral(time.time() - start_time)

        # Spend the rest of the time trying to go home.
        while not self.navigator.goto_goal(srr.navigation.ORIGIN) \
          and self.perceptor.home is None:
            time.sleep(0.01)
            if not self.is_running:
                logger.info("Mission aborted.")
                return

        start_time = None
        while True:
            if self.perceptor.home is not None:
                start_time = None
                if self.navigator.goto_home(start_time):
                    break
            else:
                if start_time is None:
                    start_time = time.time()
                self.navigator.spiral(start_time)

        # Shut down everything and complete mission.
        self.collector.home()
        self.navigator.stop()
        logger.info("Mission completed.")

    def mission2(self):
        """
        Attempts to retrieve as many samples as possible!
        """
        logger.info("Search sample mission started.")
        self.collector.home_scoop()

        # Drive off the platform
        self.navigator.drive(3.0)

        # Try to find the sample by spiraling.
        start_time = time.time()
        timeout = start_time + 3600.0  # 1 hour timeout
        while time.time() < timeout \
                and self.navigator.motors.main_voltage > 11.8:
            time.sleep(0.01)
            if not self.is_running:
                logger.info("Mission aborted.")
                return

            targets = self.perceptor.targets
            if len(targets) > 0:
                # If we see a target try to get it!
                logger.info("Diverting to target of opportunity!")
                distances = [srr.navigation.to_polar(target)[0]
                             for target in targets]
                min_distance = min(distances)
                min_target = targets[distances.index(min_distance)]

                if min_distance > MissionPlanner.DISTANCE_THRESHOLD:
                    self.navigator.goto_target(min_target)
                else:
                    self.collector.collect()
            else:
                # If we don't see anything, just spiral around.
                self.navigator.spiral(time.time() - start_time)

        # Spend the rest of the time trying to go home.
        start_time = time.time()
        while not self.navigator.goto_home(start_time):
            time.sleep(0.01)
            if not self.is_running:
                logger.info("Mission aborted.")
                return

        # Shut down everything and complete mission.
        self.collector.home()
        self.navigator.stop()
        logger.info("Mission completed.")

    def perform_mission(self):
        """
        Attempts to perform a mission from the YAML specification.
        """
        logging.info("Starting mission.")
        self.collector.home_scoop()

        for task in self.mission:
            self.task = task
            logging.info("Executing task '{0}'.".format(task.name))

            # Try to complete this task until the timeout.
            while srr.util.elapsed_time() <= task.timeout:
                if not self.is_running:
                    logger.info("Mission aborted.")
                    return

                if self.perform_task(task):
                    break
                else:
                    time.sleep(1)

        # Report that we are giving up and going home.
        if srr.util.elapsed_time() > task.timeout:
            logger.info("Aborting tasks, going home.")
        else:
            logger.info("Completed tasks, going home.")

        # Spend the rest of the time trying to go home.
        while not self.navigator.goto_home():
            if not self.is_running:
                logger.info("Mission aborted.")
                return
            time.sleep(1)

        # Shut down everything and complete mission.
        self.collector.home()
        self.navigator.stop()
        logger.info("Mission completed.")

    def perform_task(self, task):
        """
        Logic for how to execute tasks.

        @return Boolean indicating if the task is completed.
        """
        # Get current location estimate
        # TODO: use perception estimate if available
        rover_location = self.navigator.position

        # If we see a target of opportunity, get it if we can!
        if not task.is_forced:
            targets = self.perceptor.targets

            if len(targets) > 0:
                logger.info("Diverting to target of opportunity!")
                polar_targets = [srr.navigation.to_polar(target)
                                 for target in targets]
                distances = [distance for (distance, angle) in polar_targets]
                min_distance = min(distances)
                min_target = polar_targets[distances.index(min_distance)]

                if min_distance > 2.0:
                    self.navigator.goto_angle(min_target)
                    return False
                if abs(min_target[1]) > 0.1:
                    self.navigator.angle(min_target[1])
                else:
                    self.collector.collect()
                    return False

        # Attempt to navigate based on distance to task.
        task_distance = rover_location.distance(task.bounds)
        if task_distance > MissionPlanner.DISTANCE_THRESHOLD:
            # If we are not near the waypoint or inside the bounds,
            # try to get there.
            return self.navigator.goto_goal(task.location)
        elif task.bounds.type != shapely.geometry.Point:
            # If we are inside a bounded area, just drive around.
            logger.info("Searching '{0}'.".format(task.name))
            self.navigator.goto_angle(0)
        else:
            # If we have reached a destination point, skip to next task.
            logger.info("Task '{0}' completed.".format(task.name))
            return True
