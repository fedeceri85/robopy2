from libtiff import TIFF
#Prova
class TiffSequence:
	def __init__(self, fName):
		self.fileName = fName
		self.width = 0
		self.height = 0
		self.frames = 0
		
		self.tifHandler = None
		self.open()
		self.getTifInfo()
		
	def __del__(self):
		self.clearTifHandler()
	
	def clearTifHandler(self):
		if self.tifHandler != None:
			TIFF.close(self.tifHandler)
			self.tifHandler = None
		
	
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
		self.tifHandler = TIFF.open(self.getFileName(), 'r')
		
	def getTifInfo(self):
		
		th = self.tifHandler
		
		if th != None:
			self.width = th.GetField(256)
			self.height = th.GetField(257)
			cnt = 100000
			while not th.SetDirectory(cnt):
				cnt = cnt + 10000
				
			self.frames = th.CurrentDirectory().value
		
	def getFrame(self, n):
		if self.tifHandler != None:
			self.tifHandler.SetDirectory(n)
			if n < 0 or n > self.frames - 1:
				return None
			return self.tifHandler.read_image()
		
		return None
