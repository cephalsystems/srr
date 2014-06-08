import cv2
import numpy as np
import math
from groundtrack.perspective import PerspectiveCorrector, Unwarper
from objdetect.colorblobs import do_bloom_marker_detection

if __name__ == '__main__':
    srcim = cv2.flip(cv2.imread("vlog/f10_fl.jpg"), 0)

    cmatrix = np.array([[1.18444524e+03,   0.00000000e+00,   6.64141923e+02],
                        [0.00000000e+00,   1.17962564e+03,   4.86803620e+02],
                        [0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
    coeffs = np.array(
        [-0.49905684,  0.70083743, -0.00104716, -0.00104024, -0.76812372])

    pc = PerspectiveCorrector(srcim.shape, 1000)
    pc.shift_view = False
    pc.set_angle(60.0 * math.pi / 180.0)
    pc.set_focal_length(cmatrix[0, 0] / 960.0 * 1.0)
    pc.set_height(1.6)
    pc.set_patch_size(10.0)

    uw = Unwarper(cmatrix, coeffs)
    uwim = cv2.flip(uw.apply(srcim),0)
    pcuwim = pc.apply(uwim)
    #cv2.imshow("raw", srcim)
   # cv2.imshow("unwarped", uwim)
    #cv2.imshow("everything", pcuwim)
    cv2.imwrite("unwarped.jpg", uwim)
    cv2.imwrite("perspcorr.jpg", pcuwim)

    rawcoords = np.array([[1280.0/2.0, 960.0/2.0, 1.0],
                          [0.0, 0.0, 1.0]]).T
    tcoords = pc.image_coords_to_metric(rawcoords)
    print(tcoords)

    msizes = pc.calculate_metric_sizes()
    print(msizes.shape)
    print(msizes)

    #cv2.waitKey(0)
