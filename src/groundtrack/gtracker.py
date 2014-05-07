import cv2
import numpy as np
from operator import attrgetter
import sys
import drawmatch
import math

class RigidImageAligner:
	def __init__(self):
		# nothing to do
		pass

	def alignImages(self, im0, im1):
		A0 = np.identity(3, dtype=np.float64)
		A = cv2.findTransformECC(im0, im1, A0, cv2.MOTION_EUCLIDEAN)
		return A

class BasicMatcher:
	def __init__(self):
		# use brute-force matcher for now
		self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

	def matchFeatures(self, im0, im1):
		# find keypoints and features
		kp1, des1 = self.feat.detectAndCompute(im0,None)
		kp2, des2 = self.feat.detectAndCompute(im1,None)
		self.keypoints = [kp1, kp2]
		self.descriptors = [des1, des2]

		# Match descriptors.
		matches = self.matcher.match(des1,des2)

		# Sort them in the order of their distance.
		self.matches = sorted(matches, key = attrgetter("distance"))
		return (self.matches, self.keypoints, self.descriptors)

class ORBMatcher(BasicMatcher):
	def __init__(self):
		BasicMatcher.__init__(self)
		self.feat = cv2.ORB()

class BRISKMatcher(BasicMatcher):
	def __init__(self):
		BasicMatcher.__init__(self)
		self.feat = cv2.BRISK()

class AffinePoseEstimator:
	def __init__(self, fullaffine=False):
		self.fullaffine = fullaffine

	def estimatePose(self, pts0, pts1):
		return cv2.estimateRigidTransform(pts0, pts1, self.fullaffine)

	def composeTransformations(self, t0, t1):
		return t0.dot(t1)

def rigid2dToRT(A):
	# on the assumption that A is a true rigid transformation,
	# A = 	[ R_0 R_1 t_x]
	#		[-R_1 R_0 t_y]
	# then the rotation matrix R = [ cos_theta -sin_theta]
	#							   [ sin_theta  cos_theta]
	# so theta = arccos(R_0)
	tx = A[0,2]
	ty = A[1,2]
	theta = math.acos(A[0,0])
	return (theta, (tx, ty))

class GroundTracker:
	def __init__(self, featMatcher, poseEstimator, imageAligner):
		self.images = [None, None]
		self.featMatcher = featMatcher
		self.poseEstimator = poseEstimator
		self.imageAligner = imageAligner
		self.matches = None

	def setImages(self, im0, im1):
		self.images[0] = im0
		self.images[1] = im1

	def pushFrame(self, im):
		self.images[0] = self.images[1]
		self.images[1] = im
		self.processImageMatching()

	def processImageMatching(self):
		if self.featMatcher:
			(m, k, d) = self.featMatcher.matchFeatures(	self.images[0],
														self.images[1])
			self.matches 	 = m
			self.keypoints   = k
			self.descriptors = d
		if self.imageAligner:
			self.tf = self.imageAligner.alignImages( self.images[0], self.images[1])


	def drawMatchedFeatures(self):
		return cv2.drawMatches( self.images[0], self.keypoints[0],
								self.images[1], self.keypoints[1],
								self.matches, flags=2)

	def exploreMatches(self):
		p1, p2, kp_pairs = drawmatch.filter_matches(self.keypoints[0], 
										  self.keypoints[1],
										  self.matches)
		drawmatch.explore_match('orb_matches', self.images[0], self.images[1], kp_pairs)
		cv2.waitKey(0)

if __name__ == '__main__':
	# demo the matching by showing features between argv[1] and argv[2]
	print("Matching between %s --> %s" % (sys.argv[1], sys.argv[2]))
	im0 = cv2.imread(sys.argv[1], 0) # the 0 flag indicates load as grayscale
	im1 = cv2.imread(sys.argv[2], 0)

	tracker = GroundTracker(ORBMatcher(), None, None)
	tracker.setImages(im0, im1)
	tracker.processImageMatching()
	tracker.exploreMatches()

