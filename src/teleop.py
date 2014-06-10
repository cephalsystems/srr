#!/usr/bin/env python
description = """
Simple script to teleoperate rover with WASD controls.
W - forward
S - stop
X - backwards
A - Left
D - Right
Q - Left-Forward
E - Right Forward
] - Scoop ON
[ - Scoop OFF
> - Lift UP
< - Lift DOWN
/ - Lift STOP
) - Bagger ON
( - Bagger OFF
* - Bagger REV
"""
import sys, tty, termios
import roboclaw

if __name__ == '__main__':
    # Drivetrain
    r = roboclaw.Roboclaw('/dev/serial/by-path/pci-0000:00:14.0-usb-0:4:1.0')
    r.reset_encoders()

    # Lift and Bag
    c = roboclaw.Roboclaw('/dev/serial/by-path/pci-0000:04:00.0-usb-0:1:1.0')
    c.reset_encoders()

    # Scoop
    s = roboclaw.Roboclaw('/dev/serial/by-path/pci-0000:04:00.0-usb-0:2:1.0')
    s.reset_encoders()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    print description
    print "SPACE to exit!"
    
    try:
        tty.setraw(fd)            
        while (True):
            try: 
                ch = sys.stdin.read(1)
                if ch == ' ':
                    break
                elif ch == 'w':
                    print "Half Forwards!\r\n"
                    r.mixed_set_speed_accel(75000, 30000, 30000)
                elif ch == 'W':
                    print "Forwards!\r\n"
                    r.mixed_set_speed_accel(75000, 80000, 80000)
                elif ch == 's' or ch == 'S':
                    print "Stop!\r\n"
                    r.mixed_set_speed(0, 0)
                elif ch == 'a':
                    print "Left!\r\n"
                    r.mixed_set_speed_accel(75000, -30000, 30000)
                elif ch == 'd':
                    print "Right!\r\n"
                    r.mixed_set_speed_accel(75000, 30000, -30000)
                elif ch == 'x':
                    print "Half Backwards!\r\n"
                    r.mixed_set_speed_accel(75000, -30000, -30000)
                elif ch == 'X':
                    print "Backwards!\r\n"
                    r.mixed_set_speed_accel(75000, -60000, -60000)
                elif ch == 'z':
                    print "Backward Left!\r\n"
                    r.mixed_set_speed_accel(75000, -60000, -80000)
                elif ch == 'c':
                    print "Backwards Right\r\n"
                    r.mixed_set_speed_accel(75000, -80000, -60000)
                elif ch == '[':
                    print "Scoop OFF\r\n"
                    s.m1_forward(0)
                elif ch == ']':
                    print "Scoop ON\r\n"
                    s.m1_forward(74)
                elif ch == '.':
                    print "Lift UP\r\n"
                    print str(c.m1_encoder) + '\r\n'
                    c.m1_forward(120)
                elif ch == ',':
                    print "Lift DOWN\r\n"
                    print str(c.m1_encoder) + '\r\n'
                    c.m1_backward(90)
                elif ch == '/':
                    print "Lift STOP\r\n"
                    print str(c.m1_encoder) + '\r\n'
                    c.m1_forward(0)
                elif ch == '0':
                    print "Bagger ON\r\n"
                    print str(c.m2_encoder) + '\r\n'
                    c.m2_forward(80)
                elif ch == '9':
                    print "Bagger OFF\r\n"
                    print str(c.m2_encoder) + '\r\n'
                    c.m2_forward(0)
                elif ch == '8':
                    print "Bagger REV\r\n"
                    print str(c.m2_encoder) + '\r\n'
                    c.m2_backward(64)
            except ValueError:
                print 'Lost communication with drivers?\r\n'
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
            
