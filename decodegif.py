import sys

def Main( filename ):
	try:
		image = []
		file = open(filename, 'rb')
		version = DecodeHead( file )
		screen = DecodeScreenDescriptor( file )

		for key, value in screen.items():
			print(key, "corresponds to ", value)

		if screen['globaltable'] == 1:
			gtablesize = 2**screen['gtablesize']
			gtable = CreateColorTable(gtablesize, file)

#		for i in gtable:
#			print(i)

		next = file.read(1)

		ImageDescriptor( file, screen, image, gtable )

	finally:
		file.close()

def DecodeImage( colortable, file, screen ):
	minsize = file.read(1)
	print("minimum size is: ", minsize)
	return 1

def ImageDescriptor(file, screen, image, gtable):
	leftpos   = file.read(2)
	toppos    = file.read(2)
	width     = file.read(2)
	height    = file.read(2)
	pckdfield = file.read(1)

	localtable = (pckdfield)        >> 7
	interlaced = (pckdfield & 0x40) >> 6
	sortedflag = (pckdfield & 0x20) >> 5
	reserved   = (pckdfield & 0x18) >> 3
	ltablesize = (pckdfield & 0x07)
	ltablesize = 2**(ltablesize+1)

	if localtable > 0:
		localcolor = CreateColorTable( ltablesize, file )
		print("1")
		imagechunk = DecodeImage( localcolor, file, screen )
	else:
		print("1")
		imagechunk = DecodeImage( gtable, file, screen )

def CreateColorTable(size, file):
	table = []
	while size > 0:
		size -= 1
		colors = file.read(3)
		table.append([colors[0],colors[1],colors[2]])

	return table

def DecodeScreenDescriptor( gif ):
	screen = {}
	width = gif.read(2)
	assert( width != 0x00 )
	#check if Block Terminator
	width = width[0]+width[1]*2**8
	height = gif.read(2)
	height = height[0]+height[1]*2**8

	packedfield = gif.read(1)
	gcolorflag =      (packedfield[0] & 0x80) >> 7
	colorresolution =((packedfield[0] & 0x70) >> 4) + 1
	sortflag =        (packedfield[0] & 0x08) >> 3
	gtablesize =      (packedfield[0] & 0x07)      + 1

	

	backgroundclridx   = gif.read(1)[0]
	aspectratio        = gif.read(1)[0]
	if aspectratio > 0:
		aspectratio = (aspectratio + 15) / 64

	screen['width']            = width
	screen['height']           = height
	screen['globaltable']      = gcolorflag
	screen['colorresolution']  = colorresolution
	screen['sortflag']         = sortflag
	screen['gtablesize']       = gtablesize
	screen['backgroundcolor']  = backgroundclridx
	screen['aspectratio']      = aspectratio

	return screen

def DecodeHead( gif ):
	signature = gif.read(3)
	print(signature)
	assert( signature == bytes([71,73,70]) )
	#check if 'GIF' in ascii]

	version = gif.read(3)
	versionstr = version
	print("version is:", versionstr)
	assert( version == bytes([56,57,97]) or version == bytes([56,55,97]) )
	#check if version is '87a' or '89a'

	return version
	#this is a real gif header
	#return the version


if __name__ == "__main__":
	args = sys.argv
	file = args[1]
	image = Main(file)
