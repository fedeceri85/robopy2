import PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

from RoboPyGui import Ui_RoboMainWnd
from SequenceDisplay import SequenceDisplay
'''
Main window of Robopy project
Launches various windows and tools

'''

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
		self.connect(self.roboActionLoadInRam, SIGNAL("triggered()"), self.roboActionLoadInRamCb)
		
	def makeImageOptionsConnections(self, seqDisp, procOpt):
		seqDisp.ImageTabWidget.currentChanged.connect(procOpt.sequenceChangedTab)
		
	def roboActionOpenCb(self):
		
		files = self.getFileNamesGui("Select tiff sequence", QString(), "Images (*.tif)")
		
		sd = SequenceDisplay(self, files)
		#self.sequences.append(sd)
		
		self.showStatusMessage("Ready!" + " sequences " + str(len(self.sequences)))

	def roboActionLoadInRamCb(self):
		
		files = self.getFileNamesGui("Select tiff sequence", QString(), "Images (*.tif)")
		
		sd = SequenceDisplay(self, files,loadInRam = True)
		#self.sequences.append(sd)
		
		self.showStatusMessage("Ready!" + " sequences " + str(len(self.sequences)))
		
	def showStatusMessage(self, msg):
		self.statusBar().showMessage(msg)
		
	def getFileNamesGui(self, caption, directory, filt):
		fnames = QFileDialog.getOpenFileNames(self, caption, directory, filt)
		
		nFiles = fnames.count()
		
		files = [fnames[i].toAscii().data() for i in xrange(nFiles)]
			
		return files

if __name__== "__main__":
	app = PyQt4.QtGui.QApplication(sys.argv)
	window = RoboPy()
	window.show()
	
	sys.exit(app.exec_())
