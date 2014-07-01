import PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from OpenGL import GL
from Roi import Roi
from PreviewDisplayGui import Ui_PreviewDisplayWnd
from ImageDisplayWidget import ImageDisplayWidget
from TiffSequence import TiffSequence, HDF5Sequence
from ProcessOptions import ProcessOptions
from math import sqrt,ceil
class PreviewDisplay(Ui_PreviewDisplayWnd, PyQt4.QtGui.QMainWindow):
	def __init__(self, parent = None, tiffSequence=None,cropL=None):
		PyQt4.QtGui.QMainWindow.__init__(self, parent=parent)
		self.setupUi(self)
		#l = dir(self.CurrentFrameSlider)
		#for i in l:
		#	print(i)
		self.RoboMainWnd = parent
		
		hlay = PyQt4.QtGui.QHBoxLayout(self.ImageFrameWidget)
		imWidget = ImageDisplayWidget(self)
		
		self.imWidget = imWidget
		hlay.addWidget(imWidget)
		
		self.imWidget.createShaders()
		
		if tiffSequence is not None:
			self.tiffSequence = tiffSequence
			img2 = tiffSequence.getFramesInterval(1,10)
			img = img2.mean(2)
		else:
			self.close()

		self.connect(self.imWidget, SIGNAL("roiAdded(long)"), self.roiAdded)
		self.connect(self.imWidget, SIGNAL("roiRecomputeNeeded(bool)"), self.roiAdded)

		self.imWidget.computeRoiPointMaps = False
		self.frameHeight = img.shape[0]# int(ceil(sqrt(img.shape[0]**2 + img.shape[1]**2)))
		self.frameWidth = img.shape[1]#self.frameHeight
		self.optionsDlg = ProcessOptions(self)
		self.roiMonitor = False
		self.imWidget.ImageZoom = 0.3
		self.imWidget.ImageZoomSteps = -5.4

		if cropL is not None:
			a,b,c,d = cropL
			roi = Roi()
			roi.addPoint(a,c)
			roi.addPoint(b,c)
			roi.addPoint(b,d)
			roi.addPoint(a,d)
			self.imWidget.addRoi(roi,False)
		self.FrameImage, self.FrameData = self.loadImageGray(img)
		self.updateDisplay()
		self.show()

	def loadImageGray(self,im,needQImage=True):
		
		
		
		if im == None:
			return None
			

		# if self.displayParameters.autoAdjust:
		# 	self.changeDisplayGrayMin(im.min())
		# 	self.changeDisplayGrayMax(im.max())
	
		#if viewType == 0:
		tex = self.imWidget.processData(list([im]), list([0]), list([list([im.min(), im.max()])]))
		return tex, im
		#else:
		#	return None, None

	def updateDisplay(self):
		
		if self.FrameImage == None:
			return
			
		h, w = self.frameHeight, self.frameWidth
			
		self.imWidget.currentDrawData["tex"] = self.FrameImage
		self.imWidget.currentDrawData["width"] = w
		self.imWidget.currentDrawData["height"] = h
		self.imWidget.updateGL()

	def roiAdded(self):
		if len(self.imWidget.rois)>1:
			self.imWidget.deleteRoi(0)

		rf =  self.imWidget.rois[0].boundingRect()
		[a,b,c,d] = [rf.left(),rf.left()+rf.width(), rf.top(), rf.top()+ rf.height()]
	#	print [a,b,c,d]
		self.emit(SIGNAL("roiChanged(int, int, int, int)"),a,b,c,d)
	
	def closeEvent(self, event):
        # do stuff

		self.optionsDlg.close()
		event.accept() # let the window close
	