import numpy as np
import scipy.misc as smp

data = np.zeros( (512, 512, 3), dtype=np.uint8)

data[254,254] = [254,0,0]
data[254,255] = [0,0,255]

img = smp.toimage( data )

img.show()

