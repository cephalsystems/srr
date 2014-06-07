import numpy as np
import cv2
import sys

def to24Bit(srcim):
	res = np.zeros((srcim.shape[0], srcim.shape[1]), dtype=np.uint32)
	#res = res + srcim[:,:,0] + srcim[:,:,1]*256 + srcim[:,:,2]*256*256
	res += srcim[:,:,0]
	res *= 256
	res += srcim[:,:,1]
	res *= 256
	res += srcim[:,:,2]
	return res

def buildFakeLUT():
	res = np.zeros((2**24), dtype=np.uint8)
	p = 0
	for r in range(256):
		for g in range(256):
			for b in range(256):
				res[p] = max(r,g,b)
				p += 1
	return res

if __name__ == '__main__':
	srcim = cv2.imread(sys.argv[1])
	print("Building LUT")
	#lut = np.arange(2**24)
	#lut = np.random.randint(256, size=(2**24, 1, 3))
	lut = buildFakeLUT()
	print("LUT built")
	retim = np.take(lut, to24Bit(srcim))
	print("Resulting shape:")
	print(retim.shape)
	cv2.imshow("res", retim)
	cv2.waitKey(0)