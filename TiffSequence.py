from libtiff import TIFF
from numpy import zeros,loadtxt,array,uint16
import Roi
from os.path import splitext
import thread
#from pubTools import oneColumnFigure
class TiffSequence:
	def __init__(self, fNames):
		
		self.fileName = None
		self.width = -1
		self.height = -1
		self.frames = 0
		
		self.SequenceFiles = fNames
		
		self.FramesPerFile = list()
		
		self.tifHandlers = list()
		self.rois = list()
		self.arraySequence = None
		self.timesDict = TimesDict()
		self.open()
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
		self.cachedFrames = {0:None, 1:None, 2:None}

		
		
	def __del__(self):
		self.clearTifHandler()
	
	def clearTifHandler(self):
		if len(self.tifHandlers) > 0:
			for f in self.tifHandlers:
				TIFF.close(f)
			self.tifHandlers = list()
		
	
	def getFileName(self):
		return self.fileName
		
	def getWidth(self):
		return self.width
		
	def getHeight(self):
		return self.height
		
	def getFrames(self):
		return self.frames
		
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
		return width, height, frames
		
	def getFileIndexes(self, n):
		if n > self.frames:
			return (-1,-1)
		
		i = 0;
		while n > self.FramesPerFile[i]:
			n = n - self.FramesPerFile[i]
			i = i + 1
			
		return (i,n)
	
	def loadWholeTiff(self):
		self.arraySequence = zeros((self.height,self.width,self.frames))
		for index in xrange(self.frames):
			if self.tifHandlers[0] != None:
				i,n = self.getFileIndexes(index)
			
				if i == -1:
					pass
				
				self.tifHandlers[i].SetDirectory(n)
				self.arraySequence[:,:,index]=self.tifHandlers[i].read_image()

		
	def getFrame(self, n):
		#index = self.timesDict.frames()[n]
		if self.arraySequence is not None:
			if not self.cachedFrames.has_key(n) or self.cachedFrames[n] == None:
				if self.cachedFrames.has_key(n-2):
					self.cachedFrames.pop(n-2)
				elif self.cachedFrames.has_key(n+2):
					self.cachedFrames.pop(n+2)
				elif len(self.cachedFrames) > 2:
					self.cachedFrames.popitem()
				self.cachedFrames[n] = self.arraySequence[:,:,n].copy()
				
			return self.cachedFrames[n]
		else:
			if self.tifHandlers[0] != None:
				i,n = self.getFileIndexes(n)
				
				if i == -1:
					return None
					
				if not self.cachedFrames.has_key(n) or self.cachedFrames[n] == None:
					if self.cachedFrames.has_key(n-2):
						self.cachedFrames.pop(n-2)
					elif self.cachedFrames.has_key(n+2):
						self.cachedFrames.pop(n+2)
					elif len(self.cachedFrames) > 2:
						self.cachedFrames.popitem()
					self.tifHandlers[i].SetDirectory(n)
					self.cachedFrames[n] = self.tifHandlers[i].read_image()
				
				return self.cachedFrames[n]
			
			return None
	
		
	def getFramesFromList(self,listOfFrames):
		 #Ensure listOfFrames is actually a list, not a tuple
		listOfFrames = list(listOfFrames)
		outArray = zeros((self.height,self.width,len(listOfFrames)))
		for n in range(len(listOfFrames)):
			outArray[:,:,n]=self.getFrame(listOfFrames[n])
		return outArray

	def getFramesInterval(self,firstIndex,lastIndex):
		return self.getFramesFromList(range(firstIndex,lastIndex))
				
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
		
	def saveSequence(self, f):
		th = TIFF.open(str(f), 'w')
		
		for i in range(self.frames):
			th.SetField(256, self.width)
			th.SetField(257, self.height)
			th.SetField(277, 1) #phtometric interpretation black is minimum
			th.SetField(258, 16) #bits per sample
			th.SetField(262, 1) #samples per pixel
			
			th.write_image(self.getFrame(i), "lzw", False)
		
		
	def initTimesDict(self,filename=None):
		if filename is None:
			#if (size(self.SequenceFiles))==1:
		#		filename=splitext(self.SequenceFiles)+'_times.txt'
		#	else:
			filename=splitext(self.SequenceFiles[0])[0]+'_times.txt'
		
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
		except IOError:
			print("Warning. No associated time file")
			kv = range(self.frames)
			self.timesDict = TimesDict(zip(kv,kv))
			self.timesDict.setLabel('Frames')




		
def loadTimes(filename,firstFrameIndex=0,firstTimeValue=0,scaleFactor=1.0):
	
	#times=numpy.loadtxt(splitext(filename)[0]+'_times.txt',delimiter='\t',skiprows=1,usecols=(0,1))
	times = loadtxt(filename,delimiter='\t',skiprows=1,usecols=(0,1))
	return TimesDict(zip(list((times[:,0]+firstFrameIndex).astype(uint16)),list((times[:,1]+firstTimeValue)/scaleFactor)))



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
		return (diff(self.times())/(diff(self.frames())*1.0)).mean()
	
	def setLabel(self,label):
		self.label=label
	
