from PyQt4.QtGui import QImage, QColor
import os
import numpy as np
import colorconv
from scipy.misc import imresize
from matplotlib import cm
from scipy.io import loadmat,savemat
from scipy import weave, misc, ndimage
import Roi
from scipy import weave
from scipy.weave import converters
import threading
#import pyopencl as cl

'''
A module to hold computations on images or sequences

TODO:
1-generare average roi
2-creare un immagine 8 bit di un frame con limiti
3-

'''



def CreateOpenClContext():
	platforms = cl.get_platforms()
	if len(platforms) == 0:
		print "Failed to find any OpenCL platforms."
		return None
	devices = platforms[0].get_devices(cl.device_type.GPU)
	
	if len(devices) == 0:
		print "Could not find GPU device, trying CPU..."
		devices = platforms[0].get_devices(cl.device_type.CPU)
		
		if len(devices) == 0:
			print "Could not find OpenCL GPU or CPU device."
			return None, None
			
	context = cl.Context([devices[0]])
	return context, devices[0]

#openClCtx = cl.create_some_context(interactive=False, answers='1')
#openClCtx, openClDevice = CreateOpenClContext()
#openClQueue = cl.CommandQueue(openClCtx, openClDevice)
#openClmf = cl.mem_flags

class ThreadWorker(threading.Thread):
	def __init__(self, myCallback, data):
		self.myCallback = myCallback
		self.data = data
		self.result = None
		threading.Thread.__init__(self)
		
	def getResult(self):
		return self.results
		
	def run(self):
		self.result = self.myCallback(*self.data)

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
	if shape is not None and shape != background.shape:
		bckgrn2=imresize(background,(shape[0],shape[1]))
	else:
		bckgrn2=background.copy()
	value = (bckgrn2-bckgrn2.min())/(bckgrn2.max()*1.0-bckgrn2.min()*1.0)
	return value.astype(np.float32)

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
		
def HSVImageByMap(image,value, mp, vmin=None,vmax=None,hsvcutoff=0.45,returnQImage=False):
	'''
	Given a numpy image and background returns (classic) HSVImage using a map
	'''

	#d=image.copy() #Determine if image is passed by reference or by value
	if vmin == None:
		dmin = image.min()
	else:
		dmin = vmin
		
	if vmax == None:		
		dmax = image.max()
	else:
		dmax = vmax
	
	np.clip(image,dmin,dmax,image)
	#hue =  1-((image*1.0 - dmin)/(dmax -  dmin)*(1-hsvcutoff)) + hsvcutoff)
	hue =  (1.0 - (((image- dmin)/(dmax -  dmin)) * (1-hsvcutoff))) + hsvcutoff
	h,w = hue.shape
	hue = hue * 65535.0
	hue = hue.astype(np.uint16)
	value = value * 255.0
	value = value.astype(np.uint16)
	
	rgbMat = mp[value + hue]
	
	
	if not returnQImage:
		return rgbMat
	else:
		return QImage(rgbMat,w,h,QImage.Format_ARGB32)
		
def HSVImageByMapSSE(image,value, mp, vmin=None,vmax=None,hsvcutoff=0.45,returnQImage=False):
	'''
	Given a numpy image and background returns (classic) HSVImage using a map
	'''

	#d=image.copy() #Determine if image is passed by reference or by value
	if vmin == None:
		dmin = image.min()
	else:
		dmin = vmin
		
	if vmax == None:		
		dmax = image.max()
	else:
		dmax = vmax
		
	h,w = image.shape
	
	h = int(h)
	w = int(w)
	
	rgbMat = np.zeros((h,w), dtype = np.uint32)
		
	vrs = ["image", "value", "mp", "rgbMat", "w", "h", "dmin", "dmax", "hsvcutoff"]
	
	code = """
		__m128 im, v, xcutoff, notcutoff, oneps, xmin, xmax, xrange, x255, x256;
		__m128i imInt, vInt;
		float *pimage = (float *)image;
		float *pv = (float *)value;
		unsigned int *pmp = (unsigned int*)mp;
		unsigned int *pres = (unsigned int *)rgbMat;
		
		unsigned els = w*h;
		unsigned cycles = els / 4;
		unsigned remainder = els % 4;
		
		unsigned hIdx[4], vIdx[4];
		
		xcutoff = _mm_set1_ps(hsvcutoff);
		oneps = _mm_set1_ps(1.0);
		notcutoff = _mm_sub_ps(oneps, xcutoff);
		xmin = _mm_set1_ps(dmin);
		xmax = _mm_set1_ps(dmax);
		xrange = _mm_sub_ps(xmax, xmin);
		xrange = _mm_max_ps(xrange, _mm_set1_ps(0.01));
		
		x255 = _mm_set1_ps(255.0);
		x256 = _mm_set1_ps(256.0);
		
		for(unsigned int i=0; i<cycles; i++) {
			im = _mm_loadu_ps(pimage);
			pimage += 4;
			v = _mm_loadu_ps(pv);
			pv += 4;
			
			im = _mm_max_ps(im, xmin);
			im = _mm_min_ps(im, xmax);
			
			im = _mm_sub_ps(im, xmin);
			im = _mm_div_ps(im, xrange);
			
			
			v = _mm_mul_ps(v, x255);
			v = _mm_mul_ps(v, x256);
			vInt = _mm_cvttps_epi32(v);
			_mm_storeu_si128((__m128i *)vIdx, vInt);
			
			im = _mm_mul_ps(im, notcutoff);
			
			im = _mm_add_ps(im, xcutoff); //hue
			im = _mm_sub_ps(oneps, im);
			
			im = _mm_mul_ps(im, x255);
			imInt = _mm_cvttps_epi32(im);
			
			_mm_storeu_si128((__m128i *)hIdx, imInt);
			
			*pres++ = pmp[hIdx[0] + vIdx[0]];
			*pres++ = pmp[hIdx[1] + vIdx[1]];
			*pres++ = pmp[hIdx[2] + vIdx[2]];
			*pres++ = pmp[hIdx[3] + vIdx[3]];
		}
		
		for(unsigned int i=0; i<remainder; i++) {
			float h = (1.0 - ((*pimage++ - dmin) / (dmax-dmin) * (1-hsvcutoff))) + hsvcutoff;
			h *= 255*256;
			*pres++ = pmp[(unsigned)h + (unsigned)(*pv++)];
		}
		
		"""
	
	
	weave.inline(code, vrs, headers = ['"emmintrin.h"'], extra_compile_args=["-mfpmath=sse -msse3"], compiler="gcc")
	
	if not returnQImage:
		return rgbMat
	else:
		return QImage(rgbMat,w,h,QImage.Format_ARGB32)
		
def applyColormapGLSL(procWdg, image, w, h, imMin, imMax, returnType = "texture"):
	
	f = procWdg.applyColormapGLSL(image, w, h, imMin, imMax, returnType)	
	
	return f
	
def HSVImageGLSL(procWdg, image,value, w, h, imMin, imMax, vmin=0.0, vmax=1.0, hsvcutoff=0.45, returnType = "texture"):
		
	f = procWdg.HSVImageGLSL(image, value, w, h, imMin, imMax, vmin, vmax, hsvcutoff, returnType)
	
	return f
		
def medianFilter3x3(im):
	
	h,w = im.shape
	vrs = ["im", "im2", "h", "w"]
	
	im2 = np.zeros_like(im)
	
	code = """
		for(unsigned i=0; i<h-2; i++) {
			float *p1 = im + i*w;
			float *p2 = p1 + w;
			float *p3 = p2 + w;
			
			float *res = im2 + (i+1)*w;
			
			float a[9];
			
			float *pstop = p1 + w - 2;
			do {
				a[0] = *p1++;
				a[1] = *p1++;
				a[2] = *p1--;
				a[3] = *p2++;
				a[4] = *p2++;
				a[5] = *p2--;
				a[6] = *p3++;
				a[7] = *p3++;
				a[8] = *p3--;
				
				for(unsigned k=0; k < 5; k++) {
					unsigned minIndex = k;
					float minValue = a[k];
					for(unsigned l = k+1; l<9; l++) {
						if(a[l] < minValue) {
							minIndex = l;
							minValue = a[l];
						}
					}
					
					float t = a[k];
					a[k] = a[minIndex];
					a[minIndex] = t;
				}
				
				*res++ = a[4];
				
			} while (p1 < pstop);
		}
	"""
	
	weave.inline(code, vrs, headers = ['"emmintrin.h"'], extra_compile_args=["-mfpmath=sse -msse3"], compiler="gcc")
	
	return im2
	
def medianFilterOpenCl(im):
	h,w = im.shape
	
	out = np.empty_like(im)
	
	im_buf = cl.Buffer(openClCtx, openClmf.READ_ONLY | openClmf.COPY_HOST_PTR, hostbuf=im)
	out_buf = cl.Buffer(openClCtx, openClmf.WRITE_ONLY, out.nbytes)
	prgMedian = cl.Program(openClCtx, """
		__kernel void procMedian(__global const float* f, __global float *out, const int w, const int h) {
			int col = get_global_id(0);
			int row = get_global_id(1);
			int id = w * row + col;
			
			if((row < 1 || row > h-2) || (col < 1 || col > w-2)) {
				out[id] = f[id];
			} else {
				float a[9];
				
				int sid = w * (row - 1) + col - 1;
				
				a[0] = f[sid++];
				a[1] = f[sid++];
				a[2] = f[sid];
				sid += w - 2;
				a[3] = f[sid++];
				a[4] = f[sid++];
				a[5] = f[sid];
				sid += w - 2;
				a[6] = f[sid++];
				a[7] = f[sid++];
				a[8] = f[sid];
				
				for(unsigned k=0; k < 5; k++) {
					unsigned minIndex = k;
					float minValue = a[k];
					for(unsigned l = k+1; l<9; l++) {
						if(a[l] < minValue) {
							minIndex = l;
							minValue = a[l];
						}
					}
					
					float t = a[k];
					a[k] = a[minIndex];
					a[minIndex] = t;
				}
				
				out[id] = a[4];
			}
		}
		""").build()
	event = prgMedian.procMedian(openClQueue, (w,h), None, im_buf, out_buf, np.int32(w), np.int32(h))
	event.wait()
	cl.enqueue_copy(openClQueue, out, out_buf)
	return out
	
def gaussianFilterOpenCl(im):
	h,w = im.shape
	
	out = np.empty_like(im)
	
	im_buf = cl.Buffer(openClCtx, openClmf.READ_ONLY | openClmf.COPY_HOST_PTR, hostbuf=im)
	out_buf = cl.Buffer(openClCtx, openClmf.WRITE_ONLY, out.nbytes)
	prgGaussian = cl.Program(openClCtx, """
		__kernel void procGaussian(__global const float* f, __global float *out, const int w, const int h) {
			int col = get_global_id(0);
			int row = get_global_id(1);
			int id = w * row + col;
			
			if((row < 2 || row > h-3) || (col < 2 || col > w-3)) {
				out[id] = f[id];
			} else {
			
				int sid = w * (row - 2) + col - 2;
				out[id] = 0.0;
				
				const float g[25] = {0.000000069624782, 0.000028088641754 ,  0.000207548549665,   0.000028088641754, 0.000000069624782, 
					0.000028088641754  , 0.011331766853774 ,  0.083731060982536 ,  0.011331766853774, 0.000028088641754, 
					0.000207548549665 ,  0.083731060982536  , 0.618693506822940 ,  0.083731060982536, 0.000207548549665, 
					0.000028088641754  , 0.011331766853774 ,  0.083731060982536 ,  0.011331766853774, 0.000028088641754,
					0.000000069624782, 0.000028088641754 ,  0.000207548549665,   0.000028088641754, 0.000000069624782 
				};
				
				for(unsigned i=0; i<25; i++) {
					out[id] += g[i] * f[sid + w*(i/5) + (i%5)];
				}
			}
		}
		""").build()
	event = prgGaussian.procGaussian(openClQueue, (w,h), None, im_buf, out_buf, np.int32(w), np.int32(h))
	event.wait()
	cl.enqueue_copy(openClQueue, out, out_buf)
	return out
	
def medianFilterScipy(im, thrds = 2):
	h,w = im.shape
	
	if thrds == 1:
		im = ndimage.median_filter(im, (3,3))
		return im.astype(np.float32)
	
	pieceSize = int(w / thrds)
	
	lowLim = range(0, w, pieceSize)
	highLim = range(pieceSize, w, pieceSize)
	
	if len(lowLim) > len(highLim):
		highLim.append(w)
	
	threadList = list()
	for ll, hl in zip(lowLim, highLim):
		th = ThreadWorker(medianFilterScipyTile, (im,ll,hl))
		th.start()
		threadList.append(th)
		
	for th in threadList:
		th.join()
		im[:, th.data[1]:th.data[2]] = th.result
		
	return im.astype(np.float32)
	
def medianFilterScipyTile(im, ll, hl):
	return ndimage.median_filter(im[:, ll:hl], (3,3))
		
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
		

def median_filter(im):
	ndimage.median_filter(im,3,output=im)

def gaussian_filter(im):
	ndimage.gaussian_filter(im,3,output=im)

def applyRoiComputationOptions(rdata, times, fo, rois):
	
	nrois = len(rois)
	
	#print("processType is " + str(fo.processType))
	
	if fo.processType == 0:
		#print("firstFrame " + str(fo.firstFrame) + " firstWawvelength " + str(fo.firstWavelength))
		
		outData = rdata[fo.firstFrame-2 + fo.firstWavelength:fo.lastFrame:fo.cycleSize, 0:nrois]
		times = times[fo.firstFrame-2 + fo.firstWavelength:fo.lastFrame:fo.cycleSize]
		
		f0 = outData[0:fo.referenceFrames,:].mean(0)
		
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
	
def computeProcessedFrame(tif, n, fo,do, ref):
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
	if do.medianFilterOn:
		f=medianFilterScipy(f)
	if do.gaussianFilterOn:
		ndimage.gaussian_filter(f,3,output=f)
		
	return f
	
def computeProcessedFrameOpenCL2(tif, n, fo, ref, medFiltOn = True, gaussFiltOn = True):
	f1 = tif.getFrame(n + fo.firstWavelength - 1)
	
	h,w = f1.shape
	pType = np.int32(fo.processType)
	dType = np.int32(fo.displayType)
	
	if pType == 0:
		f2 = f1.copy()
	else:
		f2 = tif.getFrame(n + fo.secondWavelength - 1)
		
	
	f1_buf = cl.Buffer(openClCtx, openClmf.READ_ONLY | openClmf.COPY_HOST_PTR, hostbuf=f1)
	f2_buf = cl.Buffer(openClCtx, openClmf.READ_ONLY | openClmf.COPY_HOST_PTR, hostbuf=f2)
	ref_buf = cl.Buffer(openClCtx, openClmf.READ_ONLY | openClmf.COPY_HOST_PTR, hostbuf=ref)
	
	out = np.empty_like(f1, dtype=np.float32)
	out_buf = cl.Buffer(openClCtx, openClmf.READ_WRITE, out.nbytes)
	out_buf2 = cl.Buffer(openClCtx, openClmf.READ_WRITE, out.nbytes)
	
	buffSwap = 0
	
	prgCompute = cl.Program(openClCtx, """
			__kernel void procCompute(__global const unsigned short* f1, __global const unsigned short* f2, 
				__global const float* ref, __global float* out, const int w, const int h, 
				const int pType, const int dType) {
				
				int col = get_global_id(0);
				int row = get_global_id(1);
				int id = w * row + col;
				
				float v1 = (float)f1[id];
				float v2 = v1;
				if (pType == 1) {
					v2 = (float)f2[id];
					if( v2 < 1.0) {
						v2 = 1.0;
					}
					
					v1 /= v2;
				}
				
				float r = 0.0f;
				
				if( dType >  0) {
					r = ref[id];
					v1 -= r;
				} 
				
				if(dType == 2) {
					if (r == 0.0f) {
						if (r < 0.0f) {
							r = -0.001f;
						} else {
							r = 0.001f;
						}
					}
					
					v1 /= r;
				}
				
				out[id] = v1;
				
			}
		""").build()
		
	event = prgCompute.procCompute(openClQueue, (w,h), None, f1_buf, f2_buf, ref_buf, out_buf, np.int32(w), np.int32(h), pType, dType)
	event.wait()
	
	prgMedian = cl.Program(openClCtx, """
		__kernel void procMedian(__global const float* f, __global float *out, const int w, const int h) {
			int col = get_global_id(0);
			int row = get_global_id(1);
			int id = w * row + col;
			
			if((row < 1 || row > h-2) || (col < 1 || col > w-2)) {
				out[id] = f[id];
			} else {
				float a[9];
				
				int sid = w * (row - 1) + col - 1;
				
				a[0] = f[sid++];
				a[1] = f[sid++];
				a[2] = f[sid];
				sid += w - 2;
				a[3] = f[sid++];
				a[4] = f[sid++];
				a[5] = f[sid];
				sid += w - 2;
				a[6] = f[sid++];
				a[7] = f[sid++];
				a[8] = f[sid];
				
				for(unsigned k=0; k < 5; k++) {
					unsigned minIndex = k;
					float minValue = a[k];
					for(unsigned l = k+1; l<9; l++) {
						if(a[l] < minValue) {
							minIndex = l;
							minValue = a[l];
						}
					}
					
					float t = a[k];
					a[k] = a[minIndex];
					a[minIndex] = t;
				}
				
				out[id] = a[4];
			}
		}
		""").build()
		
	prgGaussian = cl.Program(openClCtx, """
		__kernel void procGaussian(__global const float* f, __global float *out, const int w, const int h) {
			int col = get_global_id(0);
			int row = get_global_id(1);
			int id = w * row + col;
			
			if((row < 2 || row > h-3) || (col < 2 || col > w-3)) {
				out[id] = f[id];
			} else {
			
				int sid = w * (row - 2) + col - 2;
				out[id] = 0.0;
				
				const float g[25] = {0.000000069624782, 0.000028088641754 ,  0.000207548549665,   0.000028088641754, 0.000000069624782, 
					0.000028088641754  , 0.011331766853774 ,  0.083731060982536 ,  0.011331766853774, 0.000028088641754, 
					0.000207548549665 ,  0.083731060982536  , 0.618693506822940 ,  0.083731060982536, 0.000207548549665, 
					0.000028088641754  , 0.011331766853774 ,  0.083731060982536 ,  0.011331766853774, 0.000028088641754,
					0.000000069624782, 0.000028088641754 ,  0.000207548549665,   0.000028088641754, 0.000000069624782 
				};
				
				for(unsigned i=0; i<25; i++) {
					out[id] += g[i] * f[sid + w*(i/5) + (i%5)];
				}
			}
		}
		""").build()
		
	if medFiltOn:
		event = prgMedian.procMedian(openClQueue, (w,h), None, out_buf, out_buf2, np.int32(w), np.int32(h))
		event.wait()
		
		buffSwap = 1
		
	if gaussFiltOn:
		
		if buffSwap == 0:
			source_buf = out_buf
			result_buf = out_buf2
		else:
			source_buf = out_buf2
			result_buf = out_buf
			
		buffSwap = buffSwap + 1
		
		event = prgGaussian.procGaussian(openClQueue, (w,h), None, source_buf, result_buf, np.int32(w), np.int32(h))
		event.wait()
		
		
	if buffSwap == 1:
		result_buf = out_buf2
	else:
		result_buf = out_buf
	
	cl.enqueue_copy(openClQueue, out, result_buf)
		
	return out
	
def computeProcessedFrameOpenCL(tif, n, fo, ref):
	f = tif.getFrame(n + fo.firstWavelength - 1).astype(np.float32)
	
	if fo.processType == 0 and fo.displayType == 0:
		return f
		
	h,w = f.shape
	
	
	#ctx = cl.create_some_context()
	#queue = cl.CommandQueue(ctx)
	
	#mf = cl.mem_flags
	
	pType = np.int32(fo.processType)
	dType = np.int32(fo.displayType)
	
	f2 = None
	
	f_buf = cl.Buffer(openClCtx, openClmf.READ_WRITE | openClmf.COPY_HOST_PTR, hostbuf=f)
	ref_buf = cl.Buffer(openClCtx, openClmf.READ_ONLY | openClmf.COPY_HOST_PTR, hostbuf=ref)
	
	#res = np.empty_like(f)
	#res_buf = cl.Buffer(ctx, mf.WRITE_ONLY, res.nbytes)
	
	#print("Opencl in action")
	
	if pType == 0:
		prgRef = cl.Program(openClCtx, """
		__kernel void procRef(__global float* f, __global const float* ref, const int dType, const int w) {
			int col = get_global_id(0);
			int row = get_global_id(1);
			int id = w * row + col;
			//res[id] = f[id];
			if(dType != 0) {
				f[id] = f[id] - ref[id];
			}
			
			if(dType == 2) {
				f[id] = f[id] / ref[id];
			}
		}
		""").build()
		event = prgRef.procRef(openClQueue, (w,h), None, f_buf, ref_buf, dType, np.int32(w))
	if pType == 1:
		f2 = tif.getFrame(n + fo.secondWavelength - 1).astype(np.float32)
		f2_buf = cl.Buffer(openClCtx, openClmf.READ_ONLY | openClmf.COPY_HOST_PTR, hostbuf=f2)
		
		prgDiv = cl.Program(openClCtx, """
			__kernel void procDiv(__global float* f, __global const float* f2, __global const float *ref, const int w, const int dType) {
				int col = get_global_id(0);
				int row = get_global_id(1);
				int id = w * row + col;
				f[id] = f[id] / f2[id];
				
				if(dType != 0) {
					f[id] = f[id] - ref[id];
				}
				
				if(dType == 2) {
					f[id] = f[id] / ref[id];
				}
			}
		""").build()
		event = prgDiv.procDiv(openClQueue, (w,h), None, f_buf, f2_buf, ref_buf, np.int32(w), dType)
	
	
	event.wait()
	cl.enqueue_copy(openClQueue, f, f_buf)
	return f
	
	
def computeProcessedFrameGLSL(procWdg, tif, n, fo, do, ref, b1=0, b2=0, returnType="float"):
		
		f1 = tif.getFrame(n + fo.firstWavelength - 1)
		f2 = f1
		if f1 == None:
			return None
			
		if fo.processType == 0 and fo.displayType == 0 and do.medianFilterOn == False and do.gaussianFilterOn == False:
			f1 = f1.astype(np.float32)
			return f1
			
		h = f1.shape[0]
		w = f1.shape[1]
		
		if fo.processType == 1:
			f2 = tif.getFrame(n + fo.secondWavelength - 1)
			
		#print("f1[0][0] " + str(f1[0][0]) + " ref[0][0] " + str(ref[0][0]))
			
		#preparing arguments for processing
		buffers = list([f1, f2, ref])
		bufferType = list(['uint16', 'uint16', 'float'])
		
		argList = list([list([fo.processType, fo.displayType, b1, b2])])
		
		programs = list([4])
		if do.medianFilterOn:
			programs.append(1)
			argList.append(list())
		if do.gaussianFilterOn:
			programs.append(2)
			argList.append(list())
			
		f = procWdg.processData(buffers, programs, argList, returnType, bufferType)
		
		if returnType == "texture":
			return f
			
		#print("f[0][0] " + str(f[0][0]))
		
		f = f.squeeze()
		h,w = f.shape
		f = f.reshape(w,h)
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
		x2thresh = _mm_set_epi16(usth2, usth2, usth2, usth2, usth2, usth2, usth2, usth2); """
		
	if fo.processType == 1:
		code = code + """
		unsigned short *pf2 = (unsigned short *)f2;
		"""
	
	code = code + """
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
				*pres = (float)(*pf1 - b1);"""
				
	if fo.processType == 1:
		code = code + """
				unsigned short t2 = (*pf2 -b2);
				if (t2 < wave2Threshold) {
					t2 = wave2Threshold;
				}
				*pres /= (float)t2;
		"""
		
	if fo.displayType == 1:
		code = code + """
				*pres -= *pref;
		"""
				
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
	
	weave.inline(code, vrs, headers = ['"emmintrin.h"'], extra_compile_args=["-mfpmath=sse -msse3"], compiler="gcc")
	
	return res
		

def loadRoisFromFile(filename, w, h):
	roiprofile = None
	times = None
	if os.path.splitext(filename)[1] == '.mat':
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
	elif os.path.splitext(filename)[1] == '.npy':
		R = np.load(filename)
		R = np.expand_dims(R,1)[0]
		ROIS = R['ROIS']
		roiprofile = R['traces']
		times = R['times']
		roboRois = []

		for roi in ROIS:
			r = Roi.Roi()
			c = roi['Coordinates']
			
			isValidRoi = True
			
			for x,y in zip(c[0],c[1]):
				if w < x or x < 0 or h < y or y < 0:
					isValidRoi = False
				r.addPoint(x,y)
				
			if isValidRoi:
				r.computePointMap()
				roboRois.append(r)
			

		
	return roboRois, roiprofile, times

def saveRoisToFile(filename,rois,roiprofile = None,times = None):
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
	if os.path.splitext(filename)[1] == '.mat':
		savemat(filename,{'ROIS':roilist})
	elif os.path.splitext(filename)[1] == '.npy':
		d = {'ROIS':roilist, 'traces':roiprofile, 'times':times}
		np.save(filename, d)
		
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





class ProcessedSequence:
	def __init__(self,tiffSequence,processedWidget,displayParameters,frameOptions,displayOptions,timeOptions):
		self.tiffSequence = tiffSequence
		self.processedWidget = processedWidget
		self.falseColorRefFrame = None
		self.HSVvalue = None
		self.displayParameters = displayParameters
		self.frameOptions = frameOptions
		self.displayOptions = displayOptions
		self.timeOptions = timeOptions
		self.currentProcessedFrame = 0
	
	def computeProcessedFrame(self,n,returnType="float"):
		self.currentProcessedFrame = n
		return computeProcessedFrameGLSL(self.processedWidget, self.tiffSequence, n, self.frameOptions,self.displayOptions, self.falseColorRefFrame,returnType=returnType)
		
	
	def computeReference(self):
		self.falseColorRefFrame = computeReference(self.tiffSequence, self.frameOptions)
		#return self.falseColorRefFrame
	
	def computeValue(self,ValueFrame):
		self.HSVvalue = computeValue(ValueFrame,(self.tiffSequence.height,self.tiffSequence.width))
		#return self.HSVvalue
	
	def applyColormap(self,f,w,h,returnType = "texture"):
		tex = applyColormapGLSL(self.processedWidget, f, w, h,self.displayParameters.displayColorMin,self.displayParameters.displayColorMax,returnType=returnType)
		
		#self.processedWidget.drawText(str(self.tiffSequence.timesDict[self.currentProcessedFrame]) + " s", 50, 50, [1.0, 1.0, 1.0],fontsize=24.0)
		#data = np.array([10.0, 10.0, 50.0, 10.0, 50.0, 35.0, 70.0, 35.0,70.0,10.0]).astype(np.float32)*2.0
		#self.processedWidget.drawTraces(data, 5, self.currentProcessedFrame, self.currentProcessedFrame,lineWidth=4)
		if self.timeOptions.displayTimeStamp:
			self.processedWidget.drawText(str(self.tiffSequence.timesDict[self.currentProcessedFrame]) + " s", self.timeOptions.xOffset,
				 self.timeOptions.yOffset, [1.0, 1.0, 1.0],fontsize=float(self.timeOptions.fontSize))
		
		if self.displayOptions.displayScalebar:
			data = np.array([10.0,10.0,10.0+round(self.displayOptions.scaleBarLength/self.displayOptions.scaleBarScaleFactor), 10.0]).astype(np.float32)
			self.processedWidget.drawTraces(data, 2, self.displayOptions.scaleBarXOffset, self.displayOptions.scaleBarYOffset,lineWidth=float(self.displayOptions.scaleBarLineSize))
		return tex
		
	def HSVImage(self,f,w,h):
		tex = HSVImageGLSL(self.processedWidget, f,self.HSVvalue, w, h, self.displayParameters.displayColorMin, self.displayParameters.displayColorMax, hsvcutoff=self.displayOptions.hsvcutoff)
		
		if self.timeOptions.displayTimeStamp:
			self.processedWidget.drawText(str(self.tiffSequence.timesDict[self.currentProcessedFrame]) + " s", self.timeOptions.xOffset,
				 self.timeOptions.yOffset, [1.0, 1.0, 1.0],fontsize=float(self.timeOptions.fontSize))
		
		
		return tex
	
	def drawTimeStamp(self,to):
		self.processedWidget.drawText(str(self.tiffSequence.timesDict[self.currentProcessedFrame]).zfill(3) + " s", to.xOffset, to.yOffset, [1.0, 1.0, 1.0],fontsize=to.fontSize)
		
