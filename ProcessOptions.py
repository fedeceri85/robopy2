import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ProcessOptionsGui import Ui_ProcessOptionsDlg
import cPickle
class Properties(object):
	
	def __init__(self, parent = None):
		self.parentWidget = parent
		self.widgetIds = list()
		self.widgetNames = list()
	
	def add(self, name, value, obj=None):
		fget = lambda self: self._get_property(name)
		fset = lambda self, value: self._set_property(name, value)
		
		
		setattr(self, '_obj_' + name, obj)
		setattr(self.__class__, name, property(fget, fset))
		setattr(self, '_' + name, value)
		
		self.widgetIds.append(obj)
		self.widgetNames.append(name)
		
		if hasattr(obj, "valueChanged"):
			if type(obj) == QDoubleSpinBox:	
				self.parentWidget.connect(obj, SIGNAL("valueChanged(double)"), self._widget_changed)
			elif type(obj) == QSpinBox:
				self.parentWidget.connect(obj, SIGNAL("valueChanged(int)"), self._widget_changed)
			else:
				print("class Properties: Unknown type of widget!")
		elif hasattr(obj, "sliderReleased"):
			self.parentWidget.connect(obj, SIGNAL("sliderReleased()"), self._widget_changed)
		elif hasattr(obj, "currentIndexChanged"):
			self.parentWidget.connect(obj, SIGNAL("currentIndexChanged(int)"), self._widget_changed)
		elif hasattr(obj, "toggled"):
			self.parentWidget.connect(obj, SIGNAL("toggled(bool)"), self._widget_changed)
		
		self._set_property(name, value)
		
	def _set_property(self, name, value):
		setattr(self, '_' + name, value)
		obj = getattr(self, '_obj_' + name)
		if obj != None:
			obj.blockSignals(True)

			if hasattr(obj, "setValue"):
				obj.setValue(value)
			elif hasattr(obj, "setCurrentIndex"):
				obj.setCurrentIndex(value)
			elif hasattr(obj, "setChecked"):
				if value == 0:
					obj.setChecked(False)
				else:
					obj.setChecked(True)
				
			obj.blockSignals(False)
			self.parentWidget.valueDict[name] = value


			
	def _get_property(self, name):
		return getattr(self, '_' + name)
		
	def _widget_changed(self, value=None):
		obj = self.parentWidget.sender()
		
		if obj in self.widgetIds:
			name = self.widgetNames[self.widgetIds.index(obj)]
		else:
			return
		
		if hasattr(obj, "setChecked"):
			if value:
				value = 1
			else:
				value = 0
		elif obj.__class__.__name__ == "QSlider":
			value = obj.value()
					
		self.parentWidget.valueDict[name] = value

		cPickle.dump(self.parentWidget.valueDict,open(self.parentWidget.saveFile,'w'))

		setattr(self, '_' + name, value)
		#print("widget " + str(obj) + " changed value to " + str(value))
			

class ProcessOptions(Ui_ProcessOptionsDlg, QDialog):
	def __init__(self, parent=None,saveFolder=None):
		QDialog.__init__(self, parent=parent)
		self.setupUi(self)
		self.valueDict = {}	
		if saveFolder is not None:
			self.saveFile = os.path.join(saveFolder,'roboPySave')
		else:
			self.saveFile = None
		self.frameOptions = self.initFrameOptions()
		self.timeOptions = self.initTimeOptions()
		self.displayOptions = self.initDisplayOptions()
		self.roiOptions = self.initRoiOptions()

		


	def sequenceChangedTab(self, idx):
		self.PO_TabWidget.setCurrentIndex(idx)
	
	
	def initFrameOptions(self):
		fo = Properties(self)
		try:
			d=cPickle.load(open(self.saveFile,'r'))
			fo.add('firstFrame', d['firstFrame'], self.FirstFrameSpinBox)
			fo.add('lastFrame', d['lastFrame'], self.LastFrameSpinBox)
			fo.add('cycleSize', d['cycleSize'], self.CycleSizeSpinBox)
			fo.add('firstWavelength', d['firstWavelength'], self.FirstWavelengthSpinBox)
			fo.add('secondWavelength', d['secondWavelength'], self.SecondWavelengthSpinBox)
			fo.add('processType', d['processType'], self.ProcessTypeComboBox)
			fo.add('displayType', d['displayType'], self.DisplayTypeComboBox)
			fo.add('referenceFrames', d['referenceFrames'], self.referenceFrameSpinBox)
			fo.add('zproject', d['zproject'], self.zProjectSpinBox)
			fo.add('movingAverage',d['movingAverage'],self.movingAverageCheckBox)
			
		except:	
			fo.add('firstFrame', 1, self.FirstFrameSpinBox)
			fo.add('lastFrame', 1, self.LastFrameSpinBox)
			fo.add('cycleSize', 1, self.CycleSizeSpinBox)
			fo.add('firstWavelength', 1, self.FirstWavelengthSpinBox)
			fo.add('secondWavelength', 0, self.SecondWavelengthSpinBox)
			fo.add('processType', 0, self.ProcessTypeComboBox)
			fo.add('displayType', 0, self.DisplayTypeComboBox)
			fo.add('referenceFrames', 4, self.referenceFrameSpinBox)
			fo.add('zproject', 1, self.zProjectSpinBox)
			fo.add('movingAverage',0,self.movingAverageCheckBox)


		self.connect(self.ProcessTypeComboBox, SIGNAL("currentIndexChanged(int)"), self.processTypeChangedCb)
		return fo
		
	def processTypeChangedCb(self, value):
		dispTypeLabels = self.getdispTypeLabels()
		for i in xrange(0,self.DisplayTypeComboBox.count()):	
			self.DisplayTypeComboBox.setItemText(i, dispTypeLabels[i])
		
		self.frameOptions.displayType = 0
		
		#print("processTypeChangedCb ")
	def getdispTypeLabels(self):
		dispTypeLabels = QStringList()
		value = self.frameOptions.processType
		if value == 0:
			dispTypeLabels.append("F")
			dispTypeLabels.append("dF")
			dispTypeLabels.append("dF/F0")
		elif value == 1:
			dispTypeLabels.append("R")
			dispTypeLabels.append("dR")
			dispTypeLabels.append("dR/R0")
		return dispTypeLabels
		
	def initTimeOptions(self):
		fo = Properties(self)
		try:
			d=cPickle.load(open(self.saveFile,'r'))
			fo.add('useAssociatedTimes', d['useAssociatedTimes'], self.associatedTimesRadioButton)
			fo.add('useInterframeInverval', d['useInterframeInverval'], self.userInterframeRadioButton)
			fo.add('interframeInterval', d['interframeInterval'], self.interframeIntervalSpinBox)
			fo.add('frameBasedTimes', d['frameBasedTimes'], self.FrameBasedRadioButton)
			fo.add('time0Frame',d['time0Frame'], self.time0SpinBox)
			fo.add('displayTimeStamp',d['displayTimeStamp'],self.displayTimesCheckBox)
			fo.add('fontSize',d['fontSize'],self.fontSizeSpinBox)
			fo.add('xOffset',d['xOffset'],self.xOffsetSpinBox)
			fo.add('yOffset',d['yOffset'],self.yOffsetSpinBox)
			fo.add('PlayInterframe',d['PlayInterframe'],self.PlayInterframeSpinBox)
			fo.add('decimalPlaces',d['decimalPlaces'],self.decimalPlacesSpinBox)

			
		except:	
			fo.add('useAssociatedTimes', 1, self.associatedTimesRadioButton)
			fo.add('useInterframeInverval', 0, self.userInterframeRadioButton)
			fo.add('interframeInterval', 40.0, self.interframeIntervalSpinBox)
			fo.add('frameBasedTimes', 0, self.FrameBasedRadioButton)
			fo.add('time0Frame', 0, self.time0SpinBox)
			fo.add('displayTimeStamp',1,self.displayTimesCheckBox)
			fo.add('fontSize',12,self.fontSizeSpinBox)
			fo.add('xOffset',50,self.xOffsetSpinBox)
			fo.add('yOffset',50,self.yOffsetSpinBox)
			fo.add('PlayInterframe',50,self.PlayInterframeSpinBox)
			fo.add('decimalPlaces',2,self.decimalPlacesSpinBox)
			
		return fo
	
	def initDisplayOptions(self):
		fo = Properties(self)
		try:
			d=cPickle.load(open(self.saveFile,'r'))
			fo.add('useLUT', d['useLUT'], self.LUTradioButton)
			fo.add('lutMapId',  d['lutMapId'], self.ColorMapcomboBox)
			fo.add('useHSV',  d['useHSV'], self.HSVradioButton)
			fo.add('hsvSaturation',  d['hsvSaturation'], self.saturationSpinBox)
			fo.add('enlargeToBackground', d['enlargeToBackground'], self.enlargeToBckCheckBox)
			fo.add('medianFilterOn',  d['medianFilterOn'], self.medianFilterCheckbox)
			fo.add('gaussianFilterOn',  d['gaussianFilterOn'], self.gaussianFilterCheckbox)
			fo.add('gammah',  d['gammah'], self.gammaHSpinBox)
			fo.add('FrameByFrameBackground', d['FrameByFrameBackground'],self.FrameByFrameRadioButton)
			fo.add('NomarskiBackground', d['NomarskiBackground'],self.NomarskiRadioButton)
			
			fo.add('displayScalebar', d['displayScalebar'],self.scalebarCheckBox)
			fo.add('textOnScalebar',d['textOnScalebar'],self.textOnScalebarCheckBox)
			fo.add('scaleBarScaleFactor', d['scaleBarScaleFactor'],self.sbScaleFactorSpinBox)
			fo.add('scaleBarLength', d['scaleBarLength'],self.sbLengthSpinBox)
			fo.add('scaleBarFontSize', d['scaleBarFontSize'],self.sbFontSizeSpinBox)
			fo.add('scaleBarXOffset', d['scaleBarXOffset'],self.sbXOffsetSpinBox)
			fo.add('scaleBarYOffset', d['scaleBarYOffset'],self.sbYOffsetSpinBox)
			fo.add('scaleBarLineSize', d['scaleBarLineSize'],self.lineSizeSpinBox)
			fo.add('hsvcutoff', d['hsvcutoff'],self.hsvcutoffSpinBox)
			
			
		except:
			fo.add('useLUT', 1, self.LUTradioButton)
			fo.add('lutMapId', 0, self.ColorMapcomboBox)
			fo.add('useHSV', 0, self.HSVradioButton)
			fo.add('hsvSaturation', 1.0, self.saturationSpinBox)
			fo.add('enlargeToBackground', 0, self.enlargeToBckCheckBox)
			fo.add('medianFilterOn', 0, self.medianFilterCheckbox)
			fo.add('gaussianFilterOn', 0, self.gaussianFilterCheckbox)
			fo.add('gammah',  1.0, self.gammaHSpinBox)
			fo.add('FrameByFrameBackground',1,self.FrameByFrameRadioButton)
			fo.add('NomarskiBackground',0,self.NomarskiRadioButton)
			
			fo.add('displayScalebar',0,self.scalebarCheckBox)
			fo.add('textOnScalebar',0,self.textOnScalebarCheckBox)
			fo.add('scaleBarScaleFactor',0.47,self.sbScaleFactorSpinBox)
			fo.add('scaleBarLength',25.0,self.sbLengthSpinBox)
			fo.add('scaleBarFontSize',12.0,self.sbFontSizeSpinBox)
			fo.add('scaleBarXOffset',50,self.sbXOffsetSpinBox)
			fo.add('scaleBarYOffset',50,self.sbYOffsetSpinBox)
			fo.add('scaleBarLineSize',10,self.lineSizeSpinBox)
			fo.add('hsvcutoff',0.47,self.hsvcutoffSpinBox)
			
		self.connect(self.HSVradioButton,SIGNAL('toggled(bool)'),self.HSVchanged)

		return fo
	def initRoiOptions(self):
		fo = Properties(self)
		try:
			d=cPickle.load(open(self.saveFile,'r'))
			fo.add('rectangularRois', d['rectangularRois'], self.rectangularRoisCheckBox)
			fo.add('semicircularRois', d['semicircularRois'], self.semicircularRoisCheckBox)
			fo.add('freehandRois', d['freehandRois'], self.freehandRoisCheckBox)

			fo.add('polygonalRois', d['polygonalRois'], self.polygonalRoisCheckBox)
			fo.add('roiSameSize', d['roiSameSize'], self.roiSameSizeCheckBox)
			fo.add('roiSize',d['roiSize'],self.roiSizeSpinBox)
			fo.add('lockRoiPositions',d['lockRoiPositions'],self.lockRoiPositionCheckBox)
			fo.add('scaleBarsCheckBox',d['scaleBarsCheckBox'],self.scaleBarsCheckBox)

			fo.add('automaticColor',d['automaticColor'],self.autoColorRadioButton)
			fo.add('setColor',d['setColor'],self.setColorradioButton)
			fo.add('drawRoiNumbers',d['drawRoiNumbers'],self.drawRoiNumberscheckBox)


		except:
			fo.add('rectangularRois', 1, self.rectangularRoisCheckBox)
			fo.add('semicircularRois',0, self.semicircularRoisCheckBox)
			fo.add('freehandRois', 0, self.freehandRoisCheckBox)
			fo.add('polygonalRois', 0, self.polygonalRoisCheckBox)
			fo.add('roiSameSize', 0, self.roiSameSizeCheckBox)
			fo.add('roiSize',0,self.roiSizeSpinBox)
			fo.add('lockRoiPositions',0,self.lockRoiPositionCheckBox)
			fo.add('scaleBarsCheckBox',0,self.scaleBarsCheckBox)
			fo.add('automaticColor',1,self.autoColorRadioButton)
			fo.add('setColor',0,self.setColorradioButton)
			fo.add('drawRoiNumbers',1,self.drawRoiNumberscheckBox)

		fo.add('roiColor',[1.0,0,0],None)
		self.connect(self.chooseColorButton,SIGNAL('clicked()'),self.chooseColor)
		return fo

	def HSVchanged(self):
		if self.HSVradioButton.isChecked():
			self.HSVbackGroupBox.setEnabled(True)
			self.saturationLabel.setEnabled(True)
			self.saturationSpinBox.setEnabled(True)
		else:
			self.HSVbackGroupBox.setEnabled(False)
			self.saturationLabel.setEnabled(False)
			self.saturationSpinBox.setEnabled(False)

	def chooseColor(self):
		col = QColorDialog.getColor()
		if col.isValid():
			self.roiOptions.roiColor = col.getRgbF()[:3]
			self.chooseColorButton.setStyleSheet("QWidget { background-color: %s }"% col.name())
	def applyWidgetValueWithoutSignal(self, obj, v):
		obj.blockSignals(True)
		obj.setValue(v)
		obj.blockSignals(False)
