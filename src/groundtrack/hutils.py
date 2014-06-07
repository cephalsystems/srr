import numpy as np
import numpy.linalg
import cv2

def decomposeHomography(H, pts0, pts1):
	(u,s,v) = numpy.linalg.svd(H)
	