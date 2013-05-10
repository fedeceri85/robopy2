from libtiff import TIFF
#Prova
class TiffSequence:
	def __init__(self, fNames):
		
		self.fileName = None
		self.width = -1
		self.height = -1
		self.frames = 0
		
		self.SequenceFiles = fNames
		self.FramesPerFile = list()
		
		self.tifHandlers = list()
		
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
			width = th.GetField(256)
			height = th.GetField(257)
			cnt = 100000
			while not th.SetDirectory(cnt):
				cnt = cnt + 10000
				
			frames = th.CurrentDirectory().value
			
		return width, height, frames
		
	def getFileIndexes(self, n):
		if n > self.frames:
			return (-1,-1)
		
		i = 0;
		while n > self.FramesPerFile[i]:
			n = n - self.FramesPerFile[i]
			i = i + 1
			
		return (i,n)
		
	def getFrame(self, n):
		if self.tifHandlers[0] != None:
			i,n = self.getFileIndexes(n)
			
			if i == -1:
				return None
			
			self.tifHandlers[i].SetDirectory(n)
			
			return self.tifHandlers[i].read_image()
		
		return None
