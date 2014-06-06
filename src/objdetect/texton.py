from filterbank import flatten_image_array
import numpy as np
import math
import cv2


def sample_rows(arr, n):
    """randomly sample n rows out of an array"""
    return np.random.permutation(arr)[0:n, :]


class Textonator:

    """ Computes per-pixel texton labels for an image """

    def __init__(self, filterbank, library=None):
        self.filterbank = filterbank
        if library:
            self.library = library
        else:
            self.library = None

    def generate_library(self, trainimages, libsize, sample_prop=1.0):
        """
        generates the texton library from a set of training images

        sample_prop is the proportion of pixels in each training image to use
        """
        samps = []  # gather all the samples into one big array
        for im in trainimages:
            filtered = flatten_image_array(self.filterbank.apply(im))
            nsamps = int(math.floor(float(filtered.shape[0]) * sample_prop))
            samps.append(sample_rows(filtered, nsamps))
        all_samples = np.vstack(samps)

        # generate library as k-means centers of samples
        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 1, 10)
        retval, bestLabels, centers = cv2.kmeans(all_samples,
                                                 libsize,
                                                 criteria,
                                                 10,
                                                 cv2.KMEANS_RANDOM_CENTERS)

        self.library = centers
        self.retrain_knn()

    def retrain_knn(self):
        """
        rebuilds internal knn classifier from library

        if you manually set the library, call this afterwards
        """
        self.knn_eng = cv2.KNearest()
        self.knn_eng.train(self.library,
                           np.arange(self.library.shape[0], dtype=np.uint32))

    def apply(self, img):
        """
        apply the texton library to an image

        returns a uint32 array of the per-pixel labels
        """
        orig_shape = img.shape
        filtered = flatten_image_array(self.filterbank.apply(im))
        retv, res, neigh, dists = self.knn_eng.find_nearest(filtered, 1)
        return np.array(res, dtype=np.uint32)

    def load_library(self, filename):
        self.library = np.load(filename)
        self.retrain_knn()

    def save_library(self, filename):
        np.save(filename, self.library)
