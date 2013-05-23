from PyQt4.QtGui import QImage
import numpy as np
import colorconv
from scipy.misc import imresize
from matplotlib import cm

'''
A module to hold computations on images or sequences

TODO:
1-generare average roi
2-creare un immagine 8 bit di un frame con limiti
3-

'''

def convert16Bitto8Bit(img,vmin,vmax,returnQimage=False):
	#img[img<vmin]=vmin
	#img[img>vmax]=vmax
	
	img = img - vmin
	img = img * (255.0 / (vmax - vmin) )
	
	
	im2 = img.astype(np.uint8)
	if not returnQimage:
		return im2
	else:
		h,w = img.shape
		return QImage(im2.data,w,h,QImage.Format_Indexed8)
		
def HSVImage(image,background,vmin=None,vmax=None,hsvcutoff=0.45,returnQimage=False):
	'''
	Given a numpy image and background returns (classic) HSVImage
	'''

	bckgrn2=imresize(background,(image.shape[0],image.shape[1]))
	value = (bckgrn2-bckgrn2.min())/(bckgrn2.max()*1.0-bckgrn2.min()*1.0)

	d=image.copy() #Determine if image is passed by reference or by value
	if vmin == None:
		dmin = image.min()
		if dmin<0:
			dmin = 0
		
	else:
		dmin = vmin
	if vmax == None:		
		dmax = image.max()
	else:
		dmax = vmax
	
	d[d<dmin] = dmin
	d[d>dmax] = dmax
	hue =  1-((d*1.0 - dmin)/(dmax -  dmin)*(1-hsvcutoff)+hsvcutoff)
	saturation = np.ones(hue.shape)
	hsvMat = np.array([hue,saturation,value]).transpose(1,2,0)

	rgbMat = colorconv.convert_colorspace(hsvMat,'HSV','RGB')
	if not returnQimage:
		return rgbMat
	else:
		return rgbToQimage(rgbMat)
		
		
def applyColormap(image,vmin=None,vmax=None,returnQimage=False,cmap=cm.jet):
	#d=image.copy() #Determine if image is passed by reference or by value

	if vmin == None:
		dmin = image.min()
		if dmin<0:
			dmin = 0
		
	else:
		dmin = vmin
	if vmax == None:		
		dmax = image.max()
	else:
		dmax = vmax
	
	image[image<dmin] = dmin
	image[image>dmax] = dmax
	
	rgbMat =  cmap((image*1.0-dmin)/(dmax-dmin))*255

	if not returnQimage:
		return rgbMat
	else:
		return rgbToQimage(rgbMat)
		
		
def rgbToQimage(rgbMat):
	'''
	Convert an RGB image to a QImage (ignoring alpha channel if present)
	'''
	rgbMat=rgbMat.astype(np.uint32)
	rgbMat2 = (255 << 24 | rgbMat[:,:,0] << 16 | rgbMat[:,:,1] << 8 | rgbMat[:,:,2]).flatten() 
	h,w,col = rgbMat.shape
	return QImage(rgbMat2,w,h,QImage.Format_RGB32)
		

def mean_filter():
	pass

def gaussian_filter():
	pass

def applyRoiComputationOptions(rdata, fo, rois):
	
	nrois = len(rois)
	
	#print("processType is " + str(fo.processType))
	
	if fo.processType == 0:
		#print("firstFrame " + str(fo.firstFrame) + " firstWawvelength " + str(fo.firstWavelength))
		
		outData = rdata[fo.firstFrame-2 + fo.firstWavelength:fo.lastFrame:fo.cycleSize, 0:nrois]
		
		f0 = np.mean(outData[0:fo.referenceFrames])
		
		#print("outData " + str(outData))
		
		if fo.displayType == 1:
			outData = outData - f0
		elif fo.displayType == 2:
			outData = (outData - f0) / f0
	elif fo.processType == 1:
		
		fwFrames = np.arange(fo.firstFrame-2 + fo.firstWavelength, fo.lastFrame, fo.cycleSize)
		swFrames = np.arange(fo.firstFrame-2 + fo.secondWavelength, fo.lastFrame, fo.cycleSize)
		
		fwSize = len(fwFrames)
		swSize = len(swFrames)
		
		if fwSize != swSize:
			if fwSize > swSize:
				fwFrames = fwFrames[0:swSize]
			else:
				swFrames = swFrames[0:fwSize]
		
		outData = np.divide(rdata[fwFrames, 0:nrois], rdata[swFrames, 0:nrois])
		
		r0 = np.mean(outData[0:fo.referenceFrames])
		
		if fo.displayType == 1:
			outData = outData - r0
		elif fo.displayType == 2:
			outData = (outData - r0) / r0
	return outData

def singleWavelengthProcess(tiffSeq,frameNumber,fo,f0=None,returnQimage=True):
	
	if fo.displayType == 1 or fo.displayType==2:
		if f0 == None:
			f0Frames= tiffSeq.getFramesInterval(fo.firstFrame,fo.firstFrame+fo.referenceFrames*fo.cycleSize)
			f0 = f0Frames[:,:,0:-1:fo.cycleSize].mean(2)

	rawImg = tiffSeq.getFrame(frameNumber)
	#TODO:filter processing here.
	
	if fo.displayType == 1:
		rawImg = rawImg - f0
	elif fo.displayType == 2:
		rawImg = (rawImg -f0)/f0
		
	if fo.useLUT:
		return applyColormap(rawImg,vmin=None,vmax=None,returnQimage=returnQimage) #TODO: add the type of colormap here, vmin and vmax
	elif fo.useHSV:
		return HSVImage(rawImg,fo.HSVbackground,vmin=None,vmax=None,hsvcutoff=0.45,returnQimage=returnQimage)#TODO: add the background and hsvcutoff to processoptions, vmin and vmax
