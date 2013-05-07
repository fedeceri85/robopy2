import PyQt4
from PyQt4.QtCore import *
import sys

from RoboPyGui import Ui_RoboMainWnd

class RoboPy(Ui_RoboMainWnd, PyQt4.QtGui.QMainWindow):
	def __init__(self, parent = None):
		PyQt4.QtGui.QMainWindow.__init__(self, parent=parent)
		
		self.setupUi(self)
		
		self.makeConnections()
		
		self.show()
		
	def makeConnections(self):
		self.connect(self.roboActionOpen, SIGNAL("triggered()"), self.roboActionOpenCb)
		
	def roboActionOpenCb(self):
		self.showStatusMessage("Ready!")
		
	def showStatusMessage(self, msg):
		self.statusBar().showMessage(msg)

if __name__== "__main__":
	app = PyQt4.QtGui.QApplication(sys.argv)
	window = RoboPy()
	window.show()
	
	sys.exit(app.exec_())
