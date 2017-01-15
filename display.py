import numpy as np
import scipy.misc as smp
import random

def display(pixelmat):
	img = smp.toimage( pixelmat )
	img.show()

if __name__ == "__main__":
	data = np.zeros( (512,512,3), dtype=np.uint8)

	for i in range(500):
		x = random.randrange(0,512)
		y = random.randrange(0,512)
		r = random.randrange(0,256)
		g = random.randrange(0,256)
		b = random.randrange(0,256)

		data[x,y] = [r,g,b]

	display(data)