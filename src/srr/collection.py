#!/usr/bin/env python
import time
import math
import logging
import roboclaw
import srr.navigation
logger = logging.getLogger('collection')

SCOOPING_TIMEOUT = 20.0
SCOOPING_DRIVE_SPEED = 30000
SCOOPING_DRIVE_ACCEL = 15000

LIFTER_RAISED_POSITION = 5000  # Position of the lifter when upright.
LIFTER_HOLD_POSITION = 4100  # Position of the lifter when clear of bagger.
LIFTER_STANDBY_POSITION = 1000  # Position of the lifter when in standby.

BAGGER_REVOLUTION = 69000  # Ticks per bagging revolution.
BAGGER_SPEED = 90
BAGGER_TIMEOUT = 10.0

BAGGER_PRELOAD = 12500


class Collector(object):
    """
    Collection wrapper object which controls the motion of the scoop and
    collector, in conjunction with the navigation and perception subsystems.
    """
    def __init__(self, navigator, perceptor, args):
        self.navigator = navigator
        self.perceptor = perceptor

        # Connect to bagging/lifing and scooping Roboclaw.
        # bagger.m1 is lifter
        # bagger.m2 is bagger
        # scoop.m1 is scoop brushes
        self.bagger = roboclaw.Roboclaw(args.bagger_port)
        self.scoop = roboclaw.Roboclaw(args.scoop_port)

        # Reset encoders on roboclaws.
        self.bagger.reset_encoders()
        self.scoop.reset_encoders()

        # Maintain a local offset for encoders
        self.bagger_offset = 0

        logger.info("Collector initialized.")

    def shutdown(self):
        """
        Shuts down the main function for this object and waits for it
        to complete.
        """
        logger.info("Collector shutdown.")

    def collect(self):
        """
        Perform a scoop and collect action.
        Assumes the scoop is in the 'safe' position.
        """
        logger.info("COLLECTING!")
        self.lower_scoop()
        self.start_scoop()
        self.navigator.motors.mixed_set_speed_accel(SCOOPING_DRIVE_ACCEL,
                                                    SCOOPING_DRIVE_SPEED,
                                                    SCOOPING_DRIVE_SPEED)
        time.sleep(5.0)
        self.navigator.motors.mixed_set_speed_accel(SCOOPING_DRIVE_ACCEL,
                                                    0, 0)
        self.drive_scoop(LIFTER_HOLD_POSITION)
        self.stop_scoop()
        self.drive_bagger(BAGGER_PRELOAD)
        self.start_scoop()
        self.drive_scoop(LIFTER_RAISED_POSITION)
        time.sleep(2.0)
        self.stop_scoop()
        self.drive_scoop(LIFTER_HOLD_POSITION)
        self.drive_bagger(BAGGER_REVOLUTION)
        self.drive_bagger(BAGGER_REVOLUTION)
        self.drive_scoop(LIFTER_STANDBY_POSITION)

    def drive_bagger(self, position):
        """
        Move the bagger to its home location.
        """
        # Wait for bagger to come back online.
        logger.info("Waiting for bagger to be enabled.")
        while not self.bagger.is_connected:
            time.sleep(0.5)
        logger.info("Rotating bagger.")

        # Get current bagger location.
        try:
            curr_encoder, status = self.bagger.m2_encoder
            curr_encoder += self.bagger_offset
            curr_encoder = max(0, curr_encoder)
        except ValueError:
            return

        # Move to position in next bagger revolution.
        next_encoder = position + BAGGER_REVOLUTION * \
            (math.floor(curr_encoder / BAGGER_REVOLUTION))

        timeout = time.time() + BAGGER_TIMEOUT
        self.bagger.m2_forward(BAGGER_SPEED)

        while time.time() < timeout:
            try:
                time.sleep(0.01)
                curr_encoder, status = self.bagger.m2_encoder
                curr_encoder += self.bagger_offset
                curr_encoder = max(0, curr_encoder)

                if self.bagger.motor_currents[1] > 15.0:
                    logger.info("Bagger is stalled {0}".format(position))
                    break
                if curr_encoder > next_encoder - 400:
                    logger.info("Bagging completed.")
                    break

            except ValueError, e:
                logger.info("Rehome interrupted by '{0}'".format(e))
                self.bagger_offset = curr_encoder

                while not self.bagger.is_connected:
                    time.sleep(1)
                timeout = time.time() + BAGGER_TIMEOUT
                self.bagger.m2_forward(BAGGER_SPEED)

        self.bagger.m2_forward(0)

    def home_scoop(self):
        while True:
            # Wait for bagger to come back online.
            logger.info("Waiting to rehome scoop.")
            while not self.bagger.is_connected:
                time.sleep(0.5)
            logger.info("Rehoming scoop.")

            # Slowly lower scoop until we stop seeing motion.
            try:
                timeout = time.time() + SCOOPING_TIMEOUT
                prev_encoder, status = self.bagger.m1_encoder
                self.bagger.m1_backward(64)

                while time.time() < timeout:
                    time.sleep(0.25)
                    curr_encoder, status = self.bagger.m1_encoder
                    if prev_encoder - curr_encoder < 3:
                        logger.info("Valid home found.")
                        break
                    prev_encoder = curr_encoder

                self.bagger.reset_encoders()
                self.bagger.m1_backward(0)
                logger.info("Scoop home set.")
                return
            except ValueError, e:
                logger.info("Rehome interrupted by '{0}'".format(e))
                time.sleep(1)

    def lower_scoop(self):
        logger.info("Lowering scoop.")
        timeout = time.time() + SCOOPING_TIMEOUT
        prev_encoder = 9000000
        self.bagger.m1_backward(127)

        while time.time() < timeout:
            try:
                time.sleep(0.25)
                curr_encoder, status = self.bagger.m1_encoder
                if prev_encoder - curr_encoder < 10:
                    logger.info("Scoop lowered.")
                    break
                prev_encoder = curr_encoder
            except ValueError:
                logger.info("Waiting for resume.")
                self.home_scoop()
                break

        self.bagger.m1_backward(0)

    def drive_scoop(self, position):
        logger.info("Driving scoop.")
        timeout = time.time() + SCOOPING_TIMEOUT

        while time.time() < timeout:
            try:
                time.sleep(0.1)
                curr_position, status = self.bagger.m1_encoder
                if self.bagger.motor_currents[0] > 15.0:
                    logger.info("Scoop stalled before {0}".format(position))
                    break
                if curr_position < position - 20:
                    self.bagger.m1_forward(127)
                elif curr_position > position + 20:
                    self.bagger.m1_backward(127)
                else:
                    logger.info("Scoop moved to {0}".format(position))
                    break
            except ValueError:
                logger.info("Waiting for resume.")
                self.home_scoop()

                # Reset timeout and resume raising.
                timeout = time.time() + SCOOPING_TIMEOUT

        self.bagger.m1_forward(0)

    def start_scoop(self):
        logger.info("Starting scoop.")
        self.scoop.m1_forward(74)

    def stop_scoop(self):
        logger.info("Stopping scoop.")
        self.scoop.m1_backward(32)
        time.sleep(0.25)
        self.scoop.m1_backward(0)

    def home(self):
        """
        Attempts to drive onto the home platform if we are really close.
        """
        logger.info("HOMING")
        polar_home = (10.0, math.pi)

        # Aim at the home platform.
        while abs(polar_home[1]) > 0.1:
            time.sleep(0.1)

            home = self.perceptor.home
            if home is not None:
                polar_home = srr.navigation.to_polar(home)

            self.navigator.angle(polar_home[1])

        # Drive onto the platform.
        self.navigator.drive(polar_home[0])
        logger.info("I think we are on the platform.")
        return True
