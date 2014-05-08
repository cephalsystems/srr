# import this to setup some basic stuff for testing

import roboclaw
from roboclaw import *
import serial

def do_setup():
    print "Roboclaw Example 1\r\n"

    # Open serial ports
    port_rake = serial.Serial("/dev/roboclaw_rake", baudrate=38400, timeout=1)
    port_drive = serial.Serial("/dev/roboclaw_drive", baudrate=38400, timeout=1)
    cmult = 65536.0
    port = port_drive
    roboclaw.port = port_drive
    roboclaw.SetM1pidq(int(10.0 * cmult),
                       int(0 * cmult),
                       int(0.5 * cmult), 180000)
    roboclaw.SetM2pidq(int(10.0 * cmult),
                       int(0 * cmult),
                       int(0.5 * cmult), 180000)

    # Get version string.
    sendcommand(128,21);
    rcv = port.read(32)
    print repr(rcv)

    return (port_rake, port_drive)
