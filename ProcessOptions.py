import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ProcessOptionsGui import Ui_ProcessOptionsDlg

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
			self.parentWidget.connect(obj, SIGNAL("valueChanged(int)"), self._widget_changed)
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
					
		
		setattr(self, '_' + name, value)
		#print("widget " + str(obj) + " changed value to " + str(value))
			

class ProcessOptions(Ui_ProcessOptionsDlg, QDialog):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent=parent)
		self.setupUi(self)
		
		self.frameOptions = self.initFrameOptions()
		self.timeOptions = self.initTimeOptions()
		self.displayOptions = self.initDisplayOptions()
       
	def sequenceChangedTab(self, idx):
		self.PO_TabWidget.setCurrentIndex(idx)
		
	def initFrameOptions(self):
		fo = Properties(self)
		fo.add('firstFrame', 1, self.FirstFrameSpinBox)
		fo.add('lastFrame', 1, self.LastFrameSpinBox)
		fo.add('cycleSize', 1, self.CycleSizeSpinBox)
		fo.add('firstWavelength', 1, self.FirstWavelengthSpinBox)
		fo.add('secondWavelength', 0, self.SecondWavelengthSpinBox)
		fo.add('processType', 0, self.ProcessTypeComboBox)
		fo.add('displayType', 0, self.DisplayTypeComboBox)
		fo.add('referenceFrames', 1, self.referenceFrameSpinBox)
		
		self.connect(self.ProcessTypeComboBox, SIGNAL("currentIndexChanged(int)"), self.processTypeChangedCb)
		
		return fo
		
	def processTypeChangedCb(self, value):
		dispTypeLabels = QStringList()
		if value == 0:
			dispTypeLabels.append("F")
			dispTypeLabels.append("dF")
			dispTypeLabels.append("dF/F0")
		else:
			dispTypeLabels.append("R")
			dispTypeLabels.append("dR")
			dispTypeLabels.append("dR/R0")
		
		for i in xrange(0,self.DisplayTypeComboBox.count()):	
			self.DisplayTypeComboBox.setItemText(i, dispTypeLabels[i])
		
		self.frameOptions.displayType = 0
		
		#print("processTypeChangedCb ")
		
	def initTimeOptions(self):
		fo = Properties(self)
		fo.add('useAssociatedTimes', 1, self.associatedTimesRadioButton)
		fo.add('useInterframeInverval', 0, self.userInterframeRadioButton)
		fo.add('interframeInterval', 40.0, self.interframeIntervalSpinBox)
		fo.add('frameBasedTimes', 0, self.FrameBasedRadioButton)
		fo.add('time0Frame', 0, self.time0SpinBox)
		fo.add('displayTimeStamp',1,self.displayTimesCheckBox)
		fo.add('fontSize',12,self.fontSizeSpinBox)
		fo.add('xOffset',50,self.xOffsetSpinBox)
		fo.add('yOffset',50,self.yOffsetSpinBox)
		return fo
	
	def initDisplayOptions(self):
		fo = Properties(self)
		fo.add('useLUT', 1, self.LUTradioButton)
		fo.add('lutMapId', 0, self.ColorMapcomboBox)
		fo.add('useHSV', 0, self.HSVradioButton)
		fo.add('hsvSaturation', 1.0, self.saturationSpinBox)
		fo.add('enlargeToBackground', 0, self.enlargeToBckCheckBox)
		fo.add('medianFilterOn', 0, self.medianFilterCheckbox)
		fo.add('gaussianFilterOn', 0, self.gaussianFilterCheckbox)
		fo.add('FrameByFrameBackground',1,self.FrameByFrameRadioButton)
		fo.add('NomarskiBackground',0,self.NomarskiRadioButton)
		self.connect(self.HSVradioButton,SIGNAL('toggled(bool)'),self.HSVchanged)
		
		fo.add('displayScalebar',1,self.scalebarCheckBox)
		fo.add('scaleBarScaleFactor',50.0,self.sbScaleFactorSpinBox)
		fo.add('scaleBarLength',25,self.sbLengthSpinBox)
		fo.add('scaleBarFontSize',12.0,self.sbFontSizeSpinBox)
		fo.add('scaleBarXOffset',50,self.sbXOffsetSpinBox)
		fo.add('scaleBarYOffset',50,self.sbYOffsetSpinBox)
		fo.add('scaleBarLineSize',10,self.lineSizeSpinBox)
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
			
	def applyWidgetValueWithoutSignal(self, obj, v):
		obj.blockSignals(True)
		obj.setValue(v)
		obj.blockSignals(False)
