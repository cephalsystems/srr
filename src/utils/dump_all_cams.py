import sys
import numpy as np
import cv2
import pygray
import pygrayutils
import time
import argparse

def open_all_cams():
    camlist = pygray.listcams()
    cams = [pygray.Camera(guid) for guid in camlist]
    return cams

def start_all_cams(cams, colormode=True):
    for cam in cams:
        cam.setcolormode(colormode)
        cam.start()

def stop_all_cams(cams):
    for cam in cams:
        cam.stop()

def capture_all_cams(cams, frameidx, destdir):
    for (camidx, cam) in enumerate(cams):
        try:
            cam.start()
            cam.setcolormode(True)
            camdata = cam.getframe()
            cam.stop()
            imdata = pygrayutils.framestr_to_array(camdata)
            destfn = "%s/cam%d_frame%d.png" % (destdir, camidx, frameidx)
            cv2.imwrite(destfn, imdata)
        except pygray.FrameError as e:
            print("had frame error, but ignoring: " + str(e))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--destdir",
                        help="Directory to dump frames into",
                        default="frames/")
    parser.add_argument("-c", "--color", help="Whether to use color",
                        type=int, default=0)
    parser.add_argument("-n", "--numframes", type=int, default=100,
                        help="Number of frames to record.")
    parser.add_argument("-r", "--rate",
                        help="Framerate to capture at.", type=float, default=1.0)
    args = parser.parse_args()

    sleeptime = 1.0 / args.rate

    cams = open_all_cams()
    #start_all_cams(cams, args.color > 0)
    for frameidx in range(args.numframes):
        print("Capturing frame %d" % frameidx)
        capture_all_cams(cams, frameidx, args.destdir)
        time.sleep(sleeptime)
    #stop_all_cams(cams)

if __name__ == '__main__':
    # kind of stupid, but it's the python way
    main()
