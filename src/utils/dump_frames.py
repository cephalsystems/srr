import sys
import numpy as np
import cv2
import pygray
import pygrayutils
import time
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern",
                        help="sprintf type pattern for frame filenames.",
                        default="frames/frame%d.png")
    parser.add_argument("-i", "--index",
                        help="Camera index (not consistent!)", type=int, default=0)
    parser.add_argument("-s", "--serialnumber",
                        help="Camera serial number", type=int, default=0)
    parser.add_argument("-c", "--color", help="Whether to use color",
                        type=int, default=0)
    parser.add_argument("-n", "--numframes", type=int, default=100,
                        help="Number of frames to record.")
    parser.add_argument("--buffer", type=bool, default=False,
                        help="Whether to buffer frames in RAM while capturing")
    parser.add_argument("--list",
                        help="List cameras (overrides all other options)",
                        action="store_true")
    args = parser.parse_args()


    def print_cameras(camlist):
        for guid in camlist:
            cam = pygray.Camera(guid)
            print(guid + ": " + repr(cam.getinfo()))


    def get_cam_by_serial(serialnum, camlist):
        for guid in camlist:
            cam = pygray.Camera(guid)
            caminfo = cam.getinfo()
            if caminfo["serial_number"] == serialnum:
                return cam
        return None

    cams = pygray.listcams()
    cam = None

    if args.list:
        print_cameras(cams)
        return

    if args.serialnumber > 0:
        cam = get_cam_by_serial(args.serialnumber, cams)
        if not cam:
            print("No camera found with serial number %d" % args.serialnumber)
            print("Run with --list argument to get camera information.")
            return
    else:
        cam = pygray.Camera(cams[args.index])

    if args.color:
        print("Capturing color images.")
        cam.setcolormode(True)
    else:
        print("Capturing mono images.")

    cam.start()
    starttime = time.time()
    framebuf = []
    frameid = 0
    for rawid in range(args.numframes):
        try:
            camdata = cam.getframe()
            imdata = pygrayutils.framestr_to_array(camdata)
            if args.buffer:
                framebuf.append((frameid, imdata))
            else:
                destfn = args.pattern % frameid
                cv2.imwrite(destfn, imdata)
            frameid += 1
        except pygray.FrameError as e:
            print("Had a frame error, but ignoring: " + str(e))

    endtime = time.time()
    cam.stop()

    nframes = frameid

    if args.buffer:
        print("Captured %d frames in %f seconds." % (nframes, endtime - starttime))
        starttime = time.time()
        for frameid, imdata in framebuf:
            destfn = args.pattern % frameid
            cv2.imwrite(destfn, imdata)
        endtime = time.time()

    print("Wrote %d frames in %f seconds." % (nframes, endtime - starttime))

if __name__ == '__main__':
    # kind of stupid, but it's the python way
    main()
