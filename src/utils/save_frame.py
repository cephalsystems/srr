import sys
import numpy as np
import cv2
import pygray
import pygrayutils
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename",
                    help="Filename to save image as.", default="frame.png")
parser.add_argument("-i", "--index",
                    help="Camera index (not consistent!)", type=int, default=0)
parser.add_argument("-s", "--serialnumber",
                    help="Camera serial number", type=int, default=0)
parser.add_argument("-c", "--color", help="Whether to use color",
                    type=bool, default=False)
parser.add_argument("--list",
                    help="List cameras (overrides all other options)",
                    action="store_true")
args = parser.parse_args()


def print_cameras(camlist):
    for guid in camlist:
        cam = pygray.Camera(guid)
        print(repr(cam.getinfo()))


def get_cam_by_serial(serialnum, camlist):
    for guid in camlist:
        cam = pygray.Camera(guid)
        caminfo = cam.getinfo()
        if caminfo.serial_number == serialnum:
            return cam
    return None

cams = pygray.listcams()
cam = None

if args.list:
    print_cameras(cams)
    return

if args.serialnumber > 0:
    cam = get_cam_by_serial(args.serialnumber)
    if not cam:
        print("No camera found with serial number %d" % args.serialnumber)
        print("Run with --list argument to get camera information.")
        return
else:
    cam = pygray.Camera(cams[args.index])

if args.color:
    cam.setcolormode(True)
cam.start()
camdata = cam.getframe()
cam.stop()

imdata = pygrayutils.framestr_to_array(camdata)

cv2.imwrite(args.filename, imdata)
