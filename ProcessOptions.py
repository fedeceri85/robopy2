import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ProcessOptionsGui import Ui_ProcessOptionsDlg

class Properties(object):
	def add(self, name, value, obj=None):
		fget = lambda self: self._get_property(name)
		fset = lambda self, value: self._set_property(name, value)
		
		
		setattr(self, '_obj_' + name, obj)
		setattr(self.__class__, name, property(fget, fset))
		setattr(self, '_' + name, value)
		
		self._set_property(name, value)
		
	def _set_property(self, name, value):
		setattr(self, '_' + name, value)
		obj = getattr(self, '_obj_' + name)
		if obj != None:
			obj.blockSignals(True)
			
			pp = dir(obj)
		
			if "setValue" in pp:
				obj.setValue(value)
				#obs.valueChanged.connect(self._widget_changed)
			elif "setCurrentIndex" in pp:
				obj.setCurrentIndex(value)
				
			obj.blockSignals(False)
			
	def _get_property(self, name):
		return getattr(self, '_' + name)
		
	def _widget_changed(self, value):
		pass
			

class ProcessOptions(Ui_ProcessOptionsDlg, QDialog):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent=parent)
		self.setupUi(self)
		
		self.frameOptions = self.initFrameOptions()
       
	def sequenceChangedTab(self, idx):
		self.PO_TabWidget.setCurrentIndex(idx)
		
	def initFrameOptions(self):
		
		fo = Properties()
		
		fo.add('firstFrame', 1, self.FirstFrameSpinBox)
		fo.add('lastFrame', 1, self.LastFrameSpinBox)
		fo.add('cycleSize', 1, self.CycleSizeSpinBox)
		fo.add('firstWavelength', 1, self.FirstWavelengthSpinBox)
		fo.add('secondWavelength', 0, self.SecondWavelengthSpinBox)
		fo.add('processType', 0, self.ProcessTypeComboBox)
		
		return fo
		
	def applyWidgetValueWithoutSignal(self, obj, v):
		obj.blockSignals(True)
		obj.setValue(v)
		obj.blockSignals(False)
