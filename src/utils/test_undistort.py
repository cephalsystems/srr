import cv2
import sys
import numpy as np

srcfn = sys.argv[1]
destfn = sys.argv[2]

srcim = cv2.imread(srcfn)

# camera matrix:
# [[  1.12807356e+03   0.00000000e+00   6.62029079e+02]
#  [  0.00000000e+00   1.12227244e+03   5.17535427e+02]
#  [  0.00000000e+00   0.00000000e+00   1.00000000e+00]]
# distortion coefficients:  [-0.4534179   0.45527789 -0.00469093 -0.00191627 -0.3651152 ]

# [[  1.25138158e+03   0.00000000e+00   6.93023130e+02]
#  [  0.00000000e+00   1.25368587e+03   4.83075622e+02]
#  [  0.00000000e+00   0.00000000e+00   1.00000000e+00]]
# distortion coefficients:  [ -6.54346881e-01   1.56164084e+00  -6.51562135e-04  -7.71270447e-03
#   -2.64645478e+00]

cmatrix = np.array([[  1.18444524e+03,   0.00000000e+00,   6.64141923e+02],
 [  0.00000000e+00,   1.17962564e+03,   4.86803620e+02],
 [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
coeffs = np.array([-0.49905684,  0.70083743, -0.00104716, -0.00104024, -0.76812372])

destim = cv2.undistort(srcim, cmatrix, coeffs)

cv2.imwrite(destfn, destim)