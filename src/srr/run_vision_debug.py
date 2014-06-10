import pygray
import cv2
import numpy as np
import math
from cameraprocess import CameraProcess
from groundtrack.perspective import PerspectiveCorrector, Unwarper
from groundtrack.run_tracking import DefaultTracker
from objdetect.colorblobs import do_bloom_marker_detection,do_bloom_platform_detection
import logging
logger = logging.getLogger('vision')

class VisionRunner:
    def __init__(self):
        self.pc = None
        self.altpc = None
        self.rearpc = None
        self.fidx = 0
        self.objmod = 10
        self.cams = CameraProcess()
        self.frate = 10.0
        self.logdir = "/home/cephal/vlog_debug"
        self.odo_multiplier = 0.00167
        self.sizetable = None

        self.theta = 0
        self.scaled_pos = [0.0,0.0]

        self.platpos = None
        self.platscale = 0.1

        self.run_rear = False
        self.run_frontL = True
        self.run_frontR = False

        if self.run_frontL:
            self.cams.add_camera("beb81a4eda09d70e9c8038688a06fce0",
                                 "front_left", True, self.frate)
        if self.run_frontR:
            self.cams.add_camera("b2e944402e6ae32816dcf9108bfd6c70",
                                 "front_right", True, self.frate)
        if self.run_rear:
            self.cams.add_camera("4f350bf72d86c847732377c088108d50",
                                 "rear", False, self.frate)

        self.cmatrix = np.array([[1.18444524e+03, 0.00000000e+00,
                                  6.64141923e+02],
                                 [0.00000000e+00, 1.17962564e+03,
                                  4.86803620e+02],
                                 [0.00000000e+00,   0.00000000e+00,
                                  1.00000000e+00]])
        self.coeffs = np.array([-0.49905684,  0.70083743,
                                -0.00104716, -0.00104024,
                                -0.76812372])
        self.unwarper = Unwarper(self.cmatrix, self.coeffs)
        self.odometry = None

    def start_vision(self):
        self.cams.start_cams(10)

    def stop_vision(self):
        self.cams.stop_cams()

    def process_frame(self):
        self.fidx += 1
        allgood = self.cams.do_iteration()
        if not allgood:
            return []
        front_left = None
        uw_left = None
        if self.run_frontL:
            uw_left = self.unwarper.apply(self.cams.get_data("front_left"))
            front_left = cv2.flip(cv2.flip(uw_left,1), 0)
        front_right = None
        if self.run_frontR:
            front_right = self.cams.get_data("front_right")
        rear = None
        if self.run_rear:
            rear = cv2.flip(cv2.transpose(self.cams.get_data("rear")),0)
            cv2.imwrite("%s/f%d_rear_raw.jpg" % (self.logdir,self.fidx), rear)

        if self.pc == None and self.run_frontL:
            self.pc = PerspectiveCorrector(front_left.shape, 500)
            self.pc.set_angle(64.0 * math.pi / 180.0)
            self.pc.set_focal_length(self.cmatrix[0,0] / 960.0)
            self.pc.set_height(1.6)
            self.pc.set_patch_size(10.0)
            self.pc.shift_view = False
            self.sizetable = self.pc.calculate_metric_sizes()
            self.altpc = PerspectiveCorrector(front_left.shape, 500)
            self.altpc.set_angle(60.0 * math.pi / 180.0)
            self.altpc.set_focal_length(self.cmatrix[0,0] / 960.0 * 1.0)
            self.altpc.set_height(1.6)
            self.altpc.set_patch_size(60.0)
            self.altpc.shift_view = False

        if self.rearpc == None and self.run_rear:
            self.rearpc = PerspectiveCorrector(rear.shape, 500)
            self.rearpc.set_angle(15.0 * math.pi / 180.0)
            self.rearpc.set_focal_length(2.6)
            self.rearpc.set_height(1.6)
            self.rearpc.set_patch_size(1.5)

        rear_corrected = None
        if self.run_rear:
            rear_corrected = self.rearpc.apply(rear)
            cv2.imwrite("%s/f%drear_pc.jpg" % (self.logdir,self.fidx), rear_corrected)

        if self.odometry == None:
            self.odometry = DefaultTracker()


        if self.run_rear:
            logger.debug("Doing tracking...")
            totaltheta, totalpos, dtheta, dpos = self.odometry.do_tracking(rear_corrected)
            scaled_pos = [v*self.odo_multiplier for v in totalpos]
            self.theta = totaltheta
            print("Total theta: %f, total pos: (%f,%f)" % (totaltheta, totalpos[0], totalpos[1]))
            print("Scaled pos: (%f,%f)" % tuple(scaled_pos))
            self.scaled_pos = scaled_pos
            logger.debug("Dtheta: %f, dpos: (%f, %f)" % (dtheta, dpos[0], dpos[1]))
            logger.debug("Frame %d, nfeats: %d" % (self.fidx, self.odometry.nfeats))
            dbgimg = self.odometry.tracker.draw_features()
            cv2.imwrite("%s/f%d_tdbg.jpg" % (self.logdir,self.fidx), dbgimg)

        if self.fidx % self.objmod == 0 and self.run_frontL:
            logger.debug("Doing object detection...")
            nodes, objimage = do_bloom_marker_detection(front_left,
                                                        254, 5, 0.4)
            cv2.imwrite("%s/f%d_fl.jpg" % (self.logdir,self.fidx), front_left)
            cv2.imwrite("%s/f%d_obj.png" % (self.logdir,self.fidx), objimage)

            impwarp = self.pc.apply(front_left)
            altwarp = self.altpc.apply(front_left)
            #cv2.imwrite("%s/f%d_pc.jpg" % (self.logdir,self.fidx), impwarp)
            cv2.imwrite("%s/f%d_pcalt.jpg" % (self.logdir,self.fidx), altwarp) 
            #warpim = self.pc.apply(
            pts = np.ones((3, len(nodes)), dtype=np.float32) 
            for i, p in enumerate(nodes):
                pts[0,i] = p[0]
                pts[1,i] = p[1]
            logger.debug("FOUND NODES: " + str(pts))
            if len(nodes) > 0:
                tpts = self.pc.image_coords_to_metric(pts)
                logger.debug("TF NODES: " + str(tpts))

            #platnodes, platimage = do_bloom_platform_detection(front_left,
            #                                                   254,
            #                                                   self.sizetable)
            platnodes, platimage = do_bloom_marker_detection(altwarp,
                                                               254,
                                                               10,
                                                               0.2)
            self.platpos = None
            if len(platnodes) > 0:
                tx = self.platscale * (platnodes[0][0] - 250.0)
                ty = self.platscale * (250.0 - platnodes[0][1])
                self.platpos = (tx, ty)
                print("Platpos (m): (%f, %f)" % (tx, ty))
            print("Platnodes: " + str(platnodes))
            #ptpts = None
            #if len(platnodes) > 0:
            #    ptpts = self.pc.image_coords_to_metric(pts)
            #    print("PLATFORM LOCATED?: " + str(ptpts))
            cv2.imwrite("%s/f%d_plat.png" % (self.logdir,self.fidx), platimage)

def main():
    vt = VisionRunner()
    vt.start_vision()
    while True:
        vt.process_frame()

if __name__ == '__main__':
    main()
