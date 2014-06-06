import numpy as np
import pygray

def framestr_to_array(framestr):
    rows = framestr[0]
    cols = framestr[1]
    stride = framestr[2]
    datasize = framestr[3]
    color = False
    if rows*cols*3 == datasize:
        color = True
    elif rows*cols == datasize:
        color = False
    else:
        print("Image size mismatch: r[%d], c[%d], ds[%d], s[%d]" %
              (rows, cols, datasize, stride))
        return None
    rawdata = np.fromstring(framestr[4], dtype=np.uint8)
    if color:
        return np.reshape(rawdata, (rows, cols, 3))
    else:
        return np.reshape(rawdata, (rows, cols))
