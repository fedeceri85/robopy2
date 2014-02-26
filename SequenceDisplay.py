import PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
import numpy as np
from pubTools import oneColumnFigure
from OpenGL import GL

import DisplayParameters
from SequenceDisplayGui import Ui_SequenceDisplayWnd
from ImageDisplayWidget import ImageDisplayWidget
from TiffSequence import TiffSequence
import SequenceProcessor
from mplot import MPlot

from ProcessOptions import ProcessOptions
from Worker import Worker

from AviSettings import AviSettings
from AviWriter import AviWriter

from SequenceProcessor import ProcessedSequence
import Plugins

class SequenceDisplay(Ui_SequenceDisplayWnd, PyQt4.QtGui.QMainWindow):
	def __init__(self, parent = None, files=None,loadInRam=False,rawTiffOptions = None):
		PyQt4.QtGui.QMainWindow.__init__(self, parent=parent)
		
		self.setupUi(self)
		self.imageWidgetSetup()
		#l = dir(self.CurrentFrameSlider)
		#for i in l:
		#	print(i)
		self.rawTiffOptions = rawTiffOptions
		self.RoboMainWnd = parent
		self.MaxFrames = 0
		self.CurrentShownFrame = 0
		
		self.displayParameters = DisplayParameters.DisplayPamrameters()
		#print(str(self.displayParameters.displayGrayMax))
		
		#self.roiProfile = None
		#self.roiAverageRecomputeNeeded = False
		
		self.PlayInterframe = 50
		self.IsPlaying = False
		self.timer = QBasicTimer()
		self.FrameImage = None
		
		self.makeConnections()
		
		self.show()
		
		self.tiffFiles = files
		self.loadInRam = loadInRam
		#self.worker = Worker(self, self.tiffLoad, self, True)
		#self.worker.connect(self.worker, SIGNAL("jobDone()"), self, SLOT("tiffLoadFinished()"))
		#self.connect(self, SIGNAL("startWorkerJob()"), self.worker, SLOT("startJob()"))
		#self.worker.start()
		
		#Load plugins
		self.plugins=[]
		#self.emit(SIGNAL("startWorkerJob()"))
		
		for i in Plugins.getPlugins():
			print("Loading plugin " + i["name"])
			plug = Plugins.loadPlugin(i)
			if (plug == None):
				continue
			
			self.plugins.append(plug)
			try:
				#Try to execute load method of the plugin
				self.plugins[-1].load(self)
			except:
				#If it fails, delete the plugin, 
				self.plugins.pop()
				
	
		self.optionsDlg = ProcessOptions(self,saveFolder=os.path.split(files[0])[0])		
		self.tiffSequence = None
		self.processedSequence = None

		if os.path.splitext(files[0])[1] == '.tif':
			self.tiffSequence = TiffSequence(files,self.rawTiffOptions)
			self.processedSequence = ProcessedSequence(self.tiffSequence,self.processedWidget,self.displayParameters,self.optionsDlg.frameOptions,
				self.optionsDlg.displayOptions,self.optionsDlg.timeOptions)
		else:
			for plugin in self.plugins:
				if plugin.associatedFileType == os.path.splitext(files[0])[1]:
					plugin.run(self)
					print('HERE')
		
		if loadInRam:
			self.tiffSequence.loadWholeTiff()
		self.MaxFrames = self.tiffSequence.getFrames()
		self.updateFrameWidgetsRange()
		self.showStatusMessage("Counted " + str(self.MaxFrames) + " frames")
		self.FrameImage, self.FrameData = self.getSequenceFrame(0)
		self.frameWidth = self.tiffSequence.width
		self.frameHeight = self.tiffSequence.height
		self.updateDisplay()
		
		self.setWindowTitle(files[0])
		
		self.colorAutoRadioButton.setChecked(self.displayParameters.autoAdjust)
		

		#rc = self.frameGeometry()
		#dlgRc = self.optionsDlg.geometry()
		#dlgRc.moveTo(rc.right()+5, rc.top())
		#self.optionsDlg.setGeometry(dlgRc)
		self.optionsDlg.show()
		
		self.optionsDlg.frameOptions.lastFrame = self.MaxFrames
		
		self.recomputeFalseColorReference()
		self.makeProcessReferenceConnections(self.optionsDlg)
		
	def tiffLoad(self):
		print("entering tiffLoad from worker")
		self.tiffSequence = TiffSequence(self.files,self.rawOptions)
		if self.loadInRam:
			self.tiffSequence.loadWholeTiff()
		
	def tiffLoadFinished(self):
		print("Tiff load finished")
		self.MaxFrames = self.tiffSequence.getFrames()
		self.updateFrameWidgetsRange()
		self.showStatusMessage("Counted " + str(self.MaxFrames) + " frames")
		self.FrameImage, self.FrameData = self.getSequenceFrame(0)
		
		self.optionsDlg.frameOptions.lastFrame = self.MaxFrames
		
	def imageWidgetSetup(self):
		#raw sequence display widget
		hlay = PyQt4.QtGui.QHBoxLayout(self.ImageFrameWidget)
		imWidget = ImageDisplayWidget(self)
		
		self.imWidget = imWidget
		hlay.addWidget(imWidget)
		
		self.imWidget.createShaders()
		
		#processed sequence display widget
		hlay = PyQt4.QtGui.QHBoxLayout(self.ProcessedFrameWidget)
		processedWidget = ImageDisplayWidget(self)
		
		self.processedWidget = processedWidget
		hlay.addWidget(processedWidget)
		
		self.processedWidget.createShaders()
		
	def makeConnections(self):
		self.connect(self.ForwardFrameButton, SIGNAL("clicked()"), self.getNextSequenceFrame)
		self.connect(self.BackFrameButton, SIGNAL("clicked()"), self.getPreviousSequenceFrame)
		self.connect(self.FirstFrameButton, SIGNAL("clicked()"), self.getFirstSequenceFrame)
		self.connect(self.LastFrameButton, SIGNAL("clicked()"), self.getLastSequenceFrame)
		self.connect(self.PlayButton, SIGNAL("clicked()"), self.playButtonCb)
		self.connect(self.CurrentFrameSlider, SIGNAL("sliderReleased()"), self.currentFrameSliderCb)
		self.connect(self.actionLoad_from_file,SIGNAL("triggered()"),self.loadROISCb)
		self.connect(self.actionSave_to_file,SIGNAL("triggered()"),self.saveROISCb)
		self.connect(self.actionSave_traces,SIGNAL("triggered()"),self.saveRoiComputations)
		self.connect(self.actionForce_recomputation,SIGNAL("triggered()"),self.forceRoiRecomputation)
		
		self.connect(self.actionSave_raw_sequence,SIGNAL("triggered()"),self.saveRawSequence)
		self.connect(self.actionSave_as_avi, SIGNAL("triggered()"), self.saveSequenceAsAvi)
		
		self.connect(self.imWidget, SIGNAL("mousePositionChanged(int, int)"), self.imageNewMousePosition)
		self.connect(self.processedWidget, SIGNAL("mousePositionChanged(int, int)"), self.imageNewMousePosition)
		self.connect(self.imWidget, SIGNAL("roiRecomputeNeeded(bool)"), self.roiRecomputeNeeded)
		self.connect(self.processedWidget, SIGNAL("roiRecomputeNeeded(bool)"), self.roiRecomputeNeeded)
		
		self.connect(self.imWidget, SIGNAL("roiAdded(int)"), self.roiAdded)
		self.connect(self.processedWidget, SIGNAL("roiAdded(int)"), self.roiAdded)
		
		self.connect(self.colorMinSpinBox, SIGNAL("valueChanged(float)"), self.displayMinChangedBox)
		self.connect(self.colorMaxSpinBox, SIGNAL("valueChanged(float)"), self.displayMaxChangedBox)
		self.connect(self.colorMinSlider, SIGNAL("sliderMoved(int)"), self.displayMinChangedSlider)
		self.connect(self.colorMaxSlider, SIGNAL("sliderMoved(int)"), self.displayMaxChangedSlider)
		self.connect(self.colorAutoRadioButton, SIGNAL("toggled(bool)"), self.displayAutoAdjustChanged)
		
		
		
		#menus
		##ROIS
		self.connect(self.actionCompute_Rois, SIGNAL("triggered()"), self.computeRoisCb)
		
	
	def makeProcessReferenceConnections(self, dlg):
		self.connect(dlg.FirstFrameSpinBox, SIGNAL("valueChanged(int)"), self.recomputeFalseColorReference)
		self.connect(dlg.CycleSizeSpinBox, SIGNAL("valueChanged(int)"), self.recomputeFalseColorReference)
		self.connect(dlg.FirstWavelengthSpinBox, SIGNAL("valueChanged(int)"), self.recomputeFalseColorReference)
		self.connect(dlg.SecondWavelengthSpinBox, SIGNAL("valueChanged(int)"), self.recomputeFalseColorReference)
		self.connect(dlg.referenceFrameSpinBox, SIGNAL("valueChanged(int)"), self.recomputeFalseColorReference)
		self.connect(dlg.ProcessTypeComboBox, SIGNAL("currentIndexChanged(int)"), self.recomputeFalseColorReference)
		
		self.connect(dlg.HSVradioButton, SIGNAL("released()"), self.recomputeHSVvalue)
		self.connect(dlg.NomarskiRadioButton,SIGNAL("released()"),self.recomputeHSVvalue)
	def showStatusMessage(self, msg):
		self.statusBar().showMessage(msg)
		
	def changeDisplayGrayMin(self, v):
		v = int(v)
		mn, mx, steps = self.recomputeDisplayRange(v, self.displayParameters.displayGrayMax)
		self.displayParameters.displayGrayMin = v
		self.updateDisplayRangeWidgets(mn, mx, steps)
		
		self.colorMinSpinBox.blockSignals(True)
		self.colorMinSpinBox.setValue(v)
		self.colorMinSpinBox.blockSignals(False)
		
		self.colorMinSlider.blockSignals(True)
		self.colorMinSlider.setValue(v)
		self.colorMinSlider.blockSignals(False)
		
	def changeDisplayGrayMax(self, v):
		v = int(v)
		mn, mx, steps = self.recomputeDisplayRange(self.displayParameters.displayGrayMin, v)
		self.displayParameters.displayGrayMax = v
		self.updateDisplayRangeWidgets(mn, mx, steps)
		
		self.colorMaxSpinBox.blockSignals(True)
		self.colorMaxSpinBox.setValue(v)
		self.colorMaxSpinBox.blockSignals(False)
		
		self.colorMaxSlider.blockSignals(True)
		self.colorMaxSlider.setValue(v)
		self.colorMaxSlider.blockSignals(False)
		
	def displayAutoAdjustChanged(self, v):
		self.displayParameters.autoAdjust = v
		self.updateCurrentFrame()
		
	def changeDisplayColorMin(self, v):
		mn, mx, steps = self.recomputeDisplayRange(float(v), self.displayParameters.displayColorMax)
		self.displayParameters.displayColorMin = float(v)
		#print("changeDisplayColorMin: mn=" + str(mn) + ", mx" + str(mx) + ", steps=" + str(steps))
		self.updateDisplayRangeWidgets(mn, mx, steps)
		
		self.colorMinSpinBox.blockSignals(True)
		self.colorMinSpinBox.setValue(v)
		self.colorMinSpinBox.blockSignals(False)
		
		
		mn, mx, stepSize = self.computeRangeParameters()
		
		if stepSize == 0.0:
			return
		
		self.colorMinSlider.blockSignals(True)
		nv = int((v - mn) / stepSize)
		self.colorMinSlider.setValue(nv)
		self.colorMinSlider.blockSignals(False)
		
	def changeDisplayColorMax(self, v):
		
		mn, mx, steps = self.recomputeDisplayRange(float(self.displayParameters.displayColorMin), float(v))
		self.displayParameters.displayColorMax = float(v)
		self.updateDisplayRangeWidgets(mn, mx, steps)
		
		self.colorMaxSpinBox.blockSignals(True)
		self.colorMaxSpinBox.setValue(v)
		self.colorMaxSpinBox.blockSignals(False)
		
		mn, mx, stepSize = self.computeRangeParameters()
		
		if stepSize == 0.0:
			return
		
		self.colorMaxSlider.blockSignals(True)
		nv = int((v - mn) / stepSize)
		self.colorMaxSlider.setValue(nv)
		self.colorMaxSlider.blockSignals(False)
		
	def displayMinChangedSlider(self, v):
		#print("displayMinSlider changed")
		if self.displayParameters.autoAdjust:
			return
		
		viewType = self.getViewType()
		if viewType == 0:
			self.displayParameters.displayGrayMin = v
			#print("displayMinSlider value " + str(v))
			mn, mx, steps = self.recomputeDisplayRange(self.displayParameters.displayGrayMin, self.displayParameters.displayGrayMax)
		elif viewType == 1:
			mn, mx, stepSize = self.computeRangeParameters()
			self.displayParameters.displayColorMin = mn + v * stepSize
			v = self.displayParameters.displayColorMin
			mn, mx, steps = self.recomputeDisplayRange(self.displayParameters.displayColorMin, self.displayParameters.displayColorMax)
		
		#self.updateDisplayRangeWidgets(mn, mx, steps)
		
		self.colorMinSpinBox.blockSignals(True)
		self.colorMinSpinBox.setValue(v)
		self.colorMinSpinBox.blockSignals(False)
		self.updateCurrentFrame()
		
	def displayMaxChangedSlider(self, v):
		
		#print("displayMaxSlider changed")
		if self.displayParameters.autoAdjust:
			return
		
		viewType = self.getViewType()
		if viewType == 0:
			self.displayParameters.displayGrayMax = v
			#print("displayMaxSlider value " + str(v))
			mn, mx, steps = self.recomputeDisplayRange(self.displayParameters.displayGrayMin, self.displayParameters.displayGrayMax)
		elif viewType == 1:
			mn, mx, stepSize = self.computeRangeParameters()
			self.displayParameters.displayColorMax = mn + v * stepSize
			v = self.displayParameters.displayColorMax
			mn, mx, steps = self.recomputeDisplayRange(self.displayParameters.displayColorMin, self.displayParameters.displayColorMax)
		
		#self.updateDisplayRangeWidgets(mn, mx, steps)
		
		self.colorMaxSpinBox.blockSignals(True)
		self.colorMaxSpinBox.setValue(v)
		self.colorMaxSpinBox.blockSignals(False)
		
		self.updateCurrentFrame()
		
	def displayMinChangedBox(self, v):
		
		if not self.displayParameters.autoAdjust:
			return
		
		viewType = self.getViewType()
		if viewType == 0:
			self.displayParameters.displayGrayMin = v
			mn, mx, steps = self.recomputeDisplayRange(self.displayParameters.displayGrayMin, self.displayParameters.displayGrayMax)
		elif viewType == 1:
			self.displayParameters.displayColorMin = v
			mn, mx, stepSize = self.computeRangeParameters()
			nv = (v - mn) / stepSize
			mn, mx, steps = self.recomputeDisplayRange(self.displayParameters.displayColorMin, self.displayParameters.displayColorMax)
		
		#self.updateDisplayRangeWidgets(mn, mx, steps)
		
		nv = int(nv)
		
		self.colorMinSlider.blockSignals(True)
		self.colorMinSlider.setValue(nv)
		self.colorMinSlider.blockSignals(False)
		self.updateCurrentFrame()
		
	def displayMaxChangedBox(self, v):
		
		if not self.displayParameters.autoAdjust:
			return
		
		viewType = self.getViewType()
		if viewType == 0:
			self.displayParameters.displayGrayMax = v
			mn, mx, steps = self.recomputeDisplayRange(self.displayParameters.displayGrayMin, self.displayParameters.displayGrayMax)
		elif viewType == 1:
			self.displayParameters.displayColorMax = v
			mn, mx, stepSize = self.computeRangeParameters()
			nv = (v - mn) / stepSize
			mn, mx, steps = self.recomputeDisplayRange(self.displayParameters.displayColorMin, self.displayParameters.displayColorMax)
		
		#self.updateDisplayRangeWidgets(mn, mx, steps)
		
		nv = int(nv)
		
		self.colorMaxSlider.blockSignals(True)
		self.colorMaxSlider.setValue(nv)
		self.colorMaxSlider.blockSignals(False)
		self.updateCurrentFrame()
		
	def updateCurrentFrame(self):
		self.FrameImage, self.FrameData = self.getSequenceFrame(self.CurrentShownFrame)
		self.updateDisplay()
		
	def computeRangeParameters(self):
		mn = self.colorMinSpinBox.minimum()
		mx = self.colorMinSpinBox.maximum()
		#print("computeRangeParameters mn=" + str(mn) + ", mx=" + str(mx))
		stepSize = (mx - mn)/self.displayParameters.displayColorSteps
		
		return mn, mx, stepSize
		
	def recomputeDisplayRange(self, l, h):
		#mn = l, mx = h, rng = h - l, steps = 1000
		mn, mx, rng, steps = l, h, h-l, self.displayParameters.displayColorSteps
		if type(mn) == int:
			mn, mx = l - int(rng * 0.1), h + int(rng * 0.1)
			
			if mn < 0:
				mn = 0
				
			if mx > 65535:
				mx = 65535
				
			steps = mx - mn + 1
			#print("mn " + str(mn) + ", mx " + str(mx) + ", steps" + str(steps))
		elif type(mn) == float:
			mn, mx = l - rng*0.1, h + rng*0.1
			#if mn < 0:
				#mn = mn - 1
			#mn = float(int(mn))
			
			#print("float mn " + str(mn) + ", mx " + str(mx) + ", steps" + str(steps))
			
		return mn, mx, steps
			
	def updateDisplayRangeWidgets(self, mn, mx, steps):
		self.colorMinSpinBox.blockSignals(True)
		self.colorMinSpinBox.setRange(mn, mx)
		self.colorMinSpinBox.blockSignals(False)
		
		self.colorMaxSpinBox.blockSignals(True)
		self.colorMaxSpinBox.setRange(mn, mx)
		self.colorMaxSpinBox.blockSignals(False)
		
		self.colorMinSlider.blockSignals(True)
		if type(mn) == int:
			self.colorMinSlider.setRange(mn, mx)
		else:
			self.colorMinSlider.setRange(0, steps)
		self.colorMinSlider.blockSignals(False)
		
		self.colorMaxSlider.blockSignals(True)
		if type(mn) == int:
			self.colorMaxSlider.setRange(mn, mx)
		else:
			self.colorMaxSlider.setRange(0, steps)
		self.colorMaxSlider.blockSignals(False)
	
	def getSequenceFrame(self, n, needQImage = True):
			
		im = self.tiffSequence.getFrame(n)
		h,w = im.shape
		
		if im == None:
			return None
			
		viewType = self.getViewType()
		if viewType == 0:
			if self.displayParameters.autoAdjust:
				self.changeDisplayGrayMin(im.min())
				self.changeDisplayGrayMax(im.max())
		
		self.showStatusMessage("Frame " + str(self.CurrentShownFrame+1) + " of " + str(self.MaxFrames))	
		if viewType == 0:
			tex = self.imWidget.processData(list([im]), list([0]), list([list([self.displayParameters.displayGrayMin, self.displayParameters.displayGrayMax])]))
			return tex, im
		elif viewType == 1:
			if self.displayParameters.autoAdjust:
				f=self.processedSequence.computeProcessedFrame(n)
				
				self.changeDisplayColorMin(f.min())
				self.changeDisplayColorMax(f.max())
			else:
				f=self.processedSequence.computeProcessedFrame(n,returnType ="texture")
			
			if self.optionsDlg.displayOptions.useLUT == 1:
				tex = self.processedSequence.applyColormap(f,w,h)
				if self.displayParameters.autoAdjust == False:
					f=None
				return tex, f
			elif self.optionsDlg.displayOptions.useHSV == 1:
				if self.optionsDlg.FrameByFrameRadioButton.isChecked():
					self.processedSequence.computeValue(im)
				tex = self.processedSequence.HSVImage(f,w,h)	
				if self.displayParameters.autoAdjust == False:
					f=None
					
				return tex, f
			
		return None, None
		
	def getSequenceFrameAsRgb(self, n):
		tex, f = self.getSequenceFrame(n)
		if self.ImageTabWidget.currentIndex() == 0:
			self.imWidget.makeCurrent()
			data = self.imWidget.textureToArray(tex, "uint8RGB")
			self.imWidget.doneCurrent()
		else:
			self.processedWidget.makeCurrent()
			data = self.processedWidget.textureToArray(tex, "uint8RGB")
			self.processedWidget.doneCurrent()
			
		return data
			
		
	def getViewType(self):
		return self.ImageTabWidget.currentIndex()
		
	def getSequenceStartAndStep(self):
		viewType = self.getViewType()
		if viewType == 0:
			return self.optionsDlg.frameOptions.firstFrame - 1, 1
		elif viewType == 1:
			return self.optionsDlg.frameOptions.firstFrame - 1, self.optionsDlg.frameOptions.cycleSize
		
	def updateDisplay(self):
		
		if self.FrameImage == None:
			return
			
		h, w = self.frameHeight, self.frameWidth
			
		if self.ImageTabWidget.currentIndex() == 0:
			self.imWidget.currentDrawData["tex"] = self.FrameImage
			self.imWidget.currentDrawData["width"] = w
			self.imWidget.currentDrawData["height"] = h
			self.imWidget.updateGL()
		else:
			self.processedWidget.currentDrawData["tex"] = self.FrameImage
			self.processedWidget.currentDrawData["width"] = w
			self.processedWidget.currentDrawData["height"] = h
			self.processedWidget.updateGL()
			
		
		
	def getNextSequenceFrame(self):
		first, step = self.getSequenceStartAndStep()
		self.CurrentShownFrame = self.CurrentShownFrame + step
		if self.CurrentShownFrame >= self.MaxFrames:
			self.showStatusMessage("Trying to show frame " + str(self.CurrentShownFrame) + " of " + str(self.MaxFrames) + ". Impossible!!")
			self.CurrentShownFrame = self.CurrentShownFrame - step
			return
			
		self.FrameImage, self.FrameData = self.getSequenceFrame(self.CurrentShownFrame, True)
		
		self.updateDisplay()
		#self.imWidget.updateGL()
		self.updateCurrentFrameWidgets()
		
	def getPreviousSequenceFrame(self):
		first, step = self.getSequenceStartAndStep()
		self.CurrentShownFrame = self.CurrentShownFrame - step
		if self.CurrentShownFrame < 0:
			self.showStatusMessage("Trying to show frame " + str(self.CurrentShownFrame) + " of " + str(self.MaxFrames) + ". Impossible!!")
			self.CurrentShownFrame = self.CurrentShownFrame + step
			return
		
		
		self.FrameImage, self.FrameData = self.getSequenceFrame(self.CurrentShownFrame)
		self.updateDisplay()
		self.updateCurrentFrameWidgets()
		
	def getFirstSequenceFrame(self):
		first, step = self.getSequenceStartAndStep()
		self.CurrentShownFrame = first
		self.FrameImage, self.FrameData = self.getSequenceFrame(self.CurrentShownFrame)
		self.updateDisplay()
		self.updateCurrentFrameWidgets()
		
	def getLastSequenceFrame(self):
		first, step = self.getSequenceStartAndStep()
		self.CurrentShownFrame = ((self.MaxFrames - first) / step - 1) * step + first
		self.FrameImage, self.FrameData = self.getSequenceFrame(self.CurrentShownFrame)
		self.updateDisplay()
		self.updateCurrentFrameWidgets()
		
	def updateCurrentFrameWidgets(self):
		self.CurrentFrameSlider.blockSignals(True)
		self.CurrentFrameSlider.setValue(self.CurrentShownFrame)
		self.CurrentFrameSlider.blockSignals(False)
		
		self.CurrentFrameSpinBox.blockSignals(True)
		self.CurrentFrameSpinBox.setValue(self.CurrentShownFrame)
		self.CurrentFrameSpinBox.blockSignals(False)
	
	def changeCurrentFrameWidget(self,n):
		self.CurrentFrameSlider.blockSignals(True)
		self.CurrentFrameSlider.setValue(n)
		self.CurrentFrameSlider.blockSignals(False)
		
		self.CurrentFrameSpinBox.blockSignals(True)
		self.CurrentFrameSpinBox.setValue(n)
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
		
		self.updateDisplay()
		self.updateCurrentFrameWidgets()
		
	def currentFrameSpinBoxCb(self):
		self.CurrentShownFrame = self.CurrentFrameSpinBox.value()
		self.FrameImage, self.FrameData = self.getSequenceFrame(self.CurrentShownFrame, True)
		
		self.updateDisplay()
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
		if nrois < 1:
			return
		
		if self.displayParameters.roiAverageRecomputeNeeded:
			self.displayParameters.roiProfile = np.zeros((lf, nrois))
		
			for i in xrange(ff, lf, 100):
				tlf = i + 100
				if tlf > lf:
					tlf = lf
				self.displayParameters.roiProfile[i:tlf, 0:nrois] = self.tiffSequence.computeRois(i, tlf)		
				self.showStatusMessage("Processed " + str(tlf) + "/" + str(lf))
				self.update()
				
			self.displayParameters.roiAverageRecomputeNeeded = False	
			
		
			
		##FOR TESTING PURPOSES ONLY
		#fig,ax = oneColumnFigure(addAxes=True)
		#ax.plot(roiProfile)
		#fig.show()
		
		fig = MPlot(self)
		
		rdata, times = SequenceProcessor.applyRoiComputationOptions(self.displayParameters.roiProfile, self.tiffSequence.timesDict.times(), self.optionsDlg.frameOptions, self.tiffSequence.rois)
		
		fig.plot(times,rdata)
		fig.axes.set_xlabel(self.tiffSequence.timesDict.label)
		fig.show()
		return times,rdata
	
	def roiRecomputeNeeded(self, isNeeded):
		self.roiAverageRecomputeNeeded = isNeeded
		#print("roiRecompute is needed " + str(isNeeded))
		
	def roiAdded(self, objId):
		if objId == id(self.imWidget):
			self.processedWidget.rois.append(self.imWidget.rois[-1])
		else:
			self.imWidget.rois.append(self.processedWidget.rois[-1])
			
		self.displayParameters.roiAverageRecomputeNeeded = True
	
	def saveRoiComputations(self):
		fname = QFileDialog.getSaveFileName(self, "Input file name",QString(),"CSV Files (*.csv)")
		
		roiFile = fname.toAscii().data()

		times,rdata = self.computeRoisCb()
		if times.ndim < 2:
			times = np.expand_dims(times,1)
		
		np.savetxt(roiFile, np.hstack((times,rdata)), delimiter="\t")

	def loadROISCb(self):
		
		if self.FrameImage == None:
			return
		
		fname = QFileDialog.getOpenFileName(self, "Select Vimmaging Roi file",QString(),"Vimmaging roi file (*.mat);;Roi and traces data (*.npy)")
		
		roiFile = fname.toAscii().data()
		rois, self.displayParameters.roiProfile, times = SequenceProcessor.loadRoisFromFile(roiFile, self.frameWidth, self.frameHeight)
		for roi in rois:
			self.imWidget.addRoi(roi,fromImageDisplayWidget=False)
		if self.displayParameters.roiProfile is None or self.displayParameters.roiProfile.shape[0]!=self.tiffSequence.getFrames():

			self.displayParameters.roiAverageRecomputeNeeded = True
		else:	
			
			try:
				self.displayParameters.roiAverageRecomputeNeeded = False
				self.computeRoisCb()
			except:
				print("Traces data not valid, ignoring")
				self.displayParameters.roiAverageRecomputeNeeded = True
	
	def saveROISCb(self):
		fname = QFileDialog.getSaveFileName(self, "Input file name",QString(),"Vimmaging roi file (*.mat);;Roi and traces data (*.npy)")
		roiFile = fname.toAscii().data()
		#rois = SequenceProcessor.saveRoisToFile(roiFile,self.imWidget.rois, self.displayParameters.roiProfile, self.tiffSequence.timesDict.times())
		self.processedSequence.saveRoisToFile(roiFile)
		
	def forceRoiRecomputation(self):
		self.displayParameters.roiAverageRecomputeNeeded = True
		self.displayParameters.roiProfile = None
		
	def saveRawSequence(self):
		if self.tiffSequence == None:
			return
			
		fname = QFileDialog.getSaveFileName(self, "Save tif sequence to file", QString(), "Images (*.tif)")
		if not fname.isEmpty():
			self.tiffSequence.saveSequence(fname.toAscii())
	
	def saveSequenceAsAvi(self):
		first, step = self.getSequenceStartAndStep()
		fps = int(round(1.0/(self.tiffSequence.timesDict.dt())))
		self.aviOptions={'fps':fps,'width':self.tiffSequence.getWidth(),'height':self.tiffSequence.getHeight(),
		'fname':'', 'firstFrame':1, 'lastFrame':self.tiffSequence.getFrames()}
		
		aviSettings = AviSettings(parent=self, aviOptions=self.aviOptions)
		aviSettings.exec_()
		
		opt = self.aviOptions
		aviWriter = AviWriter(opt["fname"], (opt["height"], opt["width"]), opt["fps"])
		totalFrames = int(round((opt["lastFrame"] - opt["firstFrame"]+1)/step))
		for i in range(opt["firstFrame"]-1, opt["lastFrame"],step):
			data = self.getSequenceFrameAsRgb(i)

			h,w,k,z = data.shape
			data = data.reshape(h*w,z)
			#data = np.swapaxes(data, 0, 1)
			data = data.reshape(w,h,z)
			#data = data[:,:,::-1]
			#st = 'Saving frame number '+str(i+1) + 'of ' + str(totalFrames)
			#self.showStatusMessage(st)
			aviWriter.addFrame(data)
			
		aviWriter.clearAviHandler()
		
			
	def recomputeFalseColorReference(self):
		#self.displayParameters.falseColorRefFrame = SequenceProcessor.computeReference(self.tiffSequence, self.optionsDlg.frameOptions)
		self.processedSequence.computeReference()
		
	def recomputeHSVvalue(self):
		if self.optionsDlg.NomarskiRadioButton.isChecked():
			fname = QFileDialog.getOpenFileName(self, "Select tiff file",QString(),"Tiff Files (*.tif)")
			fname = fname.toAscii().data()
			self.optionsDlg.backgroundLineEdit.setText(fname)
			nomarski = TiffSequence([fname,])
			#self.displayParameters.HSVvalue = SequenceProcessor.computeValue(nomarski.getFrame(1),(self.tiffSequence.height,self.tiffSequence.width))
			#Try loading the second frame of the nomarski stack (the first one is usually black). If it fails, it may be possible 
			#that the nomarski is a single image
			try:
				self.processedSequence.computeValue(nomarski.getFrame(1))
			except AttributeError:
				self.processedSequence.computeValue(nomarski.getFrame(0))
				
if __name__== "__main__":
	app = PyQt4.QtGui.QApplication(sys.argv)
	window = RoboPy()
	window.show()
	
	sys.exit(app.exec_())

