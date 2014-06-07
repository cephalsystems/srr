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
        else:
            self.perform_mission()

        self.perceptor.shutdown()
        self.navigator.shutdown()
        self.collector.shutdown()
        logger.info("Shutdown complete.")

    def perform_mission(self):
        """
        Attempts to complete an entire mission.
        """
        logger.info("Mission started.")
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
        rover_angle = self.navigator.rotation

        # If we see a target of opportunity, get it if we can!
        if not task.is_forced:
            targets = self.perceptor.targets

            if len(targets) > 0:
                logger.info("Diverting to target of opportunity!")
                distances = [rover_location.distance(target)
                             for target in targets]
                min_distance = min(distances)
                min_target = targets[distances.index(min_distance)]

                if min_distance > MissionPlanner.DISTANCE_THRESHOLD:
                    self.navigator.goto_target(min_target)
                    return False
                else:
                    self.collector.scoop()
                    self.collector.bag()
                    return False

        # Attempt to navigate based on distance to task.
        task_distance = rover_location.distance(task.bounds)
        if task_distance > MissionPlanner.DISTANCE_THRESHOLD:
            # If we are not near the waypoint or inside the bounds,
            # try to get there.
            logger.info("Driving to '{0}'.".format(task.name))
            vector = task.location - rover_location
            target_angle = math.atan2(vector.y, vector.x)
            self.navigator.goto_angle(target_angle - rover_angle)
            return False
        elif task.bounds.type != shapely.geometry.Point:
            # If we are inside a bounded area, just drive around.
            logger.info("Searching '{0}'.".format(task.name))
            self.navigator.goto_angle(0)
        else:
            # If we have reached a destination point, skip to next task.
            logger.info("Task '{0}' completed.".format(task.name))
            return True
