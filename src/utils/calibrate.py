#!/usr/bin/env python
# stolen from opencv:
# https://github.com/Itseez/opencv/blob/master/samples/python2/calibrate.py

import numpy as np
import cv2

# built-in modules
import os


USAGE = '''
USAGE: calib.py [--save <filename>] [--debug <output path>] [--square_size] [<image mask>]
'''



if __name__ == '__main__':
    import sys
    import getopt
    from glob import glob

    args, img_mask = getopt.getopt(sys.argv[1:], '', ['save=', 'debug=', 'square_size='])
    args = dict(args)
    try:
        img_mask = img_mask[0]
    except:
        img_mask = '../cpp/left*.jpg'

    img_names = glob(img_mask)
    print(img_names)
    debug_dir = args.get('--debug')
    square_size = float(args.get('--square_size', 1.0))

    pattern_size = (9, 6)
    pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 )
    pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size

    obj_points = []
    img_points = []
    h, w = 0, 0
    for fidx, fn in enumerate(img_names):
        print 'processing %s...' % fn,
        img = cv2.imread(fn, 0)
        if img is None:
          print "Failed to load", fn
          continue

        h, w = img.shape[:2]
        found, corners = cv2.findChessboardCorners(img, pattern_size)
        if found:
            term = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 )
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)
        if debug_dir:
            vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            cv2.drawChessboardCorners(vis, pattern_size, corners, found)
            dbfn = '%s/%d_chess.png' % (debug_dir, fidx)
            print("Saving debug... %s" % dbfn)
            cv2.imwrite(dbfn, vis)
        if not found:
            print 'chessboard not found'
            continue
        img_points.append(corners.reshape(-1, 2))
        obj_points.append(pattern_points)

        print 'ok'

    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)
    print "RMS:", rms
    print "camera matrix:\n", camera_matrix
    print "distortion coefficients: ", dist_coefs.ravel()
    cv2.destroyAllWindows()