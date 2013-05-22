import PyQt4
from PyQt4.QtCore import *
import sys
import numpy as np
from pubTools import oneColumnFigure
from OpenGL import GL

from SequenceDisplayGui import Ui_SequenceDisplayWnd
from ImageDisplayWidget import ImageDisplayWidget
from TiffSequence import TiffSequence
import SequenceProcessor
from mplot import MPlot

from ProcessOptions import ProcessOptions

class SequenceDisplay(Ui_SequenceDisplayWnd, PyQt4.QtGui.QMainWindow):
	def __init__(self, parent = None, files=None,loadInRam=False):
		PyQt4.QtGui.QMainWindow.__init__(self, parent=parent)
		
		self.setupUi(self)
		self.imageWidgetSetup()
		
		#l = dir(self.CurrentFrameSlider)
		#for i in l:
		#	print(i)
		
		self.RoboMainWnd = parent
		self.MaxFrames = 0
		self.CurrentShownFrame = 0
		
		self.roiProfile = None
		
		self.PlayInterframe = 10
		self.IsPlaying = False
		self.timer = QBasicTimer()
		
		self.makeConnections()
		
		self.show()
		
		
		self.tiffSequence = TiffSequence(files)
		if loadInRam:
			self.tiffSequence.loadWholeTiff()
		self.MaxFrames = self.tiffSequence.getFrames()
		self.updateFrameWidgetsRange()
		self.showStatusMessage("Counted " + str(self.MaxFrames) + " frames")
		self.FrameImage, self.FrameData = self.getSequenceFrame(0)
		
		
		self.optionsDlg = ProcessOptions(self)
		rc = self.geometry()
		dlgRc = self.optionsDlg.geometry()
		dlgRc.moveTo(rc.right()+5, rc.top())
		self.optionsDlg.setGeometry(dlgRc)
		self.optionsDlg.show()
		
		self.optionsDlg.frameOptions.lastFrame = self.MaxFrames
		
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
		self.connect(self.CurrentFrameSlider, SIGNAL("sliderReleased()"), self.currentFrameSliderCb)
		self.connect(self.imWidget, SIGNAL("mousePositionChanged(int, int)"), self.imageNewMousePosition)
		#menus
		##ROIS
		self.connect(self.actionCompute_Rois, SIGNAL("triggered()"), self.computeRoisCb)
		

		
	def showStatusMessage(self, msg):
		self.statusBar().showMessage(msg)
	
	def getSequenceFrame(self, n, needQImage = True):
			
		im = self.tiffSequence.getFrame(n)
		
		if im == None:
			return None
		
		self.showStatusMessage("Frame " + str(self.CurrentShownFrame+1) + " of " + str(self.MaxFrames))
		
		return SequenceProcessor.convert16Bitto8Bit(im, im.min(), im.max(), needQImage), im
		#return SequenceProcessor.returnJet(im,returnQimage=True)
		
	def getNextSequenceFrame(self):
		self.CurrentShownFrame = self.CurrentShownFrame + 1
		if self.CurrentShownFrame >= self.MaxFrames:
			self.showStatusMessage("Trying to show frame " + str(self.CurrentShownFrame) + " of " + str(self.MaxFrames) + ". Impossible!!")
			self.CurrentShownFrame = self.CurrentShownFrame - 1
			return
			
		self.FrameImage, self.FrameData = self.getSequenceFrame(self.CurrentShownFrame, True)
		
		self.imWidget.repaint()
		#self.imWidget.updateGL()
		self.updateCurrentFrameWidgets()
		
	def getPreviousSequenceFrame(self):
		self.CurrentShownFrame = self.CurrentShownFrame - 1
		if self.CurrentShownFrame < 0:
			self.showStatusMessage("Trying to show frame " + str(self.CurrentShownFrame) + " of " + str(self.MaxFrames) + ". Impossible!!")
			self.CurrentShownFrame = self.CurrentShownFrame + 1
			return
		
		
		self.FrameImage, self.FrameData = self.getSequenceFrame(self.CurrentShownFrame)
		self.imWidget.repaint()
		self.updateCurrentFrameWidgets()
		
	def getFirstSequenceFrame(self):
		self.CurrentShownFrame = 0
		self.FrameImage, self.FrameData = self.getSequenceFrame(self.CurrentShownFrame)
		self.imWidget.repaint()
		self.updateCurrentFrameWidgets()
		
	def getLastSequenceFrame(self):
		self.CurrentShownFrame = self.MaxFrames - 1
		self.FrameImage, self.FrameData = self.getSequenceFrame(self.CurrentShownFrame)
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
		
	def currentFrameSliderCb(self):
		fr = self.CurrentFrameSlider.value()
		if fr == self.CurrentShownFrame:
			return
			
		self.CurrentShownFrame = self.CurrentFrameSlider.value()
		self.FrameImage, self.FrameData = self.getSequenceFrame(self.CurrentShownFrame, True)
		
		self.imWidget.repaint()
		self.updateCurrentFrameWidgets()
		
	def currentFrameSpinBoxCb(self):
		self.CurrentShownFrame = self.CurrentFrameSpinBox.value()
		self.FrameImage, self.FrameData = self.getSequenceFrame(self.CurrentShownFrame, True)
		
		self.imWidget.repaint()
		self.updateCurrentFrameWidgets()
		
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
				
	def imageNewMousePosition(self, x, y):
		if self.FrameData != None:
			imy, imx = self.FrameData.shape
			if imy > y and y >= 0 and imx > x and x >= 0:
				self.showStatusMessage(str(x) + ":" + str(y) + "=" + str(self.FrameData[y][x]))
	
	def computeRoisCb(self):
		ff = 0
		lf = self.tiffSequence.getFrames()
		
		nrois = len(self.tiffSequence.rois)
		self.roiProfile = np.zeros((lf, nrois))
		
		for i in xrange(ff, lf, 100):
			tlf = i + 100
			if tlf > lf:
				tlf = lf
			self.roiProfile[i:tlf, 0:nrois] = self.tiffSequence.computeRois(i, tlf)
			self.showStatusMessage("Processed " + str(tlf) + "/" + str(lf))
			self.update()
			
		##FOR TESTING PURPOSES ONLY
		#fig,ax = oneColumnFigure(addAxes=True)
		#ax.plot(roiProfile)
		#fig.show()
		
		fig = MPlot(self)
		
		rdata = SequenceProcessor.applyRoiComputationOptions(self.roiProfile, self.optionsDlg.frameOptions, self.tiffSequence.rois)
		
		fig.plot(rdata)
		fig.show()
		
		
if __name__== "__main__":
	app = PyQt4.QtGui.QApplication(sys.argv)
	window = RoboPy()
	window.show()
	
	sys.exit(app.exec_())

