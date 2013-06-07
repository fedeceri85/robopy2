from PyQt4.QtGui import QImage, QColor
import numpy as np
import colorconv
from scipy.misc import imresize
from matplotlib import cm
from scipy.io import loadmat,savemat
from scipy import weave
import Roi
from scipy import weave
from scipy.weave import converters

'''
A module to hold computations on images or sequences

TODO:
1-generare average roi
2-creare un immagine 8 bit di un frame con limiti
3-

'''

def convert16Bitto8Bit(img,vmin,vmax,returnQimage=False):
	img[img<vmin]=vmin
	img[img>vmax]=vmax
	
	img = img - vmin
	img = img * (255.0 / (vmax - vmin) )
	
	
	im2 = img.astype(np.uint8)
	if not returnQimage:
		return im2
	else:
		h,w = img.shape
		return QImage(im2.data,w,h,QImage.Format_Indexed8)

def computeValue(background,shape=None):
	if shape is not None:
		bckgrn2=imresize(background,(shape[0],shape[1]))
	else:
		bckgrn2=background
	value = (bckgrn2-bckgrn2.min())/(bckgrn2.max()*1.0-bckgrn2.min()*1.0)
	return value

def HSVImage(image,value,vmin=None,vmax=None,hsvcutoff=0.45,returnQImage=False):
	'''
	Given a numpy image and background returns (classic) HSVImage
	'''


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
	
	np.clip(image,dmin,dmax,image)
	hue =  1-((image*1.0 - dmin)/(dmax -  dmin)*(1-hsvcutoff)+hsvcutoff)
	saturation = np.ones(hue.shape)
	hsvMat = np.array([hue,saturation,value]).transpose(1,2,0)

	rgbMat = colorconv.convert_colorspace(hsvMat,'HSV','RGB')
	if not returnQImage:
		return rgbMat
	else:
		return rgbToQimage(rgbMat*2**8)
		
		
def applyColormap(image,vmin=None,vmax=None,returnQImage=False,cmap=cm.jet):
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
	
	np.clip(image,dmin,dmax,image)

	if not returnQImage:
		rgbMat =  cmap((image*1.0-dmin)/(dmax-dmin))*255
		return rgbMat
	else:
		imMat = ((image*1.0-dmin)/(dmax-dmin) * 255).astype(np.int8)
		h,w = imMat.shape
		im = QImage(imMat, w,h, QImage.Format_Indexed8)
		im.setColorCount(256)
		
		cols = cmap(xrange(256))
		cols = (cols * 255).astype(np.long)
		colTable = list(cols[:,3] << 24 | cols[:,0] << 16 | cols[:,1] << 8 | cols[:,2])
		colTable = map(long, colTable)
			
		im.setColorTable(colTable)
			
		return im
		
		
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

def applyRoiComputationOptions(rdata, times, fo, rois):
	
	nrois = len(rois)
	
	#print("processType is " + str(fo.processType))
	
	if fo.processType == 0:
		#print("firstFrame " + str(fo.firstFrame) + " firstWawvelength " + str(fo.firstWavelength))
		
		outData = rdata[fo.firstFrame-2 + fo.firstWavelength:fo.lastFrame:fo.cycleSize, 0:nrois]
		times = times[fo.firstFrame-2 + fo.firstWavelength:fo.lastFrame:fo.cycleSize]
		
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
		
		times = times[fwFrames]
		outData = np.divide(rdata[fwFrames, 0:nrois], rdata[swFrames, 0:nrois])
		
		r0 = np.mean(outData[0:fo.referenceFrames])
		
		if fo.displayType == 1:
			outData = outData - r0
		elif fo.displayType == 2:
			outData = (outData - r0) / r0
	return outData, times

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

def computeReference(tiffSeq, fo):
	if fo.processType == 0:
		f0Frames = tiffSeq.getFramesInterval(fo.firstFrame,fo.firstFrame+fo.referenceFrames*fo.cycleSize)
		f0 = f0Frames[:,:,0::fo.cycleSize].mean(2)
	elif fo.processType == 1:
		f1Frame = tiffSeq.getFrame(fo.firstFrame + fo.firstWavelength - 1)
		f2Frame = tiffSeq.getFrame(fo.firstFrame + fo.secondWavelength - 1)
		f0 = np.divide(f1Frame, f2Frame)
	
	return f0.astype(np.float32)
	
def computeProcessedFrame(tif, n, fo, ref):
	f = None
	if fo.processType == 0:
		f = tif.getFrame(n + fo.firstWavelength - 1)
		f = f.astype(np.float32)
	elif fo.processType == 1:
		f1 = tif.getFrame(n + fo.firstWavelength - 1)
		f2 = tif.getFrame(n + fo.secondWavelength - 1)
		f1 = f1.astype(np.float32)
		f = np.divide(f1, f2)
	else:
		return None
		
	
	if fo.displayType == 0:
		f = f
	elif fo.displayType == 1:
		f = f-ref
	elif fo.displayType == 2:
		f = np.divide((f-ref), ref) 	
		
	return f
	
def computeProcessedFrameWeave(tif, n, fo, ref, b1 = 0, b2 = 0, wave2Threshold = 16):
	f1 = tif.getFrame(n + fo.firstWavelength - 1)
	f2 = None
	if f1 == None:
		return None
		
		
	if fo.processType == 0 and fo.displayType == 0:
		f1 = f1.astype(np.float32)
		return f1
		
	h = f1.shape[0]
	w = f1.shape[1]
	res = np.zeros(f1.shape, dtype=np.float32)
	
	if fo.processType == 1:
		f2 = tif.getFrame(n + fo.secondWavelength - 1)
	
	codes = list()
	vrs = ["f1", "f2", "w", "h", "ref", "res", "b1", "b2", "wave2Threshold"]
	
	code = """
		__m128i x1, x2, xzero, x1low, x1high, x2low, x2high, xb1, xb2, x2thresh;
		unsigned short *pf1 = (unsigned short *)f1;
		unsigned short *pf2 = (unsigned short *)f2;
		
		float *pref = ref, *pres = res;
		__m128	fl1Low, fl1High, fl2Low, fl2High, flrefLow, flrefHigh;
		unsigned cycles = w / 8;
		unsigned rmd = w % 8;
		
		xzero = _mm_setzero_si128();
		unsigned short usb1 = (unsigned short)b1;
		unsigned short usb2 = (unsigned short)b2;
		unsigned short usth2 = (unsigned short)wave2Threshold;
		xb1 = _mm_set_epi16(usb1, usb1, usb1, usb1, usb1, usb1, usb1, usb1);
		xb2 = _mm_set_epi16(usb2, usb2, usb2, usb2, usb2, usb2, usb2, usb2);
		x2thresh = _mm_set_epi16(usth2, usth2, usth2, usth2, usth2, usth2, usth2, usth2);
		
		for(unsigned i=0; i<h; i++){
			for(unsigned j=0; j<cycles; j++) {
				x1 = _mm_loadu_si128((__m128i *)pf1);
				pf1+=8;
				x1 = _mm_sub_epi16(x1, xb1);
				x1low = _mm_unpacklo_epi16(x1, xzero);
				flrefLow = _mm_loadu_ps(pref);
				pref+=4;
				fl1Low = _mm_cvtepi32_ps(x1low);
				
				x1high = _mm_unpackhi_epi16(x1, xzero);
				flrefHigh = _mm_loadu_ps(pref);
				pref+=4;
				fl1High = _mm_cvtepi32_ps(x1high);
				"""
				
	if fo.processType == 1:
		code = code + """
				x2 = _mm_loadu_si128((__m128i *)pf2);
				pf2+=8;
				x2 = _mm_sub_epi16(x2, xb2);
				x2 = _mm_max_epi16(x2, x2thresh);
				x2low = _mm_unpacklo_epi16(x2, xzero);
				fl2Low = _mm_cvtepi32_ps(x2low);
				fl1Low = _mm_div_ps(fl1Low, fl2Low);
				
				x2high = _mm_unpackhi_epi16(x2, xzero);
				fl2High = _mm_cvtepi32_ps(x2high);
				fl1High = _mm_div_ps(fl1High, fl2High);
		"""
		
	if fo.displayType == 1:
		code = code + """
				fl1High = _mm_sub_ps(fl1High, flrefHigh);
				fl1Low = _mm_sub_ps(fl1Low, flrefLow);
		"""
	
	if fo.displayType == 2:
		code = code + """
		fl1Low = _mm_div_ps(fl1Low, flrefLow);
		fl1High = _mm_div_ps(fl1High, flrefHigh);
		"""
				
	code = code + """
				_mm_storeu_ps(pres, fl1Low);
				pres += 4;
				_mm_storeu_ps(pres, fl1High);
				pres += 4;
			}
			
			for(unsigned j=0; j<rmd; j++) {
				*pres = (float)(*pf1 - b1) - *pref;"""
				
	if fo.displayType == 2:
		code = code + """
				*pres /= *pref;"""
				
	code = code + """
				++pres;
				++pref;
				++pf1;
			}
		}
	"""
	
	#print(code)
	
	weave.inline(code, vrs, headers = ['"emmintrin.h"'], extra_compile_args=["-mfpmath=sse -msse3"])
	
	return res
		

def loadRoisFromFile(filename, w, h):
	ROIS = loadmat(filename,struct_as_record=False, squeeze_me=True)['ROIS']
	#try to solve issue when rois is composed of just one roi
	try:
		len(ROIS)
	except TypeError:
		ROIS = [ROIS,]
		
	roboRois = []
	for roi in ROIS:
		r = Roi.Roi()
		c = roi.Coordinates
		
		isValidRoi = True
		
		for x,y in zip(c[0],c[1]):
			if w < x or x < 0 or h < y or y < 0:
				isValidRoi = False
			r.addPoint(x,y)
			
		if isValidRoi:
			r.computePointMap()
			roboRois.append(r)
		
	return roboRois

def saveRoisToFile(filename,rois):
	roilist=[]
	for roi in rois:
		color = np.array(roi.color.getRgb()[:3])
		x = []
		y = []
		for i in xrange(0, roi.size()):
			p = roi.point(i)
			x.append(p.x())
			y.append(p.y())
		coordinates=np.vstack((np.array(x),np.array(y)))
		
		roisdict={'Color': color, 'Coordinates':coordinates, 'LineType':u'-','Map':np.array([], dtype=np.float64),'Rectangular':0, 'h_MovieLine':0,'h_MovieTxt':0,'h_line':0,'h_text':0}
		
		roilist.append(roisdict)
		
	savemat(filename,{'ROIS':roilist})


def HSVtoRGB(arr):
	code = """
	#include <stdlib.h>
	#include <math.h>

	int rows = Narr[0];
	int cols = Narr[1];
	int depth = Narr[2];

	double chroma;
	double H1;
	double m;
	double x;
	npy_intp dims[3]  ={rows,cols,depth};
	PyObject* out_array = PyArray_SimpleNew(3, dims, NPY_DOUBLE);
	double* out = (double*) ((PyArrayObject*) out_array)->data;

	for (int i=0; i < rows; i++)
		{
			for (int j=0; j < cols; j++)
			{
				chroma = arr[(i*cols + j)*depth + 1]*arr[(i*cols + j)*depth + 2];
				H1 =  arr[(i*cols + j)*depth] * 6.0;
				m =  arr[(i*cols + j)*depth + 2] - chroma;
				x = chroma*(1 - abs((int(floor(H1))%2) -1) );
				
				if ((H1>=0) && (H1<1))
				{
					out[(i*cols + j)*depth + 0]=chroma+m;
					out[(i*cols + j)*depth + 1]=x+m;
					out[(i*cols + j)*depth + 2]=m;
				}
				if ((H1>=1) && (H1<2))
				{
					out[(i*cols + j)*depth + 0]=x+m;
					out[(i*cols + j)*depth + 1]=chroma+m;
					out[(i*cols + j)*depth + 2]=m;
				}				
				 if ((H1>=2) && (H1<3))
				{
					out[(i*cols + j)*depth + 0]=m;
					out[(i*cols + j)*depth + 1]=chroma+m;
					out[(i*cols + j)*depth + 2]=x+m;
				}
				 if ((H1>=3) && (H1<4))
				{
					out[(i*cols + j)*depth + 0]=m;
					out[(i*cols + j)*depth + 1]=x+m;
					out[(i*cols + j)*depth + 2]=chroma+m;
				}
				 if ((H1>=4) && (H1<5))
				{
					out[(i*cols + j)*depth + 0]=x+m;
					out[(i*cols + j)*depth + 1]=m;
					out[(i*cols + j)*depth + 2]=chroma+m;
				}
				 if ((H1>=5) && (H1<6))
				{
					out[(i*cols + j)*depth + 0]=chroma+m;
					out[(i*cols + j)*depth + 1]=m;
					out[(i*cols + j)*depth + 2]=x+m;
				}
			}

		}
	return_val = out_array;
	"""
	return weave.inline(code,['arr'])
