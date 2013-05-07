from PyQt4.QtGui import QImage
import numpy
'''
A module to hold 

TODO:
1-generare average roi
2-creare un immagine 8 bit di un frame con limiti
3-

'''

def convert16Bitto8Bit(img,vmin,vmax,returnQimage=False):
	img[img<vmin]=vmin
	img[img>vmax]=vmax
	
	im = img - vmin
	im = numpy.dot(im, 255.0 / (vmax - vmin) )
	
	
	im2 = im.astype(numpy.uint8)
	if not returnQimage:
		return im2
	else:
		h,w = img.shape
		return QImage(im2.data,w,h,QImage.Format_Indexed8)
		
