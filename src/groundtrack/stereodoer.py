class DenseStereoThing:
	def __init__(self, method, cropheight):
		if method == "FANCY":
			self.sm = cv2.StereoSGBM(0, 64, 7)
		else:
			self.sm = cv2.StereoBM(cv2.BASIC_PRESET)

		self.cropheight = cropheight

	def computeDisparityMap(self, im0, im1):
		im0p = im0
		im1p = im1
		if self.cropheight != None:
			srch = im0.cols
			srcw = im0.rows
			sy = int((im0.rows - self.cropheight) / 2)
			ey = sy + self.cropheight
			im0p = im0[sy:ey,:]
			im1p = im1[sy:ey,:]

		self.dm = self.sm.compute(im0p, im1p)
		return self.dm

class SparseStereoThing:
	def __init__(self, featmatcher):
		self.matcher = featmatcher

	def computeDisparityPairs(self, im0, im1):
		(m, k, d) = self.matcher.matchFeatures(im0, im1)
		ret = []
		for m in matches:
			p0 = k[0][m.queryIdx]
			p1 = k[1][m.trainIdx]
			ret.append((p0, p1, p0[0] - p1[0]))
		self.disparities = ret
		return ret