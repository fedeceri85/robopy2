import PyQt4
from PyQt4.QtCore import *
import sys

from OpenGL import GL

from SequenceDisplayGui import Ui_SequenceDisplayWnd
from ImageDisplayWidget import ImageDisplayWidget

class SequenceDisplay(Ui_SequenceDisplayWnd, PyQt4.QtGui.QMainWindow):
	def __init__(self, parent = None, files=None):
		PyQt4.QtGui.QMainWindow.__init__(self, parent=parent)
		
		self.setupUi(self)
		self.imageWidgetSetup()
		
		self.roboMainWnd = parent
		self.SequenceFiles = files
		
		self.makeConnections()
		
		self.show()
		
	def imageWidgetSetup(self):
		hlay = PyQt4.QtGui.QHBoxLayout(self.ImageFrameWidget)
		imWidget = ImageDisplayWidget()
		
		hlay.addWidget(imWidget)
		
	def makeConnections(self):
		pass
		#self.connect(self.roboActionOpen, SIGNAL("triggered()"), self.roboActionOpenCb)
		
		
	def showStatusMessage(self, msg):
		self.statusBar().showMessage(msg)

if __name__== "__main__":
	app = PyQt4.QtGui.QApplication(sys.argv)
	window = RoboPy()
	window.show()
	
	sys.exit(app.exec_())

