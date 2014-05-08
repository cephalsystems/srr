import sys
import numpy as np
import cv2
import pygray
import pygrayutils

# todo: convert this to argparse
cams = pygray.listcams()
tarcam = int(sys.argv[1])
destfn = sys.argv[2]
usecolor = (int(sys.argv[3]) > 0)

cam = pygray.Camera(cams[tarcam])
caminfo = cam.getInfo()
if usecolor:
    cam.setColorMode(True)
cam.start()
camdata = cam.getFrameStr()
cam.stop()

imdata = pygrayutils.framestr_to_array(camdata)
      
cv2.imwrite(destfn, imdata)
