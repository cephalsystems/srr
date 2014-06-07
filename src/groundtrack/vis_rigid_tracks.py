import cv2
import numpy as np
import sys
import math


def makeMatrix(v):
    cosv = math.cos(v[0])
    sinv = math.sin(v[0])
    tx = v[1]
    ty = v[2]

    return np.array([[cosv, -sinv, tx],
                     [sinv,  cosv, ty]])

rawvals = []
with open(sys.argv[1], "rt") as src:
    for line in src:
        gps = line.strip().split()
        if len(gps) == 3:
            rawvals.append(map(float, gps))

npts = len(rawvals)
x = 500
y = 500

maxx = 10000.0
maxy = 10000.0
cx = int(maxx / 2)
cy = int(maxy / 2)
destsize = 1000

destim = np.zeros((destsize, destsize, 3), np.uint8)

ptss = np.array([[0, 0, 1],
                 [0, y, 1],
                 [x, 0, 1],
                 [x, y, 1]]).T

tpts = [makeMatrix(v).dot(ptss) for v in rawvals]


def ipt(p):
    return (int(p[0]), int(p[1]))

for (idx, pts) in enumerate(tpts):
    # print(pts)
    offsets = np.tile(np.array([[cx], [cy]]), (1, pts.shape[1]))
    # print(offsets)
    dpts = (pts + offsets) * (destsize / maxx)
    # print(dpts)
    if idx % 20 == 0:
        cv2.line(destim, ipt(dpts[:, 0]), ipt(dpts[:, 1]), (255, 0, 0))
        cv2.line(destim, ipt(dpts[:, 0]), ipt(dpts[:, 2]), (255, 0, 0))
        cv2.line(destim, ipt(dpts[:, 1]), ipt(dpts[:, 3]), (255, 0, 0))
        cv2.line(destim, ipt(dpts[:, 2]), ipt(dpts[:, 3]), (255, 0, 0))

cv2.imshow("result", destim)
cv2.waitKey(0)
