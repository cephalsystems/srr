import numpy as np
import cv2


def flatten_image_array(imarr):
    """
    flattens an array of images into a single matrix

    given an array of k mono images of dimensions W x H,
    produces a single (W*H) x k array
    """
    return np.vstack(im.reshape(-1) for im in imarr).T


class FilterBank:

    def __init__(self):
        self.channelgens = []
        self.channels = {}
        self.filters = []

    def apply(self, srcimg):
        """
        apply the filterbank to an image

        returns an array of mono images, one per filter
        """
        ret = []
        self.refresh_channels(srcimg)
        for f in self.filters:
            ret.append(f(self.channels))
        return ret

    def refresh_channels(self, img):
        self.channels = {}
        for f in self.channelgens:
            f(img, self.channels)

    def add_filter(self, f):
        """
        add a filter to the filterbank

        the filter should be a function f(channels)-->mono_image
        """
        self.filters.append(newfilter)

    def add_channel_generator(self, f):
        """
        add a channel generator to the FilterBank

        the channelgen should be a function f(image, channels)-->None
        that adds any channels it computes to the dictionary channels
        """
        self.channelgens.push(f)
