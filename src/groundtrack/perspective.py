import math
import cv2
import numpy as np
import sys

# produce a matrix to convert from pixel coordinates to world (m) coordinates


def image_to_world(pixels_per_meter, width_m, height_m, cx_m, cy_m, z_m):
    # compute multipliers from pixels->m
    # and destination width,height in pixels
    mx = my = 1.0 / pixels_per_meter

    # compute offsets
    ox = cx_m - (width_m / 2.0)
    oy = cy_m - (height_m / 2.0)

    a = [[ mx, 0.0,  ox],
         [0.0,  my,  oy],
         [0.0, 0.0, z_m]]

    return np.array(a)


def world_to_camera(f_raw, width_px, height_px):
    f = f_raw * width_px / 2.0
    cx = width_px / 2.0
    cy = height_px / 2.0

    a = [[  f, 0.0,  cx],
         [0.0,   f,  cy],
         [0.0, 0.0, 1.0]]
    return np.array(a)


def proj_mat(f, cx, cy):
    return np.array([[  f, 0.0,  cx],
                     [0.0,   f,  cy],
                     [0.0, 0.0, 1.0]])


def rot_x(theta):
    c_t = math.cos(theta)
    s_t = math.sin(theta)
    return np.array([[1.0,  0.0,  0.0],
                     [0.0,  c_t,  s_t],
                     [0.0, -s_t,  c_t]])

class Unwarper:
    def __init__(self, cammatrix, distortion_coeffs):
        self.mat = cammatrix
        self.coeffs = distortion_coeffs

    def apply(self, srcim):
        return cv2.undistort(srcim, self.mat, self.coeffs)

class PerspectiveCorrector:

    def __init__(self, srcsize, destsize):
        self.srcsize = srcsize
        self.destsize = destsize
        self.tf = None
        self.inv_tf = None
        self.f = 1.0
        self.h = 0.5
        self.angle = 0.0
        self.psize = 1.0
        self.shift_view = True

    def set_patch_size(self, psize):
        self.psize = psize
        self.tf = None

    def set_focal_length(self, f):
        self.f = f
        self.tf = None

    def set_angle(self, angle):
        self.angle = angle
        self.tf = None

    def set_height(self, h):
        self.h = h
        self.tf = None

    def build_transform(self):
        ppm = self.destsize / self.psize
        self.ppm = ppm
        ytarget = 0.0
        if self.shift_view:
            ytarget = -math.tan(self.angle) * self.h
        A = image_to_world(ppm, self.psize, self.psize, 0.0, ytarget, self.h)
        R = rot_x(self.angle)
        B = world_to_camera(self.f, self.srcsize[1], self.srcsize[0])
        ret = B.dot(R.dot(A))
        return (np.linalg.inv(ret), ret)

    def get_transform(self):
        # only rebuild if it doesn't exist
        if self.tf is None:
            self.tf, self.inv_tf = self.build_transform()

        return self.tf

    def get_inv_transform(self):
        # only rebuild if it doesn't exist
        if self.tf is None:
            self.tf, self.inv_tf = self.build_transform()

        return self.inv_tf

    def image_coords_to_plane(self, coords):
        temptf = self.get_transform()
        tcoords = temptf.dot(coords)
        tcoords /= tcoords[2,:]
        return tcoords

    def image_coords_to_metric(self, coords):
        tcoords = self.image_coords_to_plane(coords)
        tcoords -= (self.destsize / 2.0)
        tcoords /= self.ppm 
        tcoords[1,:] *= -1.0
        return tcoords

    def calculate_metric_sizes(self):
        xcoords = np.zeros((1,self.srcsize[0]), dtype=np.float32)
        ycoords = np.arange(self.srcsize[0], dtype=np.float32).reshape(1,-1)
        zcoords = np.ones((1,self.srcsize[0]), dtype=np.float32)
        coords0 = np.vstack([xcoords, ycoords, zcoords])
        coords1 = np.copy(coords0)
        coords1[0,:] += 1.0
        tc0 = self.image_coords_to_metric(coords0)
        tc1 = self.image_coords_to_metric(coords1)
        diffs = np.abs(tc0[0,:] - tc1[0,:])
        return diffs


    def apply(self, srcim):
        tf = self.get_transform()
        # print(tf)
        return cv2.warpPerspective(srcim, tf, (self.destsize, self.destsize))


if __name__ == '__main__':
    srcim = cv2.flip(cv2.transpose(cv2.imread(sys.argv[1])), 0)
    cv2.imshow("warped", srcim)
    pc = PerspectiveCorrector(srcim.shape, 500)
    pc.set_angle(math.pi / 12)
    pc.set_focal_length(1.3)
    cv2.imshow("unwarped", pc.apply(srcim))
    cv2.waitKey(0)
