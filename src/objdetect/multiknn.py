import numpy as np
import cv2
import math

class MultiKNN:
	def __init__(self, classdata, kfunc=None):
		""" 
		creates a MultiKNN classifier

		classdata should be a list of np.array, where each array
		corresponds to training samples for the given class
		"""
		self.classdata = classdata
		self.trainclasses()
		if kfunc:
			self.kfunc = kfunc
		else:
			self.kfunc = gaussian_kernel(1.0)

	def trainclasses(self):
		""" train the class knns """
		self.class_knns = [trainKNN(samps) for samps in self.classdata]

	def apply(self, testpts, k):
		"""
		apply the multiknn to a set of test points

		returns an array where each row corresponds to a testpt, with
		the row values being the 'probability' of each class
		(basically doing a kernel density estimate for each class
		and then taking the relative densities)
		"""
		resps = []
		for knn in self.class_knns:
			retv, res, neigh, dists = knn.find_nearest(testpts, k)
			ndists = np.array(dists, dtype=np.float32)
			sum_k_dists = np.sum(self.kfunc(ndists),1)
			resps.append(sum_k_dists)
		all_totals = np.vstack(resps).T
		row_sums = np.sum(all_totals,1)
		# row_sums is a 1d vector so can't be broadcast against all_totals
		# so the solution is to reshape row_sums into an nx1 2d array
		norm_totals = all_totals / row_sums.reshape(-1,1)
		return norm_totals



def gaussian_kernel(sigma):
	inv_s2 = 1.0 /  (sigma*sigma)
	def k(d):
		return np.exp(-1.0 * d * d * inv_s2) 
	return k

def trainKNN(samples):
	ret = cv2.KNearest()
    ret.train(samples, np.zeros(samples.shape[0], dtype=np.uint32))
    return ret