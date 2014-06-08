#!/usr/bin/env python
import time
import math
import logging
import roboclaw
logger = logging.getLogger('collection')

SCOOPING_LOWER_TIMEOUT = 15.0
SCOOPING_RAISE_TIMEOUT = 18.0
SCOOPING_HOME_TIMEOUT = 20.0

LIFTER_TOP_POSITION = 4350  # Position of the lifter when upright.

BAGGER_REVOLUTION = 69000  # Ticks per bagging revolution.
BAGGER_SPEED = 70
BAGGER_TIMEOUT = 10.0

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

    def scoop(self):
        """
        Perform a scooping action.
        Assumes the scoop is in the 'safe' position.
        """
        logger.info("SCOOPING")
        time.sleep(2)

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
        except ValueError:
            return

        # Move to position in next bagger revolution.
        next_encoder = position + BAGGER_REVOLUTION * \
          (math.floor(curr_encoder / BAGGER_REVOLUTION))

        timeout = time.time() + BAGGER_TIMEOUT
        self.bagger.m2_forward(BAGGER_SPEED)

        while time.time() < timeout:
            try:
                time.sleep(0.05)
                curr_encoder, status = self.bagger.m2_encoder
                curr_encoder += self.bagger_offset

                print (curr_encoder, next_encoder)
                if curr_encoder > next_encoder:
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

            # If we can, move the bagger to safe position.
            self.home_bagger()
        
            # Slowly lower scoop until we stop seeing motion.
            try:
                timeout = time.time() + SCOOPING_HOME_TIMEOUT
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
        timeout = time.time() + SCOOPING_LOWER_TIMEOUT
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

    def raise_scoop(self):
        logger.info("Raising scoop.")
        timeout = time.time() + SCOOPING_RAISE_TIMEOUT
        self.bagger.m1_forward(127)
        
        while time.time() < timeout:
            try:
                time.sleep(0.25)
                position, status = self.bagger.m1_encoder
                if position > LIFTER_TOP_POSITION:
                    logger.info("Scoop raised.");
                    break
            except ValueError:
                logger.info("Waiting for resume.")
                self.home_scoop()

                # Reset timeout and resume raising.
                timeout = time.time() + SCOOPING_LOWER_TIMEOUT
                self.bagger.m1_forward(127)

        self.bagger.m1_forward(0)

    def start_scoop(self):
        logger.info("Starting scoop.")
        self.scoop.m1_forward(74)

    def stop_scoop(self):
        logger.info("Stopping scoop.")
        self.scoop.m1_forward(0)
        
    def bag(self):
        """
        Perform a bagging action.
        """
        logger.info("BAGGING")
        # Advance bagger to safe position.
        
        # Lift until we reach top position.

        time.sleep(2)

    def home(self):
        """
        Attempts to drive onto the home platform if we are really close.
        """
        logger.info("HOMING")
        time.sleep(10)
        # TODO: fill this in!!
        # While < 15 deg angle, drive forward (before ramp)

        # If we never hit a ramp, drive backwards and exit.

        # After ramp, drive until we are flat again

        # If we never flattened, drive backwards and exit.
