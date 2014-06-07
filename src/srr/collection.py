#!/usr/bin/env python
import time
import logging
logger = logging.getLogger('collection')

SCOOPING_LOWER_TIMEOUT = 5.0
SCOOPING_RAISE_TIMEOUT = 5.0
SCOOPING_HOME_TIMEOUT = 10.0

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

    def home_bagger():
        """
        Move the bagger to its home location.
        """
        # TODO: implement this.
        pass
        
    def home_scoop():
        while True:
            # Wait for bagger to come back online.
            logger.info("Waiting to rehome scoop.")
            while not bagger.is_connected():
                time.sleep(0.5)        
            logger.info("Rehoming scoop.")

            # If we can, move the bagger to safe position.
            safe_bagger()
        
            # Slowly lower scoop until we stop seeing motion.
            try:
                timeout = time.time() + SCOOPING_HOME_TIMEOUT
                last_encoder = bagger.m1_encoder
                bagger.m1_backward(40)
        
                while time.time() < timeout:
                    curr_encoder = bagger.m1_encoder
                    if last_encoder - curr_encoder < 10:
                        logger.info("Valid home found.")
                        break
                    last_encoder = curr_encoder
                    time.sleep(0.25)
                    
                logger.info("Scoop home set.")
                bagger.reset_encoders()
                return
            except ValueError:
                logger.info("Rehome interrupted.")
                time.sleep(1)
        
    def lower_scoop():
        timeout = time.time() + SCOOPING_LOWER_TIMEOUT
        last_encoder = 900000
        bagger.m1_backward(90)
        
        while time.time() < timeout:
            try:
                curr_encoder = bagger.m1_encoder
                if last_encoder - curr_encoder < 50:
                    logger.info("Scoop lowered.")
                    bagger.m1_backward(0)
                    return
                
                prev_encoder = curr_encoder
                time.sleep(0.25)
            except ValueError:
                logger.info("Waiting for resume.")
                rehome_scoop()

    def raise_scoop():
        timeout = time.time() + SCOOPING_RAISE_TIMEOUT
        bagger.m1_backward(90)
        
        while time.time() < timeout:
            try:
                if bagger.m1_encoder > 4400:
                    bagger.m1_forward(0)
                    logger.info("Reached top position")
                    return
                time.sleep(0.25)
            except ValueError:
                logger.info("Waiting for resume.")
                rehome_scoop()

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
