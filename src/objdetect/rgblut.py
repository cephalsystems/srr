import numpy as np


class RGBLUT:

    def __init__(self, f=None):
        """ 
        creates an RGB->mono per-pixel lookup table

        if a function is provided, encodes that function (see from_function)
        otherwise, generates a lut of all zeros
        """
        self.lut = np.zeros((2 ** 24), dtype=np.uint8)
        if f:
            self.from_function(f)

    def apply(self, src_image):
        """ 
        applies the lookup table to an image

        the input image should be a 3-channel uint8 image
        returns a mono image with the same dimensions
        """
        retim = np.take(self.lut, to24Bit(src_image))
        return retim

    def save(self, filename):
        """ saves the lut to a file """
        np.save(filename, self.lut)

    def load(self, filename):
        """ loads the lut from a file """
        self.lut = np.load(filename)

    def from_function(self, f):
        """ 
        generate the lut from a function f

        for efficiency, f should take a whole color image as its only
        argument and return a mono image of the same dimensions.
        (hint: this means vectorize f-- it's going to be doing a
        lot of work)
        """
        slice_size = 256 * 256
        for c0 in range(256):
            f_prime = f(colorSlice(c0))
            self.lut[c0 * slice_size:(c0 + 1) * slice_size] =
                f_prime.reshape(slice_size)


def colorSlice(c0):
    """ creates a 256x256 slice of the full 256x256x256 color cube """
    ret = np.zeros((256, 256, 3), dtype=np.uint8)
    c1, c2 = np.meshgrid(range(256), range(256))
    ret[:, :, 0] = c0
    ret[:, :, 1] = c1
    ret[:, :, 2] = c2
    return ret


def to24Bit(srcim):
    """ 
    packs a uint8 color image to uint32 mono (but only uses 24 bits) 

    useful mainly for turning color images to something suitable to
    run through a lookup table
    """
    res = np.zeros((srcim.shape[0], srcim.shape[1]), dtype=np.uint32)
    for i in range(2):
        res += srcim[:, :, i]
        res *= 256
    res += srcim[:, :, 2]
    return res
