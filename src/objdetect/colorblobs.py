import cv2
#import cv
import math
import numpy as np
import argparse
import sys
import logging

logger = logging.getLogger('vision')

def create_mask(srcim):
    grayim = cv2.cvtColor(srcim, cv2.cv.CV_RGB2GRAY)
    retval, binimg = cv2.threshold(grayim, 128, 1, cv2.THRESH_BINARY)
    return cv2.merge([binimg, binimg, binimg])

def apply_mask(srcim, mask):
    return srcim * mask

def findBloomedObjects(srcim, thresh, minrad):
    grayim = cv2.cvtColor(srcim, cv2.cv.CV_RGB2GRAY)
    return extractNodes(grayim, thresh, minrad)

def drawExtractedNodes(baseim, nodelist, drawcolor):
    for (x, y, rad) in nodelist:
        logger.debug("x: %f, y: %f, rad: %f" % (x,y,rad))
        cv2.circle(baseim, (int(x), int(y)), int(rad), drawcolor, 2)

def extractAllCircles(grayim, colorThresh):
    retval, binimg = cv2.threshold(grayim, colorThresh, 255, cv2.THRESH_BINARY)
    retbinimg = np.copy(binimg)
    contours, conthierarchy = cv2.findContours(binimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    ret = []
    logger.debug("Found %d contours" % len(contours))
    for pts in contours:
        center, rad = cv2.minEnclosingCircle(pts)
        momts = cv2.moments(pts)
        #print(momts)
        cmx = momts['m10'] / (momts['m00'] + 0.0001)
        cmy = momts['m01'] / (momts['m00'] + 0.0001)

        circarea = math.pi * rad * rad
        area = cv2.contourArea(pts)
        arclength = cv2.arcLength(pts, True)
        
        if rad > 1.0 and cmx > 0.0 and cmy > 0.0:        
            ret.append((cmx, cmy, rad, area, arclength))
    return ret, retbinimg

def extractNodeCircles(grayim, colorThresh, radThresh, fillThresh):
    retval, binimg = cv2.threshold(grayim, colorThresh, 255, cv2.THRESH_BINARY)
    retbinimg = np.copy(binimg)
    contours, conthierarchy = cv2.findContours(binimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    ret = []
    logger.debug("Found %d contours" % len(contours))
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

def do_bod_metric(srcimg, graythresh, minpsize, minsize, maxsize, fillthresh, sizetable):
    grayim = cv2.cvtColor(srcimg, cv2.cv.CV_RGB2GRAY)
    rawnodes, binimg = extractAllCircles(grayim, graythresh)
    nodes = []
    rejnodes = []
    mpos = sizetable.shape[0]
    print("Considering %d object possibilities..." % len(rawnodes))
    for cmx,cmy,rad,area,arclen in rawnodes:
        basepos = max(min(int(cmy),mpos-1),0)
        truesize = rad * sizetable[basepos]
        density = area / (rad*rad*math.pi)
        if rad > minpsize and truesize > minsize and truesize < maxsize and density > fillthresh:
            print("Added node.")
            print("xy: (%f,%f), Baserad: %f, truesize: %f" % (cmx, cmy, rad, truesize))
            nodes.append((cmx, cmy, rad))
        else:
            rejnodes.append((cmx, cmy, rad))
        
    tarimg = cv2.merge([binimg, binimg, binimg])
    drawExtractedNodes(tarimg, rejnodes, (0,0,255))
    drawExtractedNodes(tarimg, nodes, (255,255,0))
    return (nodes, tarimg)

def do_bloom_platform_detection(srcimg, graythresh, sizetable):
    grayim = cv2.cvtColor(srcimg, cv2.cv.CV_RGB2GRAY)
    rawnodes, binimg = extractAllCircles(grayim, graythresh)
    nodes = []
    mpos = sizetable.shape[0]
    print("Considering %d platform possibilities..." % len(rawnodes))
    for cmx,cmy,rad,area,arclen in rawnodes:
        basepos = max(min(int(cmy),mpos-1),0)
        truesize = rad * sizetable[basepos]
        density = area / (rad*rad*math.pi)
        #print("Baserad: %f, truesize: %f" % (rad, truesize))
        if truesize > 0.6 and truesize < 2.0 and density > 0.2:
            #print("Added node.")
            nodes.append((cmx, cmy, rad))
        
    tarimg = cv2.merge([binimg, binimg, binimg])
    drawExtractedNodes(tarimg, nodes, (255,255,0))
    return (nodes, tarimg)

def do_bloom_marker_detection(srcimg, graythresh, radthresh, fillthresh):
    grayim = cv2.cvtColor(srcimg, cv2.cv.CV_RGB2GRAY)
    nodes, binimg = extractNodeCircles(grayim, graythresh, radthresh, fillthresh)
    tarimg = cv2.merge([binimg, binimg, binimg])
    drawExtractedNodes(tarimg, nodes, (255,255,0))
    return (nodes, tarimg)
    

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
