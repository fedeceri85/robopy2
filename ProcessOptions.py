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
			obj.valueChanged.connect(self._widget_changed)
		elif hasattr(obj, "sliderReleased"):
			obj.sliderReleased.connect(self._widget_changed)
		elif hasattr(obj, "currentIndexChanged"):
			obj.currentIndexChanged.connect(self._widget_changed)
		elif hasattr(obj, "toggled"):
			obj.toggled.connect(self._widget_changed)
		
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
		
	def _widget_changed(self, value):
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
					
		
		setattr(self, '_' + name, value)
			

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
		
		self.ProcessTypeComboBox.currentIndexChanged.connect(self.processTypeChangedCb)
		
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
		
		
	def initTimeOptions(self):
		fo = Properties(self)
		fo.add('useAssociatedTimes', 1, self.associatedTimesRadioButton)
		fo.add('useInterframeInverval', 0, self.userInterframeRadioButton)
		fo.add('interframeInterval', 40.0, self.interframeIntervalSpinBox)
		fo.add('frameBasedTimes', 0, self.FrameBasedRadioButton)
		fo.add('time0Frame', 0, self.time0SpinBox)
		return fo
		
	def initDisplayOptions(self):
		fo = Properties(self)
		fo.add('useLUT', 1, self.LUTradioButton)
		fo.add('lutMapId', 0, self.ColorMapcomboBox)
		fo.add('useHSV', 0, self.HSVradioButton)
		fo.add('hsvSaturation', 1.0, self.saturationSpinBox)
		fo.add('enlargeToBackground', 0, self.enlargeToBckCheckBox)
		return fo
		
	def applyWidgetValueWithoutSignal(self, obj, v):
		obj.blockSignals(True)
		obj.setValue(v)
		obj.blockSignals(False)
