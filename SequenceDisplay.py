import PyQt4
from PyQt4.QtCore import *
import sys

from OpenGL import GL

from SequenceDisplayGui import Ui_SequenceDisplayWnd
from ImageDisplayWidget import ImageDisplayWidget
from TiffSequence import TiffSequence
import SequenceProcessor

class SequenceDisplay(Ui_SequenceDisplayWnd, PyQt4.QtGui.QMainWindow):
	def __init__(self, parent = None, files=None):
		PyQt4.QtGui.QMainWindow.__init__(self, parent=parent)
		
		self.setupUi(self)
		self.imageWidgetSetup()
		
		self.RoboMainWnd = parent
		self.SequenceFiles = files
		self.MaxFrames = 0
		self.FramesPerFile = list()
		self.Tiff = None
		
		self.makeConnections()
		
		self.show()
		
		self.countSequenceFrames()
		self.FrameImage = self.getSequenceFrame(0)
		
	def imageWidgetSetup(self):
		hlay = PyQt4.QtGui.QHBoxLayout(self.ImageFrameWidget)
		imWidget = ImageDisplayWidget()
		imWidget.SequenceDisplay = self
		
		hlay.addWidget(imWidget)
		
	def makeConnections(self):
		pass
		#self.connect(self.roboActionOpen, SIGNAL("triggered()"), self.roboActionOpenCb)
		
		
	def showStatusMessage(self, msg):
		self.statusBar().showMessage(msg)
		
	def countSequenceFrames(self):
		self.MaxFrames = 0
		if self.SequenceFiles != None:
			for s in self.SequenceFiles:
				th = TiffSequence(s)
				self.MaxFrames = self.MaxFrames + th.getFrames()
				self.showStatusMessage("Counted " + str(self.MaxFrames) + " frames")
				self.FramesPerFile.append(th.getFrames())
			
	
	def getSequenceFrame(self, n):
		(i,j) = self.getSequenceIndexes(n)
		
		if i == -1:
			return None
			
		if self.Tiff == None or self.Tiff.getFileName() != self.SequenceFiles[i]:
			self.Tiff = TiffSequence(self.SequenceFiles[i])
			
		im = self.Tiff.getFrame(j)
		
		if im == None:
			return None
		
		return SequenceProcessor.convert16Bitto8Bit(im, im.min(), im.max(), True)
	
	def getSequenceIndexes(self, n):
		if n > self.MaxFrames:
			return (-1,-1)
		
		i = 0;
		while n > self.FramesPerFile[i]:
			n = n - self.FramesPerFile[i]
			i = i + 1
			
		return (i,n)

if __name__== "__main__":
	app = PyQt4.QtGui.QApplication(sys.argv)
	window = RoboPy()
	window.show()
	
	sys.exit(app.exec_())

