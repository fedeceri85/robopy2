from PyQt4.QtGui import QImage
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
	if not returnQimage:
		return img.astype.uint8
	else:
		h,w = img.shape
		return QImage(img.data,w,h,QImage.Format_Indexed8)
		
