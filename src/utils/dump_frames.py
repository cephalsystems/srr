import sys
import numpy as np
import cv2
import pygray
import pygrayutils
import time

# todo: convert this to argparse
cams = pygray.listcams()
tarcam = int(sys.argv[1])
destpatt = sys.argv[2]
usecolor = (int(sys.argv[3]) > 0)
nframes = int(sys.argv[4])

cam = pygray.Camera(cams[tarcam])
caminfo = cam.getInfo()

if usecolor:
    cam.setColorMode(True)
    
cam.start()
starttime = time.time()
for frameid in range(nframes):
    destfn = destpatt % frameid
    print("Framed %d --> %s" % (frameid, destfn))
    camdata = cam.getFrameStr()
    imdata = pygrayutils.framestr_to_array(camdata)
    cv2.imwrite(destfn, imdata)
endtime = time.time()
cam.stop()
print("Captured %d frames in %f seconds." % (nframes, endtime-starttime))
