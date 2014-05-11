#!/usr/bin/env python
"""
Simple script that performs the actions required for the May
qualification.

1) Drive forward ~5m.
2) Pick up an object.
3) Store object.
4) Drive back to starting location.
"""

import roboclaw
import test_setup
import time

port_rake, port_drive = test_setup.do_setup()
speed = 30000

def stop():
    roboclaw.port = port_drive
    roboclaw.SetMixedSpeed(0,0)

def drive(dspeed = 30000):
    roboclaw.port = port_drive
    roboclaw.SetMixedSpeed(dspeed, dspeed)

def back_up():
    roboclaw.port = port_drive
    roboclaw.SetMixedSpeed(-speed, -speed)

def enable_rake():
    roboclaw.port = port_rake
    roboclaw.DriveM2(100)

def disable_rake():
    roboclaw.port = port_rake
    roboclaw.DriveM2(64)

fspeed = 70000
rspeed = 15000
drtime = 7.5
rrtime = 10

drive(fspeed)
time.sleep(drtime)
enable_rake()
drive(rspeed)
time.sleep(rrtime)
stop()
disable_rake()
drive(-fspeed)
time.sleep(drtime)
drive(-rspeed)
time.sleep(rrtime)
stop()
