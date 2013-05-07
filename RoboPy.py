import PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

from RoboPyGui import Ui_RoboMainWnd
from SequenceDisplay import SequenceDisplay

class RoboPy(Ui_RoboMainWnd, PyQt4.QtGui.QMainWindow):
	def __init__(self, parent = None):
		PyQt4.QtGui.QMainWindow.__init__(self, parent=parent)
		
		self.setupUi(self)
		self.initData()
		
		self.makeConnections()
		
		self.show()
		
	def initData(self):
		self.sequences = list();
		self.lastDirectory = "";
		
	def makeConnections(self):
		self.connect(self.roboActionOpen, SIGNAL("triggered()"), self.roboActionOpenCb)
		
	def roboActionOpenCb(self):
		
		files = self.getFileNamesGui("Select tiff sequence", QString(), "Images (*.tif)")
		
		sd = SequenceDisplay(self, files)
		self.sequences.append(sd)
		
		self.showStatusMessage("Ready!" + " sequences " + str(len(self.sequences)))
		
	def showStatusMessage(self, msg):
		self.statusBar().showMessage(msg)
		
	def getFileNamesGui(self, caption, directory, filt):
		fnames = QFileDialog.getOpenFileNames(self, caption, directory, filt)
		
		nFiles = fnames.size()
		
		files = [fnames.at(i).toStdString().c_str() for i in xrange(nFiles)]
		#for i in xrange(1,nFiles):
			#files.append(fnames.at(i).toStdString().c_str())
			
		return files

if __name__== "__main__":
	app = PyQt4.QtGui.QApplication(sys.argv)
	window = RoboPy()
	window.show()
	
	sys.exit(app.exec_())
