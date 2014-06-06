import cv2
#import cv
import math
import numpy as np
import argparse
import sys

def findBloomedObjects(srcim, thresh, minrad):
	grayim = cv2.cvtColor(srcim, cv2.cv.CV_RGB2GRAY)
	return extractNodes(grayim, thresh, minrad)

def drawExtractedNodes(baseim, nodelist, drawcolor):
	for (x, y, rad) in nodelist:
		print("x: %f, y: %f, rad: %f" % (x,y,rad))
		cv2.circle(baseim, (int(x), int(y)), int(rad), drawcolor, 2)

def extractNodeCircles(grayim, colorThresh, radThresh, fillThresh):
	retval, binimg = cv2.threshold(grayim, colorThresh, 255, cv2.THRESH_BINARY)
	retbinimg = np.copy(binimg)
	contours, conthierarchy = cv2.findContours(binimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	ret = []
	print("Found %d contours" % len(contours))
	for pts in contours:
		center, rad = cv2.minEnclosingCircle(pts)
		momts = cv2.moments(pts)
		#print(momts)
		cmx = momts['m10'] / (momts['m00'] + 0.0001)
		cmy = momts['m01'] / (momts['m00'] + 0.0001)

		circarea = math.pi * rad * rad
		area = cv2.contourArea(pts)
		arclength = cv2.arcLength(pts, True)

		if rad >= radThresh and (area / circarea) > fillThresh:
			#ret.append((center[0], center[1], rad))
			ret.append((cmx, cmy, rad))
	return ret, retbinimg

if __name__ == '__main__':
	srcimg = cv2.imread(sys.argv[1])
	graythresh = int(sys.argv[2])
	radthresh = int(sys.argv[3])
	fillthresh = float(sys.argv[4])

	grayim = cv2.cvtColor(srcimg, cv2.cv.CV_RGB2GRAY)
	nodes, binimg = extractNodeCircles(grayim, graythresh, radthresh, fillthresh)
	tarimg = cv2.merge([binimg, binimg, binimg])
	drawExtractedNodes(tarimg, nodes, (255,255,0))
	cv2.imshow("nodes", tarimg)
	cv2.waitKey(0)
