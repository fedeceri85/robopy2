import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from SaveRawSequenceOptionsGui import Ui_frameIntervalDialog

class SaveRawSequenceOptions(Ui_frameIntervalDialog, QDialog):
	def __init__(self, firstLast=[0,0],parent=None):
		QDialog.__init__(self, parent=parent)
		self.setupUi(self)
		self.options = firstLast
		self.initData()
		self.makeConnections()
		
	def initData(self):
		self.firstFrameSpinBox.setRange(self.options[0], self.options[1])
		self.lastFrameSpinBox.setRange(self.options[0], self.options[1])
		self.stepSpinBox.setRange(self.options[0], self.options[1])
		self.firstFrameSpinBox.setValue(self.options[0])
		self.lastFrameSpinBox.setValue(self.options[1])

	def makeConnections(self):
		self.connect(self.firstFrameSpinBox,SIGNAL("valueChanged(int)"),self.updateFirst)
		self.connect(self.lastFrameSpinBox,SIGNAL("valueChanged(int)"),self.updateLast)

		
	def updateFirst(self,value):
		self.options[0] = value

	def updateLast(self,value):
		self.options[1] = value
		
	def getFrameInterval(self):
		return range(self.options[0]-1,self.options[1],self.stepSpinBox.value())