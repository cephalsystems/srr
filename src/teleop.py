#!/usr/bin/env python
"""
Simple script to teleoperate rover with WASD controls.
W - forward
S - stop
X - backwards
A - Left
D - Right
Q - Left-Forward
E - Right Forward
"""
import sys, tty, termios
import roboclaw

if __name__ == '__main__':
    r = roboclaw.Roboclaw(sys.argv[1])
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    print "SPACE to exit!"
    
    try:
        tty.setraw(fd)            
        while (True):
            ch = sys.stdin.read(1)
            if ch == ' ':
                break
            elif ch == 'w':
                print "Forwards!\r\n"
                r.mixed_set_speed(80000, 80000)
            elif ch == 's':
                print "Stop!\r\n"
                r.mixed_set_speed(0, 0)
            elif ch == 'a':
                print "Left!\r\n"
                r.mixed_set_speed(60000, 80000)
            elif ch == 'd':
                print "Right!\r\n"
                r.mixed_set_speed(80000, 60000)
            elif ch == 'x':
                print "Backwards!\r\n"
                r.mixed_set_speed(-60000, -60000)
            elif ch == 'z':
                print "Backward Left!\r\n"
                r.mixed_set_speed(-60000, -80000)
            elif ch == 'c':
                print "Backwards Right\r\n"
                r.mixed_set_speed(-80000, -60000)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
            
