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
		
		#l = dir(self.CurrentFrameSlider)
		#for i in l:
		#	print(i)
		
		#meths = self.CurrentFrameSlider.?
		#print(meths)
		#self.CurrentFrameSlider.setBuddy(self.CurrentFrameSpinBox)
		
		self.RoboMainWnd = parent
		self.SequenceFiles = files
		self.MaxFrames = 0
		self.CurrentShownFrame = 0
		self.FramesPerFile = list()
		
		self.Tiff = None
		self.PlayInterframe = 10
		self.IsPlaying = False
		self.timer = QBasicTimer()
		
		self.makeConnections()
		
		self.show()
		
		self.countSequenceFrames()
		self.FrameImage = self.getSequenceFrame(0)
		
	def imageWidgetSetup(self):
		hlay = PyQt4.QtGui.QHBoxLayout(self.ImageFrameWidget)
		imWidget = ImageDisplayWidget()
		imWidget.SequenceDisplay = self
		
		self.imWidget = imWidget
		
		hlay.addWidget(imWidget)
		
	def makeConnections(self):
		self.connect(self.ForwardFrameButton, SIGNAL("clicked()"), self.getNextSequenceFrame)
		self.connect(self.BackFrameButton, SIGNAL("clicked()"), self.getPreviousSequenceFrame)
		self.connect(self.FirstFrameButton, SIGNAL("clicked()"), self.getFirstSequenceFrame)
		self.connect(self.LastFrameButton, SIGNAL("clicked()"), self.getLastSequenceFrame)
		self.connect(self.PlayButton, SIGNAL("clicked()"), self.playButtonCb)
		
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
				
			self.updateFrameWidgetsRange()
	
	def getSequenceFrame(self, n):
		(i,j) = self.getSequenceIndexes(n)
		
		if i == -1:
			return None
			
		if self.Tiff == None or self.Tiff.getFileName() != self.SequenceFiles[i]:
			self.Tiff = TiffSequence(self.SequenceFiles[i])
			
		im = self.Tiff.getFrame(j)
		
		if im == None:
			return None
		
		self.showStatusMessage("Frame " + str(self.CurrentShownFrame+1) + " of " + str(self.MaxFrames))
		
		return SequenceProcessor.convert16Bitto8Bit(im, im.min(), im.max(), True)
		
	def getNextSequenceFrame(self):
		self.CurrentShownFrame = self.CurrentShownFrame + 1
		if self.CurrentShownFrame >= self.MaxFrames:
			self.showStatusMessage("Trying to show frame " + str(self.CurrentShownFrame) + " of " + str(self.MaxFrames) + ". Impossible!!")
			self.CurrentShownFrame = self.CurrentShownFrame - 1
			return
		
			
		self.FrameImage = self.getSequenceFrame(self.CurrentShownFrame)
		if self.FrameImage == None:
			print("getFrame returned None")
		self.imWidget.repaint()
		self.updateCurrentFrameWidgets()
		
	def getPreviousSequenceFrame(self):
		self.CurrentShownFrame = self.CurrentShownFrame - 1
		if self.CurrentShownFrame < 0:
			self.showStatusMessage("Trying to show frame " + str(self.CurrentShownFrame) + " of " + str(self.MaxFrames) + ". Impossible!!")
			self.CurrentShownFrame = self.CurrentShownFrame + 1
			return
		
		
		self.FrameImage = self.getSequenceFrame(self.CurrentShownFrame)
		self.imWidget.repaint()
		self.updateCurrentFrameWidgets()
		
	def getFirstSequenceFrame(self):
		self.CurrentShownFrame = 0
		self.FrameImage = self.getSequenceFrame(self.CurrentShownFrame)
		self.imWidget.repaint()
		self.updateCurrentFrameWidgets()
		
	def getLastSequenceFrame(self):
		self.CurrentShownFrame = self.MaxFrames - 1
		self.FrameImage = self.getSequenceFrame(self.CurrentShownFrame)
		self.imWidget.repaint()
		self.updateCurrentFrameWidgets()
		
	def updateCurrentFrameWidgets(self):
		self.CurrentFrameSlider.blockSignals(True)
		self.CurrentFrameSlider.setValue(self.CurrentShownFrame)
		self.CurrentFrameSlider.blockSignals(False)
		
		self.CurrentFrameSpinBox.blockSignals(True)
		self.CurrentFrameSpinBox.setValue(self.CurrentShownFrame)
		self.CurrentFrameSpinBox.blockSignals(False)
		
	def updateFrameWidgetsRange(self):
		self.CurrentFrameSlider.blockSignals(True)
		self.CurrentFrameSlider.setRange(0, self.MaxFrames-1)
		self.CurrentFrameSlider.blockSignals(False)
		
		self.CurrentFrameSpinBox.blockSignals(True)
		self.CurrentFrameSpinBox.setRange(0, self.MaxFrames-1)
		self.CurrentFrameSpinBox.blockSignals(False)
	
	def getSequenceIndexes(self, n):
		if n > self.MaxFrames:
			return (-1,-1)
		
		i = 0;
		while n > self.FramesPerFile[i]:
			n = n - self.FramesPerFile[i]
			i = i + 1
			
		return (i,n)
		
	def playButtonCb(self):
		if self.IsPlaying == False:
			self.timer.start(self.PlayInterframe, self)
			self.IsPlaying = True
		else:
			self.timer.stop()
			self.IsPlaying = False
			
	def isLastFrame(self):
		if self.CurrentShownFrame >= self.MaxFrames -1:
			return True
		
		return False
		
	def timerEvent(self, event):
		if self.IsPlaying == True:
			self.getNextSequenceFrame()
			if self.isLastFrame():
				self.timer.stop()
				self.IsPlaying = False

if __name__== "__main__":
	app = PyQt4.QtGui.QApplication(sys.argv)
	window = RoboPy()
	window.show()
	
	sys.exit(app.exec_())

