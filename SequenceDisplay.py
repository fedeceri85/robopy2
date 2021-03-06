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
from TiffSequence import TiffSequence, HDF5Sequence,TimesDict,RawSequence
import SequenceProcessor
#from mplot import MPlot
from plotWindow import plotWindow
from ProcessOptions import ProcessOptions
from Worker import Worker

from AviSettings import AviSettings
from AviWriter import AviWriter

from SaveRawSequenceOptions import SaveRawSequenceOptions

from SequenceProcessor import ProcessedSequence
import Plugins
from scipy.misc import imsave
from  roiAnalysis import MainWindow as rMW
from scipy.io import savemat,loadmat
from progress import progress
from time import sleep
from matplotlib import colors as matCol
from matplotlib import rcParams
import matplotlib.pylab as pl

class SequenceDisplay(Ui_SequenceDisplayWnd, PyQt4.QtGui.QMainWindow):
	def __init__(self, parent = None, files=None,loadInRam=False,rawTiffOptions = None):
		PyQt4.QtGui.QMainWindow.__init__(self, parent=parent)
		self.setupUi(self)
		self.setAcceptDrops(True)

		self.imageWidgetSetup()
		#l = dir(self.CurrentFrameSlider)
		#for i in l:
		#	print(i)
		self.rawTiffOptions = rawTiffOptions
		self.RoboMainWnd = parent
		self.MaxFrames = 0
		self.CurrentShownFrame = 0
		self.setGeometry(0, 0,1300, 1000)

		self.displayParameters = DisplayParameters.DisplayPamrameters()
		#print(str(self.displayParameters.displayGrayMax))
		
		#self.roiProfile = None
		#self.roiAverageRecomputeNeeded = False
		self.currentImage = None
		#self.PlayInterframe = 50
		self.IsPlaying = False
		self.timer = QBasicTimer()
		self.FrameImage = None
			
		self.optionsDlg = ProcessOptions(self,saveFolder=os.path.split(files[0])[0])		
		self.tiffSequence = None
		self.processedSequence = None

		self.makeConnections()
		self.show()
		self.tiffFiles = files
		self.folder = os.path.split(files[0])[0]
		self.loadInRam = loadInRam
		#self.worker = Worker(self, self.tiffLoad, self, True)
		#self.worker.connect(self.worker, SIGNAL("jobDone()"), self, SLOT("tiffLoadFinished()"))
		#self.connect(self, SIGNAL("startWorkerJob()"), self.worker, SLOT("startJob()"))
		#self.worker.start()
		self.playRois = None
		self.drawnRois = []
		#Load plugins
		self.plugins=[]
		self.fig = None
		self.background = None
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
				


		if os.path.splitext(files[0])[1] == '.tif':
			self.tiffSequence = TiffSequence(files,self.rawTiffOptions)
			self.processedSequence = ProcessedSequence(self.tiffSequence,self.processedWidget,self.displayParameters,self.optionsDlg.frameOptions,
				self.optionsDlg.displayOptions,self.optionsDlg.timeOptions)
		elif os.path.splitext(files[0])[1] == '.h5':
			self.tiffSequence = HDF5Sequence(files,self.rawTiffOptions)
			self.processedSequence = ProcessedSequence(self.tiffSequence,self.processedWidget,self.displayParameters,self.optionsDlg.frameOptions,
				self.optionsDlg.displayOptions,self.optionsDlg.timeOptions)			
		elif os.path.splitext(files[0])[1] == '.raw':
			self.tiffSequence = RawSequence(files,self.rawTiffOptions)

			self.processedSequence = ProcessedSequence(self.tiffSequence,self.processedWidget,self.displayParameters,self.optionsDlg.frameOptions,
			self.optionsDlg.displayOptions,self.optionsDlg.timeOptions)	
		else:
			for plugin in self.plugins:
				if plugin.associatedFileType == os.path.splitext(files[0])[1]:
					plugin.run(self)

		
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
		

		rc = self.frameGeometry()
		dlgRc = self.optionsDlg.geometry()
		dlgRc.moveTo(rc.right()+100, rc.top())
		self.optionsDlg.setGeometry(dlgRc)
		self.optionsDlg.show()
		
		self.optionsDlg.frameOptions.lastFrame = self.MaxFrames
		
		self.recomputeFalseColorReference()
		self.makeProcessReferenceConnections(self.optionsDlg)
		self.clipboard = QApplication.clipboard()
		self.roiMonitor = False
		self.currentShownRoi = 0

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
		self.connect(self.CurrentFrameSlider, SIGNAL("sliderMoved(int)"), self.currentFrameSliderCb)
		self.connect(self.actionLoad_from_file,SIGNAL("triggered()"),self.loadROISDialog)
		self.connect(self.actionSave_to_file,SIGNAL("triggered()"),self.saveROISCb)
		self.connect(self.actionSave_traces,SIGNAL("triggered()"),self.saveRoiComputations)
		self.connect(self.actionForce_recomputation,SIGNAL("triggered()"),self.forceRoiRecomputation)
		self.connect(self.actionCopy_filepath_to_clipboard,SIGNAL("triggered()"),self.copyToClipboard)

		self.connect(self.actionSave_raw_sequence,SIGNAL("triggered()"),self.saveRawSequence)
		self.connect(self.actionSave_as_avi, SIGNAL("triggered()"), self.saveSequenceAsAvi)
		self.connect(self.actionSave_as_hd5_table, SIGNAL("triggered()"), self.saveSequenceAsTable)
		self.connect(self.actionSave_current_frame, SIGNAL("triggered()"), self.saveCurrentFrame)
		self.connect(self.actionSave_decorations_as_mask, SIGNAL("triggered()"), self.exportDecoration)


		

		self.connect(self.imWidget, SIGNAL("mousePositionChanged(int, int)"), self.imageNewMousePosition)
		self.connect(self.processedWidget, SIGNAL("mousePositionChanged(int, int)"), self.imageNewMousePosition)
		self.connect(self.imWidget, SIGNAL("roiRecomputeNeeded(bool)"), self.roiRecomputeNeeded)
		self.connect(self.processedWidget, SIGNAL("roiRecomputeNeeded(bool)"), self.roiRecomputeNeeded)
		
		self.connect(self.imWidget, SIGNAL("roiAdded(long)"), self.roiAdded)
		self.connect(self.processedWidget, SIGNAL("roiAdded(long)"), self.roiAdded)
		self.connect(self.imWidget, SIGNAL("roiDeleted(long)"), self.roiDeleted)
		self.connect(self.processedWidget, SIGNAL("roiDeleted(long)"), self.roiDeleted)
		
		self.connect(self.colorMinSpinBox, SIGNAL("valueChanged(float)"), self.displayMinChangedBox)
		self.connect(self.colorMaxSpinBox, SIGNAL("valueChanged(float)"), self.displayMaxChangedBox)
		self.connect(self.colorMinSlider, SIGNAL("sliderMoved(int)"), self.displayMinChangedSlider)
		self.connect(self.colorMaxSlider, SIGNAL("sliderMoved(int)"), self.displayMaxChangedSlider)
		self.connect(self.colorAutoRadioButton, SIGNAL("toggled(bool)"), self.displayAutoAdjustChanged)
		
		self.connect(self.actionAverage,SIGNAL("triggered()"),self.averageCb)
		self.connect(self.actionBack_Projection,SIGNAL("triggered()"),self.backProjCb)

		
		#menus
		##ROIS
		self.connect(self.actionCompute_Rois, SIGNAL("triggered()"), self.computeRoisCb)
		self.connect(self.actionComputeRois_from_list, SIGNAL("triggered()"), self.computeRoisFromListCb)
		self.connect(self.actionDelete_Last, SIGNAL("triggered()"), self.deleteRoi)
		self.connect(self.actionRoi_monitor, SIGNAL("triggered()"), self.showRoiMonitor)
		self.connect(self.actionDelete_number, SIGNAL("triggered()"), self.deleteRoiN)

		self.connect(self.actionRemove_frames, SIGNAL("triggered()"), self.removeFrames)
			
		self.connect(self.actionSpecify_interframe_interval, SIGNAL("triggered()"), self.specify_interframe_interval)
		self.connect(self.actionRoi_scale_factor, SIGNAL("triggered()"), self.roiscaleFactor)
		self.connect(self.actionReset_roi_Colors, SIGNAL("triggered()"), self.resetRoiColors)
		self.connect(self.actionAll_Rois_same_color, SIGNAL("triggered()"), self.allRoisSameColor)
		self.connect(self.actionMake_all_rois_rectangular, SIGNAL("triggered()"), self.rectifyRois)
		self.connect(self.actionDownsample_Roi_Ponts, SIGNAL("triggered()"), self.downSampleRois)
		self.connect(self.actionRearrange_Rois, SIGNAL("triggered()"), self.rearrangeRois)

		##DATABASE
		self.connect(self.actionNew_Database,SIGNAL("triggered()"),self.createNewDatabase)
		self.connect(self.actionOpen_Existing_Database,SIGNAL("triggered()"),self.openDatabase)
		self.connect(self.actionAdd_current_tracks_to_database,SIGNAL('triggered()'),self.addDatasetToDatabase)
		self.connect(self.actionSave_database,SIGNAL('triggered()'),self.saveDatabase)
		self.connect(self.actionRemove_current_dataset,SIGNAL('triggered()'),self.removeLastDataset)

		#
		self.connect(self.optionsDlg.zProjectSpinBox,SIGNAL('valueChanged(int)'),self.zprojectchanged)
		self.connect(self.optionsDlg.movingAverageCheckBox,SIGNAL('stateChanged(int)'),self.movavgchanged)
		self.connect(self.optionsDlg.drawRoiNumberscheckBox,SIGNAL('stateChanged(int)'),self.drawRoiNumberscChanged)


	
	def makeProcessReferenceConnections(self, dlg):
		self.connect(dlg.FirstFrameSpinBox, SIGNAL("valueChanged(int)"), self.recomputeFalseColorReference)
		self.connect(dlg.CycleSizeSpinBox, SIGNAL("valueChanged(int)"), self.recomputeFalseColorReference)
		self.connect(dlg.FirstWavelengthSpinBox, SIGNAL("valueChanged(int)"), self.recomputeFalseColorReference)
		self.connect(dlg.SecondWavelengthSpinBox, SIGNAL("valueChanged(int)"), self.recomputeFalseColorReference)
		self.connect(dlg.referenceFrameSpinBox, SIGNAL("valueChanged(int)"), self.recomputeFalseColorReference)
		self.connect(dlg.ProcessTypeComboBox, SIGNAL("currentIndexChanged(int)"), self.recomputeFalseColorReference)
		
		self.connect(dlg.HSVradioButton, SIGNAL("released()"), self.recomputeHSVvalue)
		self.connect(dlg.NomarskiRadioButton,SIGNAL("released()"),self.recomputeHSVvalue)
		self.connect(dlg.subBackCheckBox,SIGNAL("stateChanged(int)"),self.subBackChanged)


	def showStatusMessage(self, msg):
		self.statusBar().showMessage(msg)
		
	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		out = []
		for url in event.mimeData().urls():
			path = url.toLocalFile().toLocal8Bit().data()
			if os.path.isfile(path):
				out.append(path)
		if out != []:
			self.loadROISCb(out[0])
			

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
		if self.getViewType() ==0:

			if self.currentImage is None:
				self.FrameImage, self.FrameData = self.getSequenceFrame(self.CurrentShownFrame)
			else:
				self.FrameImage, self.FrameData = self.loadImageGray(self.currentImage)
		else:
			self.FrameImage, self.FrameData = self.loadImageProcessed(self.CurrentShownFrame)
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
	
	def getSequenceFrame(self, n, needQImage = True,drawRois=False):
			
		self.currentImage = self.tiffSequence.getFrame(n)
		if self.getViewType() == 0:
			return self.loadImageGray(self.currentImage,needQImage)
		elif self.getViewType() == 1:
			return self.loadImageProcessed(n,needQImage,drawRois=drawRois)

	def loadImageGray(self,im,needQImage=True):
		
		
		
		if im is None:
			return None
			

		if self.displayParameters.autoAdjust:
			self.changeDisplayGrayMin(im.min())
			self.changeDisplayGrayMax(im.max())
	
		self.showStatusMessage("Frame " + str(self.CurrentShownFrame+1) + " of " + str(self.MaxFrames))	
		#if viewType == 0:
		tex = self.imWidget.processData(list([im]), list([0]), list([list([self.displayParameters.displayGrayMin, self.displayParameters.displayGrayMax])]))
		return tex, im
		#else:
		#	return None, None

	def loadImageProcessed(self,n,needQImage=True,drawRois=False):	
		#elif viewType == 1:
		if self.displayParameters.autoAdjust:
			f=self.processedSequence.computeProcessedFrame(n)
			
			self.changeDisplayColorMin(f.min())
			self.changeDisplayColorMax(f.max())
		else:

			f=self.processedSequence.computeProcessedFrame(n,returnType ="texture")
		
		if self.optionsDlg.displayOptions.useLUT == 1:
			h,w = self.tiffSequence.height,self.tiffSequence.width

			tex = self.processedSequence.applyColormap(f,w,h,drawRois=drawRois)
			if self.displayParameters.autoAdjust == False:
				f=None
			return tex, f
		elif self.optionsDlg.displayOptions.useHSV == 1:
			if self.optionsDlg.FrameByFrameRadioButton.isChecked():
				im = self.tiffSequence.getFrame(n)
				self.processedSequence.computeValue(im)

			h,w = self.tiffSequence.height,self.tiffSequence.width
			tex = self.processedSequence.HSVImage(f,w,h,drawRois=drawRois)	
			if self.displayParameters.autoAdjust == False:
				f=None
				
			return tex, f
			
		return None, None


	def getSequenceFrameAsRgb(self, n,drawRois=False):
		tex, f = self.getSequenceFrame(n,drawRois=drawRois)
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

			if self.playRois is not None:
				curr = np.argwhere(self.roiBounds[:,0]==self.CurrentShownFrame).ravel()
				for el in curr:
					self.imWidget.addRoi(self.playRois[el],fromImageDisplayWidget=False,drawRoiNumber=False)
					self.drawnRois.append(el)

				toDelete = []
				for i,el in enumerate(self.drawnRois):
					if self.roiBounds[el,1] <= self.CurrentShownFrame:
						toDelete.append(i)

				toDelete.sort(reverse=True)
				if len(toDelete) > 0:
					self.imWidget.deleteRois(toDelete)
					for el in toDelete:
						self.drawnRois.pop(el)


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
		try:
			if self.optionsDlg.timeOptions.useAssociatedTimes:
				self.fig.marker.setValue(self.tiffSequence.times()[self.CurrentShownFrame]-self.tiffSequence.timesDict[self.optionsDlg.timeOptions.time0Frame])
				self.fig.markerpos = self.tiffSequence.times()[self.CurrentShownFrame]-self.tiffSequence.timesDict[self.optionsDlg.timeOptions.time0Frame]
			elif self.optionsDlg.timeOptions.useInterframeInverval:
				self.fig.marker.setValue((self.tiffSequence.framesDict[self.CurrentShownFrame]- self.optionsDlg.timeOptions.time0Frame)*self.optionsDlg.timeOptions.interframeInterval/1000.0)
				self.fig.markerpos = (self.tiffSequence.framesDict[self.CurrentShownFrame] - self.optionsDlg.timeOptions.time0Frame)*self.optionsDlg.timeOptions.interframeInterval/1000.0
		except:
			pass

	def changeCurrentFrameWidget(self,n):
		self.CurrentFrameSlider.blockSignals(True)
		self.CurrentFrameSlider.setValue(n)
		self.CurrentFrameSlider.blockSignals(False)
		
		self.CurrentFrameSpinBox.blockSignals(True)
		self.CurrentFrameSpinBox.setValue(n)
		self.CurrentFrameSpinBox.blockSignals(False)	
		try:
			if self.optionsDlg.timeOptions.useAssociatedTimes:
				self.fig.marker.setValue(self.tiffSequence.times()[n]-self.tiffSequence.timesDict[self.optionsDlg.timeOptions.time0Frame])
				self.fig.markerpos = self.tiffSequence.times()[n]-self.tiffSequence.timesDict[self.optionsDlg.timeOptions.time0Frame]
			elif self.optionsDlg.timeOptions.useInterframeInverval:
				self.fig.marker.setValue((self.tiffSequence.framesDict[n]- self.optionsDlg.timeOptions.time0Frame)*self.optionsDlg.timeOptions.interframeInterval/1000.0)
				self.fig.markerpos = (self.tiffSequence.framesDict[n] - self.optionsDlg.timeOptions.time0Frame)*self.optionsDlg.timeOptions.interframeInterval/1000.0

		except:
			pass

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
			self.timer.start(self.optionsDlg.timeOptions.PlayInterframe, self)
			self.IsPlaying = True
		else:
			self.timer.stop()
			self.IsPlaying = False
			
	def isLastFrame(self):

		first, step = self.getSequenceStartAndStep()
		last = self.optionsDlg.frameOptions.lastFrame-1

		if self.CurrentShownFrame >= last:#self.MaxFrames -1:
			self.CurrentShownFrame=first
		
		return False
		
	def timerEvent(self, event):
		if self.IsPlaying == True:
			self.getNextSequenceFrame()
			if self.isLastFrame():
				self.timer.stop()
				self.IsPlaying = False
				
	def imageNewMousePosition(self, x, y):
		if self.FrameData is not None:
			imy, imx = self.FrameData.shape
			if imy > y and y >= 0 and imx > x and x >= 0:
				self.showStatusMessage(str(x) + ":" + str(y) + "=" + str(self.FrameData[y][x]))
	
	def averageCb(self):
		optDlg = SaveRawSequenceOptions([1,self.tiffSequence.frames],parent=self)
		
		if optDlg.exec_():
			framesInd = optDlg.getFrameInterval()

		self.computeAverage(framesInd)
		# fig.close()

	def computeAverage(self,framesInd=range(100)):
		self.currentImage = SequenceProcessor.computeAverage(self.tiffSequence,framesInd)
		self.loadImageGray(self.currentImage)
		self.updateDisplay()
		# fig = MPlot(self)
		# fig.imshow(self.currentImage)
		# fig.show()
		fname = os.path.splitext(self.tiffFiles[0])[0]+'_average.tif'
		imsave(fname,self.currentImage)

	def backProjCb(self):
		
		optDlg = SaveRawSequenceOptions([1,self.tiffSequence.frames],parent=self)
		
		if optDlg.exec_():
			framesInd = optDlg.getFrameInterval()
		self.currentImage = SequenceProcessor.computeMax(self.tiffSequence,framesInd)
		self.loadImageGray(self.currentImage)
		self.updateDisplay()
		#fig = MPlot(self)
		#fig.imshow(self.currentImage)
		#fig.show()
		fname = os.path.splitext(self.tiffFiles[0])[0]+'_backproj.tif'
		imsave(fname,self.currentImage)
		#fig.close()

	def getYlabel(self):

		return str(self.optionsDlg.getdispTypeLabels()[self.optionsDlg.frameOptions.displayType])

	def computeRoisCb(self,showplot=True):

		ff = 0
		lf = self.tiffSequence.getFrames()
		
		nrois = len(self.tiffSequence.rois)
		if nrois < 1:
			return
		
		if self.displayParameters.roiAverageRecomputeNeeded:
			self.displayParameters.roiProfile = np.zeros((lf, nrois))
			#if self.tiffSequence.__class__ == HDF5Sequence:
		
			#	self.displayParameters.roiProfile[:, 0:nrois] = self.tiffSequence.computeRois()	

			#else:	
			for i in progress(xrange(ff, lf, 100),"Computing rois...","Cancel"):
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

		if self.optionsDlg.timeOptions.useAssociatedTimes:
			t0 = self.tiffSequence.timesDict[self.optionsDlg.timeOptions.time0Frame]
			timesToPass = np.array(self.tiffSequence.times()) -t0
			lab = self.tiffSequence.timesDict.label
		elif self.optionsDlg.timeOptions.useInterframeInverval:
			timesToPass = (np.array(self.tiffSequence.framesDict.values())-self.optionsDlg.timeOptions.time0Frame)*self.optionsDlg.timeOptions.interframeInterval/1000.0
			lab = 'Time (s)'
		rdata, times = SequenceProcessor.applyRoiComputationOptions(self.displayParameters.roiProfile,timesToPass, self.optionsDlg.frameOptions, self.tiffSequence.rois,self.background)

		if showplot:
			if self.fig is None:
				self.fig = plotWindow(self,self.optionsDlg.scaleBarsCheckBox.isChecked())
			# fig = MPlot(self)
			# fig.plot(times,rdata,linewidth=0.3)
			# fig.axes.set_xlabel(self.tiffSequence.timesDict.label)
			# fig.show()
			colors = []

			for roi in self.tiffSequence.rois:
				colors.append(roi.color.getRgb())

			if self.optionsDlg.roiOptions.traceSpacing != 0.0:
				traceSpacing = self.optionsDlg.roiOptions.traceSpacing
			else:
				traceSpacing = False

			ylabel = self.getYlabel()
			self.fig.plot(times,rdata,xlabel=lab,ylabel = ylabel,colors=colors,scalebars = self.optionsDlg.scaleBarsCheckBox.isChecked(),fixedDiff = traceSpacing,scalebarType=1)
			self.fig.show()

		return times,rdata
	
	def computeRoisFromListCb(self):

		inStr, ok = QInputDialog.getText(self,'Select rois','Comma separated, insert interval as start:end')
		inStr = str(inStr)
		pieces = inStr.split(',')
		out = []
		for piece in pieces:

			if piece.rfind(':') != -1:
				tbegin,tend = map(int, piece.split(':'))
				out.extend(range(tbegin-1,tend-1))
			else:
				piece = [piece,]
				out.append(map(int,piece)[0]-1)

		times,rdata = self.computeRoisCb(False)
		if self.fig is None:
			self.fig = plotWindow()
		
		# fig = MPlot(self)
		# fig.plot(times,rdata,linewidth=0.3)
		# fig.axes.set_xlabel(self.tiffSequence.timesDict.label)
		# fig.show()
		colors = []
		for roi in self.tiffSequence.rois:
			colors.append(roi.color.getRgb())
		colors2 = [colors[i] for i in out ]
		ylabel = self.getYlabel()

		if self.optionsDlg.roiOptions.traceSpacing != 0.0:
			traceSpacing = self.optionsDlg.roiOptions.traceSpacing
		else:
			traceSpacing = False

		self.fig.plot(times,rdata[:,out],xlabel=self.tiffSequence.timesDict.label,ylabel = ylabel,colors=colors2,title=inStr,scalebars = self.optionsDlg.scaleBarsCheckBox.isChecked(),fixedDiff = traceSpacing,scalebarType=1)
		self.fig.show()

	def showNextRoi(self):
		if self.currentShownRoi+1< len(self.tiffSequence.rois):
			self.currentShownRoi = self.currentShownRoi + 1 
			times,rdata = self.computeRoisCb(False)
			if self.fig is None:
				self.fig = plotWindow(self,self.optionsDlg.scaleBarsCheckBox.isChecked())

			ylabel = self.getYlabel()
			self.fig.plot(times,rdata[:,self.currentShownRoi].reshape((len(times),1)),xlabel=self.tiffSequence.timesDict.label,ylabel = ylabel,colors=[self.tiffSequence.rois[self.currentShownRoi].color.getRgb(),],title = 'Roi '+str(self.currentShownRoi+1),scalebars = self.optionsDlg.scaleBarsCheckBox.isChecked())

		else:
			pass
		self.fig.show()

	def showPrevRoi(self):
		if self.currentShownRoi-1>=0 :
			self.currentShownRoi = self.currentShownRoi - 1 
			times,rdata = self.computeRoisCb(False)
			if self.fig is None:
				self.fig = plotWindow(self,self.optionsDlg.scaleBarsCheckBox.isChecked())

			ylabel = self.getYlabel()
			self.fig.plot(times,rdata[:,self.currentShownRoi].reshape((len(times),1)),xlabel=self.tiffSequence.timesDict.label,ylabel = ylabel,colors=[self.tiffSequence.rois[self.currentShownRoi].color.getRgb(),],title = 'Roi '+str(self.currentShownRoi+1),scalebars = self.optionsDlg.scaleBarsCheckBox.isChecked())

		else:
			pass
		self.fig.show()

	def deleteRoi(self, n = -1):
		nRoi = len(self.imWidget.rois)
		if n == -1 and nRoi > 0:
			n = nRoi - 1
		
		if n < 0 or n >= nRoi:
			return
		
		del self.imWidget.rois[n]
		del self.processedWidget.rois[n]
		self.displayParameters.roiAverageRecomputeNeeded = True
		self.roiAverageRecomputeNeeded = True
		
		del self.tiffSequence.rois[n]
		self.imWidget.updateGL()
		self.processedWidget.updateGL()
		
	
	def roiRecomputeNeeded(self, isNeeded):

		self.displayParameters.roiAverageRecomputeNeeded = isNeeded

		self.roiAverageRecomputeNeeded = isNeeded
		#print("roiRecompute is needed " + str(isNeeded))
		
	def roiAdded(self, objId):
		if objId == id(self.imWidget):
			self.processedWidget.rois.append(self.imWidget.rois[-1])
		else:
			self.imWidget.rois.append(self.processedWidget.rois[-1])
			
		self.displayParameters.roiAverageRecomputeNeeded = True
		
	def roiDeleted(self, objId):
		if objId == id(self.imWidget):
			self.processedWidget.rois = self.imWidget.rois[:]
		else:
			self.imWidget.rois = self.processedWidget.rois[:]
			
		self.displayParameters.roiAverageRecomputeNeeded = True
	
	def saveRoiComputations(self):
		fname = QFileDialog.getSaveFileName(self, "Input file name",QString(),"CSV Files (*.csv)")
		
		roiFile = fname.toAscii().data()

		times,rdata = self.computeRoisCb()
		if times.ndim < 2:
			times = np.expand_dims(times,1)
		
		np.savetxt(roiFile, np.hstack((times,rdata)), delimiter="\t")

	
	def loadROISDialog(self):
		if self.FrameImage == None:
			return
		
		fname = QFileDialog.getOpenFileName(self, "Select Vimmaging Roi file",QString(),"Vimmaging roi file (*.mat);;Roi and traces data (*.npy)")
		
		roiFile = fname.toAscii().data()
		self.loadROISCb(roiFile)
	
	def loadROISCb(self,roiFile):
		

		rois, self.displayParameters.roiProfile, times = SequenceProcessor.loadRoisFromFile(roiFile, self.frameWidth, self.frameHeight)
		if rois.__class__ is not tuple:
			self.playRois = None
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
		else:
			self.playRois = rois[0]
			self.roiBounds = rois[1]

	def saveROISCb(self):
		fname = QFileDialog.getSaveFileName(self, "Input file name",QString(),"Vimmaging roi file (*.mat);;Roi and traces data (*.npy)")
		roiFile = fname.toAscii().data()
		#rois = SequenceProcessor.saveRoisToFile(roiFile,self.imWidget.rois, self.displayParameters.roiProfile, self.tiffSequence.timesDict.times())
		self.processedSequence.saveRoisToFile(roiFile)

	def roiscaleFactor(self):
		number, ok = PyQt4.QtGui.QInputDialog.getDouble(self, 'Set Scale Factor','Scale Factor:',1)
 		if ok:
			for i,roi in enumerate(self.imWidget.rois):
				roi.scale(number)
				roi.computePointMap()

				#self.tiffSequence.rois[i].scale(number)
				#self.processedWidget.rois[i].scale(number)

		self.imWidget.updateGL()
		self.processedWidget.updateGL()
		
	def forceRoiRecomputation(self):
		self.displayParameters.roiAverageRecomputeNeeded = True
		self.displayParameters.roiProfile = None
		
	def saveRawSequence(self):
		if self.tiffSequence == None:
			return
			
		fname = QFileDialog.getSaveFileName(self,"Save file",QString(), "Tiff images (*.tif);; HDF5 images (*.h5) ")
		optDlg = SaveRawSequenceOptions([1,self.tiffSequence.frames],parent=self)
		
		if not fname.isEmpty():
			if optDlg.exec_():
				framesInd = optDlg.getFrameInterval()
				compressionLevel = optDlg.getCompressionLevel()

			ext = os.path.splitext(str(fname))[1]
			if ext == '.tif' or ext=='.tiff' or ext =='.TIF' or ext == '.TIFF':
				tiff = TiffSequence(None)
				tiff.saveSequence(fname.toAscii(),sequence=self.tiffSequence,framesInd=framesInd)
			if ext == '.h5' or ext == 'h5f' or ext == '.H5' or ext == '.H5F':
				tiff = HDF5Sequence(None)
				tiff.saveSequence(str(fname.toAscii()),sequence=self.tiffSequence,framesInd=framesInd,filterLevel=compressionLevel)	

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
		for i in progress(range(opt["firstFrame"]-1, opt["lastFrame"],step),"Saving avi","Cancel"):
			data = self.getSequenceFrameAsRgb(i,drawRois=True)

			h,w,k,z = data.shape
			data = data.reshape(h*w,z)
			#data = np.swapaxes(data, 0, 1)
			data = data.reshape(w,h,z)
			#data = data[:,:,::-1]
			#st = 'Saving frame number '+str(i+1) + 'of ' + str(totalFrames)
			#self.showStatusMessage(st)
			aviWriter.addFrame(data)
			
		aviWriter.clearAviHandler()
		
	def saveCurrentFrame(self):
		data = self.getSequenceFrameAsRgb(self.CurrentShownFrame,drawRois=True)
		h,w,k,z = data.shape
		data = data.reshape(h*w,z)
		#data = np.swapaxes(data, 0, 1)
		data = data.reshape(w,h,z)
		fname = os.path.splitext(self.tiffFiles[0])[0]+'_frame'+str(self.CurrentShownFrame)+'.tif'

		imsave(fname,data)

	def saveSequenceAsTable(self):
		import tables as tb
		self.ImageTabWidget.setCurrentIndex(1)
		
		
		fname = QFileDialog.getSaveFileName(self, "Save processed sequence to table", QString(), "Table (*.h5)")
		if not fname.isEmpty():
			fname= str(fname.toAscii())

		first, step = self.getSequenceStartAndStep()
		last = self.optionsDlg.frameOptions.lastFrame-1
		nframes = int(np.floor((last-first)/step))
		
		#Ensure that autoAdjust = True in order to get the array image, not just the texture
		autoAdj = self.displayParameters.autoAdjust
		if self.displayParameters.autoAdjust == False:
			self.displayParameters.autoAdjust = True
		
		t,data=self.getSequenceFrame(0)
		h5file = tb.openFile(fname, mode='w')
		root = h5file.root
		atom = tb.Atom.from_dtype(data.dtype)
		filters = tb.Filters(complevel=9, complib='lzo',shuffle=True)

		x = h5file.createEArray(root,'x',atom,shape=(self.tiffSequence.getHeight(),self.tiffSequence.getWidth(),0),expectedrows=nframes)

		for i in xrange(first,last,step):
			print i
			t,data=self.getSequenceFrame(i)
			ind =  int(np.floor((i-first)/step))
			#x[:,:,ind] = data
			x.append(data.reshape((self.tiffSequence.getHeight(),self.tiffSequence.getWidth(),1)))
		
		self.displayParameters.autoAdjust = autoAdj
		
		h5file.flush()
		h5file.close()
			
	def recomputeFalseColorReference(self):
		#self.displayParameters.falseColorRefFrame = SequenceProcessor.computeReference(self.tiffSequence, self.optionsDlg.frameOptions)
		self.processedSequence.computeReference()
		
	def recomputeHSVvalue(self):
		if self.optionsDlg.NomarskiRadioButton.isChecked():

			fname = QFileDialog.getOpenFileName(self, "Select tiff file",QString(),"Tiff images (*.tif);; HDF5 images (*.h5 *.hf5)")
			fname = fname.toAscii().data()
			self.optionsDlg.backgroundLineEdit.setText(fname)
			if os.path.splitext(fname)[1] == '.tif':
				nomarski = TiffSequence([fname,])
			elif os.path.splitext(fname)[1] == '.h5':
				nomarski = HDF5Sequence([fname,])
			#self.displayParameters.HSVvalue = SequenceProcessor.computeValue(nomarski.getFrame(1),(self.tiffSequence.height,self.tiffSequence.width))
			#Try loading the second frame of the nomarski stack (the first one is usually black). If it fails, it may be possible 
			#that the nomarski is a single image
			try:
				self.processedSequence.computeValue(nomarski.getFrame(0))
			except AttributeError,KeyError:
				print("Can't load nomarski")
				#self.processedSequence.computeValue(nomarski.getFrame(1))
				
	def copyToClipboard(self):
		self.clipboard.setText(self.tiffSequence.fileName[0])
		#event = QtCore.QEvent(QtCore.QEvent.Clipboard)
		#app.sendEvent(clipboard, event)
	
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_N:
			try:
				self.RoboMainWnd.RoboActionOpen_Next()
			except:
				pass
		elif event.key() == Qt.Key_P:
			try:
				self.RoboMainWnd.RoboActionOpen_Prev()
			except:
				passw
		
		elif event.key() == Qt.Key_Space:
			self.playButtonCb()

		elif event.key() == Qt.Key_Q:
			self.showPrevRoi()
		elif event.key() == Qt.Key_W:
			self.showNextRoi()
		elif event.key() == Qt.Key_E:
			self.computeRoisCb(True)
		elif event.key() == Qt.Key_R:
			self.computeRoisFromListCb()

		elif event.key() == Qt.Key_A:
			endFrame = self.CurrentShownFrame + 100
			if endFrame >= self.tiffSequence.getFrames():
				endFrame = self.tiffSequence.getFrames()
			self.computeAverage(range(self.CurrentShownFrame,endFrame))

		elif event.key() == Qt.Key_R:

			self.computeRoisFromListCb()
		elif event.key() == Qt.Key_S:
			self.saveCurrentFrame()


	def showRoiMonitor(self):
		self.roiAnal = rMW(self)
		self.roiMonitor = True

	
	def deleteRoiN(self):
		number, ok = PyQt4.QtGui.QInputDialog.getInt(self, 'Delete Roi','Roi number:',1)
 		if ok:
			self.imWidget.deleteRoi(number-1)
		
	def closeEvent(self, event):
        # do stuff
		self.tiffSequence.close()
		self.optionsDlg.close()
		if self.fig is not None:
			self.fig.close()
		#sleep(3)

		event.accept()


	def removeFrames(self):
		inStr, ok = QInputDialog.getText(self,'Select frames to be removed','Comma separated, insert interval as start:end')
		inStr = str(inStr)
		pieces = inStr.split(',')
		out = []
		for piece in pieces:

			if piece.rfind(':') != -1:
				tbegin,tend = map(int, piece.split(':'))
				out.extend(range(tbegin,tend))
			else:
				piece = [piece,]
				out.append(map(int,piece)[0])

		self.tiffSequence.removeFramesFromList(out)
		self.tiffLoadFinished()

	def specify_interframe_interval(self):
		inStr, ok = QInputDialog.getDouble(self,'Select interframe interval','in seconds',0.1,decimals=3)
		indices = np.array(self.tiffSequence.framesDict.values())
		self.tiffSequence.timesDict = TimesDict(zip(np.arange(self.tiffSequence.getFrames()),indices*inStr))
		self.tiffSequence.timesDict.label = 'Time (s)'


	def createNewDatabase(self):
		self.sampleDatabase = './tools/sampleDatabase.mat'
		sample = loadmat(self.sampleDatabase)['database']
		self.RoboMainWnd.database = np.empty((1,0),dtype=sample.dtype)	
		#self.database = self.RoboMainWnd.database

		print("New database created")

	def openDatabase(self):
		
		fname = QFileDialog.getOpenFileName(self, "Select Vimmaging database",QString(),"Vimmaging database (*.mat)")
		dbfile = fname.toAscii().data()
		self.RoboMainWnd.database = loadmat(dbfile)['database']
		print("Opened database "+dbfile)

	def addDatasetToDatabase(self):
		self.sampleDatabase = './tools/sampleDatabase.mat'
		sample = loadmat(self.sampleDatabase)['database']
		self.dataset = np.empty((1,1),dtype=sample.dtype)

		self.dataset['peakData'] = np.empty((1,1))
		self.dataset['minData'] = np.empty((1,1))
		self.dataset['minPeakDistance'] = np.array([[10]])
		self.dataset['maxLowerSpan'] = np.array([[100]])
		self.dataset['locDist'] = np.empty((1,1))
		self.dataset['sequenceFileName'] = np.array([unicode(self.tiffFiles[0])])
		self.dataset['sequenceName'] =  np.array([u'prova.mat'])
		self.dataset['roiFileName'] =np.array([u'prova.mat'])
		self.dataset['vecData'] = np.empty((1,1))
		self.dataset['oldVecData'] = np.empty((1,1))
		#self.dataset['roiArea'] = np.empty((1,1))
		self.dataset['t'] = np.empty((1,1))
		self.dataset['peakCount'] = np.array([[0.0]])
		#self.dataset['maxAmpInRoi'] = np.empty((1,1))
		self.dataset['activeRois'] = np.empty((1,1))
	
		self.dataset['masterRoi'] = np.empty((1,1))
		self.dataset['ROIS'] = np.empty((1,1))

		self.dataset['stereociliaLine'] = np.empty((1,1))
		self.dataset['Linescale'] = np.empty((1,1))
		self.dataset['admittedPeakPercentage'] = np.array([[0.01]])
		self.dataset['highPassFreq'] = np.array([[0.2]])
		self.dataset['highPassFilterOnOff'] = np.array([[0]])
		self.dataset['dataThresholdOnOff'] = np.array([[0]])
		self.dataset['dataThresholdVal'] =  np.array([[0]])
		self.dataset['freqData'] = np.empty((1,1))
		self.dataset['peakFreqAvg'] = np.empty((1,1))
		self.dataset['peakFreqStd'] = np.empty((1,1))
		self.dataset['oscillationDurration'] = np.empty((1,1))
		self.dataset['ampData'] = np.empty((1,1))
		self.dataset['peakAmpAvg'] = np.empty((1,1))
		self.dataset['peakAmpStd'] = np.empty((1,1))

		#self.dataset['vecData'] = []
		#self.dataset['oldVecData'] = []
		if self.displayParameters.roiProfile is not None:
			rdata, times = SequenceProcessor.applyRoiComputationOptions(self.displayParameters.roiProfile, self.tiffSequence.times(), self.optionsDlg.frameOptions, self.tiffSequence.rois)
			self.dataset['vecData'][0,0] = rdata.T
			self.dataset['oldVecData'][0,0] = rdata.T
			self.dataset['t'][0,0] = np.double(times)
			self.dataset['activeRois'][0,0] = np.ones(rdata.shape[1])
			roiArea = np.array([r.mapSize for r in self.tiffSequence.rois])
			roiArea = roiArea.reshape((1,roiArea.size))
			self.dataset['roiArea'][0,0] = roiArea.astype(np.float)
			self.dataset['maxAmpInRoi'][0,0] = np.ones((1,rdata.shape[1]))
		
			if self.RoboMainWnd.database is None:
				self.createNewDatabase()
			self.RoboMainWnd.database = np.hstack((self.RoboMainWnd.database,self.dataset))

			print("New dataset added. This is the dataset number "+str(self.RoboMainWnd.database.shape[1]))
		else:
			print("No dataset added to database")

	def saveDatabase(self):
		fname = QFileDialog.getSaveFileName(self, "Input file name",QString(),"Vimmaging database (*.mat)")
		dbfile= fname.toAscii().data()
		if self.RoboMainWnd.database is not None:
			savemat(dbfile,{'database':self.RoboMainWnd.database})

	def removeLastDataset(self):
		if self.RoboMainWnd.database is not None:
			self.RoboMainWnd.database = self.RoboMainWnd.database[:,:-1]
			print("Dataset removed. "+str(self.RoboMainWnd.database.shape[1])+ " datasets left in database")	

	def zprojectchanged(self,n):
		self.getFirstSequenceFrame()

		self.tiffSequence.options['zproject'] = n
		ma = self.optionsDlg.movingAverageCheckBox.isChecked()
		self.tiffSequence.applyZproject(movingAverage=ma)
		self.tiffLoadFinished()
		self.forceRoiRecomputation()
		self.optionsDlg.subBackLineEdit.setText('ZPROJECT CHANGED RELOAD BACKGROUND')	
		self.optionsDlg.subBackCheckBox.setChecked(False)
	def movavgchanged(self,state):
		self.getFirstSequenceFrame()
		self.tiffSequence.applyZproject(movingAverage = True)
		self.tiffLoadFinished()
		self.forceRoiRecomputation()
		self.optionsDlg.subBackLineEdit.setText('ZPROJECT CHANGED RELOAD BACKGROUND')	
		self.optionsDlg.subBackCheckBox.setChecked(False)	

	def subBackChanged(self,state):
		if self.optionsDlg.subBackCheckBox.isChecked():

			fname = QFileDialog.getOpenFileName(self, "Select a roi file to use as background",QString(self.folder),"Numpy (*.npy);;Vimmaging roi (*.mat)")
			fname = fname.toAscii().data()
			self.optionsDlg.subBackLineEdit.setText(fname)
			p,roi,t = SequenceProcessor.loadRoisFromFile(fname,None,None)
			self.background = roi
			if self.background.size != self.tiffSequence.frames:
				print("Error, wrong number of frames in the background trace")
				self.background = None
				self.optionsDlg.subBackLineEdit.setText('')
				self.optionsDlg.subBackCheckBox.setChecked(False)	
		else:
			self.optionsDlg.subBackLineEdit.setText('')
			self.background = None

	def exportDecoration(self):

		img2 = self.currentImage.copy()
		# self.currentImage = np.ones(img2.shape)*(1E16-1)
		# self.loadImageGray(self.currentImage)
		# self.updateDisplay()

		pl.imshow(img2,cmap=pl.cm.gray)
		#colors = ['r','r','r','b','g']

		for j,roi in enumerate(self.imWidget.rois):
			x = []
			y = []
		#    roi.downsample(7)
			for i in xrange(roi.size()):
				p = roi.point(i)
				x.append(p.x())
				y.append(p.y())
			x.append(roi.point(0).x())
			y.append(roi.point(0).y())

			xc,yc = roi.computeMassCenter()
			pl.text(xc,yc,str(j+1),color = np.array(roi.color.getRgb()[:3])/255.0)
			pl.plot(x,y,color=np.array(roi.color.getRgb()[:3])/255.0,linewidth=2)
		#plt.gca().invert_yaxis()
		#axis('equal')
		pl.xlim((0,img2.shape[1]))
		pl.ylim((img2.shape[0]-1,0))
		a = pl.plt.gca()
		a.yaxis.set_visible(False)
		a.xaxis.set_visible(False)


	def resetRoiColors(self):
		colorCycle =  rcParams["axes.color_cycle"]
		
		for roi in self.tiffSequence.rois:
			roiCol = matCol.colorConverter.to_rgb(colorCycle[roi.ordinal % len(colorCycle)])
				
			c = QColor()
			c.setRgbF(roiCol[0], roiCol[1], roiCol[2],1)
			roi.color = c
		self.imWidget.updateGL()	
		self.processedWidget.updateGL()

	def allRoisSameColor(self):
		roiCol = self.optionsDlg.roiOptions.roiColor
		c = QColor()
		c.setRgbF(roiCol[0], roiCol[1], roiCol[2],1)
		for roi in self.tiffSequence.rois:
			roi.color = c
		self.imWidget.updateGL()	
		self.processedWidget.updateGL()

	def drawRoiNumberscChanged(self):
		self.imWidget.updateGL()	
		self.processedWidget.updateGL()

	def rectifyRois(self):
		if self.optionsDlg.roiOptions.roiSize == 0:
			d = 10
		else:
			d = self.optionsDlg.roiOptions.roiSize
		for roi in self.imWidget.rois:
			x,y = roi.computeMassCenter()
			roi.setPoints([x-d/2,y-d/2,x+d/2,y-d/2,x+d/2,y+d/2,x-d/2,y+d/2])
			roi.clearPointMap()
			roi.computePointMap()
		self.imWidget.updateGL()	
		self.processedWidget.updateGL()		
		self.roiRecomputeNeeded(True)

	def downSampleRois(self):
		number, ok = PyQt4.QtGui.QInputDialog.getInt(self, 'Downsample roi','Factor:',1)
 		if ok:
 			for roi in self.imWidget.rois:
				roi.downsample(number)
				roi.clearPointMap()
				roi.computePointMap()
		self.imWidget.updateGL()	
		self.processedWidget.updateGL()		
		self.roiRecomputeNeeded(True)
					
	def rearrangeRois(self):
		inStr, ok = QInputDialog.getText(self,'Select rois order','Comma separated, insert interval as start:end')
		inStr = str(inStr)
		pieces = inStr.split(',')
		out = []
		for piece in pieces:

			if piece.rfind(':') != -1:
				tbegin,tend = map(int, piece.split(':'))
				out.extend(range(tbegin-1,tend-1))
			else:
				piece = [piece,]
				out.append(map(int,piece)[0]-1)

		self.imWidget.sortRois(out)




if __name__== "__main__":
	app = PyQt4.QtGui.QApplication(sys.argv)
	window = RoboPy()
	window.show()
	
	sys.exit(app.exec_())

