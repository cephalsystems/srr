import perspective
import gtracker
import sys
import cv2
import math
import numpy as np

class DefaultTracker:
    def __init__(self):
        self.tracker = gtracker.GroundTracker(gtracker.BRISKMatcher(),
                                     gtracker.AffinePoseEstimator(), None)
        self.prevframe = None
        self.total_tf = np.eye(3,3)
        self.totaltheta = 0.0
        self.totalpos = [0.0,0.0]
        self.nfeats = 0

    def orient_raw_frame(self, f):
        return cv2.flip(cv2.transpose(cv2.imread(fname)), 0)

    def do_tracking(self, rawim):
        #srcim = rawim #self.orient_raw_frame(rawim)
        #curframe = self.pc.apply(srcim)
        curframe = rawim
        dtheta = 0.0
        dpos = [0.0, 0.0]
        prevframe = self.prevframe
        if prevframe is not None:
            self.tracker.setImages(prevframe, curframe)
            self.tracker.processImageMatching()
            
            if self.tracker.tf is not None:
                temp_tf = np.eye(3, 3)
                dtheta, dpos = gtracker.rigid2dToRT(self.tracker.tf)
                temp_tf[0:2, 0:3] = self.tracker.tf
                self.total_tf = self.total_tf.dot(temp_tf)

                totaltheta, totalpos = gtracker.rigid2dToRT(self.total_tf)
                self.totaltheta = totaltheta
                self.totalpos = totalpos
            self.nfeats = self.tracker.nfeats

        self.prevframe = curframe
        return (self.totaltheta, self.totalpos, dtheta, dpos)



if __name__ == '__main__':
    srcpatt = sys.argv[1]
    nframes = int(sys.argv[2])

    pc = None
    tracker = gtracker.GroundTracker(gtracker.ORBMatcher(),
                                     gtracker.AffinePoseEstimator(), None)
    prevframe = None

    temp_tf = np.eye(3, 3)
    total_tf = np.eye(3, 3)

    logdest = open(sys.argv[3], "wt")

    for n in range(nframes):
        fname = srcpatt % n
        print(fname)
        srcim = cv2.flip(cv2.transpose(cv2.imread(fname)), 0)
        cv2.imshow("warped", srcim)
        if not pc:
            pc = perspective.PerspectiveCorrector(srcim.shape, 500)
        pc.set_angle(math.pi / 12)
        pc.set_focal_length(1.3)
        curframe = pc.apply(srcim)
        cv2.imshow("unwarped", curframe)
        if prevframe is not None:
            tracker.setImages(prevframe, curframe)
            tracker.processImageMatching()
            print(tracker.tf)
            if tracker.tf is not None:
                dtheta, dpos = gtracker.rigid2dToRT(tracker.tf)
                print("DTheta: %f" % dtheta)
                print("DPos: (%f, %f)" % dpos)
                temp_tf[0:2, 0:3] = tracker.tf
                total_tf = total_tf.dot(temp_tf)

                totaltheta, totalpos = gtracker.rigid2dToRT(total_tf)
                print("theta: %f, pos: [%f,%f]" %
                      (totaltheta, totalpos[0], totalpos[1]))
                logdest.write("%f %f %f\n" %
                              (totaltheta, totalpos[0], totalpos[1]))
        prevframe = curframe
        cv2.waitKey(1)

    logdest.close()
