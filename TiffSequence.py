from libtiff import TIFF
from numpy import zeros,loadtxt,array,uint16,argwhere
import numpy as np
import Roi
from os.path import splitext, getsize
import threading
from scipy.ndimage import zoom
import tables as tb
#from pubTools import oneColumnFigure

class ThreadedRead(threading.Thread):
	def __init__(self, threadId, tifSequence):
		threading.Thread.__init__(self)
		self.threadId = threadId
		
		self.tifSequence = tifSequence
		self.frameToLoad = 0
		
	def run(self):
		self.tifSequence.threadLock.acquire()
		self.tifSequence.loadFrameInCache(self.frameToLoad)
		self.tifSequence.threadLock.release()
class Sequence:
	"""
	Abstract sequence class from which other classes should inherit. Every derived class must override the open, getRawImage and (possibly) 
	saveSequence methods
	"""
	def __init__(self,fNames,options=None):
		self.fileName = fNames
		self.width = -1
		self.height = -1
		self.frames = 0
		self.origWidth = -1
		self.origHeight = -1
		self.SequenceFiles = fNames
		self.options = options
		if self.options is None:
			self.options = {}
			self.options['rebin'] = None
			self.options['LineCorrection'] = False
			self.options['crop'] = False
		self.FramesPerFile = list()
		self.rois = list()
		self.arraySequence = None
		self.timesDict = TimesDict()
		try:
			self.open()
		except TypeError:
			print("Not able to open image file. Trying to continue..")
		self.cachedFrames = {0:None, 1:None, 2:None}
				

		self.threadLock = threading.Lock()
	
	def open(self):
		pass
	
	def getRawImage(self,n):
		pass	
	
	def saveSequence(self, f):
		pass
	
	def getFileName(self):
		return self.fileName
		
	def getWidth(self):
		return self.width
		
	def getHeight(self):
		return self.height
		
	def getFrames(self):
		return self.frames	
	

	
	
	def initTimesDict(self,filename=None):
		if filename is None:
			#if (size(self.SequenceFiles))==1:
		#		filename=splitext(self.SequenceFiles)+'_times.txt'
		#	else:
			try:
				filename=splitext(self.SequenceFiles[0])[0]+'_times.txt'
			except TypeError:
				return
		try:
			self.timesDict = loadTimes(filename,firstFrameIndex = 0, firstTimeValue = 0.0,scaleFactor=1000.0)
			self.timesDict.setLabel('Time (s)')
			if len(self.timesDict)< self.frames:
				print("Warning. More frames than timepoints")
				print("Timepoints: "+str(len(self.timesDict)))
				print("Number of frames: " + str(self.frames))
				kv = range(self.frames)
				self.timesDict = TimesDict(zip(kv,kv))
				self.timesDict.setLabel('Frames')
				

			#delete unnecessary timepoints
			elif len(self.timesDict)>self.frames:
				print("Warning. More timepoints than frames. Discarding unnecessary timepoints")
				for key in xrange(self.frames,len(self.timesDict)):
					del(self.timesDict[key])
					
			#Check for autosave timepoints error
				if self.timesDict.checkAutoSaveErrors():
					print('Correcting times mismatch due to autosave')
					self.timesDict.correctAutoSaveFrameTime()
		except IOError:
			print("Warning. No associated time file")
			kv = range(self.frames)
			self.timesDict = TimesDict(zip(kv,kv))
			self.timesDict.setLabel('Frames')
			
			
	def computeRois(self,firstIndex = None, lastIndex = None):
		if firstIndex == None:
			firstIndex = 0
		if lastIndex == None:
			lastIndex = self.getFrames()
			
		roiProfile = zeros((lastIndex-firstIndex,len(self.rois)))
		
		for ind in xrange(firstIndex,lastIndex):
			img = self.getFrame(ind)
			for i,r in enumerate(self.rois):
				#print str(ind) + " " + str(i) + " " + str(lastIndex)
				roiProfile[ind-firstIndex,i] = r.computeAverage(img)
				
		return roiProfile
	
	def applyOptions(self,img):
			if self.options['crop']:
				lm = self.options['leftMargin']
				rm = self.options['rightMargin']
				tm = self.options['topMargin']
				bm = self.options['bottomMargin']
			if self.options['rebin'] is not None:
				if self.options['LineCorrection']:
					
					lsub = img[:,:self.options['LeftLC']]
					if self.options['RightLC']!=0:
						rsub = img[:,-self.options['RightLC']::]
						lrsub = np.hstack((lsub,rsub)).mean(1)

					else:
						lrsub = lsub.mean(1)
					
					lrsub = lrsub.reshape((lrsub.shape[0],1))
					sub = uint16(np.tile(lrsub,(1,img.shape[1])))
					#img = zoom(img-sub+uint16(lrsub.mean()),1.0/self.options['rebin'],order=0)
					img = rebin(img-sub+uint16(lrsub.mean()),(img.shape[0]/self.options['rebin'],img.shape[1]/self.options['rebin']))
					if self.options['crop']:
						img = img[tm:bm,lm:rm]
					#self.arraySequence[:,:,index] = img
					
				else:	
					#img = zoom(img,1.0/self.options['rebin'],order=0)
					img = rebin(img,(img.shape[0]/self.options['rebin'],img.shape[1]/self.options['rebin']))
					if self.options['crop']:
						img = img[tm:bm,lm:rm]
					#self.arraySequence[:,:,index] = img
			else:
				if self.options['LineCorrection']:
					#img = self.tifHandlers[i].read_image()
					
					lsub = img[:,:self.options['LeftLC']]
					if self.options['RightLC']!=0:
						rsub = img[:,-self.options['RightLC']::]
						lrsub = np.hstack((lsub,rsub)).mean(1)

					else:
						lrsub=lsub.mean(1)
						
					lrsub = lrsub.reshape((lrsub.shape[0],1))
					sub = uint16(np.tile(lrsub,(1,img.shape[1])))
					#self.arraySequence[:,:,index] = img-sub+uint16(lrsub.mean())
					img = img-sub+uint16(lrsub.mean())
					if self.options['crop']:
						img = img[tm:bm,lm:rm]
					#self.arraySequence[:,:,index] = img-sub+uint16(lrsub.mean())
					
				else:	
					if self.options['crop']:
						img = img[tm:bm,lm:rm]	
						
			return img
					#self.arraySequence[:,:,index] = img

	def loadWholeTiff(self):
		self.arraySequence = zeros((self.height,self.width,self.frames))
		for index in xrange(self.frames):
			img = self.getRawImage(index)
			img = self.applyOptions(img)
			self.arraySequence[:,:,index] = img
			
	def loadFrameInCache(self, n):
		if self.arraySequence is not None:
			self.cachedFrames[n] = self.arraySequence[:,:,n].copy()
		else:
			img = self.getRawImage(n)
			img = self.applyOptions(img)
			self.cachedFrames[n] = img
			

		
	def getFrame(self, n):
		#index = self.timesDict.frames()[n]
		if self.arraySequence is not None:
			return self.arraySequence[:, :, n].copy()
		else:
			

					
			ks = self.cachedFrames.keys()
			if len(ks) > 3:
				for k in ks:
					if k != n-1 and k != n+1:
						del self.cachedFrames[k]
				
			if not self.cachedFrames.has_key(n) or self.cachedFrames[n] == None:
				self.threadLock.acquire()
				img = self.getRawImage(n)
				img = self.applyOptions(img)
				self.cachedFrames[n] = img

				self.threadLock.release()	
			
				
			if not self.cachedFrames.has_key(n+1):
				loader1 = ThreadedRead(1, self)
				loader1.frameToLoad = n+1
				loader1.start()
				
			if n > 1 and not self.cachedFrames.has_key(n-1):
				loader2 = ThreadedRead(2, self)
				loader2.frameToLoad = n-1
				loader2.start()
				
			#print("Returning frame " + str(n) + " with values" + str(self.cachedFrames[n]))
			
			return self.cachedFrames[n]
		
		return None
	
		
	def getFramesFromList(self,listOfFrames):
		 #Ensure listOfFrames is actually a list, not a tuple
		listOfFrames = list(listOfFrames)
		outArray = zeros((self.height,self.width,len(listOfFrames)), dtype=uint16)
		for n in range(len(listOfFrames)):
			outArray[:,:,n]=self.getFrame(listOfFrames[n])
		return outArray

	def getFramesInterval(self,firstIndex,lastIndex):
		return self.getFramesFromList(range(firstIndex,lastIndex))
		
		
	
class TiffSequence(Sequence):
	def __init__(self, fNames,options = None):
		self.tifHandlers = list()	
		Sequence.__init__(self,fNames,options)
		
		for i in self.tifHandlers:
			width, height, frames = self.getTifInfo(i)
			print(str(width) + " " + str(height) + " " + str(frames))
			if self.width == -1:
				self.width = width
				self.height = height
			else:
				if width != self.width or height != self.height:
					print("TiffSequence::Inconsistent width or height across the sequence files")
					self.clearTifHandler()
					break
			self.FramesPerFile.append(frames)
			self.frames = self.frames + frames
		
		self.initTimesDict()


		
	def __del__(self):
		self.clearTifHandler()
	
	def clearTifHandler(self):
		if len(self.tifHandlers) > 0:
			for f in self.tifHandlers:
				TIFF.close(f)
			self.tifHandlers = list()
		
			
	def open(self):
		self.clearTifHandler()
		
		for i in self.SequenceFiles:
			self.tifHandlers.append(TIFF.open(i, 'r'))
		
	def getTifInfo(self, th):
		
		width = 0
		height = 0
		frames = 0
		
		if th != None:
			currDir = th.CurrentDirectory().value
			width = th.GetField(256)
			height = th.GetField(257)
			cnt = 100000
			while th.SetDirectory(cnt):
				cnt = cnt + 10000
				
			frames = th.CurrentDirectory().value
			th.SetDirectory(currDir)
		if self.options['rebin'] is not None:
			width = width/self.options['rebin']
			height = height/self.options['rebin']
		self.origWidth = width
		self.origHeight = height
		if self.options['crop']:
			width = self.options['rightMargin'] - self.options['leftMargin']
			height = self.options['bottomMargin'] - self.options['topMargin']
		
		return width, height, frames
		
	def getFileIndexes(self, n):
		if n > self.frames:
			return (-1,-1)
		
		i = 0;
		while n > self.FramesPerFile[i]:
			n = n - self.FramesPerFile[i]
			i = i + 1
			
		return (i,n)
	
	def getRawImage(self,index):
		if self.tifHandlers[0] != None:
			i,n = self.getFileIndexes(index)
		
			if i == -1:
				pass
			
			self.tifHandlers[i].SetDirectory(n)
			img = self.tifHandlers[i].read_image()
			return img
		else:
			return None
	

					

		
	def saveSequence(self, f,sequence=None,framesInd = None):
		if sequence == None:
			sequence = self
			
	
		th = TIFF.open(str(f), 'w')
		count = 0
		if framesInd is None:
			framesInd = range(sequence.frames)
		for i in framesInd:
			th.SetField(256, sequence.width)
			th.SetField(257, sequence.height)
			th.SetField(277, 1) #phtometric interpretation black is minimum
			th.SetField(258, 16) #bits per sample
			th.SetField(262, 1) #samples per pixel
			
			th.write_image(sequence.getFrame(i), "lzw", False)
			if getsize(f)>2.274032144*1E9:
				count = count +1 
				fname2,ext = splitext(str(f))
				f = fname2+'_part'+str(count).zfill(2)+ext
				th = TIFF.open(f,'w')
				
	def openWriteSequence(self, f):
		th = TIFF.open(str(f), 'w')
		return th
	
	def addSequenceFrame(self, th, f, w, h):
		th.SetField(256, w)
		th.SetField(257, h)
		th.SetField(277, 1) #phtometric interpretation black is minimum
		th.SetField(258, 16) #bits per sample
		th.SetField(262, 1) #samples per pixel
		
		th.write_image(f, "lzw", False)
		if getsize(th.FileName()) > 2.274032144*1E9:
			return 1
		else:
			return 0
		
	def closeWriteSequence(self, th):
		th.close()
	


class HDF5Sequence(Sequence):
	def __init__(self, fNames,options = None):
		

		
		#self.tifHandlers = list()	
		self.hdf5Handler = None
		Sequence.__init__(self,fNames,options)
		try:
			height,width, frames = self.hdf5Handler.shape
		except:
			height,width,frames = 0,0,1
		if self.options['rebin'] is not None:
			width = width/self.options['rebin']
			height = height/self.options['rebin']
		self.origWidth = width
		self.origHeight = height
		if self.options['crop']:
			width = self.options['rightMargin'] - self.options['leftMargin']
			height = self.options['bottomMargin'] - self.options['topMargin']
		
		self.width=width
		self.height=height
		self.frames=frames - 1
		
		self.origWidth = self.width 
		self.origHeight = self.height
		self.initTimesDict()
	
	def open(self):
		fi = tb.openFile(self.SequenceFiles[0])
		self.hdf5Handler = fi.root.x
	
	def getRawImage(self,n):
		return self.hdf5Handler[:,:,n]	
	
	
	def saveSequence(self, f,sequence=None,framesInd = None):
		if sequence == None:
			sequence = self
			
		data = sequence.getFrame(0)
		
		if framesInd is None:
			framesInd = range(sequence.frames)
		
		h5file = tb.openFile(f, mode='w')
		root = h5file.root
		atom = tb.Atom.from_dtype(data.dtype)
		#filters = tb.Filters(complevel=9, complib='lzo',shuffle=True)

		x = h5file.createEArray(root,'x',atom,shape=(sequence.getHeight(),sequence.getWidth(),0),expectedrows=sequence.frames)

		for i in framesInd:		
			data = sequence.getFrame(i)
			x.append(data.reshape((sequence.getHeight(),sequence.getWidth(),1)))
		
		h5file.flush()
		h5file.close()
	
def loadTimes(filename,firstFrameIndex=0,firstTimeValue=0,scaleFactor=1.0):
	
	#times=numpy.loadtxt(splitext(filename)[0]+'_times.txt',delimiter='\t',skiprows=1,usecols=(0,1))
	times = loadtxt(filename,delimiter='\t',skiprows=1,usecols=(0,1))
	return TimesDict(zip(list((times[:,0]+firstFrameIndex).astype(uint16)),list((times[:,1]+firstTimeValue)/scaleFactor)))

def rebin(a, shape):
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
    return a.reshape(sh).sum(-1).sum(1)

class TimesDict(dict):
	"""
	A dict to hold the original times of the tiff sequence. Each time is stored as framenumber:time.
	times and frames method returns all times and frames as a numpy array
	"""
	def __init__(self,*arg,**kw):
		super(TimesDict, self).__init__(*arg, **kw)
		self.label=''

		
	def times(self):
		"""
		Return times array as a numpy array
		"""
		a=[]
		for val in self.itervalues():
			a.append(val)
		return array(a)
	
	def frames(self):
		"""
		Return frames as a numpy array
		"""
		a=[]
		for key in self.iterkeys():
			a.append(key)
		return array(a)
	
	def dt(self):
		"""
		Return the average time step
		"""
		return (np.diff(self.times())/(np.diff(self.frames())*1.0)).mean()
	
	def setLabel(self,label):
		self.label=label
	
	def checkAutoSaveErrors(self):
		dt = (np.diff(self.times())/(np.diff(self.frames())*1.0))
		pts = argwhere(dt<0)
		if pts.size != 0:
			return True
		else:
			return False
			
	def correctAutoSaveFrameTime(self):
		dt = (np.diff(self.times())/(np.diff(self.frames())*1.0))
		pts = argwhere(dt<0)
		pts = np.append(pts,dt.size)
		if pts.size == 0:
			return

		meanDt = dt[0:pts[0]].mean()
		
		for i in xrange(len(pts)-1):
			for ind in xrange(pts[i],pts[i+1]):
				self[ind+1]=self[ind+1]+meanDt + self[pts[i]]
