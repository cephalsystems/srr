import pygray
import cv2
import numpy as np
import math
from cameraprocess import CameraProcess
from groundtrack.perspective import PerspectiveCorrector, Unwarper
from objdetect.colorblobs import do_bloom_marker_detection

class VisionRunner:
    def __init__(self):
        self.pc = None
        self.fidx = 0
        self.objmod = 10
        self.cams = CameraProcess()
        self.frate = 5.0
        self.cams.add_camera("beb81a4eda09d70e9c8038688a06fce0",
                             "front_left", True, self.frate)
        self.cams.add_camera("b2e944402e6ae32816dcf9108bfd6c70",
                             "front_right", True, self.frate)
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

    def start_vision(self):
        self.cams.start_cams(10)

    def stop_vision(self):
        self.cams.stop_cams()

    def process_frame(self):
        self.fidx += 1
        allgood = self.cams.do_iteration()
        if not allgood:
            return []
        uw_left = self.unwarper.apply(self.cams.get_data("front_left"))
        front_left = cv2.flip(uw_left,0)
        front_right = self.cams.get_data("front_right")
        rear = self.cams.get_data("rear")

        if self.pc == None:
            self.pc = PerspectiveCorrector(front_left.shape, 500)
            self.pc.set_angle(60.0 * math.pi / 180.0)
            self.pc.set_focal_length(self.cmatrix[0,0] / 960.0)
            self.pc.set_height(1.6)
            self.pc.set_patch_size(10.0)
            self.pc.shift_view = False

        if self.fidx % self.objmod == 0:
            print("Doing object detection...")
            nodes, objimage = do_bloom_marker_detection(front_left,
                                                        254, 5, 0.4)
            cv2.imwrite("vlog/f%d_fl.jpg" % self.fidx, front_left)
            cv2.imwrite("vlog/f%d_obj.png" % self.fidx, objimage)

            impwarp = self.pc.apply(front_left)
            cv2.imwrite("vlog/f%d_pc.jpg" % self.fidx, impwarp) 
            #warpim = self.pc.apply(
            pts = np.ones((3, len(nodes)), dtype=np.float32) 
            for i, p in enumerate(nodes):
                pts[0,i] = p[0]
                pts[1,i] = p[1]
            print("FOUND NODES: " + str(pts))
            if len(nodes) > 0:
                tpts = self.pc.image_coords_to_metric(pts)
                print("TF NODES: " + str(tpts))


if __name__ == '__main__':
    vt = VisionRunner()
    vt.start_vision()
    while True:
        vt.process_frame()
