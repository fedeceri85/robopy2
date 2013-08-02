import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from AviSettingsGui import Ui_aviSettingsWnd

class AviSettings(Ui_aviSettingsWnd, QDialog):
	def __init__(self, aviOptions,parent=None):
		QDialog.__init__(self, parent=parent)
		self.setupUi(self)
		self.aviOptions = aviOptions
		self.initData()
		self.makeConnections()
		
	def initData(self):
		self.fpsSpinBox.setValue(self.aviOptions['fps'])
		self.widthSpinBox.setValue(self.aviOptions['width'])
		self.heightSpinBox.setValue(self.aviOptions['height'])
		self.fileNameEdit.setText(self.aviOptions['fname'])
		
		self.firstFrameSpinBox.setRange(1, self.aviOptions['lastFrame'])
		self.firstFrameSpinBox.setValue(self.aviOptions['firstFrame'])
		self.lastFrameSpinBox.setRange(1, self.aviOptions['lastFrame'])
		self.lastFrameSpinBox.setValue(self.aviOptions['lastFrame'])

	def makeConnections(self):
		self.connect(self.selectFileButton, SIGNAL("clicked()"), self.selectFile)
		self.connect(self.fpsSpinBox,SIGNAL("valueChanged(int)"),self.changeFps)
		self.connect(self.widthSpinBox,SIGNAL("valueChanged(int)"),self.changeWidth)
		self.connect(self.heightSpinBox,SIGNAL("valueChanged(int)"),self.changeHeight)
		self.connect(self.firstFrameSpinBox,SIGNAL("valueChanged(int)"),self.changeFirstFrame)
		self.connect(self.lastFrameSpinBox,SIGNAL("valueChanged(int)"),self.changeLastFrame)
		
		
		
	def selectFile(self):
		self.aviOptions["fname"] = QFileDialog.getSaveFileName(self, "Select avi file", QString(), "Avi movies (*.avi)")
		self.fileNameEdit.setText(self.aviOptions["fname"])
		self.aviOptions["fname"] = self.aviOptions["fname"].toAscii().data()

	def changeFps(self,value):
		self.aviOptions["fps"] = value
		
	def changeWidth(self,value):
		self.aviOptions["width"] = value
		
	def changeHeight(self,value):
		self.aviOptions["height"] = value
		
	def changeFirstFrame(self,value):
		self.aviOptions["firstFrame"] = value
		
	def changeLastFrame(self,value):
		self.aviOptions["lastFrame"] = value
